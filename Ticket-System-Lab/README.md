<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=cylinder&color=auto&height=150&section=header&text=Ticket%20System%20Lab&fontSize=45&animation=fadeIn" width="100%"/>

  <p><em>"Turning chaos into structured resolutions."</em></p>

  <p>
    <img src="https://img.shields.io/badge/Service_Desk-ITSM-FF7D00?style=flat&logo=reverbnation&logoColor=white">
    <img src="https://img.shields.io/badge/Platform-osTicket-1E8BC3?style=flat">
    <img src="https://img.shields.io/badge/Containers-Docker-2496ED?style=flat&logo=docker&logoColor=white">
    <img src="https://img.shields.io/badge/Troubleshooting-Root_Cause_Analysis-CC0000?style=flat&logo=search&logoColor=white">
  </p>

  <p>
    📸 <a href="images.md"><b>Screenshots</b></a> &nbsp;·&nbsp; 🛠️ <a href="labs.md"><b>Troubleshooting Log</b></a>
  </p>
</div>

---

## 🎯 Project Overview
This project simulates a real-world **IT Service Management (ITSM)** workflow. I deployed the **osTicket** help desk platform in **Docker** and used it to practice end-to-end incident lifecycle management — from the initial user report to Root Cause Analysis (RCA) and final resolution. The lab bridges technical infrastructure skills with the "soft" skill of professional user support.

## 🚀 Key Objectives
*   **Workflow Simulation:** Manage the full lifecycle of an IT ticket (Open → In-Progress → Pending → Resolved).
*   **Incident Response:** Handle common corporate IT scenarios (VPN connectivity, Outlook sync errors, printer issues).
*   **Documentation:** Keep professional records of incidents to build a knowledge base (KB).
*   **Root Cause Analysis (RCA):** Find the underlying issue instead of applying temporary "band-aid" fixes.

---

## 🔄 Ticket Lifecycle
```
User submits ticket ──► Agent claims it ──► Investigation & fix ──► Closed with resolution summary
```
Each step is documented with screenshots in **[images.md](images.md)**.

---

## 🏗️ Implementation Highlights
1.  **Environment Setup:** Deployed osTicket and its MySQL database as Docker containers on a Windows host (Docker Desktop).
2.  **Scenario Creation:** Built a catalog of typical user issues based on common Help Desk ticket trends.
3.  **Documentation Standard:** Adopted a structured reporting format to ensure consistency and accountability in every resolution.

---

## 🔍 Incident Log & Troubleshooting
Full write-up, diagnostic matrix and evidence in **[labs.md](labs.md)**.

| Incident | Symptom | Root Cause | Resolution |
| :--- | :--- | :--- | :--- |
| **Connection Refused** | osTicket web interface unreachable while containers appeared to run | Unstable Docker base image silently crashing internal services | Found via Docker Desktop logs; replaced with the stable `campbellsoftwaresolutions/osticket` image |

> **Pro-Tip:** When the obvious fixes (ports, versions, caches) fail, read the logs. Three failed attempts came before the log audit that revealed the real cause.

---

## 📌 Technical References
* [osTicket Documentation](https://docs.osticket.com)
* [Docker Documentation](https://docs.docker.com)
* [ITIL Foundation: Incident Management Best Practices](https://www.axelos.com/certifications/itil-certifications)
* [CompTIA A+ Troubleshooting Methodology](https://www.comptia.org)

---

<div align="center">
  <p>Building efficiency in IT service delivery.</p>
  <a href="https://github.com/ChrisFrank23/IT-Projects">← Back to Main Portfolio</a>
</div>
