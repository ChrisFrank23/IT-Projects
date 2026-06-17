<div align="center">

# 🛠️ Technical Incident & Troubleshooting Log

*Documenting the primary infrastructure challenge encountered during the containerized setup of the IT Service Management (ITSM) ticketing platform.*

</div>

---

## 📋 Incident Index

| # | Incident | Status |
|---|----------|--------|
| [01](#-incident-01-docker-port-allocation--binding-conflict) | Docker Port Allocation / Binding Conflict | ✅ Resolved |

---

## 🛑 Incident 01: Docker Port Allocation / Binding Conflict

> **Environment:** Windows Host · Docker · osTicket · **Category:** Containerization / Network

```
ERROR: "bkmts: port is already allocated" | "address already in use"
→ osTicket web interface failed to launch on Port 80
```

<table>
<tr><td><b>🔍 Symptom</b></td><td>Container deployment halted with a bind error — Docker could not claim Port 80, preventing the osTicket web interface from launching</td></tr>
<tr><td><b>🧪 Root Cause</b></td><td>The Windows host was already occupying Port 80 via a resident system service (World Wide Web Publishing Service / IIS or a local dev server). Since two distinct processes cannot share the same host port simultaneously, Docker's binding attempt was rejected</td></tr>
<tr><td><b>🔧 Resolution</b></td><td>
  <b>Step 1:</b> Audited the <code>docker-compose.yml</code> port mapping configuration<br/>
  <b>Step 2:</b> Remapped host port <code>8080</code> → container internal port <code>80</code><br/>
  <b>Step 3:</b> Re-ran deployment — database connectivity initialized and platform came online successfully
</td></tr>
</table>

> 💡 **Key Insight:** Containerized deployments require strict port management hygiene. Mapping alternative ingress ports (e.g., `8080`, `8000`) prevents conflicts with native OS processes while preserving internal container behavior.

---

## 📸 Lab Evidence — Infrastructure Validation

> Platform validation after custom port re-routing:

![Successful container initialization showing operational web service traffic mapping](../images/docker_port_success.png)
*📁 Fig. 1 — Docker engine container status log showing network traffic successfully routed via alternate host port mapping.*

---

<div align="center">
  <sub>📁 Part of <a href="https://github.com/ChrisFrank23">Cristhofer Frank's</a> Enterprise Home Lab Documentation</sub>
</div>
