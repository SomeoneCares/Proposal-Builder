# IP-PBX / Unified Communications

**Token:** `{{module_ipbx}}`  
**Group:** DeviceX/SDX — Edge & Branch Layer  
**Required:** No (optional add-on)

---

## Solution Overview

The DeviceX IP-PBX delivers enterprise telephony with local call processing at each site. It reduces telephony costs, improves collaboration through unified communications and scales with {{customer_short}}'s needs.

## Core Capabilities

- SIP and IAX2 protocol support
- Advanced call routing and queuing
- Interactive voice response (IVR)
- Voicemail-to-email
- Call recording and monitoring
- Conference calling
- Mobile app integration
- Integration with CRM systems

## Call Flows

The call-flow patterns below illustrate what the platform PBX implements. The exact flows, queues, IVR structure and routing are designed with {{customer_short}} during the design stage.

| Flow | Trigger | Behavior |
| :--- | :--- | :--- |
| Scheduled session | A booked appointment | The originating extension dials the remote extension or bridge directly; presence confirms availability; media is prioritized end to end and can be recorded under the agreed retention policy. |
| On-demand expert request | A user needs a specialist's input | A soft key or IVR option routes the call to the right queue, presenting the site's identity; unanswered calls overflow to a secondary group. |
| Urgent escalation | A time-critical case | A priority code bypasses the standard queue, rings the on-call group simultaneously and raises the call to the top traffic class. |
| Inter-site and administrative | Day-to-day coordination | Extension-to-extension dialing across all sites, voicemail-to-email, IVR reception and optional local breakout where regulation permits. |

<!-- Diagram guidance: the four call flows and the local survivability path (site continues on local services when the WAN is down). No extension numbers or site names. -->
[[figure: ipbx-call-flows | Call flows and local survivability | Diagram | Architect]]
## Value to Distributed Sites

- Clear voice connectivity between the central site and every site
- Encryption of all voice traffic
- One consolidated voice platform
- Lower telephony costs across the footprint

## Local Survivability

Internal telephony continues during a wide-area outage: each site keeps local call handling, extension-to-extension dialing and voicemail, and resumes routing to remote queues when the overlay is restored.

<!-- if per_product_sizing -->

## Sizing Basis

| Dimension | Counted As | Confirmed Figure |
| :--- | :--- | :--- |
| Extensions | Per site and total | {{sizing_ipbx_extensions}} |
| Concurrent calls | Per site busy hour | {{sizing_ipbx_concurrent_calls}} |
| Trunks | SIP channels / carrier | {{sizing_ipbx_trunks}} |
| Recording retention | Days | {{sizing_ipbx_recording_retention}} |

*[Confirm every figure for this bid against the confirmed requirement. Do not carry numbers forward from a prior engagement.]*

<!-- endif -->

<!-- if services -->

## Acceptance Tests

The tests below are executed jointly and form part of the acceptance test plan for this module.

| Test | Method | Pass Criterion |
| :--- | :--- | :--- |
| Registration | Register all site handsets | 100 % registered |
| Survivability | Disconnect WAN; dial internal and emergency test | Both calls succeed |
| Call quality | Inter-site call under load | MOS ≥ agreed target |

<!-- endif -->

---

*This module is a reusable building block. Define call flows, queues, IVR structure and routing against the current RFP/ITB; do not assert telephony licensing or numbering positions that have not been validated.*
