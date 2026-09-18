# Configuration Management and Discovery <!-- if not named_product_ot_ucmdb -->
# OpenText UCMDB and Universal Discovery <!-- if named_product_ot_ucmdb -->

**Token:** `{{product_ot_ucmdb}}`
**Group:** OpenText Products
**Required:** No

---

Discovery finds what is deployed, and the configuration management database keeps the result as a governed record of components and the services they support. <!-- if not named_product_ot_ucmdb -->
OpenText Universal Discovery finds what is deployed, and OpenText UCMDB keeps the result as a governed record of components and the services they support. <!-- if named_product_ot_ucmdb -->

The product is two halves that are bought and deployed together: a discovery engine that reaches into the estate through credentialed, agentless access, and a modelled database that identifies, reconciles and ages what discovery returns. Neither is useful alone — discovery without reconciliation produces duplicates, and a database without discovery becomes a spreadsheet that ages the day it is signed off.

## Where It Fits in This Project

{{customer_short}}'s requirement is to know what is deployed, what depends on what, and which business services are affected when a component fails or changes. That answer has to be produced automatically, because a manually maintained inventory is out of date within weeks of the project closing.

In this project the product is the source of that answer for every other platform in scope: the service desk raises tickets against its records, correlation separates cause from symptom using its service model, and change impact is assessed against its relationships. Its scope is the address ranges, configuration item classes and business services agreed during the design stage; the quantities that bound the work are held in the professional services scope and are not repeated here.

## Platform Components

<!-- if not named_product_ot_ucmdb -->
- **Configuration management database server** — the modelled store of configuration items, their attributes and their relationships, with the class model that defines what may be recorded.
- **Database** — the relational store behind the server, holding the current model and its change history.
- **Discovery probe** — the component placed in each network zone that performs the credentialed scan, holds the credentials locally and returns results to the server. One or more per zone, depending on reach and scan volume.
- **Discovery content** — the supplied, regularly updated library of discovery logic per technology: operating systems, network devices, databases, middleware, virtualization, storage, cloud services and common applications.
- **Inventory agent and scanner** — the optional component installed on hosts where deeper hardware and installed-software detail is needed than agentless access can return.
- **Reconciliation and identification engine** — the rules that decide when two findings are the same real thing, so several sources merge into one record.
- **Query and impact engine** — the query language and saved views used for impact analysis, reporting and the service model.
- **Service modelling** — the top-down mapping of a business service from its entry point, and the bottom-up dependency mapping from infrastructure.
- **Browser interface** — the read-oriented interface used by the service desk and operations to look up a component, its dependencies and its history.
- **Integration framework** — the inbound population and outbound push interfaces that exchange records with other platforms.
<!-- endif -->

<!-- if named_product_ot_ucmdb -->
- **UCMDB server** — the modelled store of configuration items, their attributes and their relationships, with the class model that defines what may be recorded.
- **UCMDB database** — the relational store behind the server, holding the current model and its change history.
- **Data Flow Probe** — the Universal Discovery component placed in each network zone; it performs the credentialed scan, holds credentials locally, and returns results to the UCMDB server. It carries its own local database for scan data.
- **Discovery and integration content** — the supplied, regularly updated content packs holding the discovery logic per technology: operating systems, network devices, databases, middleware, virtualization, storage, cloud services and common applications.
- **Universal Discovery inventory agent and scanner** — the optional agent-based path, used where deeper hardware and installed-software detail is needed than agentless access returns, including software recognition against the supplied software library.
- **Reconciliation and identification engine** — the rules that decide when two findings are the same real thing, so several sources merge into one record.
- **Topology query language and impact rules** — the query and saved-view mechanism used for impact analysis, reporting and the service model.
- **Automated service modelling** — top-down mapping of a business service from its entry point, alongside bottom-up dependency mapping from infrastructure.
- **UCMDB Browser** — the read-oriented interface used by the service desk and operations to look up a component, its dependencies and its history.
- **Integration Studio** — the population and push integrations that exchange records with other platforms.
<!-- endif -->

