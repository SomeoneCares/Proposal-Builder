# StackX SOC Operations (SIEM / SOAR / EDR / XDR / NDR / TIP / UEBA / VulnMgmt / CaseMgmt)

**Token:** `{{module_stackx_soc}}`  
**Group:** StackX — Control / Orchestration / SOC / Operations Layer  
**Required:** No (optional module)

---

## Overview

This section outlines the operational scope for a security monitoring and response capability, leveraging the StackX compliance and operations platform. The SOC will utilize advanced analytics, machine learning, and automation to transition from a reactive security posture to a proactive and predictive one.

*[Note: This is a composite SOC module. Include it when a full SOC operations scope is required. Confirm per bid the depth of each sub-capability and whether any sub-capabilities are out of scope.]*

## How Each Security Capability Is Delivered

Every security capability in this section is delivered in one of three ways. The distinction is stated plainly because it determines both cost and accountability, and because a security function assessing this proposal is entitled to know which controls the vendor operates and which it verifies.

| Delivery Mode | What It Means |
|---------------|---------------|
| **Native** | Delivered by the DeviceX and StackX platform itself. Already included in the platform build, with no additional license or operating cost. |
| **Integrated** | A specialist product selected, deployed, integrated and operated by Verto Wave within the agreed design. Operational accountability sits with Verto Wave; the product carries its own license and operating cost. |
| **Assured** | The control is executed by the application supplier or by the customer's own team. Verto Wave tests it independently, evidences the result and supervises remediation to closure. Ownership of the control remains with the party that executes it. |

## Centralized Threat Detection and SIEM Operations

- Operate the StackX SIEM as the primary ingestion hub to parse, enrich, and store telemetry from network assets, cloud environments, and applications
- Execute real-time log correlation and automatically map detected threats to the out-of-the-box MITRE ATT&CK framework
- Manage dynamic data retention tiers (hot, warm, cold, and frozen) to optimize storage costs while ensuring data remains available for compliance and security auditing
- Run complex correlation rules and machine learning jobs across years of historical data in milliseconds utilizing the platform's distributed search and analytics engine

## Automated Response and SOAR Integration

- Utilize the StackX SOAR automation engine to execute predefined API-driven playbooks across the entire security stack without manual human intervention
- Implement automated threat intelligence enrichment and one-click containment execution to drastically reduce the Mean Time to Respond (MTTR)
- Establish bidirectional workflow integrations with IT Service Management (ITSM) tools for seamless incident handling and resolution

## Endpoint and Extended Detection & Response (EDR/XDR)

- Deploy and monitor unified, tamper-proof agents to track kernel-level processes, memory access, and registry modifications across all endpoints
- Stitch endpoint telemetry together with network and identity data for comprehensive cross-domain correlation using XDR capabilities
- Enforce behavioral ransomware prevention, memory threat protection, and utilize remote shell capabilities for live forensics
- Isolate compromised hosts immediately to stop zero-day exploits and fileless malware that bypass traditional signature-based antivirus solutions

## Network Traffic Analysis and Threat Intelligence

- Analyze East-West and North-South network traffic flows utilizing Deep Packet Inspection (DPI) and protocol parsing via StackX NDR
- Maintain full packet capture (PCAP) storage and conduct TLS/SSL decryption analysis to detect lateral movement, beaconing, or data exfiltration attempts
- Aggregate structured threat data (STIX/TAXII) from open-source, commercial, and industry feeds through the StackX Threat Intelligence Platform (TIP)
- Automate Indicator of Compromise (IoC) lifecycle management, profile threat actors, and seamlessly distribute blocklists to firewalls and endpoints

---

## Figure — SOC Architecture / Security Operations Workflow

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic SOC architecture diagram showing the security-operations delivery model (Native / Integrated / Assured), security services areas, monitoring, detection, triage, investigation, response, and escalation — plus a SOC tiers / shift-model diagram where relevant. No customer-specific SOC tooling names beyond what is agreed, no customer-specific threat intel feeds, no customer site names. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic SOC architecture / security-operations-workflow diagram here. See image-placement guidance notes.]*

---

## Behavioural Analytics and Vulnerability Management

- Leverage StackX UEBA unsupervised machine learning algorithms to build mathematical baselines of normal activity for every user, device, and service account over a 30-to-60-day period
- Perform continuous peer group analysis, track anomalous logins, monitor excessive privilege usage, and assign automated risk scores to uncover malicious insiders or compromised credentials
- Conduct active and passive scanning to identify missing patches, default passwords, and insecure configurations across the internal network and external attack surface
- Prioritize vulnerabilities based on active exploitation trends and generate automated compliance reporting for standards such as CIS and PCI-DSS

