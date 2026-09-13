# StackX Security (SIEM / EDR / XDR / NDR / TIP / UEBA / VulnMgmt / CaseMgmt)

**Token:** `{{module_stackx_security}}`  
**Group:** StackX — Control / Orchestration / SOC / Operations Layer  
**Required:** No (optional module)

---

## Overview

StackX Security provides a unified security monitoring and response capability that combines SIEM log ingestion and correlation, endpoint and extended detection and response (EDR/XDR), network traffic analysis (NDR), threat intelligence (TIP), user and entity behavioural analytics (UEBA), vulnerability management, and unified case management. It leverages advanced analytics, machine learning and automation to transition from a reactive security posture to a proactive and predictive one.

*[Note: This is a composite security module. Include it when a security monitoring and response scope is required. Confirm per bid the depth of each sub-capability and whether any sub-capabilities are out of scope. Where a fuller SOC operations scope is required, use the `{{module_stackx_soc}}` composite SOC module instead or in addition.]*

## How Each Security Capability Is Delivered

Every security capability in this section is delivered in one of three ways. The distinction is stated plainly because it determines both cost and accountability, and because a security function assessing this proposal is entitled to know which controls the vendor operates and which it verifies.

| Delivery Mode | What It Means |
| :--- | :--- |
| **Native** | Delivered by the DeviceX and StackX platform itself. Already included in the platform build, with no additional licence or operating cost. |
| **Integrated** | A specialist product selected, deployed, integrated and operated by Verto Wave within the agreed design. Operational accountability sits with Verto Wave; the product carries its own licence and operating cost. |
| **Assured** | The control is executed by the application supplier or by the customer's own team. Verto Wave tests it independently, evidences the result and supervises remediation to closure. Ownership of the control remains with the party that executes it. |

## SIEM — Log Ingestion, Correlation and Analytics

- Operate the StackX SIEM as the primary ingestion hub to parse, enrich and store telemetry from network assets, cloud environments and applications.
- Execute real-time log correlation and automatically map detected threats to the out-of-the-box MITRE ATT&CK framework.
- Manage dynamic data retention tiers (hot, warm, cold and frozen) to optimise storage costs while ensuring data remains available for compliance and security auditing.
- Run complex correlation rules and machine learning jobs across large volumes of historical data using the platform's distributed search and analytics engine.

## EDR / XDR — Endpoint and Extended Detection & Response

- Deploy and monitor unified, tamper-proof agents to track kernel-level processes, memory access and registry modifications across all endpoints.
- Stitch endpoint telemetry together with network and identity data for comprehensive cross-domain correlation using XDR capabilities.
- Enforce behavioural ransomware prevention, memory threat protection and remote-shell capabilities for live forensics.
- Isolate compromised hosts immediately to stop zero-day exploits and fileless malware that bypass traditional signature-based antivirus solutions.

## NDR — Network Traffic Analysis and Threat Intelligence

- Analyse East-West and North-South network traffic flows using Deep Packet Inspection (DPI) and protocol parsing via StackX NDR.
- Maintain full packet capture (PCAP) storage and conduct TLS/SSL decryption analysis to detect lateral movement, beaconing or data exfiltration attempts.
- Aggregate structured threat data (STIX/TAXII) from open-source, commercial and industry feeds through the StackX Threat Intelligence Platform (TIP).
- Automate Indicator of Compromise (IoC) lifecycle management, profile threat actors and distribute blocklists to firewalls and endpoints.

## UEBA and Vulnerability Management
---

## Figure — Security Architecture / Defence-in-Depth

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic defence-in-depth / layered security architecture diagram showing the security capability layers (external boundary, internal visibility & control, identity shield, data & system integrity, continuity & recovery, assurance & oversight) and the delivery-mode framing (Native / Integrated / Assured). No customer-specific control names that reveal the customer's regulatory regime beyond what is agreed, no customer site names. -->
<!-- Suggested source: Telemedicine proposal §3.7 (StackX Security) + the security-model-at-a-glance concept — genericise the diagram; strip any "clinic", "Dubai management plane", or site-specific labels. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic security / defence-in-depth architecture diagram here. See image-placement guidance notes.]*

---


- Leverage StackX UEBA unsupervised machine-learning algorithms to build mathematical baselines of normal activity for every user, device and service account over a 30-to-60-day period.
- Perform continuous peer-group analysis, track anomalous logins, monitor excessive privilege usage and assign automated risk scores to uncover malicious insiders or compromised credentials.
- Conduct active and passive scanning to identify missing patches, default passwords and insecure configurations across the internal network and external attack surface.
- Prioritise vulnerabilities based on active exploitation trends and generate automated compliance reporting for standards such as CIS and PCI-DSS.

