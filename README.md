# 🔍 Hash Identifier

A command-line tool that identifies the algorithm behind a hash string — the first step in any password-auditing workflow.

Given a string like `5f4dcc3b5aa765d61d8327deb882cf99` or `$2b$12$EixZ...`, it returns ranked candidates with a confidence level and the reason behind each guess.

## Why it matters

Password-cracking tools like **hashcat** and **John the Ripper** only work if you tell them which algorithm produced the hash (hashcat alone has 400+ modes). Identifying the hash format is always the first move — in pentests, CTFs, and breach analysis.

## Features

- Detects **prefixed formats** with high confidence: bcrypt, Argon2id, SHA-512/MD5 crypt, Apache MD5-crypt
- Detects **raw hex hashes by length**: MD5, NTLM, SHA-1, SHA-224, SHA-256, SHA-384, SHA-512 and more
- Recognizes **special formats**: MySQL5, NetNTLMv2 (Active Directory), legacy DES crypt
- Flags inputs that are **not hashes** (JWT tokens, Base64 blobs)
- Ranked results with `high` / `medium` / `low` confidence and a reason for each guess
- Colored table output and exit codes (`0` = identified, `1` = not identified)
- 28 automated tests with pytest

## Demo

```
$ python hash_identifier.py 5f4dcc3b5aa765d61d8327deb882cf99

           Candidatos para: 5f4dcc3b5aa765d61d8327deb882cf99
┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ algoritmo ┃ confiança ┃ motivo                                      ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ MD5       │ medium    │ 32 caracteres hex — candidato mais provável │
│ NTLM      │ low       │ 32 caracteres hex — também possível         │
│ MD4       │ low       │ 32 caracteres hex — também possível         │
└───────────┴───────────┴─────────────────────────────────────────────┘
```

> Output messages are in Portuguese.

## Installation

Requires **Python 3.13+**.

```bash
git clone https://github.com/SEU-USUARIO/hash-identifier.git
cd hash-identifier
python -m venv .venv
# Windows:      .venv\Scripts\Activate.ps1
# Linux/macOS:  source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Usage

```bash
python hash_identifier.py <hash>
python hash_identifier.py <hash> --top 1     # show only the best guess
python hash_identifier.py --help
```

⚠️ Wrap hashes containing `$` in **single quotes**, otherwise the shell will mangle them:

```bash
python hash_identifier.py '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQNQy.uK4Of2T7G.VHvgvWK'
```

## How it works

A hash leaks three clues about itself:

1. **Prefix** — modern formats announce themselves (`$2b$` = bcrypt, `$argon2id$` = Argon2id). → `high` confidence
2. **Length** — hash functions always produce fixed-size output (MD5 = 32 hex chars, SHA-256 = 64). → `medium` / `low` confidence, since several algorithms share the same length
3. **Charset** — hex uses only `0-9a-f`; characters like `+ / =` indicate Base64 instead

The `identify()` function runs a six-step pipeline, from the strongest signal to the weakest, and stops at the first match:

| Step | Check | Confidence |
|------|-------|-----------|
| 1 | Known prefix | high |
| 2 | Special formats (NetNTLMv2, MySQL5, DES crypt) | high / medium |
| 3 | Hex string → lookup by length | medium / low |
| 4 | Generic `$algo$...` PHC format | low |
| 5 | Not a hash (JWT, Base64) | low |
| 6 | No match → empty result | — |

## Running the tests

```bash
python -m pytest -v
```

## What I learned

- How cryptographic hashes work (determinism, fixed length, one-way, avalanche effect)
- Why passwords are stored as hashes, and why slow hashes (bcrypt, Argon2) beat fast ones (MD5, SHA-1)
- Real-world hash formats: Linux `/etc/shadow`, MySQL, Apache `.htpasswd`, Windows NetNTLM
- Python: dataclasses, type hints, `argparse`, the `rich` library
- Automated testing with pytest and version control with Git

## Credits

Based on the [hash-identifier](https://github.com/CarterPerez-dev/Cybersecurity-Projects/tree/main/PROJECTS/foundations/hash-identifier) project from **CarterPerez-dev/Cybersecurity-Projects**, rebuilt step by step as a learning exercise.

## Disclaimer

For educational use and authorized security testing only. Only analyze hashes you own or have explicit permission to test.

## License

[AGPL-3.0](LICENSE)