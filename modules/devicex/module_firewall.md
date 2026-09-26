# Firewall

**Token:** `{{module_firewall}}`  
**Group:** DeviceX/SDX — Edge & Branch Layer  
**Required:** No (optional add-on)

---

## Solution Overview

The DeviceX/SDX firewall is a stateful packet-inspection engine that tracks TCP and UDP sessions in context. Port-based access control lists permit or deny traffic by service port, and protocol-aware filtering identifies and handles specific protocols so that security policy can be tailored precisely.

## Core Capabilities

- Stateful packet inspection with context-aware session tracking
- Port-based access control lists
- Protocol-aware filtering
- NAT, policy-based routing and traffic shaping
- Zone-based firewall policies

## Next-Generation Firewall (Optional Enhancement)

*[Choose per bid: the base stateful firewall above, or the enhanced next-generation variant below.]*

The enhanced variant adds:

- Application identification using deep packet inspection, working even on non-standard ports
- Application control per user, group or network — for example social media, streaming, peer-to-peer file sharing and remote-access tools
- Category-based URL filtering, domain and URL allow and block lists, safe-search and DNS-based filtering
- Time-based browsing policies
- An integrated intrusion detection and prevention engine with signature- and anomaly-based inspection, real-time blocking, geolocation-based blocking, DNS security and sinkholing
- VPN inspection and policy enforcement
- Optional TLS inspection for visibility into encrypted traffic

## Template Deployment

- Define and allocate resources for the firewall control and data planes
- Create a template firewall policy for the remote sites
- Deploy the template to every site from the central management platform

## In-Site Micro-Segmentation

Security at each site depends on isolation. Each traffic type is placed on its own segment, and all traffic between segments passes through the DeviceX firewall, so lateral movement is blocked rather than merely observed.

A typical segmentation model separates:

- The primary application and user segment
- A connected peripheral and device segment, with an explicit allow-list and no direct Internet access
- A surveillance and camera segment, isolated from all application traffic <!-- if module_nvr -->
- A voice segment for telephony endpoints <!-- if module_ipbx -->
- A management segment, reachable only from the central management platform
- An administrative and guest segment with no route to any application resource

The least-trusted device on a site is often the most common entry point. Under this model, a compromised peripheral or camera can reach neither the application segment nor the central site.

<!-- Diagram guidance: the site's security zones with allow-list boundaries between them and no unwanted paths. No device names, site names or addressing. -->
[[figure: firewall-segmentation | In-site micro-segmentation zones | Diagram | Architect]]
<!-- if per_product_sizing -->

## Sizing Basis

| Dimension | Counted As | Confirmed Figure |
| :--- | :--- | :--- |
| Firewall policies | Rules in the class template | {{sizing_firewall_firewall_policies}} |
| Zones per site | Per 6.6 | {{sizing_firewall_zones_site}} |
| Inspection | IPS / URL / TLS enabled? | {{sizing_firewall_inspection}} |

*[Confirm every figure for this bid against the confirmed requirement. Do not carry numbers forward from a prior engagement.]*

<!-- endif -->

<!-- if services -->

## Acceptance Tests

The tests below are executed jointly and form part of the acceptance test plan for this module.

| Test | Method | Pass Criterion |
| :--- | :--- | :--- |
| Inter-zone deny | Attempt camera → user zone connection | Blocked and logged centrally |
| IPS | Replay a test signature | Detected, blocked and logged |
| Template consistency | Compare site policy hash with template | Hashes match |

<!-- endif -->

---

*This module is a reusable building block. Define the variant and the per-site segmentation model against the current RFP/ITB. Do not assert certifications not validated for this engagement.*
