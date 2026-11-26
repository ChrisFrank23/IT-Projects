"""
hash_identifier.py
Identifica o tipo de um hash pelo seu formato.
"""

import argparse
import sys
from dataclasses import dataclass
from typing import Literal

from rich.console import Console
from rich.table import Table

# A confiança só pode ser um destes três valores
Confidence = Literal["high", "medium", "low"]


@dataclass(frozen=True)
class HashCandidate:
    """Um palpite: qual algoritmo, quão confiante, e por quê."""
    algorithm: str
    confidence: Confidence
    reason: str


# Tabela de prefixos: (prefixo, nome do algoritmo, observação)
PREFIX_RULES = [
    ("$argon2id$", "Argon2id", "padrão moderno, o mais recomendado hoje"),
    ("$2b$", "bcrypt", "variante 2b (atual)"),
    ("$2y$", "bcrypt", "variante 2y (PHP)"),
    ("$6$", "SHA-512 crypt", "padrão do /etc/shadow no Linux"),
    ("$1$", "MD5 crypt", "formato antigo do Linux, considerado fraco"),
    ("$apr1$", "Apache MD5-crypt", "usado em arquivos .htpasswd"),
]

# Caracteres válidos em um hash hexadecimal
HEX_CHARSET = frozenset("0123456789abcdefABCDEF")

# Tamanho (em caracteres hex) -> algoritmos possíveis, do mais comum ao menos comum
HEX_LENGTH_RULES = {
    32: ["MD5", "NTLM", "MD4"],
    40: ["SHA-1", "RIPEMD-160"],
    56: ["SHA-224", "SHA3-224"],
    64: ["SHA-256", "SHA3-256", "BLAKE2s-256"],
    96: ["SHA-384", "SHA3-384"],
    128: ["SHA-512", "SHA3-512", "BLAKE2b-512", "Whirlpool"],
}


def is_hex(text: str) -> bool:
    """Retorna True se o texto só tiver caracteres hexadecimais."""
    return bool(text) and all(c in HEX_CHARSET for c in text)


# Hex só com letras maiúsculas (o MySQL5 sempre gera assim)
HEX_UPPER_CHARSET = frozenset("0123456789ABCDEF")

# Alfabeto usado pelo DES crypt (formato antigo do /etc/passwd)
DESCRYPT_CHARSET = frozenset(
    "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
)


def is_mysql5(text: str) -> bool:
    """MySQL5: um '*' seguido de exatamente 40 caracteres hex MAIÚSCULOS."""
    if len(text) != 41 or not text.startswith("*"):
        return False
    return all(c in HEX_UPPER_CHARSET for c in text[1:])


def is_descrypt(text: str) -> bool:
    """DES crypt: exatamente 13 caracteres do alfabeto ./0-9A-Za-z."""
    return len(text) == 13 and all(c in DESCRYPT_CHARSET for c in text)


