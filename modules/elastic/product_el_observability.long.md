# Server and Infrastructure Monitoring <!-- if not named_product_el_observability -->
# Elastic Observability <!-- if named_product_el_observability -->

**Token:** `{{product_el_observability}}`
**Group:** Elastic Products
**Required:** No

---

Server and infrastructure monitoring collects metrics from physical, virtual and containerized systems and turns them into health, capacity and performance views. <!-- if not named_product_el_observability -->
Elastic Observability collects metrics from physical, virtual and containerized systems and turns them into health, capacity and performance views. <!-- if named_product_el_observability -->

## What It Delivers

- One platform for physical, virtual and containerized hosts, with a single collector per host driven from a central policy
- Processor, memory, disk, filesystem and network metrics, current and historical, at the collection interval agreed per source type
- Process-level visibility, so a fault can be traced to the process that consumed the resource rather than to the host alone
- Collection from systems that do not accept a local collector — hypervisors, storage arrays, cloud services and network devices — through their own management interfaces
- Hardware health where the platform exposes it, including disk, power supply, fan and sensor status
- Threshold, rate-of-change and anomaly-based alerting, with maintenance periods to keep planned work quiet
- Service level objectives tracked against agreed indicators such as availability and latency, with the error budget shown against the target
- Dashboards per host group, and reporting on capacity trends for planning
- Role-based access, so each team sees the hosts it owns and no others

The operational benefit is a single inventory of what is running, one place to see whether it is healthy, and one alerting model across the whole estate instead of one console per platform. The commercial benefit is that capacity decisions are made against measured trend data rather than against a supplier's renewal quotation.

## Platform Components

The platform is assembled from the following functional parts. Each is deployed and configured as part of the work described below.

| Component | Function |
| :--- | :--- |
| Host collector | A single lightweight process per monitored host that gathers metric data for every enabled source type on that host and ships it to the ingest endpoint. |
| Remote collector | Collection against a management interface for systems that take no local process — hypervisor, storage, cloud and network sources. |
| Collector management service | Central enrollment, policy assignment, configuration push and version upgrade for every deployed collector. |
| Ingest and enrichment pipeline | Parses, normalizes and enriches incoming documents into the common field structure before they are stored. |
| Distributed storage and search engine | Indexes and holds the data across the tiers, and serves the queries behind every dashboard, alert and investigation. |
| Lifecycle controller | Moves data between tiers on age and deletes it at the end of the agreed retention. |
| Alerting and anomaly-detection service | Evaluates the agreed rules on a schedule, learns normal behavior where anomaly detection is enabled, and routes notifications to the agreed destinations. |
| Visualization and investigation console | Dashboards, inventory views, ad-hoc analysis, service level objective tracking and case handling. |
| Security and access layer | Authentication, role-based access control, encrypted transport and audit logging for the platform itself. |

<!-- if named_product_el_observability -->
In product terms, these are delivered by Elastic Agent with the integration set for each source type, enrolled, policed and upgraded centrally through Fleet; Elasticsearch for ingest pipelines, storage across the data tiers, index lifecycle management and search; and Kibana for the Observability applications — the infrastructure inventory and hosts views, dashboards, alerting, service level objectives, cases and the machine learning anomaly jobs. The Beats shippers remain available for source types that still need them, and an OpenTelemetry collector can deliver metrics to the same ingest endpoint where {{customer_short}} already has that standard in place. The whole of this is one Elastic Stack deployment shared with the other Elastic products in scope.

*[Confirm with the Verto Wave product team which collection route is proposed per source type, and that the integrations for the estate in scope are generally available in the release being quoted. If continuous profiling or synthetic monitoring is being offered, confirm it separately — neither is included in this module as written.]*
<!-- endif -->

## Fit to {{customer_short}}'s Scope

This module covers the server and infrastructure layer of {{customer_short}}'s estate: the hosts, the platforms they run on and the systems that expose their health through a management interface. It answers the requirement for a single, current view of infrastructure health and capacity across sites and platforms, replacing per-platform tools with one inventory, one alerting model and one set of access rules. It is deliberately bounded at the infrastructure layer: what happens inside an application is covered by application performance monitoring, and what a system writes to its logs is covered by log management. Where those are also in scope they run on the same platform, so the three views join rather than sit side by side.

