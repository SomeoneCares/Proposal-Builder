# Service Management Platform <!-- if not named_product_ot_smax -->
# OpenText SMAX <!-- if named_product_ot_smax -->

**Token:** `{{product_ot_smax}}`
**Group:** OpenText Products
**Required:** No

---

The service management platform gives {{customer_short}} one place to raise, route and resolve work, with the service catalog, workflows and service-level targets held in the same system. <!-- if not named_product_ot_smax -->
OpenText SMAX gives {{customer_short}} one place to raise, route and resolve work, with the service catalog, workflows and service-level targets held in the same system. <!-- if named_product_ot_smax -->

The platform is delivered as a set of containerized services on a single management cluster, so the portal, the process engine, the configuration tooling, the knowledge service and the reporting service are deployed, patched and scaled as one platform rather than as separate installations. Processes follow ITIL practice out of the box and are adjusted to the model agreed with {{customer_short}} during the design stage, using the platform's own configuration tooling rather than code.

## Where It Fits in This Project

{{customer_short}}'s requirement is a single, governed entry point for service work: one place where a user raises a request, where a fault becomes a tracked incident, where a change is assessed and approved before it touches production, and where performance against service-level targets can be shown rather than asserted. This platform is that entry point. Every other product in this proposal ends its own work at an event, a discovered record or an executed flow; this is where that work becomes a record with an owner, a target and an audit trail.

Its scope in this project is the process model, the service catalog and the workflows agreed during the design stage, configured for the service domains in scope and integrated with the other platforms selected. The quantities that bound the configuration work are held in the professional services scope and are not repeated here.

## Platform Components

<!-- if not named_product_ot_smax -->
- **Self-service portal** — the business user's interface: the service catalog, request status, announcements and self-help articles, presented under {{customer_short}}'s branding.
- **Agent workspace** — the interface used by the service desk and resolver groups, with queues, the record being worked, the knowledge suggested for it and the collaboration around it.
- **Process engine** — the workflow, approval, notification and escalation logic behind incident, request, problem, change, release and knowledge work.
- **Service-level engine** — targets per service and per record type, with the calendars, pauses and warning thresholds that go with them.
- **Configuration tooling** — the studio in which record types, fields, forms, rules, workflows and catalog items are configured without code, and in which configuration is versioned and promoted between environments.
- **Embedded configuration record** — the platform's own store of the items it manages, so a ticket can be raised against a service or an asset even before an external configuration management database is connected.
- **Knowledge and search service** — the article store and the search that serves both the portal and the agent workspace.
- **Reporting and dashboard service** — operational dashboards, scheduled reports and the export used for external reporting.
- **Integration service** — the inbound and outbound interfaces through which other platforms raise, update and close records, and through which the platform calls other systems.
- **Machine-assisted services** — classification, routing, search and conversational assistance, where the licensed edition provides them.
<!-- endif -->

<!-- if named_product_ot_smax -->
- **Service Portal** — the business user's interface: the service catalog, request status, announcements and self-help articles, presented under {{customer_short}}'s branding.
- **Agent workspace** — the interface used by the service desk and resolver groups, with queues, the record being worked, the knowledge suggested for it and the collaboration around it.
- **Service Management domains** — the process content itself: Incident, Service Request, Problem, Change, Release, Knowledge and Configuration Management, each configurable per service domain.
- **Enterprise Service Management domains** — the same engine serving business functions beyond IT, such as HR or facilities, each with its own catalog, agents and access.
- **Asset Management** — hardware and software asset records, contracts and lifecycle, where that entitlement is in scope.
- **Studio** — the codeless configuration environment in which record types, fields, forms, rules, workflows and catalog items are configured, versioned and promoted between environments.
- **Embedded configuration record** — SMAX carries its own store of managed items, so a ticket can be raised against a service or an asset before an external configuration management database is connected.
- **Knowledge and search service** — the article store and the search serving both the portal and the agent workspace.
- **Reporting and dashboards** — operational dashboards, scheduled reports and the export used for external reporting.
- **Integration service** — the inbound and outbound interfaces used by other platforms to raise, update and close records, and used by SMAX to call other systems.
- **Machine-assisted services** — smart ticket classification and routing, smart search and the virtual agent, where the licensed edition provides them.
<!-- endif -->

