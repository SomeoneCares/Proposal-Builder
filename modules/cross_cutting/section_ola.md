# Operations Level Agreement (OLA)

**Token:** `{{section_ola}}`  
**Group:** Cross-Cutting  
**Required:** No

---

## Introduction

This Operations Level Agreement defines the service levels, priority definitions, response and escalation times, authority matrix and RACI model for the managed services Verto Wave provides to {{customer_short}}. Its aim is timely and effective handling of incidents and requests, to keep the in-scope services performing and available.

*[Response times, escalation times, coverage hours and the RACI model must be confirmed per bid against {{customer_short}}'s service-level requirements.]*

## Scope of Operations

Operations begin once the build stage completes and the service is handed over. For every in-scope system, Verto Wave:

- Performs regular health-check assessments and addresses the issues they identify
- Deploys supported updates and patches for the in-scope systems
- Monitors performance and functionality, and applies the tuning and adjustments that keep operations within target
- Manages {{customer_short}}'s team access to the in-scope systems — granting, revoking and reviewing it — on the approval of the designated stakeholder
- Manages report generation so the agreed reports stay accurate and complete
- Refers issues outside this scope to the responsible team within {{customer_short}}'s organization
- Provides the information {{customer_short}}'s stakeholders and change advisory board need for decisions
- Proposes improvements based on what the platform reports, and presents them to the agreed stakeholders
- Coordinates communication with the vendors of the in-scope products

## Priority Definitions

| Priority | Definition |
| :--- | :--- |
| Priority 1 (Critical) | The entire system or a critical business function is down, with severe impact on operations and no workaround. |
| Priority 2 (High) | A major component or business function is severely impacted; a workaround may exist but is not sustainable. |
| Priority 3 (Medium) | A non-critical component is impacted, causing moderate disruption; a workaround exists. |
| Priority 4 (Low) | A minor issue or request with little or no impact on business operations. |

### Examples

- **Priority 1:** central platform unavailable; loss of overlay connectivity for a location; no service possible at multiple sites. <!-- if devicex -->
- **Priority 1:** central platform unavailable; loss of monitoring or security visibility across the estate. <!-- if stackx and not devicex -->
- **Priority 2:** single site offline; service quality persistently below target at a site. <!-- if devicex -->
- **Priority 2:** NVR not recording at a site. <!-- if module_nvr -->
- **Priority 2:** call queue misrouting. <!-- if module_ipbx or module_stackx_call_center -->
- **Priority 3:** single extension fault. <!-- if module_ipbx -->
- **Priority 3:** monitoring dashboard error; intermittent minor degradation on a secondary path.
- **Priority 4:** general inquiries, routine service requests, report additions and cosmetic issues.

## Response and Escalation Times

| Priority | Response | Escalation to L2 | Escalation to L3 |
| :--- | :--- | :--- | :--- |
| Priority 1 | 30 business minutes | 1 business hour | 2 business hours |
| Priority 2 | 1 business hour | 2 business hours | 4 business hours |
| Priority 3 | 2 business hours | 4 business hours | 1 business day |
| Priority 4 | 4 business hours | 1 business day | 2 business days |

## Operations Team Availability

Verto Wave provides operations services 8x5, Sunday to Thursday, 9 AM to 5 PM local time.

*[If 24x7 or extended coverage is required, it must be explicitly agreed and documented per bid.]*

## Authority Matrix

- **L1 operations engineer** — first point of contact: receives incidents from the help desk, logs tickets, verifies the issue, performs basic troubleshooting and approved standard actions, and escalates to L2.
- **L2 operations engineer** — works escalated cases, implements approved changes and configurations, updates and closes tickets, and escalates to L3.
- **L3 operations engineer** — subject-matter expert for the most advanced cases; implements approved advanced changes and manages communication with vendors.
- **Operations team lead** — oversees the L1 and L2 teams to ensure effective incident management and service delivery.
- **Operations manager** — leads the L3 team, complex problem resolution and continuous improvement.
- **Technical account manager** — {{customer_short}}-facing role managing the technical relationship.

| Role | Responsibility | Staffing |
| :--- | :--- | :--- |
| L1 operations engineer | Incident and request logging, verification, basic troubleshooting and approved standard actions | {{ola_l1_engineers}} |
| L1 operations manager | Manages L1 activity, confirms the OLA targets are met and escalates to L2 | {{ola_l1_manager}} |
| L2 operations engineer | Advanced troubleshooting, system configuration and application operations | {{ola_l2_engineers}} |
| L3 operations engineer | Expert troubleshooting, complex resolution and vendor coordination | Remote, on site when needed |
| Operations team lead | Manages L2 activity and escalates to L3 | Remote, on site when needed |
| Operations manager | Oversees L3 activity and manages escalated cases | Remote, on site when needed |

## RACI Model

R responsible · A accountable · C consulted · I informed

| Activity | L1 engineer | L1 manager | L2 engineer | Team lead | L3 engineer | Operations manager |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Incident and request logging | R | A | — | — | — | — |
| Basic troubleshooting | R | A | C | — | — | — |
| Advanced troubleshooting | I | I | R | A | C | I |
| Complex issue resolution | I | I | I | I | R | A |
| System configuration | I | I | R | A | C | — |
| Application operations | I | I | R | A | C | — |
| Vendor coordination | I | I | I | I | R | A |
| First-level escalation | I | I | R | A | — | — |
| Second-level escalation | I | I | I | I | R | A |
| OLA performance reporting | I | I | I | A | I | A |
| OLA review meetings | I | I | I | A | I | A |

In some engagements {{customer_short}} assigns and manages the L1 operations engineers and the L1 operations manager; where that applies, the L1 rows above sit with {{customer_short}}'s team and Verto Wave takes the L2 and L3 responsibilities.

*[Confirm per bid who owns L1, and whether the operations team lead covers both the L1 and L2 lead functions.]*

## Escalation

A case that reaches the escalation times in the table above is escalated first to the operations team lead and then to the operations manager. Verto Wave commits to the response and escalation times stated in this agreement; restoration time is not a committed deliverable, because it depends on the fault, the vendor and {{customer_short}}'s environment.

## Reporting and Review

OLA performance is reported to {{customer_short}} monthly and reviewed quarterly to confirm service quality and identify improvements. Reports include availability, service-quality trends and an incident summary.

## OLA Conditions

- The OLA clock is paused while a case is outside Verto Wave's coverage, dispatched to {{customer_short}}'s team, or escalated to vendor support.
- Critical and major requests must be raised by phone or email to be eligible for the KPIs.

---

*This section applies only when managed services are part of the offering. Confirm priority definitions, times, coverage and KPI rules with Verto Wave Operations before issue.*
