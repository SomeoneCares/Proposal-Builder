# Configuration Management and Discovery <!-- if not named_product_ot_ucmdb -->
# OpenText UCMDB and Universal Discovery <!-- if named_product_ot_ucmdb -->

**Token:** `{{product_ot_ucmdb}}`
**Group:** OpenText Products
**Required:** No

---

Discovery finds what is deployed, and the configuration management database keeps the result as a governed record of components and the services they support. <!-- if not named_product_ot_ucmdb -->
OpenText Universal Discovery finds what is deployed, and OpenText UCMDB keeps the result as a governed record of components and the services they support. <!-- if named_product_ot_ucmdb -->

## What It Delivers

- Agentless and credential-based discovery of servers, network devices, databases, middleware and applications
- Dependency mapping upward from the infrastructure, so each business service shows what it runs on
- One configuration record shared by the service desk, operations and reporting
- Change history per component, so a fault can be read against what changed
- Reconciliation rules that merge findings from several sources without creating duplicates
- Impact views used when a change is approved or an incident is triaged

## Build Activities <!-- if services -->

<!-- if services -->
- Deploy the servers and discovery probes and bring them to the supported patch level
- Configure credentials and discovery schedules for the in-scope ranges
- Model the agreed business services and their component types
- Configure reconciliation, ageing and data-quality rules
- Synchronize the configuration record with the service management platform <!-- if product_ot_smax -->
- Validate discovered data against a sample of known systems and hand over the administration guide
<!-- endif -->

## Acceptance Criteria

Discovery is accepted when the agreed ranges are scanned, the modelled services resolve to their components, and the duplicate rate is within the threshold recorded in the design document.

*[Confirm the ranges, credential owners and the services to model per bid.]*
