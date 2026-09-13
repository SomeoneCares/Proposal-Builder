# Operations Level Agreement (OLA) Template

**Token:** `{{section_ola}}`  
**Group:** Cross-Cutting  
**Required:** Yes

---

## Introduction

This OLA outlines the level of service, priority definitions, response times, escalation times, authority matrix, and RACI model provided by Verto Wave for the IT managed services to the customer. The aim is to ensure timely and effective handling of incidents and requests to maintain optimal performance and availability of IT services.

*[Note: The OLA below is a reusable template. Response times, escalation times, operations team availability, and the RACI model must be confirmed per bid. Do not issue with placeholder values without validation against the current customer's SLA/OLA requirements.]*

## Priority Definitions

Incidents and requests are categorized based on their priority and impact on business operations. The following priority levels are defined:

### Priority 1 (Critical)

**Definition:** The entire system or a critical business function is down, causing a severe impact on operations with no workaround.

**Examples:** Loss of overlay connectivity for a location; central platform unavailable; hub down; no session possible at multiple sites.

### Priority 2 (High)

**Definition:** A major component of the system or a major business function is severely impacted, causing significant disruption. A workaround may exist but is not sustainable for long-term use.

**Examples:** Single site offline; session quality persistently below target at a site; NVR not recording; queue misrouting.

### Priority 3 (Medium)

**Definition:** A non-critical component is impacted, causing moderate disruption. A workaround exists and operations can continue.

**Examples:** Single extension fault; monitoring dashboard error; intermittent minor quality degradation on a secondary path.

### Priority 4 (Low)

**Definition:** A minor issue or request that has little to no impact on business operations.

**Examples:** General enquiries, routine service requests, report additions, cosmetic issues.

## Operations Levels and Response Times

Response times are defined based on the priority of the incident or request and the level required.

*[The response-time table below reflects a common VertoWave baseline from prior proposals. Confirm and adjust per bid.]*

| Priority | Response Time | Escalation to L2 | Escalation to L3 |
| :--- | :--- | :--- | :--- |
| Priority 1 | 30 Business Minutes | 1 Business Hour | 2 Business Hours |
| Priority 2 | 1 Business Hour | 2 Business Hours | 4 Business Hours |
| Priority 3 | 2 Business Hours | 4 Business Hours | 1 Business Day |
| Priority 4 | 4 Business Hours | 1 Business Day | 2 Business Days |

## Operations Team Availability

Verto Wave commits to providing operations services 8x5 (Sunday to Thursday, 9am–5pm), ensuring continuous availability and quick response to all incidents and requests.

*[If 24x7 or extended coverage is required, this must be explicitly agreed and documented per bid. 24x7 coverage is aligned to service hours across all locations and the central site, and applies where the customer selects the extended operations option.]*

## Authority Matrix

The following authority matrix outlines the roles and responsibilities for incident management and escalation:
---

## Figure — <Insert approved generic diagram / screenshot here>

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic diagram or screenshot relevant to this section's content (architecture, flow, dashboard, or topology as appropriate). No customer-specific names, environment, architecture, site names, or branding. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic image here. See image-placement guidance notes.]*

---


### L1 Operations Engineer

The first point of contact for all IT-related requests/issues.

- Receiving calls and incidents from help desk.
- Logging tickets.
- Verifying the issue and performing basic troubleshooting.
- Executing approved standard actions.
- Escalating cases beyond their skills to Level 2 specialists.

### L2 Operations Engineer

Handles more complex technical requests and issues escalated by L1.

- Work on escalated cases regarding provided solutions.
- Implement approved changes and configurations.
- Update, close, and approve closure of tickets.
- Escalate cases beyond their skills to Level 3 specialists.

### L3 Operations Engineer

Subject matter expert responsible for resolving the most advanced IT requests and issues.

- Work on escalated cases from Level 2.
- Implement approved advanced changes and configurations.
- Opening support tickets and managing communication with the vendor.

### Operations Team Lead

Oversees the L1 and L2 Operations teams, ensuring efficient and effective incident management and service delivery.

### Operations Manager

Leads the L3 Operations team, focusing on strategic IT initiatives, complex problem resolution, and continuous improvement of IT services.

### Technical Account Manager

Customer-facing role focusing on managing and supporting the technical aspects and relationship with its clients.

## RACI Model

The RACI model outlines who is Responsible, Accountable, Consulted, and Informed for various tasks and activities.

*[Attach or insert the RACI matrix per bid. Note: in some cases the Operations Team Lead can assume both functions of L1 and L2 Operations Manager.]*

## Escalation Process

If an incident is not resolved within the specified resolution time, it will be escalated according to the following hierarchy:

- **First Escalation:** Operations Team Lead
- **Second Escalation:** Operations Manager

## Reporting and Review

Regular reports on OLA performance will be provided to the customer on a monthly basis. OLA performance reviews will be conducted quarterly to ensure service quality and identify areas for improvement. Reporting includes per-location availability, service quality trend and incident summary.

## OLA Conditions

- The OLA clock will be paused if the case falls outside Verto Wave coverage or is dispatched to the customer team.
- Customer-reported critical and major requests must be raised by phone or email to be eligible for the KPIs.

---

*This section is a reusable building block. The OLA template above reflects the standard 4-priority, 8x5 model used across prior VertoWave proposals. Per-bid: confirm priority definitions, response/escalation times, coverage hours, RACI assignments, and KPI eligibility rules with the customer and with VertoWave Operations before issuance.*