## Incident Triage and Unified Case Management

- Manage security incidents through a centralized ticketing and workflow engine integrated directly into the StackX console
- Automate digital evidence gathering by immediately attaching PCAPs, endpoint logs, and threat intelligence to security tickets
- Enforce role-based access control and integrated collaboration chat for incident handlers
- Track comprehensive SLAs and provide management with clear dashboards detailing SOC efficiency and analyst performance

## Extended Security Services (optional, selected and quoted per service area)

Everything described so far is delivered by the platform itself, and secures the network, the edge and the communications path. Where the customer prefers one accountable party across a wider picture rather than a platform supplier alone, Verto Wave can deliver the following services around the platform. These are scoped per service area; nothing in this list forms part of the platform build unless it is explicitly selected and separately quoted.

- **Identity and access** — single sign-on and multi-factor authentication for users, including phishing-resistant factors, contextual authorization policy, and blocking of known-compromised credentials. Complements the machine identity model, which secures the nodes rather than the people using them.
- **Privileged access** — credential vaulting, brokered administrative sessions, and session recording for privileged users, alongside the credential-free administration model already native to the platform.
- **Application edge protection** — web application firewall, API gateway protection, and distributed denial-of-service mitigation in front of the published service, complementing the firewall and intrusion prevention enforced at every site.
- **Key and secret management** — centralized key and secret custody: rotation, separation of key operator from key user, expiry alerting, and prevention of secrets held in code or configuration. Extends the hardware-sealed secret handling beyond the appliance itself.
- **Data protection** — classification and tagging of sensitive data, masking of data used in non-production environments, and data-loss prevention on the endpoints that handle sensitive records.
- **Endpoint detection and response** — a detection engine licensed and operated alongside the platform-managed endpoint agent and telemetry pipeline, so detection and response share one console with the rest of the estate.
- **Backup and continuity** — backup design and operation, a documented disaster recovery plan, and recovery point and recovery time targets agreed with the customer and exercised on an agreed cycle.
- **Security assurance and testing** — independent penetration testing coordinated by Verto Wave, application and interface security testing, and cloud configuration assessment, with findings tracked to closure in StackX ITSM.

## Delivery Mode Boundaries (generic)

- Products are not named at proposal stage. Selection is made during design against the customer's existing security standards, held licenses, and the regulatory position in each operating location.
- The application / application layer remains its supplier's product. Verto Wave does not write, modify, or assume ownership of the application's code. Where a control lives inside that application, the Verto Wave role is independent testing, evidencing, and supervision.
- Recovery targets are agreed, not assumed. Recovery point and recovery time objectives are set during design against the customer's priorities. No figure is committed ahead of that exercise.
- Customer-owned infrastructure stays customer-owned. Where a control depends on equipment or tenancy the customer supplies (access-layer switching, cloud accounts, directory services), the vendor's commitment is to design, verify, and evidence it, not to operate what it does not supply.
- The connectivity boundary is unchanged. Wide-area access services remain a customer procurement. Selecting any security service does not alter that boundary.
- Where the customer has issued a formal cybersecurity requirements document, Verto Wave provides a separate point-by-point compliance response mapping each stated requirement to one of the three delivery modes above. That response, not this section, is the correct artefact for a requirement-by-requirement assessment.

## Out-of-Scope (explicitly)

- Security Penetration Testing, vulnerability assessment, code review, and Forensics activities, unless explicitly stated as in scope (note: many prior proposals explicitly exclude penetration testing, vulnerability assessment, code review, and forensics — confirm per bid whether any of these are requested)
- Any development and debugging activities not explicitly in scope
- Operating 3rd party security systems aside from the systems included in this scope
- Managing and supporting systems and devices not allowing ways of integration

---

*This module is a reusable building block. The SOC scope is the most sensitive area in the template — confirm with Security/Compliance SME per bid: which sub-capabilities are in scope, whether penetration testing/vulnerability assessment/code review/forensics are requested or explicitly excluded, whether certified SOC staff resourcing is in place, and which extended security services (if any) are selected. The Native/Integrated/Assured delivery-modes framing and the extended-security-services list are platform-agnostic — tailor the service list and naming policy to the current engagement.*
