# Firewall

**Token:** `{{module_firewall}}`  
**Group:** DeviceX/SDX — Edge & Branch Layer  
**Required:** No (optional add-on)

---

## Solution Overview

The DeviceX/SDX firewall delivers a stateful packet inspection engine that monitors and maintains context-aware sessions, ensuring seamless tracking of TCP/UDP connections. The flexible port-based access control lists allow administrators to permit or deny traffic based on well-known service ports, enabling fine-grained regulation of network access. Additionally, the firewall's protocol-aware filtering capabilities can identify and selectively handle traffic from specific network protocols, to enforce granular tailored security policies.

## Core Capabilities (Base — Stateful Firewall)

- Stateful packet inspection engine with context-aware session tracking (TCP/UDP)
- Flexible port-based access control lists — permit/deny by well-known service ports
- Protocol-aware filtering — identify and selectively handle traffic from specific network protocols
- NAT, policy-based routing, and traffic shaping
- Zone-based firewall policies

## Next-Generation Firewall (NGFW) — Optional Enhancement

When the Enhanced NGFW variant is selected, the firewall platform additionally provides:

- Application identification using Deep Packet Inspection (DPI)
- Control and block applications such as:
  - Social media
  - Streaming platforms
  - P2P and file sharing
  - Remote access tools
  - Per-user, per-group, or per-network policies
- Works even when applications use non-standard ports
- Category-based URL filtering (education, social media, gambling, malware, etc.)
- Domain and URL blacklists / whitelists
- SafeSearch and DNS-based filtering
- Time-based browsing policies
- Integrated Suricata IDS/IPS
  - Real-time attack detection and blocking
  - Signature-based and anomaly-based inspection
  - GeoIP-based blocking
  - DNS security and sinkholing
- VPN inspection and policy enforcement
- Encrypted traffic visibility (TLS inspection — optional)
---

## Figure — Firewall Security Zones / In-Site Micro-Segmentation

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic in-site micro-segmentation diagram showing distinct security zones (e.g. untrusted/guest, user/application, peripheral/device, surveillance/camera, voice, management) with explicit allow-list boundaries and no unwanted egress between zones. No customer-specific device names, no customer site names, no customer IP addressing. -->
<!-- Suggested source: Telemedicine proposal §4.3.3 (in-clinic micro-segmentation, 6 segments) — reuse only the generic zone model; strip any "telemedicine room", "consultation station", "medical device", "examination camera" labels before use. -->
<!-- Alternative: a network-perimeter firewall policy / zone-based firewall diagram (e.g.Guest Wi-Fi vs Corporate Core) — EGYCash-style zone-based firewall concept, genericised. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic firewall / micro-segmentation diagram here. See image-placement guidance notes.]*

---


## Firewall Template Deployment

- Define and allocate resources for the firewall control and data plane
- Create Template Firewall Policy to be installed on remote branches
- Deploy Firewall Template on remote branches

## In-Site Micro-Segmentation

Security at each site depends on isolation. Each traffic type is placed on its own segment, and all traffic between segments is forced through the device firewall so that lateral movement is blocked rather than merely observed.

A typical per-site segmentation model separates the following traffic classes. The exact segments and policy baseline are defined per engagement against the customer's traffic profile:

- Primary application / user segment
- Connected peripheral / device segment — explicit allow-list, no direct internet egress
- Surveillance / camera segment — isolated from all application traffic
- Voice segment for telephony endpoints
- Management segment — reachable only from the central management platform
- Administrative / guest segment — no route to any application resource

This matters in practice: the least-trusted device type on a site is often the most common initial foothold. Under this model, a compromised peripheral or camera can reach neither the application segment, the sensitive devices, nor the hub.

## Out-of-Scope (explicitly)

- Any security penetration testing, vulnerability assessments, code reviews, and forensic activities
- Any backup, network, and security activities not explicitly in scope
- Acquisition of any necessary commercial certificates (unless explicitly in scope)
- Any integration with components that don't support standard protocols used by DeviceX
- Any design changes to the existing environment
- Any change to existing customer devices or configurations (switches, routers, existing firewalls, and similar)

---

*This module is a reusable building block. Decide whether the customer requires the base stateful firewall or the enhanced NGFW variant (with IDS/IPS, URL filtering, DPI, TLS inspection), and define the per-site segmentation model against the current RFP/ITB. Do not assert certifications or compliance claims not validated for the current engagement.*