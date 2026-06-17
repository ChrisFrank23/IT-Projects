<div align="center">

# 🛠️ Technical Incident & Troubleshooting Log

*Documenting the primary infrastructure challenge encountered during the containerized setup of the IT Service Management (ITSM) ticketing platform.*

</div>

---

## 📋 Incident Index

| # | Incident | Status |
|---|----------|--------|
| [01](#-incident-01-persistent-connection-refused-error--docker-image-instability) | Persistent Connection Refused Error & Docker Image Instability | ✅ Resolved |

---

## 🛑 Incident 01: Persistent Connection Refused Error & Docker Image Instability

> **Environment:** Windows Host · Docker Desktop · osTicket · **Category:** Containerization / Image Management

```
ERROR: "Connection Refused"
→ osTicket web interface completely inaccessible despite containers appearing to run
```

<table>
<tr><td><b>🔍 Symptom</b></td><td>Browser continuously returned <i>Connection Refused</i> when attempting to reach the osTicket web interface — containers appeared active but the application was unreachable</td></tr>
<tr><td><b>🧪 Root Cause</b></td><td>The Docker base image in use was inherently unstable, causing quiet crashes of critical internal services. Discovered via live log audit inside Docker Desktop</td></tr>
<tr><td><b>🔧 Resolution</b></td><td>Replaced the unstable image with the production-stable build <code>campbellsoftwaresolutions/osticket</code> in the deployment config. All service dependencies initialized correctly and network routing succeeded on rebuild</td></tr>
</table>

---

### 🔬 Diagnostic Steps & Trial Matrix

| Step | Action Taken | Outcome |
|------|-------------|---------|
| 1️⃣ | **Database Versioning** — switched MySQL version to isolate config handshake issues | ❌ Issue persisted |
| 2️⃣ | **Environment Sanitization** — full stop/start cycles + purged local cache directories | ❌ Issue persisted |
| 3️⃣ | **Security Constraints** — disabled legacy Docker security policies to force MySQL auth compatibility | ❌ Issue persisted |
| 4️⃣ | **Log Analysis** — audited internal runtime logs via Docker Desktop | ✅ Root cause identified: unstable base image with silent service crashes |

> 💡 **Key Insight:** In containerized orchestration, not all public images are built equal. When standard debugging (ports, versions, caches) fails, digging into live engine logs inside Docker Desktop is paramount — identifying a bad base image and pivoting to a community-verified stable build can be the decisive fix.

---

## 📸 Lab Evidence — Infrastructure Validation

> Docker Engine Status Log before migrating to the corrected image:

<img width="1267" height="717" alt="Captura de tela 2026-06-14 220551" src="https://github.com/user-attachments/assets/1f098c71-a5c1-465f-85cf-7f1d6ce27c47" />

*📁 Fig. 1 — Docker Desktop log with error before the resolution, you can see the logs mentioning the root cause for the error.*

---

<div align="center">
  <sub>📁 Part of <a href="https://github.com/ChrisFrank23">Cristhofer Frank's</a> Enterprise Home Lab Documentation</sub>
</div>