def identify(raw_input: str) -> list[HashCandidate]:
    """Recebe um texto e devolve uma lista de palpites."""
    text = raw_input.strip()

    if not text:
        return []

    # Passo 1: procurar um prefixo conhecido
    for prefix, algorithm, note in PREFIX_RULES:
        if text.startswith(prefix):
            return [
                HashCandidate(
                    algorithm=algorithm,
                    confidence="high",
                    reason=f"prefixo {prefix} — {note}",
                )
            ]

    # Passo 2: formatos especiais (sem prefixo $, mas com formato inconfundível)

    # NetNTLMv2 — capturado em testes de Active Directory (ex.: Responder)
    # Formato: usuario::dominio:desafio:hmac(32 hex):blob
    if "::" in text and text.count(":") >= 4:
        parts = text.split(":")
        if len(parts) >= 6 and len(parts[4]) == 32 and is_hex(parts[4]):
            return [
                HashCandidate(
                    algorithm="NetNTLMv2",
                    confidence="high",
                    reason="formato usuario::dominio:desafio:hmac:blob",
                )
            ]

    if is_mysql5(text):
        return [
            HashCandidate(
                algorithm="MySQL5",
                confidence="high",
                reason="'*' seguido de 40 caracteres hex maiúsculos",
            )
        ]

    if is_descrypt(text):
        return [
            HashCandidate(
                algorithm="DES crypt",
                confidence="medium",
                reason="13 caracteres em ./0-9A-Za-z — formato antigo do /etc/passwd",
            )
        ]

    # Passo 3: se for hexadecimal, identificar pelo tamanho
    if is_hex(text):
        algorithms = HEX_LENGTH_RULES.get(len(text), [])
        candidates = []
        for index, algorithm in enumerate(algorithms):
            if index == 0:
                confidence = "medium"
                label = "candidato mais provável"
            else:
                confidence = "low"
                label = "também possível"
            candidates.append(
                HashCandidate(
                    algorithm=algorithm,
                    confidence=confidence,
                    reason=f"{len(text)} caracteres hex — {label}",
                )
            )
        return candidates

    # Passo 4: formato genérico $algoritmo$... que não está na nossa tabela
    if text.startswith("$"):
        rest = text[1:]
        if "$" in rest:
            algo_name = rest.split("$", 1)[0]
            if algo_name and all(c.isalnum() or c in "-_" for c in algo_name):
                return [
                    HashCandidate(
                        algorithm=f"Formato PHC ({algo_name})",
                        confidence="low",
                        reason=f"formato ${algo_name}$... — sem regra específica",
                    )
                ]

    # Passo 5: coisas que NÃO são hash, mas que as pessoas costumam colar
    if text.startswith("eyJ"):
        return [
            HashCandidate(
                algorithm="JWT (não é hash)",
                confidence="low",
                reason="começa com 'eyJ' — token JWT, não um hash",
            )
        ]

    if any(c in text for c in "+/=") and len(text) > 8:
        return [
            HashCandidate(
                algorithm="Base64 (não é hash)",
                confidence="low",
                reason="contém caracteres de base64 (+, / ou =)",
            )
        ]

    # Passo 6: nada encontrado
    return []


# =====================================================================
# Interface de linha de comando (CLI)
# =====================================================================

# Cor de cada nível de confiança na tabela
CONFIDENCE_COLORS = {
    "high": "green",
    "medium": "yellow",
    "low": "cyan",
}


def build_parser() -> argparse.ArgumentParser:
    """Define quais argumentos o programa aceita no terminal."""
    parser = argparse.ArgumentParser(
        prog="hash_identifier",
        description="Identifica o tipo de um hash pelo prefixo e tamanho.",
    )
    parser.add_argument(
        "hash",
        help="O hash a identificar (use aspas simples se tiver $).",
    )
    parser.add_argument(
        "--top",
        "-n",
        type=int,
        default=5,
        help="Quantidade máxima de palpites a mostrar (padrão: 5).",
    )
    return parser


def render_table(raw_input: str, candidates: list[HashCandidate], console: Console) -> None:
    """Mostra os palpites numa tabela colorida."""
    table = Table(title=f"Candidatos para: {raw_input.strip()}", title_style="bold cyan")
    table.add_column("algoritmo", style="bold white", no_wrap=True)
    table.add_column("confiança", no_wrap=True)
    table.add_column("motivo", style="dim")

    for candidate in candidates:
        color = CONFIDENCE_COLORS[candidate.confidence]
        table.add_row(
            candidate.algorithm,
            f"[{color}]{candidate.confidence}[/{color}]",
            candidate.reason,
        )

    console.print(table)


def main() -> int:
    """Ponto de entrada do programa. Retorna 0 se achou algo, 1 se não."""
    parser = build_parser()
    args = parser.parse_args()
    console = Console()

    candidates = identify(args.hash)

    if not candidates:
        console.print("[red]Não foi possível identificar.[/red] Nenhum prefixo ou tamanho conhecido.")
        return 1

    render_table(args.hash, candidates[: args.top], console)
    return 0


if __name__ == "__main__":
    sys.exit(main())