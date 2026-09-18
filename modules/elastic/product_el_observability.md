# Server and Infrastructure Monitoring <!-- if not named_product_el_observability -->
# Elastic Observability <!-- if named_product_el_observability -->

**Token:** `{{product_el_observability}}`
**Group:** Elastic Products
**Required:** No

---

Server and infrastructure monitoring collects metrics from physical, virtual and containerized systems and turns them into health, capacity and performance views. <!-- if not named_product_el_observability -->
Elastic Observability collects metrics from physical, virtual and containerized systems and turns them into health, capacity and performance views. <!-- if named_product_el_observability -->

## What It Delivers

- One platform for physical, virtual and containerized servers, with agent and agentless collection
- Processor, memory, disk, filesystem and network metrics, current and historical
- Process-level visibility, so a fault can be traced to what consumed the resource
- Hardware health where the platform exposes it, including disk and sensor status
- Threshold and baseline alerting, with maintenance windows to keep planned work quiet
- Dashboards per server group, and reporting on capacity trends

## Build Activities <!-- if services -->

<!-- if services -->
- Deploy the platform and roll out collection to the servers in scope
- Configure agentless collection where an agent is not permitted
- Create the monitors, groups and tags agreed for each server role
- Configure alerts, notification routes and role-based access
- Build the agreed dashboards and reports, and hand over the administration guide
<!-- endif -->

## Sizing Basis

Sizing follows the number of monitored hosts, the collection interval and the retention period. The figures are recorded in the design document.

*[Confirm host counts, collection intervals and retention per bid.]*
