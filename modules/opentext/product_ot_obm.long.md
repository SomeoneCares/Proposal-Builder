# Event Correlation and Root-Cause Analysis <!-- if not named_product_ot_obm -->
# OpenText OBM <!-- if named_product_ot_obm -->

**Token:** `{{product_ot_obm}}`
**Group:** OpenText Products
**Required:** No

---

Events from every monitoring source arrive in one console, where correlation removes duplicates and symptoms and leaves the operator with a probable cause. <!-- if not named_product_ot_obm -->
OpenText OBM collects events from every monitoring source into one console, where correlation removes duplicates and symptoms and leaves the operator with a probable cause. <!-- if named_product_ot_obm -->

The product plays two roles at once. It monitors servers, databases, middleware and virtualization directly, through its own agents and the supplied monitoring content; and it acts as the manager of managers, consuming events from every other monitoring tool in the estate so that one console, one severity model and one routing map cover all of them. Both roles feed the same correlation engine, which uses a topology of the services being monitored to separate the fault from its symptoms.

## Where It Fits in This Project

{{customer_short}}'s requirement is to stop operators reading raw alerts from several consoles and deciding for themselves which ones matter. The operational problem is not detection — most tools detect — it is that one failure produces alerts in every tool that can see it, and the operator has to work out which alert is the cause.

In this project the console is the point at which every monitoring source in scope converges, and the point from which work leaves for the service desk or for automation. Its scope is the event sources agreed during the design stage, the correlation and routing rules built against the agreed service model, and the tuning period that follows. The number of sources is held in the professional services scope and is not repeated here.

## Platform Components

<!-- if not named_product_ot_obm -->
- **Event management server** — receives, deduplicates, enriches, correlates and stores events, and presents the operator console.
- **Database** — the store for events, their history and the service model behind the console.
- **Service model store** — the topology the correlation engine reasons over: components, services and the relationships between them.
- **Monitoring agent** — deployed on hosts in scope, collecting metrics, faults, process state and log conditions locally and forwarding what the policy defines as an event.
- **Monitoring content** — the supplied, per-technology policy libraries for operating systems, databases, middleware, virtualization and cloud platforms, so common components are monitored to a known standard rather than through hand-built checks.
- **Agentless collector** — the component that takes events from tools and devices that cannot host an agent: traps, syslog, web calls, database queries and structured files.
- **Correlation engine** — topology-based, time-based and repetition-based correlation, plus event-storm handling.
- **Service health views** — indicators per service, showing the current state and the events behind it.
- **Dashboard and reporting service** — operator dashboards, management dashboards and reporting on event volumes, sources and console load.
- **Automation interface** — the mechanism by which an event runs a pre-approved action or calls an external flow.
<!-- endif -->

<!-- if named_product_ot_obm -->
- **Operations Bridge Manager server** — receives, deduplicates, enriches, correlates and stores events, and presents the operator console.
- **Database** — the store for events, their history and the run-time service model behind the console.
- **Run-time service model** — the topology the correlation engine reasons over: components, services and the relationships between them, populated locally or from the configuration management database.
- **Operations Agent** — deployed on hosts in scope, collecting metrics, faults, process state and log conditions locally and forwarding what the policy defines as an event.
- **Management packs** — the supplied, per-technology policy libraries for operating systems, databases, middleware, virtualization and cloud platforms, so common components are monitored to a known standard rather than through hand-built checks.
- **Operations Connector** — the agentless path for tools and devices that cannot host an agent: traps, syslog, web calls, database queries and structured files.
- **Correlation engine** — topology-based, stream-based and time-based correlation, plus event-storm handling.
- **Service health and indicators** — health and event type indicators per service, showing the current state and the events behind it.
- **Dashboards and reporting** — operator dashboards, business-facing dashboards and reporting on event volumes, sources and console load.
- **Automation interface** — the mechanism by which an event runs a pre-approved action or calls an external flow.
<!-- endif -->

