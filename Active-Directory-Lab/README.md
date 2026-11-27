<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=cylinder&color=auto&height=150&section=header&text=Active%20Directory%20Lab&fontSize=45&animation=fadeIn" width="100%"/>

  <p><em>"Identity is the new perimeter."</em></p>

  <p>
    <img src="https://img.shields.io/badge/Windows_Server-2022-0078D4?style=flat&logo=windows&logoColor=white">
    <img src="https://img.shields.io/badge/Active_Directory-AD_DS-0052CC?style=flat&logo=windows&logoColor=white">
    <img src="https://img.shields.io/badge/SIEM-Splunk-000000?style=flat&logo=splunk&logoColor=white">
    <img src="https://img.shields.io/badge/Attacker-Kali_Linux-557C94?style=flat&logo=kalilinux&logoColor=white">
    <img src="https://img.shields.io/badge/Virtualization-VirtualBox-21A4DE?style=flat&logo=virtualbox&logoColor=white">
  </p>

  <p>
    📸 <a href="images.md"><b>Screenshots</b></a> &nbsp;·&nbsp; 🛠️ <a href="labs.md"><b>Troubleshooting Log</b></a>
  </p>
</div>

---

## 🎯 Project Overview
This project simulates an **enterprise domain environment monitored like a small SOC**. I deployed a full Active Directory infrastructure, forwarded its logs to **Splunk**, and then attacked it from a **Kali Linux** machine — bridging the gap between identity administration and security operations.

The lab is my sandbox for testing GPOs, user lifecycle management, attack simulation and, next, detection engineering.

## 🚀 Key Objectives
*   **Infrastructure:** Deploy a Domain Controller and configure DNS on an isolated virtual network.
*   **Administration:** Manage Organizational Units (OUs), security groups and user objects.
*   **Security Hardening:** Enforce **Group Policy Objects (GPO)** for password complexity, session timeouts and restricted software installation.
*   **Log Collection:** Install the **Splunk Universal Forwarder** to ship Windows logs to a dedicated Splunk server.
*   **Attack Simulation:** Run a password brute-force attack against a domain user from Kali Linux (Crowbar → Hydra).
*   **Adversary Emulation (setup):** Install **Atomic Red Team** for future MITRE ATT&CK-based tests.

---

## 🏗️ Lab Architecture

| Machine | Role |
| :--- | :--- |
| **Windows Server 2022** | Domain Controller — AD DS, DNS, GPO |
| **Windows Client** | Domain-joined target machine |
| **Splunk Server (Linux)** | SIEM — receives and indexes logs |
| **Kali Linux** | Attacker machine — brute-force simulation |

All machines run in VirtualBox on a dedicated internal network, isolated from the host network.

<img width="509" height="713" alt="ActiveDirectoryServerDiagram" src="https://github.com/user-attachments/assets/6ad4e8de-e1cd-4331-8245-3023b3dff5e2" />

---

## ⚔️ Attack Simulation

| Item | Detail |
| :--- | :--- |
| **Technique** | Password brute force — MITRE ATT&CK [T1110](https://attack.mitre.org/techniques/T1110/) |
| **Target** | Domain user account |
| **Tools** | Crowbar (failed — dependency issues) → **Hydra** (success) |
| **Result** | Test account credentials recovered, validating weak passwords as a real attack vector |

> **Lesson:** a weak password defeats every other control. This is exactly why the lab enforces password-complexity GPOs.

---

## 🔍 Troubleshooting Log
Full write-ups with symptom, root cause and resolution in **[labs.md](labs.md)**.

| # | Issue | Resolution |
| :--- | :--- | :--- |
| 01 | Netplan configuration failure (Linux server) | Removed a duplicate `.yaml` file in `/etc/netplan/` |
| 02 | Domain join failure — DC could not be contacted | Put both VMs on the same internal network and pointed client DNS to the DC |
| 03 | Crowbar execution failure during brute-force | Pivoted to Hydra |
| 04 | Atomic Red Team install error in PowerShell | Fixed a typo in the download URL |

> **Pro-Tip:** Documentation is as important as the deployment itself. Troubleshooting these errors gave me a deeper understanding of how AD depends on DNS and network design.

---

## 🔭 Next Steps
*   Build a Splunk detection for the brute-force attack (failed logons — Windows Event ID **4625**) and trigger an alert.
*   Run Atomic Red Team tests and verify which ones Splunk can detect.
*   Add an account lockout GPO and re-run the attack to measure the difference.

---

## 📌 Technical References
* [Microsoft AD DS Documentation](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/ad-ds-concepts)
* [Splunk Universal Forwarder Documentation](https://docs.splunk.com/Documentation/Forwarder)
* [MITRE ATT&CK — T1110 Brute Force](https://attack.mitre.org/techniques/T1110/)
* [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)
* [CompTIA Security+ — Identity & Access Management](https://www.comptia.org)

---

<div align="center">
  <p>Developed with passion for IT infrastructure and Security.</p>
  <a href="https://github.com/ChrisFrank23/IT-Projects">← Back to Main Portfolio</a>
</div>