*[The component list follows the vendor's current packaging. Confirm the component and edition names with the Verto Wave product team before issue, and remove Asset Management if that entitlement is not being quoted.]*

## What It Delivers

- A self-service portal and service catalog, so requests arrive structured rather than by mail or phone, with the catalog item carrying its own form, approval route and fulfilment path
- Incident, request, problem, change and release management against one record of the service, with the relationships between those records kept — an incident that leads to a problem, a problem that leads to a change
- Change management with normal, standard and emergency routes, risk assessment, collision checking against the change calendar, and the post-implementation review recorded against the change
- Service-level management with targets per service and per record type, calendars and pauses, and warnings raised before a target is missed rather than after
- A knowledge base that offers articles to the agent while the ticket is worked, and to the user in the portal before a ticket is raised
- Approval routes for changes and for catalog items that carry cost or risk, with the approver, the decision and the time it took held on the record
- Configuration through the platform's own configuration tooling rather than code, so the agreed workflows, forms and rules carry forward across upgrades
- Machine-assisted classification, routing and knowledge suggestion, where the edition in scope provides them and enough history exists to train on
- More than one service domain on the same platform, each with its own catalog, agents and access, where business functions beyond IT are in scope
- Reporting on volumes, ageing, first-line resolution, reopened records, backlog and service-level attainment, per service and per group


[[figure: ot-smax-flow | Service management flow]]

## Integration

The links below are configured only where both platforms are part of this proposal.

- The configuration management database supplies the affected service, its components and their relationships, so a ticket is raised against a known record and a change can be assessed for impact before it is approved. <!-- if product_ot_ucmdb -->
- The event console opens, updates and closes a ticket as a fault is detected, correlated and cleared, so the service desk does not retype what monitoring already knows. <!-- if product_ot_obm -->
- The network monitoring platform raises incidents for network faults directly where no event console is in scope, carrying the device, interface and fault detail into the record. <!-- if product_ot_nom and not product_ot_obm -->
- The automation platform fulfils catalog items and executes standard changes, returning the result to the record that requested it. <!-- if product_ot_oo -->
- Alerts from the server and infrastructure monitoring platform raise and update records through the platform's inbound interface. <!-- if product_el_observability -->
- Alerts from the log platform raise records, with a link back to the search that produced them for the agent to follow. <!-- if product_el_logs -->
- Alerts from the application performance platform raise records against the affected application service. <!-- if product_el_apm -->
- Alerts from the observability platform raise and update records through the platform's inbound interface. <!-- if module_stackx_observability_apm -->
- Alerts from the network operations platform raise and update records for network faults. <!-- if module_stackx_network_ops -->
- Alerts from the event and log management platform raise records for the conditions agreed with {{customer_short}}. <!-- if module_stackx_event_log_mgmt -->
- Configuration item and service data from the operations configuration management platform is used as the ticket's service context. <!-- if module_stackx_ops_config_mgmt -->
- Approved standard changes and catalog requests are handed to the automation and orchestration platform for execution. <!-- if module_stackx_automation_orchestration -->
- The directory service supplies users, groups and the attributes used for routing and approval, and the mail platform carries notification and mail-raised tickets. Both are configured in every deployment.

*[Integrations to platforms outside this proposal are designed against the receiving system's supported interface and are counted in the professional services integration figure. Confirm the inbound interface each alerting platform will use before issue.]*

## Build Activities <!-- if services -->

<!-- if services -->
**Design confirmation**

- Confirm the process model per record type: the states, the transitions, who owns each state and what closes it.
- Confirm the categorization tree, the priority matrix (impact against urgency), the service hierarchy and the naming standards, and record them in the design document.
- Confirm the service domains in scope, their agent groups and the separation required between them.
- Confirm the service-level targets, their calendars, their pause conditions and their warning thresholds.

**Platform deployment**

- Size and prepare the cluster, its storage and its database against the figures recorded in the design document.
- Deploy the platform's containerized services and bring every component to the supported patch level.
- Configure the published names, the load balancing and the certificates for the portal and the agent workspace.
- Configure backup of the database and the platform's persistent storage, and prove a restore before go-live.
- Deploy the non-production environment where one is in scope, and configure promotion of configuration between it and production.

**Access and identity**

- Connect the directory service, and map users, groups and the attributes used for routing and approval.
- Configure single sign-on for the portal and the agent workspace where it is in scope.
- Configure the role model: agents, approvers, process owners, administrators and read-only reporting users.

**Process and catalog configuration**

- Configure incident and request management: forms, fields, states, assignment rules, notification and escalation.
- Configure the service catalog: each item's form, eligibility, approval route, fulfilment path and target.
- Configure change management: change types, risk assessment, the change calendar, collision checking, approval routes and the post-implementation review.
- Configure problem management, including its link from incident and its link to change.
- Configure release management where it is in scope.
- Configure service-level targets, the priority matrix, the notification rules and the escalation rules.
- Load the agreed knowledge articles, configure the article lifecycle and configure how articles are offered in the portal and the agent workspace.
- Configure the portal branding, the announcements and the language set agreed for {{customer_short}}.
- Configure the machine-assisted classification and search where the edition provides them, and agree the review period before their output is trusted for routing.

**Integration build**

- Integrate with the configuration management database so tickets carry the affected service, and agree which system owns which attribute. <!-- if product_ot_ucmdb -->
- Integrate with the event console, including event-to-ticket mapping, update behavior and the closure loop back from the service desk. <!-- if product_ot_obm -->
- Integrate with the network monitoring platform for network incidents where no event console is in scope. <!-- if product_ot_nom and not product_ot_obm -->
- Integrate with the automation platform so approved catalog items and standard changes run without manual work, and so the result returns to the record. <!-- if product_ot_oo -->
- Integrate the alerting platforms in scope with the platform's inbound interface, and confirm de-duplication behavior so one condition does not open many records. <!-- if product_el_observability or product_el_logs or product_el_apm or module_stackx_observability_apm or module_stackx_network_ops or module_stackx_event_log_mgmt -->
- Configure mail routing in both directions, including the mailbox that raises tickets and the sender address used for notification.

**Reporting, test and handover**

- Build the agreed operational dashboards and scheduled reports, per service and per group.
- Execute the agreed test scenarios with {{customer_short}}'s service desk: raise, route, escalate, approve, resolve and close one record of each type, and one of each integration path.
- Run a load check against the concurrency figure recorded in the design document.
- Hand over the administration guide, the configuration record and the agent and portal user guides, and run the knowledge transfer sessions listed in the training scope.
<!-- endif -->

## Hardware Requirements

The platform is deployed on a cluster of virtual machines at the central site. The specifications below are the vendor's recommended figures for a deployment of this shape, are indicative, and are confirmed against the concurrency and volume figures recorded in the design document.

| Component | Small tier | Medium tier | Large tier |
| :--- | :--- | :--- | :--- |
| Cluster control-plane nodes | 3 × 4 vCPU / 16 GB RAM / 100 GB SSD | 3 × 8 vCPU / 32 GB RAM / 150 GB SSD | 3 × 8 vCPU / 32 GB RAM / 200 GB SSD |
| Application worker nodes | 3 × 16 vCPU / 64 GB RAM / 500 GB SSD | 5 × 16 vCPU / 64 GB RAM / 500 GB SSD | 8 × 16 vCPU / 64 GB RAM / 750 GB SSD |
| Database node | 8 vCPU / 32 GB RAM / 500 GB SSD | 16 vCPU / 64 GB RAM / 1 TB SSD | 24 vCPU / 128 GB RAM / 2 TB SSD |
| Shared persistent storage | 1 TB, SSD-backed | 2 TB, SSD-backed | 4 TB, SSD-backed |
| Load balancer | Two published names, TLS termination or pass-through | Same | Same |
| Non-production environment, where in scope | One worker node and one database node at the same specification as the tier | Same | Same |

| Tier | Indicative basis |
| :--- | :--- |
| Small | Up to approximately 50 concurrent agents and a low ticket volume |
| Medium | Up to approximately 150 concurrent agents |
| Large | Above approximately 150 concurrent agents, or where several service domains run on one platform |

- Storage must be SSD-class throughout; the database and the platform's persistent storage are the components most sensitive to storage latency.
- The cluster nodes must be able to reach each other on the ports recorded in the design document, without address translation between them.
- Time synchronization from a common source is required across every node.

*[Hardware figures are indicative and are confirmed during the design stage. Confirm with the Verto Wave product team which release the figures are drawn from, and re-check them against that release's sizing guide before issue.]*

## What the Platform Needs

- Published names and trusted certificates for the portal and the agent workspace, reachable from {{customer_short}}'s client estate
- A directory service for users and groups, with the attributes to be used for routing and approval agreed
- Mail routing in both directions, with the mailbox and sender addresses the platform will use
- Name resolution, time synchronization and the network paths recorded in the design document
- Administrative accounts for the platform and for each system it integrates with, held by named owners
- A nominated process owner per record type, able to decide states, routing and targets during configuration
- Agreed data for the service catalog and the service hierarchy, supplied before configuration begins

## Scope Boundaries

Workflow, catalog, form and report configuration is bounded, and the agreed counts are recorded in the design document. Anything beyond them is handled as a change request. Configuration is performed with the platform's own configuration tooling; work that requires code outside it is quoted separately. The machine-assisted features depend on the edition licensed and on the volume and quality of the history available to them, so their benefit is assessed after a period of live use rather than committed in advance.

### Not Covered by This Product's Scope

- Configuration written outside the platform's own configuration tooling: custom pages, custom code and modifications that the vendor's upgrade path does not carry forward.
- Catalog items whose fulfilment depends on a system that exposes no supported interface; those items are delivered as a routed manual task instead.
- Record types, fields and relationships beyond the agreed class and form model.
- Reporting from data that does not live in the platform, and reports built in a reporting tool outside it.
- Tuning of the cluster, its storage or its database beyond the platform's documented settings.
- Language and localization beyond the agreed language set.
- Acting as the system of record for assets, contracts or software entitlements unless the asset management entitlement is in scope and its data is supplied.

## Acceptance <!-- if services -->

<!-- if services -->
The platform is accepted when, in a session run jointly with {{customer_short}}:

- One record of each configured type is raised, routed, escalated, approved where its route requires it, resolved and closed, and each step matches the design document.
- Each configured catalog item is ordered from the portal and reaches its fulfilment path.
- Each configured integration path is demonstrated once, end to end, in both directions where the integration is two-way.
- The service-level targets calculate correctly against a test record, including the warning raised before the target is reached.
- The agreed dashboards and scheduled reports render with data for the test period.

Acceptance covers the configuration delivered under this scope. It does not extend to the behavior of systems the platform integrates with, and no restoration or resolution time is committed on the basis of it.
<!-- endif -->

*[Confirm the workflow, catalog item, form and report counts per bid, the service domains in scope beyond IT, the licensed edition — it decides which machine-assisted features may be offered — and whether directory and mail integration are in scope.]*

*[Verify with the Verto Wave product team before issue: the current edition names and which editions carry the machine-assisted classification, search and virtual agent features; whether the asset management entitlement is being quoted; and whether the deployment in scope is customer-hosted or vendor-hosted, because the hardware table and half the prerequisite list do not apply to a vendor-hosted subscription.]*