*[The component list follows the vendor's current packaging, which has changed names across recent releases. Confirm the component names, and which are inside the entitlement being quoted, with the Verto Wave product team before issue.]*

## What It Delivers

- One event console for infrastructure, network, application and platform sources, fed by its own agents, by agentless collectors and by forwarding from tools already in place
- Monitoring of operating systems, databases, middleware and virtualization through the supplied monitoring content, on the hosts where agents are in scope
- Deduplication and suppression, so a single fault does not arrive as fifty alerts, with event-storm handling for the case where one source floods the console
- Topology-based correlation that uses the service model to separate cause from symptom, and repetition- and time-based correlation for faults that have no topology to reason over
- Enrichment and routing, so an event reaches the right team already carrying the service, location, severity and suggested action it needs
- Service health views per service, built from the indicators the events feed, with the event history that led to the current state
- Planned maintenance taken from the change record, so approved work does not raise alarms <!-- if product_ot_smax -->
- Pre-approved operator actions launched from the event itself, so a known check or restart does not require a separate session
- Operator and management dashboards, and reporting on event volumes, the sources that produce them and the rules that suppress them


[[figure: ot-obm-correlation | From raw events to a probable cause]]

## Integration

The links below are configured only where both platforms are part of this proposal.

- The configuration management database supplies the service model, so correlation reasons over the same components the service desk sees. <!-- if product_ot_ucmdb -->
- The service management platform receives tickets created, updated and closed from events, and returns closure so the console and the ticket agree on the current state. <!-- if product_ot_smax -->
- The automation platform runs a flow when a known fault is detected, under the conditions agreed for that fault. <!-- if product_ot_oo -->
- The network monitoring platform forwards network faults with their root-cause result already applied, so the network is polled once and judged once. <!-- if product_ot_nom -->
- The server and infrastructure monitoring platform forwards its alerts into the console as events, mapped to the agreed severity model. <!-- if product_el_observability -->
- The log platform forwards the log conditions agreed with {{customer_short}} as events, with a link back to the search that produced them. <!-- if product_el_logs -->
- The application performance platform forwards service-level and error-rate alerts as events against the affected application service. <!-- if product_el_apm -->
- The observability platform forwards its alerts into the console as events. <!-- if module_stackx_observability_apm -->
- The network operations platform forwards network incidents into the console. <!-- if module_stackx_network_ops -->
- The event and log management platform forwards the agreed conditions into the console. <!-- if module_stackx_event_log_mgmt -->
- The operations configuration management platform supplies the service model where it is the authoritative source. <!-- if module_stackx_ops_config_mgmt -->
- The service management platform in scope receives tickets raised from correlated events. <!-- if module_stackx_itSM -->
- The automation and orchestration platform in scope executes remediation flows called from an event. <!-- if module_stackx_automation_orchestration -->

## Build Activities <!-- if services -->

<!-- if services -->
**Design confirmation**

- Agree the source list, and for each source: how it will send events, what its severities mean and which component each event refers to.
- Agree the severity model and the routing map — which group receives which event class, in hours and out of hours.
- Agree the services to be modelled in the console, and which of them carry health views.
- Agree the observation period for tuning and the baseline against which noise reduction will be measured.

**Platform deployment**

- Deploy the server and its database and bring every component to the supported patch level.
- Configure the access model and the operator roles, including which operators may close, suppress or launch an action.
- Configure backup of the database and the configuration, and prove a restore before sources are connected.
- Configure event and history retention to the agreed period, and size the database against it.

**Source onboarding**

- Connect the in-scope sources one at a time, confirming per source: the transport, the event format, the severity mapping and the mapping to the affected component.
- Deploy agents and the agreed monitoring content on the hosts where agent-based monitoring is in scope, and tune each policy's thresholds against a baseline period rather than accepting defaults.
- Configure the agentless collectors for the sources that cannot host an agent, including trap, syslog, web-call and database collection as applicable.
- Prove each source end to end by injecting a test condition at the source and confirming the resulting event in the console.

**Event processing**

- Configure deduplication, including the key that decides when two events are the same event.
- Configure suppression, maintenance windows and event-storm handling.
- Configure correlation rules against the modelled services. <!-- if product_ot_ucmdb -->
- Configure correlation rules against the service definitions agreed in the design stage. <!-- if not product_ot_ucmdb -->
- Configure enrichment: the attributes each event must carry before it is routed.
- Configure assignment, notification and escalation per event class.
- Configure the health indicators and build the service health views.

**Integration build**

- Configure ticketing, including the event-to-ticket mapping, the update behavior and the closure loop. <!-- if product_ot_smax -->
- Configure maintenance suppression from the change record. <!-- if product_ot_smax -->
- Configure the automatic actions and the flows they call, with the conditions under which they may run unattended. <!-- if product_ot_oo -->
- Configure the forwarding from the network monitoring platform and confirm no duplicate polling remains. <!-- if product_ot_nom -->
- Configure the inbound event feeds from the monitoring and log platforms in scope. <!-- if product_el_observability or product_el_logs or product_el_apm or module_stackx_observability_apm or module_stackx_network_ops or module_stackx_event_log_mgmt -->

**Tuning and handover**

- Record the event volume per source at the start of the observation period.
- Tune the rules across the observation period: remove events no one acts on, correct severities, widen deduplication keys and add correlation for patterns that appear in the live stream.
- Record the volume again at the end of the period and report the difference per source.
- Build the agreed operator views, dashboards and reports.
- Hand over the administration guide, the rule set documentation and the source register.
<!-- endif -->

## Hardware Requirements

The specifications below are this product's own components. They are the vendor's recommended figures for the deployment sizes shown, are indicative, and are confirmed against the monitored-node and event-rate figures recorded in the design document.

| Component | Small — up to ~500 monitored nodes | Medium — up to ~2,000 nodes | Large — above ~2,000 nodes |
| :--- | :--- | :--- | :--- |
| Event management server | 8 vCPU / 32 GB RAM / 250 GB SSD | 16 vCPU / 64 GB RAM / 500 GB SSD | 24 vCPU / 128 GB RAM / 1 TB SSD |
| Database | 8 vCPU / 32 GB RAM / 500 GB SSD | 16 vCPU / 64 GB RAM / 1 TB SSD | 16 vCPU / 96 GB RAM / 2 TB SSD |
| Agentless collector node | 4 vCPU / 8 GB RAM / 100 GB SSD | 4 vCPU / 16 GB RAM / 200 GB SSD | 8 vCPU / 16 GB RAM / 250 GB SSD per collector |
| Reporting and dashboard node, where deployed separately | 8 vCPU / 32 GB RAM / 500 GB SSD | 16 vCPU / 64 GB RAM / 1 TB SSD | 16 vCPU / 64 GB RAM / 2 TB SSD or more, by retention |
| Monitoring agent, per monitored host | 1 vCPU share / 1 GB RAM / 5 GB disk | Same | Same |
| Second server for high availability, where in scope | Matched pair at the tier specification | Same | Same |

- Event rate drives the server and database more than node count does; a small estate that forwards a high-volume syslog stream sizes as a larger tier.
- One agentless collector is required per network zone that cannot reach the central server directly, and per source that produces a sustained high event rate.
- Database storage is set by the event and indicator retention period agreed in the design stage; the figures above assume a retention of a few months, not years.
- Storage must be SSD-class for the server and database.

*[Hardware figures are indicative and are confirmed during the design stage. Confirm with the Verto Wave product team which release the figures are drawn from, whether the deployment in scope is the classic or the containerized form — the node layout differs between them — and re-check the figures against that release's sizing guide before issue.]*

## What the Console Needs

- Each event source able to forward by a supported means — trap, syslog, web call, database or file collection — configured to the platform's addresses
- Agents permitted on the hosts where agent-based monitoring is in scope, with the ports to the management servers open
- A service model, supplied by the configuration management database <!-- if product_ot_ucmdb -->
- A service model, built from the service definitions agreed in the design stage <!-- if not product_ot_ucmdb -->
- A named owner per source who can confirm what each event means and who should receive it
- Agreed retention for events and for the indicator history behind the service views
- Name resolution, time synchronization and a common time reference across the sources, so correlation can order events correctly
- An agreed baseline period before tuning, so noise reduction is measured rather than claimed

## Scope Boundaries

### Not Covered by This Product's Scope

- Sources that emit no supported event format, and the development of collectors or parsers for proprietary or binary formats.
- Correlation across services that are not modelled; an event about an unmodelled component is routed, not correlated.
- Monitoring depth beyond what the agreed monitoring content provides; custom monitoring policies beyond the agreed list are a change request.
- Long-term metric or event warehousing beyond the agreed retention period, and historical reporting over data that has aged out.
- Tuning of the monitored systems themselves — thresholds are set on what those systems report, and are only as good as what they report.
- Automatic actions against systems that expose no supported interface or no working credential.
- Acting as the log search platform: the console consumes the log conditions agreed as events, not the full log stream.

## How Correlation Is Judged

Correlation is assessed on how far it reduces the events an operator must read, measured before and after tuning across the agreed observation period. A probable cause is presented for the operator to validate; it is not warranted to be the actual cause. Detection and notification targets are set per source class and recorded in the design document. The console shortens detection and routing; it does not repair the monitored system, and no restoration or resolution time is committed on the basis of it.

## Acceptance <!-- if services -->

<!-- if services -->
The console is accepted when, in a session run jointly with {{customer_short}}:

- A test condition raised at each connected source produces an event in the console, carrying the agreed severity and the correct affected component.
- The same condition raised repeatedly produces one deduplicated event, not many.
- An agreed correlation scenario is demonstrated: the symptom events are suppressed or grouped and the cause event is presented.
- A maintenance window is set and an event inside it is suppressed as designed.
- Each configured integration is demonstrated once, end to end, including ticket creation and closure where ticketing is in scope. <!-- if product_ot_smax -->
- Each configured integration is demonstrated once, end to end. <!-- if not product_ot_smax -->
- The event volume report for the observation period is produced, showing the volume per source at the start and at the end of tuning.

Acceptance covers detection, correlation and routing. It does not extend to repairing the monitored systems, and no restoration or resolution time is committed.
<!-- endif -->

*[Confirm the sources in scope, the observation period, the noise-reduction baseline, and whether agent-based monitoring of servers and databases is in scope or the console consumes existing tools only.]*

*[Verify with the Verto Wave product team before issue: the current suite and component names, which monitoring content is included in the entitlement being quoted, and whether the reporting and dashboard components are part of it or licensed separately.]*
