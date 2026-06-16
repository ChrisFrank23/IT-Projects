# 🏢 Enterprise Active Directory Home Lab

## 🎯 Overview
This project focuses on the deployment of a simulated corporate network environment using Windows Server 2022. The primary objective was to establish a functional Domain Controller and practice essential Identity and Access Management (IAM) tasks, including user lifecycle management, group policy implementation, and network service administration.

## 🚀 Objectives
* **Domain Infrastructure:** Provision a Domain Controller (DC) and promote a server to serve as the forest root.
* **Identity Management:** Create and manage Organizational Units (OUs), user accounts, and security groups.
* **Security Enforcement:** Implement Group Policy Objects (GPOs) to enforce password policies and desktop restrictions.
* **Network Services:** Configure core services (DNS/DHCP) to ensure internal network connectivity and resource resolution.

## 🛠️ Environment & Tools
* **Host OS:** Windows 10/11
* **Virtualization:** Oracle VirtualBox
* **Server OS:** Windows Server 2022 Evaluation
* **Client OS:** Windows 10 Pro
* **Services:** AD DS, DNS, DHCP, GPO

## 🏗️ Implementation Steps
1. **Virtual Network Setup:** Configured an Internal Network in VirtualBox to isolate the lab environment from the host's main network.
2. **Server Promotion:** Installed AD DS roles and promoted the server to a Domain Controller.
3. **User Provisioning:** Structured the Active Directory database into logical OUs (e.g., HR, IT, Finance) and populated them with test accounts.
4. **Policy Deployment:** Configured GPOs to manage account security, such as lockout thresholds and complex password requirements.

## 🔍 Troubleshooting & Insights
* **Issue:** Client machines were unable to join the domain due to DNS resolution failures.
* **Resolution:** Verified that the client’s primary DNS was pointing to the static IP address of the Domain Controller. Adjusted firewall settings to allow necessary traffic on ports 53 (DNS) and 389 (LDAP).
* **Key Learning:** Understanding the critical dependency of Active Directory on a stable DNS infrastructure is fundamental for any IT Support Specialist.

## 🖼️ Architecture & Documentation
*(Insert your diagrams or screenshots here)*
* [Diagram - Network Topology.png]
* [Screenshot - Active Directory Users and Computers.png]
* [Screenshot - Group Policy Management Console.png]

## 📌 References
* [Microsoft Learn: Active Directory Domain Services Overview](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/ad-ds-concepts)
