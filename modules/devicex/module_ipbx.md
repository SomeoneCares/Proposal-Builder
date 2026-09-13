# IP-PBX / Unified Communications

**Token:** `{{module_ipbx}}`  
**Group:** DeviceX/SDX — Edge & Branch Layer  
**Required:** No (optional add-on)

---

## Solution Overview

Enabling efficient call handling and management. The DeviceX IP-PBX delivers enterprise communications with local processing, reducing telephony costs, enhancing collaboration through unified communications, and offering scalable solutions to meet evolving business needs.

## Core Capabilities

- SIP and IAX2 protocol support
- Advanced call routing and queuing
- Voicemail-to-email integration
- Call recording and monitoring
- Conference calling and collaboration
- Mobile app integration
- Interactive Voice Response (IVR)
- Call center features and reporting
- Integration with CRM systems
- Unified communications platform

## Call Flows (generic — define per engagement)

The following call-flow patterns illustrate the kinds of behaviour the platform PBX can implement. They are shown as a reusable template; the exact flows, queues, IVR structure and routing are designed per engagement against the customer's operating model.

### Scheduled Session

| Trigger | Behaviour |
|---------|-----------|
| Booked appointment | The originating endpoint dials the remote extension or session bridge directly. Presence confirms availability before connection. Media is classified and prioritised end to end. The session may be recorded locally and archived centrally under the agreed retention policy. |

### On-Demand Remote Expert Request

| Trigger | Behaviour |
|---------|-----------|
| A user needs an opinion | A single soft-key or IVR selection routes the call to the relevant queue at the remote site. The call presents with site identity so the responder has context on answer. It overflows to a secondary responder or on-call group if unanswered. |
---

## Figure — IP-PBX Call Flows / Telephony Topology

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic IP-PBX call-flow diagram showing the four standard flows (scheduled / on-demand / urgent / inter-site) and local survivability (site continues on local services when the wide-area link is down). No customer-specific extension numbers, no customer site names, no customer-specific telephony licensing/numbering details. -->
<!-- Suggested source: Telemedicine proposal §3.4 (Clinical Communication Flows, 4 flows) — genericise the diagram and labels. -->
<!-- Alternative: a PBX topology diagram showing endpoints, trunks, voicemail, and survivability path. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic IP-PBX call-flow / topology diagram here. See image-placement guidance notes.]*

---


### Urgent Escalation

| Trigger | Behaviour |
|---------|-----------|
| Time-critical case | A priority code bypasses standard queueing, rings the on-call group simultaneously, and raises the session to the top traffic class so it is protected even under contention. |

### Inter-Site and Administrative

| Trigger | Behaviour |
|---------|-----------|
| Operational coordination | Extension-to-extension dialing across all sites, plus voicemail-to-email, IVR-based reception, and optional local breakout to the in-country / public network where regulation permits. |

## Value to Distributed Sites

- High-quality, effortless voice connectivity between the central site and all branches
- Protects all voice traffic with strong encryption for privacy
- Establishes a secure and consolidated voice communication platform
- Reduces telephony costs across the distributed footprint

## Local Survivability

Internal telephony continues during a wide-area outage. The platform PBX at each site maintains local call handling, extension-to-extension dialing, and voicemail, and can route to the remote queues — including an urgent escalation path — when the overlay is restored. Remote extensions are created for the remote sites. Call recording and retention policy are configurable per engagement.

## Out-of-Scope (explicitly)

- Any communication with the telco operators
- Any configuration/troubleshooting in the Business Virtual Machines hosted on DeviceX
- Any migration activities
- Any deployment or configuration of third-party systems not included in the proposal scope
- Supplying and mounting hardware, network equipment, and storage devices, along with the necessary cabling other than DeviceX
- Procurement of any telephony numbering, VoIP or data-service licenses and regulatory permits

---

*This module is a reusable building block. Include when branch voice / unified communications is in scope for the current engagement. Define the call flows, queues, IVR structure and routing against the current RFP/ITB; do not assert telephony licensing or numbering positions not validated for the current engagement.*