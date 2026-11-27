<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=cylinder&color=auto&height=150&section=header&text=Hash%20Identifier&fontSize=45&animation=fadeIn" width="100%"/>

  <p><em>"Before you crack it, you have to know what it is."</em></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat&logo=python&logoColor=white">
    <img src="https://img.shields.io/badge/Tests-pytest-0A9EDC?style=flat&logo=pytest&logoColor=white">
    <img src="https://img.shields.io/badge/CLI-rich-D7FF64?style=flat">
    <img src="https://img.shields.io/badge/License-AGPL_v3-purple?style=flat">
  </p>
</div>

---

## 🎯 Project Overview
A command-line tool that identifies the algorithm behind a hash string — the first step in any password-auditing workflow.

Password-cracking tools like **hashcat** and **John the Ripper** only work if you tell them which algorithm produced the hash (hashcat alone has 400+ modes). This tool inspects a hash's **prefix, length and character set** and returns ranked candidates, each with a confidence level and the reason behind the guess.

## 🚀 Key Features
*   **Prefixed formats (high confidence):** bcrypt, Argon2id, SHA-512 crypt, MD5 crypt, Apache MD5-crypt.
*   **Raw hex hashes by length:** MD5, NTLM, SHA-1, SHA-224, SHA-256, SHA-384, SHA-512 and more.
*   **Special formats:** MySQL5, NetNTLMv2 (Active Directory), legacy DES crypt.
*   **Not-a-hash detection:** flags JWT tokens and Base64 blobs instead of guessing.
*   **Clean CLI:** colored results table and exit codes (`0` = identified, `1` = not identified).
*   **Tested:** 28 automated tests with pytest.

---

## 🖥️ Demo
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

| Input | Detected as | Confidence |
| :--- | :--- | :--- |
| `5f4dcc3b5aa765d61d8327deb882cf99` | MD5 | medium |
| `$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQNQy.uK4Of2T7G.VHvgvWK` | bcrypt | high |
| `*A4B6157319038724E3560894F7F932C8886EBFCF` | MySQL5 | high |
| `admin::LAB:1122334455667788:0123...cdef:0101...` | NetNTLMv2 | high |
| `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` | JWT (not a hash) | low |

---

## 🏗️ How It Works
A hash leaks three clues about itself:

1.  **Prefix** — modern formats announce themselves (`$2b$` = bcrypt, `$argon2id$` = Argon2id).
2.  **Length** — hash functions always produce fixed-size output (MD5 = 32 hex chars, SHA-256 = 64). Several algorithms share the same length, so this is never "high" confidence.
3.  **Charset** — hex uses only `0-9a-f`; characters like `+ / =` point to Base64 instead.

The `identify()` function runs a six-step pipeline, from the strongest signal to the weakest, and stops at the first match:

| Step | Check | Confidence |
| :--- | :--- | :--- |
| 1 | Known prefix | high |
| 2 | Special formats (NetNTLMv2, MySQL5, DES crypt) | high / medium |
| 3 | Hex string → lookup by length | medium / low |
| 4 | Generic `$algo$...` PHC format | low |
| 5 | Not a hash (JWT, Base64) | low |
| 6 | No match → empty result | — |

---

## ⚙️ Installation & Usage
Requires **Python 3.13+**.

```bash
git clone https://github.com/ChrisFrank23/IT-Projects.git
cd IT-Projects/Hash-Identifier-Project
python -m venv .venv
# Windows:      .venv\Scripts\Activate.ps1
# Linux/macOS:  source .venv/bin/activate
python -m pip install -r requirements.txt
```

```bash
python hash_identifier.py <hash>
python hash_identifier.py <hash> --top 1     # show only the best guess
python hash_identifier.py --help
python -m pytest -v                          # run the test suite
```

> ⚠️ Wrap hashes containing `$` in **single quotes**, otherwise the shell will mangle them:
> `python hash_identifier.py '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQNQy.uK4Of2T7G.VHvgvWK'`

---

## 🧠 What I Learned
*   How cryptographic hashes work: determinism, fixed-length output, one-way functions, avalanche effect.
*   Why passwords are stored as hashes, and why slow hashes (bcrypt, Argon2) beat fast ones (MD5, SHA-1).
*   Real-world hash formats: Linux `/etc/shadow`, MySQL, Apache `.htpasswd`, Windows NetNTLMv2.
*   Python: dataclasses, type hints, `argparse`, and the `rich` library.
*   Automated testing with pytest and version control with Git.

---

## 📌 Credits & References
* Based on the [hash-identifier](https://github.com/CarterPerez-dev/Cybersecurity-Projects/tree/main/PROJECTS/foundations/hash-identifier) project from **CarterPerez-dev/Cybersecurity-Projects**, rebuilt step by step as a learning exercise.
* [hashcat — Example Hashes](https://hashcat.net/wiki/doku.php?id=example_hashes)
* [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

> **Disclaimer:** For educational use and authorized security testing only. Only analyze hashes you own or have explicit permission to test.

Licensed under [AGPL-3.0](LICENSE).

---

<div align="center">
  <p>Developed with passion for IT infrastructure and Security.</p>
  <a href="https://github.com/ChrisFrank23/IT-Projects">← Back to Main Portfolio</a>
</div>
