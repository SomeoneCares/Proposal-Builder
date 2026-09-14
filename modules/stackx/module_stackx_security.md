# StackX Security

**Token:** `{{module_stackx_security}}`  
**Group:** StackX — Control / Orchestration / SOC / Operations Layer  
**Required:** No (optional module)

---

## Overview

StackX Security is the platform for detecting, investigating and responding to threats across {{customer_short}}'s estate. It brings security telemetry into a shared, searchable data store and applies correlation, behavioral analytics, threat intelligence and automated response to it — moving security from a reactive posture to a proactive one.

## How Each Security Capability Is Delivered

Each capability is delivered in one of three ways. The distinction determines both cost and accountability.

| Delivery mode | What it means |
| :--- | :--- |
| Native | Delivered by the DeviceX and StackX platform itself, already included in the platform build. |
| Integrated | A specialist solution selected, deployed, integrated and operated by Verto Wave within the agreed design; it carries its own license and operating cost. |
| Assured | The control is executed by the application supplier or by {{customer_short}}'s own team; Verto Wave tests it independently, evidences the result and supervises remediation to closure. |

## Platform Capabilities

### Security Information and Event Management (SIEM)

The central ingestion hub parses, enriches and stores telemetry from network assets, cloud environments and applications, collected through lightweight shippers or API integrations. Real-time correlation maps detections to the MITRE ATT&CK framework, and customizable alerting dashboards give analysts one view.

### Security Orchestration, Automation and Response (SOAR)

A playbook engine executes predefined, API-driven sequences of actions across the security stack. Visual playbook design, threat-intelligence enrichment, one-click containment and bidirectional integration with service management reduce alert fatigue and shorten response time.

### Endpoint and Extended Detection and Response (EDR/XDR)

A unified endpoint agent monitors process activity, memory access and registry changes. XDR correlates endpoint telemetry with network and identity data across domains. Behavioral ransomware prevention, memory threat protection, process-tree reconstruction, host isolation and remote shell for live forensics address threats that bypass signature-based antivirus.

### Network Detection and Response (NDR)

Network traffic is captured from span ports or taps and analyzed with deep packet inspection and protocol parsing, East-West and North-South. Full packet capture, automated traffic baselining and encrypted-traffic analysis detect lateral movement, beaconing and data exfiltration, and provide forensic evidence.

### Threat Intelligence Platform (TIP)

Structured threat data (STIX/TAXII) from open-source, commercial and industry feeds is aggregated and matched against ingested telemetry. Indicator-of-compromise lifecycle management, threat actor profiling and false-positive filtering feed block lists to firewalls and endpoints.

### User and Entity Behavior Analytics (UEBA)

Unsupervised machine learning builds baselines of normal activity for every user, device and service account. Peer-group analysis, anomalous login detection, excessive privilege tracking and per-entity risk scoring uncover insider threats and compromised credentials without relying on known signatures.

### Vulnerability Prioritization

Vulnerability findings are correlated with active exploitation trends and asset exposure, so remediation effort goes first to the weaknesses attackers are actually using.

### Unified Case Management

A ticketing and workflow engine inside the StackX console links alerts to human resolution: evidence is attached automatically (packet captures, endpoint logs, threat intelligence), access is role-based, handlers collaborate in the case, and SLA dashboards show response performance.

<!-- Diagram guidance: layered defense — external boundary, internal visibility and control, identity, data and system integrity, recovery, and assurance — annotated with the Native / Integrated / Assured delivery modes. -->
[[figure: security-architecture | Security capability layers and delivery modes]]

## Extended Security Services (Optional)

Where {{customer_short}} prefers one accountable party across a wider picture, Verto Wave can deliver the services below around the platform. Each is scoped per service area and forms part of the platform build only if explicitly selected and quoted.

- **Identity and access** — single sign-on and multi-factor authentication for users, including phishing-resistant factors, contextual authorization and blocking of known-compromised credentials.
- **Privileged access** — credential vaulting, brokered administrative sessions and session recording.
- **Application edge protection** — web application firewall, API protection and distributed denial-of-service mitigation in front of published services.
- **Key and secret management** — central custody, rotation and expiry alerting for keys and secrets, and prevention of secrets held in code or configuration.
- **Data protection** — classification and tagging of sensitive data, masking in non-production environments and data-loss prevention on endpoints.
- **Backup and continuity** — backup design and operation, a documented disaster recovery plan, and recovery targets agreed and exercised on an agreed cycle.
- **Security assurance and testing** — independent penetration testing coordinated by Verto Wave, application and interface security testing and cloud configuration assessment, with findings tracked to closure.

## Delivery Boundaries

- Specific products for integrated services are selected during design against {{customer_short}}'s security standards, existing licenses and regulatory position.
- Recovery targets are agreed, not assumed; recovery point and time objectives are set during design.
- Where {{customer_short}} has issued a formal cybersecurity requirements document, Verto Wave provides a point-by-point compliance response mapping each requirement to a delivery mode. <!-- if not section_compliance_matrix -->
- Each security requirement is mapped to a delivery mode in the compliance matrix appendix. <!-- if section_compliance_matrix -->

---

*This module describes the security platform. The security operations service that runs it is described in StackX SOC Operations. Confirm the capabilities and any extended services in scope with the Security SME per bid.*
