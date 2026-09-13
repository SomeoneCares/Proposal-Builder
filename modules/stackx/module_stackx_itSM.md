# StackX ITSM Platform Enterprise Management

**Token:** `{{module_stackx_itSM}}`  
**Group:** StackX — Control / Orchestration / SOC / Operations Layer  
**Required:** No (optional module)

---

## Overview

StackX ITSM Platform Enterprise Management provides IT service management capabilities aligned to ITIL v4 best practices, integrated with the broader StackX platform for incident, problem, and change management, service catalog, and operational governance.

## Capabilities

- Incident, problem, and change management aligned to ITIL v4
- Service catalog management reflecting the customer's operational and strategic objectives
- Structured escalation pathways and collaborative workflows to enhance resolution efficiency
- Integration with StackX monitoring, observability, and automation for event-driven incident generation and closure
- ITSM policy and procedure implementation and fine-tuning to align with the customer's objectives and governance model
- Cabinet (CAB) and stakeholder support for data-driven decision-making
- Customer-facing access to approved standard actions and service requests
- Reporting and analytics for service performance, compliance, and efficiency

## StackX ITSM Integration Context

- StackX Observability and APM feeds event correlation into ITSM for automatic incident generation and closure
- StackX Automation & Orchestration executes approved standard actions and remediation workflows from ITSM
- StackX Compliance Assurance and Operations Integrity supports ITSM-governed change and compliance evidence
- StackX Endpoint Management and Network Operations integrate with ITSM for configuration-item (CI) context and operational ticketing

## Monitoring-to-Incident Workflow

The following workflow shows how event telemetry is converted into managed incidents. It is a reusable operating pattern; the exact mappings, signatures, assignment rules and OLA application are defined per engagement.

| Stage | What happens |
|-------|--------------|
| Detection | StackX Network Monitoring or StackX Log Management identifies an event such as link loss, high packet discards, a firewall event, an endpoint alert, or a certificate problem. |
| Normalisation | The integration maps the event to a location, site, service, asset, priority and event signature. |
| Correlation and deduplication | Repeated alarms are grouped so that one underlying fault does not create an uncontrolled ticket storm. |
| Ticket creation or enrichment | StackX ITSM creates or updates an incident and includes the event ID, timestamps, affected CI, evidence link, and current condition. |
| Assignment and escalation | Rules assign to the correct location, network, security, platform or service team and apply the appropriate OLA. |
| Resolution and closure | The resolver records action, service restoration time, root cause where known, workaround, and closure code; major incidents receive a review. |

---

## Figure — ITSM Service Desk / Incident & Request Workflow

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic ITSM service-desk dashboard image showing ticket counts, open-ticket lists, navigation structure, and dashboard-oriented visibility — plus an incident-to-resolution workflow diagram (monitoring → alert → triage → investigation → resolution → closure) and a request-fulfilment / change / major-incident operating workflow. No customer-specific service-desk configuration, no customer-specific category/workflow/asset names, no customer site names. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic ITSM service-desk / incident-workflow diagram here. See image-placement guidance notes.]*

---

## Operating Workflows

The following are representative operating workflows the StackX ITSM service can implement. They are shown as a reusable template; the exact workflows, approvals and notifications are designed per engagement.

### Request Fulfilment

A requester selects a service from the catalog, supplies structured information, and submits the request. StackX ITSM validates eligibility and access rights, applies an approval path where required, assigns the task to the responsible group, tracks fulfilment steps, sends notifications, and closes the request after confirmation or defined administrative closure.

### Change Workflow

A change is raised against one or more configuration items and services. The change manager or designated approver evaluates risk, confirms the maintenance window, validates implementation and rollback plans, authorises execution, records implementation evidence, and performs a post-implementation review. Emergency changes must retain the same evidence after execution even where prior approval is bypassed.

### Major Incident Workflow

A major incident creates a coordinated response record with incident commander, technical workstreams, communications owner, customer-impact statement, update cadence, decision log, and recovery milestones. For an active service outage, the response should prioritise service restoration, preserve evidence, coordinate platform and carrier investigations, and trigger a problem record when the incident is closed.

## Reference Screenshots Note (for the bid team)

The following note is provided for the bid team on how to handle third-party reference screenshots in an ITSM section:

> Equivalent platform reference screenshots may be included to illustrate the underlying technology. In the StackX ITSM service, equivalent screens would be presented under the StackX brand and configured with the customer's entities, categories, workflows, assets and service catalog. Any screenshots are included transparently and are not represented as screenshots of a separately developed product.

## Out-of-Scope (explicitly)

- Any ITSM platform implementation or migration not explicitly in scope
- Operating 3rd party ITSM systems aside from the systems included in this scope
- Any development and debugging activities not explicitly in scope
- Any development of custom ITSM workflows outside agreed scope

---

*This module is a reusable building block. Confirm per bid whether StackX ITSM is included, whether it integrates with an existing customer ITSM, and the scope of ITSM policy/procedure implementation and fine-tuning. The monitoring-to-incident workflow, operating workflows and screenshot-guidance note are platform-agnostic patterns — tailor the example event types and assignment rules to the current engagement.*
