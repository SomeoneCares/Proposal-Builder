# StackX SOC Operations

**Token:** `{{module_stackx_soc}}`  
**Group:** StackX — Control / Orchestration / SOC / Operations Layer  
**Required:** No (optional module)

---

## Overview

StackX SOC Operations is the security operations service Verto Wave runs for {{customer_short}} on the StackX platform. Verto Wave's analysts monitor, triage, investigate and respond to security events, and report on {{customer_short}}'s security posture, so that detection capability becomes day-to-day protection.

*[Confirm the SOC coverage hours, the scope of monitored assets and whether response actions are executed by Verto Wave or by {{customer_short}} per bid.]*

## Service Model

| Tier | Role |
| :--- | :--- |
| Tier 1 — monitoring and triage | Watches alerts, validates them, discards false positives, enriches genuine alerts and raises cases. |
| Tier 2 — investigation | Investigates cases, determines scope and impact, and recommends or executes containment. |
| Tier 3 — response and threat hunting | Leads major incident response, performs proactive threat hunting and refines detection use cases. |
| SOC manager | Owns service quality, reporting and service reviews with {{customer_short}}. |

## Service Activities

- **Continuous monitoring** of the in-scope assets during the agreed coverage hours
- **Alert triage** against defined criteria, with escalation paths per severity
- **Incident response** following the lifecycle below, coordinated with {{customer_short}}'s teams
- **Use-case management** — detection rules and playbooks reviewed, tuned and extended as the environment changes
- **Threat hunting** — hypothesis-driven searches for threats that have not triggered alerts
- **Threat intelligence** — relevant intelligence reviewed and applied to detections and block lists
- **Vulnerability follow-up** — high-risk findings tracked with the asset owners until closed

## Incident Response Lifecycle

1. **Detect** — an alert or hunt finding is confirmed as a security incident.
2. **Triage** — severity, scope and affected assets are established.
3. **Contain** — the threat is isolated, for example by isolating a host or blocking an indicator.
4. **Eradicate** — the cause is removed and affected systems are cleaned.
5. **Recover** — services are restored and monitored for recurrence.
6. **Learn** — a post-incident review records the root cause and improvements.

<!-- Diagram guidance: the SOC tiers around the incident response lifecycle, with escalation paths to the customer's teams. -->
[[figure: soc-operations | SOC tiers and incident response lifecycle]]

## Reporting and Service Reviews

- Monthly security operations report: alert volumes, incidents, response times and posture trends
- Key measures: mean time to detect (MTTD) and mean time to respond (MTTR)
- Quarterly service review with {{customer_short}} covering incidents, use cases and improvement actions

## Platform

The service operates the capabilities described in StackX Security — SIEM, SOAR, EDR/XDR, NDR, threat intelligence, behavior analytics and case management. <!-- if module_stackx_security -->

The service operates on the StackX security platform, whose capabilities are confirmed in the design. <!-- if not module_stackx_security -->

---

*This module applies only when managed services are part of the offering. Confirm staffing, coverage and response authority with the Security SME per bid.*
