<div align="center">

# 🛠️ Technical Incident & Troubleshooting Log

*Documenting real challenges encountered during enterprise lab implementation — diagnostic methodology, root cause analysis, and resolutions.*

</div>

---

## 📋 Incident Index

| # | Incident | Status |
|---|----------|--------|
| [01](#-incident-01-netplan-configuration-failure) | Netplan Configuration Failure (Linux Gateway) | ✅ Resolved |
| [02](#-incident-02-active-directory-domain-join-failure) | Active Directory Domain Join Failure (RPC / DNS) | ✅ Resolved |
| [03](#-incident-03-crowbar-execution-failure) | Crowbar Execution Failure during Brute-Force Simulation | ✅ Resolved |
| [04](#-incident-04-atomic-red-team-installation-syntax-error) | Atomic Red Team Installation Syntax Error | ✅ Resolved |

---

## 🛑 Incident 01: Netplan Configuration Failure

> **Environment:** Linux Gateway / Server · **Category:** Network Administration

```
SYMPTOM: netplan apply → FAILED
```

<table>
<tr><td><b>🔍 Symptom</b></td><td>Network configuration failed to apply when executing <code>netplan apply</code></td></tr>
<tr><td><b>🧪 Root Cause</b></td><td>Duplicate <code>.yaml</code> file found in <code>/etc/netplan/</code> — Netplan was reading conflicting directives from both files, causing the generation phase to fail</td></tr>
<tr><td><b>🔧 Resolution</b></td><td>Audited the <code>/etc/netplan/</code> directory, backed up the redundant config, deleted the duplicate file. Configuration applied successfully once only the primary file remained</td></tr>
</table>

> 💡 **Key Insight:** Configuration management hygiene in Linux is critical. Always purge stale or duplicate templates from production directories to prevent directive conflicts.

---

## 🛑 Incident 02: Active Directory Domain Join Failure

> **Environment:** Windows Server 2022 + Windows Client · **Category:** Active Directory / DNS

```
ERROR: "An Active Directory Domain Controller for the domain.local could not be contacted."
```

<table>
<tr><td><b>🔍 Symptom</b></td><td>Windows client failed to join the domain — DC could not be contacted</td></tr>
<tr><td><b>🧪 Root Cause</b></td><td>Client and DC were isolated on different network segments with no shared communication path. Client DNS was not pointing to the DC</td></tr>
<tr><td><b>🔧 Resolution</b></td><td>
  <b>Step 1:</b> Reconfigured Hypervisor network adapters to place both VMs on an isolated private network<br/>
  <b>Step 2:</b> Manually set the client's Primary DNS (TCP/IPv4) to point directly to the DC's static IP
</td></tr>
</table>

> 💡 **Key Insight:** Active Directory is entirely DNS-dependent. A client cannot discover domain services unless its DNS queries are explicitly routed to the Domain Controller.

---

## 🛑 Incident 03: Crowbar Execution Failure

> **Environment:** Kali Linux · **Category:** Offensive Security / Red Team

```
SYMPTOM: Crowbar → Execution errors + tool instability during brute-force simulation
```

<table>
<tr><td><b>🔍 Symptom</b></td><td>Dictionary/brute-force attack against AD user <code>Chris Frank</code> using Crowbar resulted in repeated execution errors and tool instability</td></tr>
<tr><td><b>🧪 Root Cause</b></td><td>Tool dependency issues and version instability in the Crowbar framework</td></tr>
<tr><td><b>🔧 Resolution</b></td><td>Pivoted to <b>Hydra</b> — configured to target the service protocol with the specified username and wordlist. Successfully identified credentials (<code>Cris&230207</code>) and validated the brute-force attack vector</td></tr>
</table>

> 💡 **Key Insight:** Cyber defense requires adaptability. When an offensive tool fails, an operator must quickly pivot to alternative industry-standard frameworks to validate vulnerabilities without losing momentum.

---

## 🛑 Incident 04: Atomic Red Team Installation Syntax Error

> **Environment:** Windows PowerShell · **Category:** Security Framework Deployment

```
SYMPTOM: Atomic Red Team install script → Connection/resource error on execution
```

<table>
<tr><td><b>🔍 Symptom</b></td><td>Automated installation script for Atomic Red Team failed in PowerShell with a connection/resource error</td></tr>
<tr><td><b>🧪 Root Cause</b></td><td>Typographical error in the download URL string within the PowerShell command</td></tr>
<tr><td><b>🔧 Resolution</b></td><td>Audited the script syntax against official framework documentation, corrected the URL string parameters, and successfully completed the framework installation</td></tr>
</table>

> 💡 **Key Insight:** Attention to detail in CLI syntax is paramount. Minor character discrepancies can break entire deployment scripts — precise code auditing is a fundamental IT skill.

---

<div align="center">
  <sub>📁 Part of <a href="https://github.com/ChrisFrank23">Cristhofer Frank's</a> Enterprise Home Lab Documentation</sub>
</div>