*[Restate the specific requirement this module answers in {{customer_short}}'s own terms per bid, using the requirement list agreed in the understanding section. Do not leave this paragraph generic in a competitive bid.]*

[[figure: el-observability-collection | Metric collection and health views]]

## Deployment Model

The platform is deployed either on infrastructure under {{customer_short}}'s control or consumed as a managed cloud service. The choice is made in the design stage and it determines the licensing basis, the node sizing below, and which party operates the platform itself. The proposal assumes one production deployment; a separate non-production deployment is a separate line of scope.

*[Confirm the deployment model, the licensing basis that follows from it, and whether a non-production environment is required per bid.]*

## What the Environment Must Provide

- Compute, memory and storage for the platform nodes, to the sizing recorded in the design document
- Network paths and firewall rules from every monitored host and management interface to the ingest endpoints
- An account with the privilege to install and run a collector on each monitored host, or read access to the management interface where collection is remote
- Time synchronization and name resolution across the monitored estate and the platform nodes
- Certificates for the platform endpoints and for encrypted collector traffic
- A supported operating system or platform release on each monitored host, confirmed against the vendor support matrix during design
- Object storage where long retention on a low-cost tier is part of the agreed retention model
- A repository for the platform's own snapshots, separate from the data nodes

## Hardware Requirements

The figures below are the hardware requirements for this module — the infrastructure monitoring workload and the nodes that carry it. They are the platform vendor's recommended specifications for a self-managed deployment, expressed per node role, and they are sized by this module's own drivers: the number of monitored hosts, the number of distinct metric series those hosts produce, the collection interval and the retention held in each tier. They are indicative: the final node counts and disk sizes are calculated from the agreed figures and recorded in the design document. Where the platform is consumed as a managed cloud service, these roles still exist but are sized by the service rather than provisioned as machines.

### Node Roles and Indicative Specifications

| Node role | vCPU | Memory | Disk | Disk type | Minimum count |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Master-eligible | 4–8 | 16 GB | 200 GB | SSD | 3 |
| Hot data | 8–16 | 64 GB | 2–4 TB | NVMe SSD | 2 |
| Warm data | 8 | 64 GB | 8–10 TB | SSD or high-throughput SAS | 2 |
| Cold data | 4–8 | 64 GB | 10–20 TB | High-capacity SAS or SATA | 2 |
| Frozen data | 8 | 64 GB | 2 TB local cache | NVMe SSD | 2 |
| Ingest / coordinating | 8 | 32 GB | 200 GB | SSD | 2 |
| Visualization console | 4–8 | 16 GB | 100 GB | SSD | 2 |
| Collector management service | 4 | 8 GB | 100 GB | SSD | 2 |
| Machine learning | 8–16 | 64 GB | 500 GB | SSD | 2 |

Minimum counts are the counts that give resilience, not the counts that give capacity. Capacity is added by scaling the data tiers.

### Ratio Guidance

The ratios below govern a cluster more than any single specification does:

- Java heap is set to at most half of a node's memory, and to no more than approximately 30 GB per node, because above that threshold the runtime loses compressed object pointers and the larger heap performs worse than the smaller one. A node with more than 64 GB of memory is therefore normally split into two nodes rather than given a larger heap.
- Memory-to-storage ratio per tier is approximately 1:30 on the hot tier, and approximately 1:160 on the warm and cold tiers. A 64 GB hot node therefore carries roughly 2 TB of data, and a 64 GB warm node roughly 10 TB.
- The frozen tier holds its data in object storage and keeps only a local cache on the node, so its local disk is sized to the working set rather than to the retained volume.
- At least three master-eligible nodes are required so that a quorum survives the loss of one.
- At least two data nodes per active tier are required before a replica can be placed on a different node from its primary.
- Usable capacity is planned below 85 percent of disk, because the engine stops allocating shards to a node at that level, stops relocating at 90 percent and enforces a read-only block at 95 percent.
- Disk throughput, not disk capacity, limits the hot tier. Local NVMe is specified for hot data; network-attached storage is used on the warm tier and below.

### Worked Reference Points

These reference points are for infrastructure monitoring data only. They assume a standard integration set per host at a thirty-second collection interval, seven days on the hot tier, thirty days on the warm tier, one replica, and the ratios above. They exist so a reader can scale from a stated estate size, not as a quotation.

| Monitored hosts | Indicative metric volume | Hot nodes | Warm nodes | Master | Ingest / coordinating | Console | Machine learning |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Up to 250 | Low tens of GB per day | 2 × (8 vCPU / 64 GB / 2 TB NVMe) | 2 × (8 vCPU / 64 GB / 8 TB) | 3 × (4 vCPU / 16 GB / 200 GB) | Carried by the data nodes | 2 × (4 vCPU / 16 GB / 100 GB) | Not required |
| Around 1,000 | Around 100 GB per day | 3 × (16 vCPU / 64 GB / 4 TB NVMe) | 3 × (8 vCPU / 64 GB / 10 TB) | 3 × (8 vCPU / 16 GB / 200 GB) | 2 × (8 vCPU / 32 GB / 200 GB) | 2 × (8 vCPU / 16 GB / 100 GB) | 1 × (8 vCPU / 64 GB / 500 GB) |
| Around 5,000, or a high-cardinality containerized estate | Several hundred GB per day | 8 × (16 vCPU / 64 GB / 4 TB NVMe) | 5 × (8 vCPU / 64 GB / 10 TB) | 3 × (8 vCPU / 32 GB / 200 GB) | 3 × (8 vCPU / 32 GB / 200 GB) | 3 × (8 vCPU / 16 GB / 100 GB) | 2 × (8 vCPU / 64 GB / 500 GB) |

The metric volume column is the assumption the node counts rest on, not a commitment: per-host volume varies several-fold with the integration set enabled, the collection interval and the label cardinality of the platform, and it is confirmed by measuring a representative host of each type before the design is signed off. A containerized estate of a given host count produces far more series, and therefore far more data, than the same host count of physical servers.

Stored volume per tier is calculated as the daily volume multiplied by the days held in that tier, multiplied by one plus the number of replicas, multiplied by the indexing overhead factor for the data type, and then divided by the planned utilization ceiling. The indexing overhead factor varies with the source type, the field mapping and the storage mode selected, and is confirmed during design rather than assumed.

### Where Other Products Share the Same Platform

The figures above size this module on its own, and are complete for a bid in which infrastructure monitoring is the only product. Where log management or application performance monitoring is also in scope, those products run on the same cluster as this one: their node roles are these node roles. The combined solution is therefore sized once against the combined data volume and retention, not by adding a second and third cluster to this one. The combined figures are the ones recorded in the design document.

*[Hardware figures are indicative and are drawn from the platform vendor's published sizing and ratio guidance for a self-managed deployment. Confirm with the Verto Wave product team which product release the figures are taken from, and have them restated against that release before issue. Confirm the assumed per-host metric volume against a measured sample before these node counts are quoted.]*

## How It Fits With the Rest of the Platform

- Metrics, logs and traces are held on one platform, so a host, the logs it writes and the services it runs are correlated without a further integration. Moving from an alert on a host to the log lines that host wrote in the same minute, and to the transactions that slowed as a result, is a query rather than an integration. <!-- if product_el_logs or product_el_apm -->
- Platform capacity is sized once against the combined data, not once per product; the sizing figures in this proposal are the combined figures. <!-- if product_el_logs or product_el_apm -->
- One collector per host carries the metric data and the log data for that host, so the rollout is performed once and the agent estate is managed as one. <!-- if product_el_logs -->
- Infrastructure metrics give the trace views the host and container context underneath a slow service, so a latency problem can be attributed to contention on the host rather than to the code. <!-- if product_el_apm -->
- Alerts are forwarded to the central event console for correlation and routing, so infrastructure events are deduplicated and correlated alongside every other source before an operator sees them. <!-- if product_ot_obm -->
- Alerts raise and update tickets in the service management platform, with the severity mapping agreed in design. <!-- if product_ot_smax or module_stackx_itSM -->
- Detected conditions can trigger an agreed automation workflow, within the boundaries set for that workflow. <!-- if product_ot_oo or module_stackx_automation_orchestration -->

## Build Activities <!-- if services -->

<!-- if services -->
**Platform build**

- Confirm the sizing inputs, then finalize the cluster topology, the node roles and the tier layout against the hardware requirements above
- Prepare the operating system on each platform node: file descriptor and memory map limits, swap disabled or memory locked, data volumes mounted and separated from the system volume, and the platform's own service account created
- Install the engine across the nodes, configure node roles and discovery, and form the cluster on a dedicated master quorum
- Generate and deploy the certificate set, enable encrypted transport between nodes and encrypted client traffic, and verify that no unencrypted path remains
- Configure the authentication realm, the role model and the access rules, and remove or secure the default credentials
- Configure the snapshot repository and the backup schedule for the platform's own data, and restore one snapshot to prove the path works
- Configure the data tiers, the index templates and the lifecycle policy that moves and expires each data type
- Deploy the visualization console tier behind the agreed name and certificate, and the collector management service

**Collection build**

- Agree the host inventory, the host roles and the grouping and tagging model that dashboards, alerts and access rules will all key on
- Build one collector policy per host role, with the integration set, collection interval and field enrichment each role needs
- Roll out collectors to a pilot group first, validate the data arriving from each host role, then roll out in agreed phases across the remaining hosts
- Configure remote collection for the systems that take no local collector, with the credentials and polling intervals agreed per interface
- Verify collector enrollment, version and health across the estate, and agree the process for the hosts that fail to enroll

**Configuration and handover**

- Configure the alert rules agreed per host role, the notification connectors, the routing and the maintenance periods for planned work
- Configure the service level objectives agreed for the hosts and services in scope, with their indicators and targets
- Configure anomaly-detection jobs where they are agreed, and tune them across an agreed observation period so they stay readable
- Build the agreed dashboards and the capacity trend reports, and configure the access rules that limit each team's view
- Run the agreed validation, tune the collection intervals and alert thresholds against what the estate actually produces, and record the result
- Hand over the administration guide, the collector policy documentation and the runbook for adding a host or a source type later
<!-- endif -->

## Sizing Basis

Sizing follows four figures, and all four are confirmed before the design is signed off:

- The number of monitored hosts and the integrations enabled on each
- The number of distinct metric series produced, which is the metric count multiplied by the label combinations; on containerized and short-lived workloads this rises far faster than the host count and is the figure that drives storage
- The collection interval per source type
- The retention held in each tier, and the number of copies held for resilience

The figures are recorded in the design document and confirmed against a measured sample from a representative host of each type, rather than estimated from the host count alone. A sustained change beyond the agreed figures is handled through the change process.

*[Confirm host counts by type, collection intervals, retention per tier and the measured sample basis per bid. Do not carry sizing forward from a prior engagement.]*

## Acceptance Criteria <!-- if services -->

<!-- if services -->
Acceptance is demonstrated against the criteria agreed in the design stage, and is expected to cover:

- Each host in the agreed inventory enrolled, reporting, and visible in the inventory view under its agreed group and tags
- The agreed metric set present for each host role, at the agreed collection interval
- Each remote-collected system returning data from its management interface
- The agreed dashboards and capacity reports rendering from live data
- Each agreed alert rule firing on a deliberately induced test condition and routing to the agreed destination
- Each agreed service level objective calculating against live data
- The access rules enforced, demonstrated by signing in as a role and seeing only the hosts agreed for it
- Data moving between tiers and expiring in line with the configured lifecycle policy, demonstrated on a shortened test policy
<!-- endif -->

## Scope Boundaries

Monitoring covers the hosts and management interfaces listed in the agreed inventory. Systems that expose no supported collection interface are recorded in the design document and reported by exception. Alert thresholds are detection targets: the platform reports a condition, and restoring the monitored system is not part of this scope.

## Product Exclusions

The following are outside what this module delivers. They are technical boundaries of the product and the configuration built on it; the proposal's commercial and legal exclusions are held in the single exclusion list elsewhere in this document and are not repeated here.

- Metrics from systems that expose no supported collection interface, and development of a custom collector for a proprietary interface
- Application-internal measurements — transaction timing, traces and code-level detail — which belong to application performance monitoring <!-- if not product_el_apm -->
- Application-internal measurements — transaction timing, traces and code-level detail — which are delivered by the application performance monitoring module, not this one <!-- if product_el_apm -->
- Log collection, parsing and log-based search, which belong to log management <!-- if not product_el_logs -->
- Network topology discovery, interface-level polling of the routed estate and traffic flow analysis
- Browser, synthetic and end-user experience monitoring, and continuous code profiling, unless separately agreed and quoted
- Tuning, patching or reconfiguring the monitored systems, and remediating the conditions the platform detects
- Changing a monitored system's own configuration, other than enabling the collection interface agreed in design
- Monitoring of platform or operating system releases outside the vendor's support matrix
- Migration of historical metric data from an existing monitoring platform
- Capacity forecasting as an ongoing analytical service beyond the trend reports listed as deliverables

*[Confirm the host inventory, the alert rules to be built and the dashboards to be delivered per bid.]*
