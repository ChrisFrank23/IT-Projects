<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=cylinder&color=auto&height=150&section=header&text=Active%20Directory%20Lab&fontSize=45&animation=fadeIn" width="100%"/>
  
  <p><em>"Identity is the new perimeter."</em></p>

  <p>
    <img src="https://img.shields.io/badge/Windows_Server-2022-0078D4?style=flat&logo=windows&logoColor=white">
    <img src="https://img.shields.io/badge/Active_Directory-AD_DS-0052CC?style=flat&logo=windows&logoColor=white">
    <img src="https://img.shields.io/badge/Virtualization-VirtualBox-21A4DE?style=flat&logo=virtualbox&logoColor=white">
  </p>
</div>

---

## 🎯 Project Overview
This project simulates an **Enterprise Domain Environment**. By deploying a full-stack Active Directory infrastructure, I aimed to bridge the gap between theoretical networking concepts and practical identity administration. This lab serves as my sandbox for testing GPOs, user lifecycle management, and disaster recovery scenarios.

## 🚀 Key Objectives
*   **Infrastructure:** Deploy a Domain Controller (DC) and configure DNS/DHCP services.
*   **Administration:** Manage Organizational Units (OUs), security groups, and user objects.
*   **Security:** Enforce **Group Policy Objects (GPO)** for password complexity, session timeouts, and restricted software installation.
*   **Networking:** Establish a secure internal virtual network environment.

---

## 🏗️ Implementation Highlights
1.  **Network Design:** Configured a dedicated internal virtual network to prevent conflicts with the host network.
2.  **IAM Implementation:** Structured the environment into functional OUs (HR, IT, Sales) to demonstrate hierarchy-based management.
3.  **Policy Hardening:** Automated security settings via GPO, ensuring compliance across all domain-joined machines.

---

## 🔍 Troubleshooting Log
| Date | Issue | Resolution |
| :--- | :--- | :--- |
| 2026-06-15 | DNS Resolution Failure | Updated client TCP/IP settings to point to the DC IP. |
| 2026-06-16 | GPO Policy Conflict | Used `gpupdate /force` and identified blocked inheritance settings. |

> **Pro-Tip:** Documentation is as important as the deployment itself. Troubleshooting these errors provided a deeper understanding of how the network handshake functions under the hood.

---

## 🖼️ Architectural View
(images/<img width="509" height="713" alt="ActiveDirectoryServerDiagram" src="https://github.com/user-attachments/assets/6ad4e8de-e1cd-4331-8245-3023b3dff5e2" />
)

---

## 📌 Technical References
* [Microsoft AD DS Documentation](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/ad-ds-concepts)
* [CompTIA Security+ Domain 2: Identity & Access Management](https://www.comptia.org)

---

<div align="center">
  <p>Developed with passion for IT infrastructure and Security.</p>
  <a href="https://github.com/ChrisFrank23/IT-Projects">← Back to Main Portfolio</a>
</div>