## Incident Triage and Unified Case Management

- Manage security incidents through a centralised ticketing and workflow engine integrated directly into the StackX console.
- Automate digital evidence gathering by immediately attaching PCAPs, endpoint logs and threat intelligence to security tickets.
- Enforce role-based access control and integrated collaboration for incident handlers.
- Track comprehensive SLAs and provide management with clear dashboards detailing SOC efficiency and analyst performance.

## Extended Security Services (optional — selected and quoted per service area)

Everything described so far is delivered by the platform itself, and secures the network, the edge and the communications path. Where the customer prefers one accountable party across a wider picture rather than a platform supplier alone, Verto Wave can deliver the following services around the platform. These are scoped per service area; nothing in this list forms part of the platform build unless it is explicitly selected and separately quoted.

- **Identity and access** — single sign-on and multi-factor authentication for users, including phishing-resistant factors, contextual authorisation policy and blocking of known-compromised credentials. Complements the machine identity model, which secures the nodes rather than the people using them.
- **Privileged access** — credential vaulting, brokered administrative sessions and session recording for privileged users, alongside the credential-free administration model already native to the platform.
- **Application edge protection** — web application firewall, API gateway protection and distributed denial-of-service mitigation in front of the published service, complementing the firewall and intrusion prevention enforced at every site.
- **Key and secret management** — centralised key and secret custody: rotation, separation of key operator from key user, expiry alerting and prevention of secrets held in code or configuration. Extends the hardware-sealed secret handling beyond the appliance itself.
- **Data protection** — classification and tagging of sensitive data, masking of data used in non-production environments and data-loss prevention on the endpoints that handle sensitive records.
- **Endpoint detection and response** — a detection engine licensed and operated alongside the platform-managed endpoint agent and telemetry pipeline, so detection and response share one console with the rest of the estate.
- **Backup and continuity** — backup design and operation, a documented disaster recovery plan and recovery point and recovery time targets agreed with the customer and exercised on an agreed cycle.
- **Security assurance and testing** — independent penetration testing coordinated by Verto Wave, application and interface security testing and cloud configuration assessment, with findings tracked to closure in StackX ITSM.

## Delivery Mode Boundaries (generic)

- Products are not named at proposal stage. Selection is made during design against the customer's existing security standards, held licences and the regulatory position in each operating location.
- The application / application layer remains its supplier's product. Verto Wave does not write, modify or assume ownership of the application's code. Where a control lives inside that application, Verto Wave's role is independent testing, evidencing and supervision.
- Recovery targets are agreed, not assumed. Recovery point and recovery time objectives are set during design against the customer's priorities. No figure is committed ahead of that exercise.
- Customer-owned infrastructure stays customer-owned. Where a control depends on equipment or tenancy the customer supplies (access-layer switching, cloud accounts, directory services), Verto Wave's commitment is to design, verify and evidence it, not to operate what it does not supply.
- The connectivity boundary is unchanged. Wide-area access services remain a customer procurement. Selecting any security service does not alter that boundary.
- Where the customer has issued a formal cybersecurity requirements document, Verto Wave provides a separate point-by-point compliance response mapping each stated requirement to one of the three delivery modes above. That response, not this section, is the correct artefact for a requirement-by-requirement assessment.

## Out-of-Scope (explicitly)

- Security penetration testing, vulnerability assessment, code review and forensics activities, unless explicitly stated as in scope (note: many prior proposals explicitly exclude penetration testing, vulnerability assessment, code review and forensics — confirm per bid whether any of these are requested).
- Any development and debugging activities not explicitly in scope.
- Operating third-party security systems aside from the systems included in this scope.
- Managing and supporting systems and devices not allowing ways of integration.

---

*This module is a reusable building block. The security scope is the most sensitive area in the template — confirm with Security/Compliance SME per bid: which sub-capabilities are in scope, whether penetration testing/vulnerability assessment/code review/forensics are requested or explicitly excluded, whether certified SOC staff resourcing is in place, and which extended security services (if any) are selected. The Native/Integrated/Assured delivery-modes framing and the extended-security-services list are platform-agnostic — tailor the service list and naming policy to the current engagement. For a fuller SOC operations scope, use the `{{module_stackx_soc}}` composite SOC module.*