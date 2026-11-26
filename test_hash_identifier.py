"""
test_hash_identifier.py
Testes automáticos do hash_identifier. Rode com: python -m pytest
"""

import hashlib

import pytest

from hash_identifier import HashCandidate, identify, main


# ---------------------------------------------------------------------
# Passo 1: prefixos (confiança high)
# ---------------------------------------------------------------------

@pytest.mark.parametrize(
    "hash_text, esperado",
    [
        ("$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQNQy.uK4Of2T7G.VHvgvWK", "bcrypt"),
        ("$argon2id$v=19$m=65536,t=3,p=4$c29tZXNhbHQ$RdescudvJCsgt3ub", "Argon2id"),
        ("$6$salt$abcdefghijklmnop", "SHA-512 crypt"),
        ("$1$abc$xyz", "MD5 crypt"),
        ("$apr1$JlOdSlVe$ipa1mTAv3LFRBHHzqaIaH/", "Apache MD5-crypt"),
    ],
)
def test_prefixos_conhecidos(hash_text: str, esperado: str) -> None:
    resultado = identify(hash_text)
    assert len(resultado) == 1
    assert resultado[0].algorithm == esperado
    assert resultado[0].confidence == "high"


# ---------------------------------------------------------------------
# Passo 2: formatos especiais
# ---------------------------------------------------------------------

def test_mysql5() -> None:
    resultado = identify("*A4B6157319038724E3560894F7F932C8886EBFCF")
    assert resultado[0].algorithm == "MySQL5"
    assert resultado[0].confidence == "high"


def test_mysql5_minusculo_e_rejeitado() -> None:
    resultado = identify("*a4b6157319038724e3560894f7f932c8886ebfcf")
    assert all(c.algorithm != "MySQL5" for c in resultado)


def test_netntlmv2() -> None:
    amostra = "admin::LAB:1122334455667788:0123456789abcdef0123456789abcdef:0101000000000000"
    resultado = identify(amostra)
    assert resultado[0].algorithm == "NetNTLMv2"


def test_descrypt() -> None:
    resultado = identify("rEK1ecacw.7.c")
    assert resultado[0].algorithm == "DES crypt"
    assert resultado[0].confidence == "medium"


# ---------------------------------------------------------------------
# Passo 3: tamanho + hex (usando hashes reais gerados pelo hashlib)
# ---------------------------------------------------------------------

@pytest.mark.parametrize(
    "algoritmo_hashlib, esperado",
    [
        ("md5", "MD5"),
        ("sha1", "SHA-1"),
        ("sha224", "SHA-224"),
        ("sha256", "SHA-256"),
        ("sha384", "SHA-384"),
        ("sha512", "SHA-512"),
    ],
)
def test_hex_por_tamanho(algoritmo_hashlib: str, esperado: str) -> None:
    hash_real = hashlib.new(algoritmo_hashlib, b"password").hexdigest()
    resultado = identify(hash_real)
    assert resultado[0].algorithm == esperado
    assert resultado[0].confidence == "medium"
    # Os demais candidatos do mesmo tamanho devem ser "low"
    assert all(c.confidence == "low" for c in resultado[1:])


def test_hex_maiusculo_tambem_funciona() -> None:
    resultado = identify("5F4DCC3B5AA765D61D8327DEB882CF99")
    assert resultado[0].algorithm == "MD5"


def test_hex_com_tamanho_desconhecido() -> None:
    assert identify("abc123") == []


# ---------------------------------------------------------------------
# Passos 4 e 5: PHC genérico e "não é hash"
# ---------------------------------------------------------------------

def test_phc_generico() -> None:
    resultado = identify("$pbkdf2-sha512$25000$abc$def")
    assert resultado[0].algorithm == "Formato PHC (pbkdf2-sha512)"
    assert resultado[0].confidence == "low"


def test_jwt() -> None:
    resultado = identify("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIn0.abc")
    assert resultado[0].algorithm == "JWT (não é hash)"


def test_base64() -> None:
    resultado = identify("aGVsbG8gbXVuZG8gdGVzdGU=")
    assert resultado[0].algorithm == "Base64 (não é hash)"


# ---------------------------------------------------------------------
# Passo 6 e casos de borda
# ---------------------------------------------------------------------

@pytest.mark.parametrize("entrada", ["", "   ", "teste", "isso nao e um hash"])
def test_entradas_sem_identificacao(entrada: str) -> None:
    assert identify(entrada) == []


def test_espacos_nas_pontas_sao_ignorados() -> None:
    resultado = identify("  5f4dcc3b5aa765d61d8327deb882cf99\n")
    assert resultado[0].algorithm == "MD5"


def test_hash_candidate_e_imutavel() -> None:
    candidato = HashCandidate("MD5", "medium", "teste")
    with pytest.raises(AttributeError):
        candidato.algorithm = "SHA-1"  # type: ignore[misc]


# ---------------------------------------------------------------------
# CLI: códigos de saída
# ---------------------------------------------------------------------

def test_cli_retorna_0_quando_identifica(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", ["hash_identifier", "5f4dcc3b5aa765d61d8327deb882cf99"])
    assert main() == 0


def test_cli_retorna_1_quando_nao_identifica(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", ["hash_identifier", "teste"])
    assert main() == 1