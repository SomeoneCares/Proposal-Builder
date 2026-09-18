# Service Management Platform <!-- if not named_product_ot_smax -->
# OpenText SMAX <!-- if named_product_ot_smax -->

**Token:** `{{product_ot_smax}}`
**Group:** OpenText Products
**Required:** No

---

The service management platform gives {{customer_short}} one place to raise, route and resolve work, with the service catalog, workflows and service-level targets held in the same system. <!-- if not named_product_ot_smax -->
OpenText SMAX gives {{customer_short}} one place to raise, route and resolve work, with the service catalog, workflows and service-level targets held in the same system. <!-- if named_product_ot_smax -->

## What It Delivers

- A self-service portal and service catalog, so requests arrive structured rather than by mail or phone
- Incident, request, problem, change and release management against one record of the service
- Service-level management with targets per service and warnings before a target is missed
- A knowledge base that offers articles to the agent while the ticket is worked
- Approval routes for changes and for catalog items that carry cost or risk
- Reporting on volumes, ageing, first-line resolution and service-level attainment

## Build Activities <!-- if services -->

<!-- if services -->
- Deploy the platform and its prerequisites, and bring every component to the supported patch level
- Configure the service catalog, the request and incident workflows and the approval routes
- Configure service-level targets, the priority matrix and the escalation rules
- Integrate with the configuration management database so tickets carry the affected service <!-- if product_ot_ucmdb -->
- Integrate with monitoring so an event opens and updates a ticket automatically
- Integrate with the automation platform so catalog items run without manual work <!-- if product_ot_oo -->
- Integrate with the directory for users and groups, and with the mail platform for notification
- Run the agreed test scenarios and hand over to the service desk team
<!-- endif -->

## Scope Boundaries

Workflow, catalog and form configuration is bounded, and the agreed counts are recorded in the design document. Anything beyond them is handled as a change request.

*[Confirm the workflow, catalog item and form counts per bid, and whether directory and mail integration are in scope.]*
