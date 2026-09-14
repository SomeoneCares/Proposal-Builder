# StackX ITSM

**Token:** `{{module_stackx_itSM}}`  
**Group:** StackX — Control / Orchestration / SOC / Operations Layer  
**Required:** No (optional module)

---

## Overview

StackX ITSM is the central service management platform for {{customer_short}}'s IT operations: the primary ticketing system, the service portal for business users, and the orchestrator of service management processes. Its out-of-the-box processes follow ITIL 4 practices and can be extended to task automation, configuration management and asset management.

## Capabilities

### Plan

- Service portfolio and service catalog management
- Service level management, with review and resolution metrics for incidents and requests
- Maintenance windows, blackout periods, work schedules and holidays for change and service level management
- Vendor and contract management

### Build

- Change management with normal, standard and emergency workflows, task management and change models
- Release management
- Knowledge management for articles, solutions and historical knowledge
- Service asset and configuration management, integrated with the CMDB <!-- if module_stackx_ops_config_mgmt -->

### Run

- Incident management with embedded workflows and collaboration
- Problem management with task planning and root-cause tracking
- Service request management
- On-call schedule management for agent availability and ticket distribution
- Software asset management

## Service Portal and Smart Service Desk

A modern service portal gives business users one place to request services, track status and find self-help articles. Machine learning drives further automation: automatic ticket classification and routing, intelligent knowledge delivery and search across internal and external content, and detection of trending topics.

## Monitoring-to-Incident Workflow <!-- if module_stackx_observability_apm or module_stackx_network_ops or module_stackx_event_log_mgmt or module_stackx_ops_config_mgmt -->

<!-- if module_stackx_observability_apm or module_stackx_network_ops or module_stackx_event_log_mgmt or module_stackx_ops_config_mgmt -->
| Stage | What happens |
| :--- | :--- |
| Detection | StackX monitoring identifies an event such as link loss, high packet discards, a firewall event, an endpoint alert or a certificate problem. |
| Normalization | The event is mapped to a location, site, service, asset, priority and event signature. |
| Correlation | Repeated alarms are grouped so one underlying fault does not create a flood of tickets. |
| Ticket creation | StackX ITSM creates or updates an incident with the event ID, timestamps, affected configuration item, evidence and current condition. |
| Assignment | Rules assign the incident to the right team and apply the agreed service level. |
| Resolution and closure | The resolver records the action, restoration time, root cause and closure code; major incidents receive a review. |
<!-- endif -->

<!-- Diagram guidance: monitoring → alert → triage → investigation → resolution → closure, plus the request fulfilment and change workflows. Generic labels only. -->
[[figure: itsm-workflow | Incident, request and change workflows]]

## Operating Workflows

- **Request fulfilment.** A requester selects a catalog service and submits it; StackX ITSM validates eligibility, applies any approval path, assigns the task, tracks fulfilment and closes the request after confirmation.
- **Change.** A change is raised against configuration items and services; the change manager evaluates risk, confirms the maintenance window, validates implementation and rollback plans, authorizes execution and holds a post-implementation review. Emergency changes keep the same evidence after execution.
- **Major incident.** A coordinated response record holds the incident commander, workstreams, communications owner, customer-impact statement, update cadence, decision log and recovery milestones, and a problem record is opened when the incident closes.

## Governance

- ITSM policies and procedures implemented and tuned to {{customer_short}}'s governance model
- Change Advisory Board (CAB) support with data for decisions
- Reporting and analytics on service performance, compliance and efficiency

## Reference Screenshots (for the bid team)

Equivalent platform reference screenshots may be included to illustrate the underlying technology. In the StackX ITSM service, screens are presented under the StackX brand and configured with {{customer_short}}'s entities, categories, workflows, assets and service catalog. Screenshots are included transparently and are not represented as screenshots of a separately developed product.

---

*This module is a reusable building block. Confirm whether StackX ITSM replaces or integrates with an existing service management platform, and the scope of process implementation.*