*[The component list follows the vendor's current packaging. Confirm the component names, and whether the inventory agent is inside the entitlement being quoted, with the Verto Wave product team before issue.]*

## What It Delivers

- Agentless, credential-based discovery of servers, network devices, databases, middleware, virtualization, storage and applications
- Agent-based inventory where deeper hardware and installed-software detail is needed, including recognition of installed software against the supplied software catalog
- Discovery of public and private cloud resources through their management interfaces, where those accounts are in scope
- Dependency mapping upward from the infrastructure, and top-down mapping of a service from its entry point, so each business service shows what it runs on
- One configuration record shared by the service desk, operations and reporting, with an agreed owner per attribute so two systems do not disagree about the same field
- Change history per component, so a fault can be read against what changed and when
- Reconciliation and identification rules that merge findings from several sources without creating duplicates
- Query-based views and impact rules used when a change is approved or an incident is triaged
- Ageing and lifecycle rules that retire records for components the estate no longer contains, so the database shrinks as well as grows
- Data-quality reporting: coverage per range, credential failures, records missing mandatory attributes, and records no discovery job has confirmed recently
- Vendor content updates that extend discovery to new device, platform and cloud types between releases


[[figure: ot-ucmdb-model | Discovery and the configuration model]]

## Integration

The links below are configured only where both platforms are part of this proposal.

- The service management platform consumes the configuration record, so a ticket is raised against a known service and a change is assessed against real relationships; the two systems synchronize on the agreed attribute ownership. <!-- if product_ot_smax -->
- The event console takes the service model, so topology-based correlation runs against the same components the service desk sees. <!-- if product_ot_obm -->
- The network monitoring platform supplies discovered network topology, devices and interfaces, so the network is not discovered twice by two products. <!-- if product_ot_nom -->
- The automation platform reads the configuration record to select and validate its targets before a flow acts on them. <!-- if product_ot_oo -->
- The operations configuration management platform and this database exchange configuration item data, with one of the two agreed as authoritative per class during the design stage. <!-- if module_stackx_ops_config_mgmt -->
- The service management platform in scope consumes the configuration record as the service context on its tickets. <!-- if module_stackx_itSM -->
- An export of the agreed configuration item attributes is supplied to the log platform as enrichment data, so a log line can be read against the host and service it came from. <!-- if product_el_logs or module_stackx_event_log_mgmt -->
- An export of the agreed configuration item attributes is supplied to the monitoring platform, so monitored objects carry the same identifiers as the configuration record. <!-- if product_el_observability or module_stackx_observability_apm -->

*[The enrichment exports are a designed, scheduled export rather than a supplied out-of-the-box connector. Confirm the direction, the attribute list and the refresh interval in the design stage, and confirm with the product team that the receiving platform in the bid can consume it.]*

## Build Activities <!-- if services -->

<!-- if services -->
**Design confirmation**

- Agree the class model: which configuration item classes are in scope, which attributes each must carry, and which system owns each attribute.
- Agree the address ranges, their owners and the scan windows that apply to each.
- Agree the business services to be modelled, and the owner who will validate each model.
- Agree the reconciliation policy, the ageing policy and what data quality will be measured against.

**Platform deployment**

- Deploy the server and its database and bring them to the supported patch level.
- Install the current discovery content, and agree how content updates will be applied after handover.
- Deploy a discovery probe in each network zone that cannot be reached from the central site, sized for the ranges it will scan.
- Configure backup of the database, and prove a restore before the model is populated.
- Configure the access model: who may run discovery, who may edit the class model and who may only read.

**Credentials and pilot discovery**

- Load credentials per technology into the probe credential store, with the owner of each recorded.
- Run a pilot scan against one agreed range per technology, and review what came back: coverage, credential failures, unreachable addresses and unexpected classes.
- Correct credentials, protocol access and probe placement against the pilot result before widening the scan.

**Full discovery and modelling**

- Enable discovery range by range, on the agreed schedule, reviewing coverage and duplicates after each stage rather than at the end.
- Configure the identification and reconciliation rules, and verify them against a set of components deliberately discovered by more than one route.
- Configure ageing and lifecycle rules, and confirm the retirement behavior on a test record.
- Model the agreed business services, top-down where an entry point exists and bottom-up where it does not, and validate each model with its application owner.
- Configure agent-based inventory where it is in scope, including its deployment route and collection schedule.
- Configure the discovery of cloud accounts where they are in scope.
- Build the agreed queries, impact rules and saved views.

**Integration build**

- Configure synchronization with the service management platform, including the attribute ownership agreed in design. <!-- if product_ot_smax -->
- Supply the service model to the event console and confirm correlation runs against it. <!-- if product_ot_obm -->
- Configure population of network topology from the network monitoring platform. <!-- if product_ot_nom -->
- Configure the agreed exports to the monitoring and log platforms in scope. <!-- if product_el_logs or product_el_observability or module_stackx_event_log_mgmt or module_stackx_observability_apm -->

**Validation and handover**

- Produce the discovery coverage report: ranges scanned, addresses reached, credential failures and classes populated.
- Validate a jointly agreed sample of records against the systems they represent.
- Hand over the administration guide, the class model documentation, the credential register and the schedule.
<!-- endif -->

## Hardware Requirements

The specifications below are this product's own components. They are the vendor's recommended figures for the deployment sizes shown, are indicative, and are confirmed against the configuration item and range counts recorded in the design document.

| Component | Small — up to ~20,000 configuration items | Medium — up to ~100,000 | Large — above ~100,000 |
| :--- | :--- | :--- | :--- |
| Configuration management database server | 4 vCPU / 16 GB RAM / 150 GB SSD | 8 vCPU / 32 GB RAM / 250 GB SSD | 16 vCPU / 64 GB RAM / 500 GB SSD |
| Database | 4 vCPU / 16 GB RAM / 250 GB SSD | 8 vCPU / 32 GB RAM / 500 GB SSD | 16 vCPU / 64 GB RAM / 1 TB SSD |
| Discovery probe, agentless scanning | 4 vCPU / 8 GB RAM / 100 GB SSD | 8 vCPU / 16 GB RAM / 250 GB SSD | 8 vCPU / 16 GB RAM / 250 GB SSD per probe |
| Discovery probe, where agent-based inventory is in scope | 8 vCPU / 16 GB RAM / 250 GB SSD | 8 vCPU / 32 GB RAM / 500 GB SSD | 8 vCPU / 32 GB RAM / 500 GB SSD per probe |
| Browser interface, where deployed separately | 2 vCPU / 8 GB RAM / 50 GB SSD | 4 vCPU / 8 GB RAM / 50 GB SSD | 4 vCPU / 16 GB RAM / 100 GB SSD |

- Probe count follows network reach, not only scale: one probe per network zone that cannot be scanned from the central site, plus additional probes where a single probe cannot complete its ranges inside the agreed scan window.
- A probe that performs agent-based inventory carries scan files locally and needs the larger disk shown.
- The inventory agent's footprint on a monitored host is small — under 1 GB of disk and a few hundred megabytes of memory during a scan — but it must be permitted by {{customer_short}}'s endpoint policy.
- Database storage grows with history retention as well as configuration item count; the retention period is agreed in the design stage.

*[Hardware figures are indicative and are confirmed during the design stage. Confirm with the Verto Wave product team which release the figures are drawn from, and re-check them against that release's sizing guide and the current probe sizing table before issue.]*

## What Discovery Needs

- Network paths open from each probe to its target ranges, on the protocols recorded in the design document
- Read-only credentials per technology — network devices, operating system families, databases, middleware, virtualization and cloud accounts — each with a named owner and an agreed rotation process
- The remote management interface of each operating system family enabled on the targets in scope
- Scan windows agreed for ranges that carry sensitive or latency-sensitive workloads
- An address range list with an owner per range, so an unreachable range can be chased rather than silently dropped
- An application owner per business service to be modelled, available to validate the model
- Name resolution and time synchronization for the platform and its probes

## Sizing Basis

Sizing follows the number of ranges and addresses scanned, the number of configuration items and relationships held, the discovery frequency and the history retained. The figures are recorded in the design document and confirmed against the range list.

## Scope Boundaries

### Not Covered by This Product's Scope

- Discovery of technologies for which the supplied content provides no logic, and the writing of new discovery logic for them.
- Targets reachable only through address translation or a jump host that prevents a probe from holding a direct credentialed session.
- Configuration item classes, attributes and relationships beyond the agreed class model.
- Deep discovery of custom or in-house applications where the owner cannot supply the signatures, ports or entry points that identify them.
- Correcting the estate that discovery exposes: duplicate hostnames, expired certificates, unsupported versions and misconfigured agents are reported, not remediated.
- Acting as the asset, contract or financial record; the database records what is deployed, not what was purchased, unless an asset entitlement is separately in scope.
- Discovery of endpoints and workstations, unless those ranges are explicitly in scope.

## Acceptance <!-- if services -->

<!-- if services -->
Discovery is accepted when:

- Every agreed range has been scanned within its agreed window, and the coverage report shows the result per range, including addresses reached, credential failures and unreachable addresses.
- Each modelled business service resolves to its components and is confirmed by its application owner.
- A jointly agreed sample of records matches the systems it represents, with duplicates inside that sample within the threshold recorded in the design document.
- The agreed queries, impact rules and saved views return results against live data.
- Each configured integration exchanges records in the agreed direction, demonstrated once end to end.

Coverage depends on the credentials and network access {{customer_short}} supplies; ranges that stay unreachable are recorded as such, with their owner, rather than counted against the result.
<!-- endif -->

*[Confirm the ranges, the credential owners, the configuration item classes and the services to model per bid, and whether agent-based inventory and cloud account discovery are in scope.]*

*[Verify with the Verto Wave product team before issue: the current product and component names, the release cadence of the discovery content updates, and whether agent-based inventory and software recognition are included in the entitlement being quoted or licensed separately.]*
