# Log Management and Analytics <!-- if not named_product_el_logs -->
# Elastic Log Management <!-- if named_product_el_logs -->

**Token:** `{{product_el_logs}}`
**Group:** Elastic Products
**Required:** No

---

Logs from the estate are collected centrally, parsed into a common structure, retained in tiers and made searchable for operations and investigation. <!-- if not named_product_el_logs -->
Elastic Log Management collects logs from the estate centrally, parses them into a common structure, retains them in tiers and makes them searchable for operations and investigation. <!-- if named_product_el_logs -->

## What It Delivers

- Central collection from servers, network devices, applications and platforms, by local collector or by receiving a forwarded stream
- Parsing into a consistent field structure, so the same fact carries the same field name whatever wrote it
- Enrichment at ingest, so an event arrives already carrying the host, service, environment and location it belongs to
- Retention tiers, so recent data stays fast to search and older data is held at a lower cost per gigabyte without being deleted
- Search and correlation across sources during an investigation, over the full retained period rather than only over recent data
- Alerting on patterns, including a rise in a message class, a threshold on a parsed field, and the absence of an expected message
- Pattern grouping and anomaly detection, so a new or unusual message class is surfaced rather than buried in volume
- Dashboards per source type and per service, with role-based access so a team sees only its own sources
- An audit trail of who searched what, where the compliance position requires it

The operational benefit is that an investigation runs in one place across every source, rather than by opening sessions on individual systems. The compliance benefit is that the retention obligation is met once, centrally, with evidence of it. The commercial benefit is that the retention cost is managed by tier rather than by deleting data the business later needs.

## Platform Components

The platform is assembled from the following functional parts. Each is deployed and configured as part of the work described below.

| Component | Function |
| :--- | :--- |
| Host collector | A single lightweight process per source host that tails the agreed log files or subscribes to the local event channel and ships the events to the ingest endpoint. |
| Stream receiver | An endpoint that accepts forwarded streams from devices and appliances that cannot run a local collector, over the agreed transport. |
| Collector management service | Central enrollment, policy assignment, configuration push and version upgrade for every deployed collector. |
| Ingest and parsing pipeline | Applies the parsing, field mapping, enrichment and routing rules to each event before it is stored. |
| Intermediate processing and buffering tier | Optional. Absorbs bursts, performs heavier transformation, and routes a copy of a stream to more than one destination where that is required. |
| Distributed storage and search engine | Indexes and holds the data across the tiers, and serves every search, dashboard and alert query. |
| Tiered storage and lifecycle controller | Places data on the hot, warm, cold and frozen tiers by age and expires it at the end of the agreed retention. |
| Alerting and anomaly-detection service | Evaluates the agreed rules on a schedule, groups message patterns, and routes notifications to the agreed destinations. |
| Search and investigation console | Ad-hoc search, saved investigations, dashboards and case handling. |
| Security and access layer | Authentication, role-based and field-level access control, encrypted transport and audit logging for the platform itself. |

<!-- if named_product_el_logs -->
In product terms, these are delivered by Elastic Agent with the integration set for each source type, enrolled and policed centrally through Fleet; Logstash where an intermediate buffer, a protocol the agent does not carry, or routing to more than one destination is required; Elasticsearch for ingest pipelines, storage across the data tiers, index lifecycle management and search; and Kibana for the log search, dashboards, alerting and case handling. Beats shippers remain available for the source types that still need them. Parsing targets the Elastic Common Schema field set, which is aligned with the OpenTelemetry semantic conventions, so fields agree across sources and with any OpenTelemetry data already present in {{customer_short}}'s estate. Data is held in data streams governed by an index lifecycle policy across the hot, warm, cold and frozen tiers, with the cold and frozen tiers backed by object storage and searched in place rather than restored first.

*[Confirm with the Verto Wave product team which storage and index mode is being quoted for log data, and whether the storage-reduction figures used in sizing are those the product team will stand behind for the release in the bid. Do not put a storage-saving percentage in a customer document without that confirmation.]*
<!-- endif -->

## Fit to {{customer_short}}'s Scope

This module covers the log layer of {{customer_short}}'s estate: what the systems in scope write about themselves, collected once and held centrally for the agreed period. It answers the requirement for a single searchable record of events across servers, network devices, applications and platforms — for troubleshooting during an incident, for investigation afterwards, and for the retention obligation that applies to {{customer_short}}'s sector. It is bounded at the log layer: numeric health and capacity data is covered by infrastructure monitoring, and code-level transaction detail by application performance monitoring. Where those are also in scope they run on the same platform, so an investigation moves between them without leaving the console.

*[Restate the specific requirement this module answers in {{customer_short}}'s own terms per bid, including the retention obligation and the source classes it applies to. Do not leave this paragraph generic in a competitive bid.]*

[[figure: el-logs-pipeline | Log pipeline and retention tiers]]

## Deployment Model

The platform is deployed either on infrastructure under {{customer_short}}'s control or consumed as a managed cloud service. The choice is made in the design stage and it determines the licensing basis, the node sizing below, and which party operates the platform itself. The proposal assumes one production deployment.

*[Confirm the deployment model and the licensing basis that follows from it per bid.]*

## What the Environment Must Provide

- Compute, memory and storage for the platform nodes, to the sizing recorded in the design document
- Object storage for the low-cost retention tiers, where the agreed retention model uses them
- Network paths and firewall rules from every log source to the collection endpoints, including the forwarding ports for devices that push their stream
- An account with the privilege to install and run a collector on each source host, or the ability to configure that source to forward its log stream
- Administrative access to configure logging on the source system itself, including raising the log level or enabling an audit log where the agreed content requires it
- Time synchronization across sources and platform nodes, so events from different systems order correctly in a single investigation
- Certificates for the collection and platform endpoints
- A documented owner per log source, for the onboarding and validation of that source
- A repository for the platform's own snapshots, separate from the data nodes

## Hardware Requirements

The figures below are the hardware requirements for this module — the log workload and the nodes that carry it. They are the platform vendor's recommended specifications for a self-managed deployment, expressed per node role, and they are sized by this module's own drivers: the daily ingest volume at peak and average, the number and type of sources, the retention held in each tier, and the number of copies held. They are indicative: the final node counts and disk sizes are calculated from the agreed figures and recorded in the design document. Where the platform is consumed as a managed cloud service, these roles still exist but are sized by the service rather than provisioned as machines.

### Node Roles and Indicative Specifications

| Node role | vCPU | Memory | Disk | Disk type | Minimum count |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Master-eligible | 4–8 | 16 GB | 200 GB | SSD | 3 |
| Hot data | 8–16 | 64 GB | 2–4 TB | NVMe SSD | 2 |
| Warm data | 8 | 64 GB | 8–10 TB | SSD or high-throughput SAS | 2 |
| Cold data | 4–8 | 64 GB | 10–20 TB | High-capacity SAS or SATA | 2 |
| Frozen data | 8 | 64 GB | 2 TB local cache | NVMe SSD | 2 |
| Ingest / coordinating | 8 | 32 GB | 200 GB | SSD | 2 |
| Intermediate processing and buffering | 4–8 | 16 GB | 200 GB | SSD | 2 |
| Search console | 4–8 | 16 GB | 100 GB | SSD | 2 |
| Collector management service | 4 | 8 GB | 100 GB | SSD | 2 |
| Machine learning | 8–16 | 64 GB | 500 GB | SSD | 2 |

Minimum counts are the counts that give resilience, not the counts that give capacity. Capacity is added by scaling the data tiers against the retained volume.

### Ratio Guidance

The ratios below govern a log cluster more than any single specification does:

- Java heap is set to at most half of a node's memory, and to no more than approximately 30 GB per node, because above that threshold the runtime loses compressed object pointers and the larger heap performs worse than the smaller one. A node with more than 64 GB of memory is therefore normally split into two nodes rather than given a larger heap.
- Memory-to-storage ratio per tier is approximately 1:30 on the hot tier, and approximately 1:160 on the warm and cold tiers. A 64 GB hot node therefore carries roughly 2 TB of data, and a 64 GB warm node roughly 10 TB.
- The frozen tier holds its data in object storage and keeps only a local cache on the node, so its local disk is sized to the working set rather than to the retained volume. Long compliance retention belongs on this tier, where the retained volume drives object storage cost rather than node count.
- At least three master-eligible nodes are required so that a quorum survives the loss of one.
- At least two data nodes per active tier are required before a replica can be placed on a different node from its primary.
- Usable capacity is planned below 85 percent of disk, because the engine stops allocating shards to a node at that level, stops relocating at 90 percent and enforces a read-only block at 95 percent.
- The hot tier is sized on ingest throughput as well as on storage. Indexing is processor- and disk-write-bound, so local NVMe is specified for hot data and the node count is checked against peak ingest, not average.
- The intermediate processing tier is sized on peak events per second and on the complexity of the transformation applied, and is scaled horizontally rather than by enlarging a single node.

### Worked Reference Points

These reference points are for log data only. They assume seven days on the hot tier, thirty days on the warm tier, the remaining retention on the frozen tier backed by object storage, and one replica on the hot and warm tiers. They exist so a reader can scale from a stated ingest volume, not as a quotation.

| Daily log ingest | Hot nodes | Warm nodes | Frozen nodes | Master | Ingest / processing | Console | Machine learning |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Up to 50 GB per day | 2 × (8 vCPU / 64 GB / 2 TB NVMe) | 2 × (8 vCPU / 64 GB / 8 TB) | Not required | 3 × (4 vCPU / 16 GB / 200 GB) | Carried by the data nodes | 2 × (4 vCPU / 16 GB / 100 GB) | Not required |
| Around 250 GB per day | 4 × (16 vCPU / 64 GB / 4 TB NVMe) | 4 × (8 vCPU / 64 GB / 10 TB) | 2 × (8 vCPU / 64 GB / 2 TB cache) | 3 × (8 vCPU / 16 GB / 200 GB) | 2 × (8 vCPU / 32 GB / 200 GB) | 2 × (8 vCPU / 16 GB / 100 GB) | 1 × (8 vCPU / 64 GB / 500 GB) |
| Around 1 TB per day | 12 × (16 vCPU / 64 GB / 4 TB NVMe) | 8 × (8 vCPU / 64 GB / 10 TB) | 3 × (8 vCPU / 64 GB / 2 TB cache) | 3 × (8 vCPU / 32 GB / 200 GB) | 4 × (8 vCPU / 32 GB / 200 GB) | 3 × (8 vCPU / 16 GB / 100 GB) | 2 × (8 vCPU / 64 GB / 500 GB) |

Stored volume per tier is calculated as the daily ingest multiplied by the days held in that tier, multiplied by one plus the number of replicas on that tier, multiplied by the indexing overhead factor for the source type, and then divided by the planned utilization ceiling. The indexing overhead factor varies with the source type, the field mapping and the storage mode selected, and is confirmed during design rather than assumed. Object storage for the frozen tier is sized on the retained volume separately from the node table above.

### Where Other Products Share the Same Platform

The figures above size this module on its own, and are complete for a bid in which log management is the only product. Where infrastructure monitoring or application performance monitoring is also in scope, those products run on the same cluster as this one: their node roles are these node roles. The combined solution is therefore sized once against the combined data volume and retention, not by adding a second and third cluster to this one. The combined figures are the ones recorded in the design document.

*[Hardware figures are indicative and are drawn from the platform vendor's published sizing and ratio guidance for a self-managed deployment. Confirm with the Verto Wave product team which product release the figures are taken from, and have them restated against that release before issue.]*

## How It Fits With the Rest of the Platform

- Logs share the platform with the metric and trace data, so a service, its host and its logs are correlated without a further integration. An investigation moves from a health alert to the log lines written in the same minute as a query, not as an export between tools. <!-- if product_el_observability or product_el_apm -->
- Platform capacity is sized once against the combined data, not once per product; the sizing figures in this proposal are the combined figures. <!-- if product_el_observability or product_el_apm -->
- One collector per host carries the log data and the metric data for that host, so the rollout is performed once and the agent estate is managed as one. <!-- if product_el_observability -->
- Trace identifiers carried in application log lines link a log entry to the transaction that produced it, so a failed transaction and its log output are read together. <!-- if product_el_apm -->
- Retained logs are available as evidence for compliance reporting, over the full retention period rather than only the recent window. <!-- if module_stackx_compliance -->
- Log-derived alerts are forwarded to the central event console for correlation and routing, so they are deduplicated alongside every other event source before an operator sees them. <!-- if product_ot_obm -->
- Log-derived alerts raise and update tickets in the service management platform, with the severity mapping agreed in design. <!-- if product_ot_smax or module_stackx_itSM -->
- Detected patterns can trigger an agreed automation workflow, within the boundaries set for that workflow. <!-- if product_ot_oo or module_stackx_automation_orchestration -->

## Build Activities <!-- if services -->

<!-- if services -->
**Platform build**

- Confirm the sizing inputs, then finalize the cluster topology, the node roles and the tier layout against the hardware requirements above
- Prepare the operating system on each platform node: file descriptor and memory map limits, swap disabled or memory locked, data volumes mounted and separated from the system volume, and the platform's own service account created
- Install the engine across the nodes, configure node roles and discovery, and form the cluster on a dedicated master quorum
- Generate and deploy the certificate set, enable encrypted transport between nodes and encrypted client traffic, and verify that no unencrypted path remains
- Configure the authentication realm, the role model, the access rules and, where agreed, field-level restrictions on sensitive log content
- Connect the object storage used by the low-cost tiers, and verify that data on those tiers is searchable in place
- Configure the snapshot repository and the backup schedule for the platform's own data, and restore one snapshot to prove the path works
- Configure the data tiers, the index templates and the lifecycle policy that moves and expires each source class on its own schedule
- Deploy the search console tier behind the agreed name and certificate, the collector management service, and the intermediate processing tier where the design calls for one

**Source onboarding**

- Agree the source inventory, and for each source the collection route, its owner, its expected daily volume, its parsing requirement and the retention tier it belongs to
- Collect a real sample from each source type before writing any parsing rule, and agree the target field set against that sample
- Build and test the parsing, field mapping and enrichment rules per source type, including the timestamp and time-zone handling for sources that do not state one
- Configure the stream receiver and the forwarding configuration for devices and appliances that push their logs rather than run a collector
- Build one collector policy per source role, and roll out to a pilot set of hosts before the phased rollout across the remainder
- Validate each onboarded source against its sample: fields populated, timestamps correct, volume within the estimate, and no events dropped or unparsed beyond the agreed tolerance
- Configure routing so each source class lands under its agreed lifecycle policy and access rule
- Record each source in the source inventory as it is accepted, with its owner and its measured volume

**Configuration and handover**

- Configure the agreed alert rules, including threshold, rate-of-change and missing-message rules, with their notification connectors and routing
- Configure pattern grouping and anomaly-detection jobs where they are agreed, and tune them across an agreed observation period so the output stays readable
- Build the agreed dashboards per source type and per service, and the saved searches the operations team will use during an incident
- Configure the access model, so each team's search scope is limited to the sources agreed for it, and enable platform audit logging where the compliance position requires it
- Run the agreed validation, tune the parsing and the alert thresholds against what the sources actually produce, and record the result
- Hand over the source inventory, the pipeline and parsing documentation, the administration guide and the runbook for onboarding a new source later
<!-- endif -->

## Sizing Basis

Sizing follows four figures, and all four are confirmed before the design is signed off:

- The daily ingest volume in gigabytes, at peak as well as average, because peaks size the ingest path while the average sizes the storage
- The number and type of sources, because parsing effort and field count vary by source type
- The retention held in each tier, which is normally set by an audit or regulatory requirement rather than by an operational one
- The number of copies held for resilience, which multiplies the storage on the tiers that hold them

Retention is the dominant cost driver on a log platform: doubling the retention period doubles the stored volume, while moving the same data to a lower tier changes its cost per gigabyte without losing it. The tier model is therefore agreed with {{customer_short}} against the audit requirement, not set to a default.

The figures are recorded in the design document and confirmed against a sample measurement taken from a representative set of sources over an agreed window, rather than estimated. A sustained change in daily volume or retention beyond the agreed figures is handled through the change process, because it changes the storage the platform needs.

*[Confirm average and peak daily volume, the source list with a volume estimate per source, retention per tier and the sample measurement window per bid. Do not carry volumes forward from a prior engagement.]*

## Acceptance Criteria <!-- if services -->

<!-- if services -->
Acceptance is demonstrated against the criteria agreed in the design stage, and is expected to cover, per source type:

- Events arriving from the agreed sources, at the agreed collection route
- The agreed fields parsed and populated on a live sample, with the unparsed proportion within the agreed tolerance
- The event timestamp resolving to the correct time and time zone, so events from different sources order correctly
- The source appearing under its agreed retention tier and access rule
- Search returning results across the retained period, including from a low-cost tier where one is in use
- Each agreed alert rule firing on a deliberately induced test condition and routing to the agreed destination
- The access model enforced, demonstrated by signing in as a role and seeing only the sources agreed for it
- Data moving between tiers and expiring in line with the configured lifecycle policy, demonstrated on a shortened test policy
<!-- endif -->

## Scope Boundaries

Collection covers the sources listed in the agreed inventory. Parsing is delivered against the message formats sampled during design; a source that changes its message format after sign-off is re-parsed through the change process. Search and alerting run over the data retained under the agreed tier model, and data aged out under that model is no longer searchable. Alert rules are detection targets: the platform reports a condition, and resolving what caused it is not part of this scope.

## Product Exclusions

The following are outside what this module delivers. They are technical boundaries of the product and the configuration built on it; the proposal's commercial and legal exclusions are held in the single exclusion list elsewhere in this document and are not repeated here.

- Sources that expose no supported collection interface and cannot forward a stream in a supported format, and development of a custom collector or codec for a proprietary format
- Parsing of message formats not sampled during design, and re-parsing after a source changes its format without notice
- Retrospective re-parsing of data already stored, unless agreed as a separate activity
- Changing a source system's own logging configuration, beyond enabling the collection or forwarding agreed in design; the source system's log content is what that system chooses to write
- Migration or back-loading of historical log archives from an existing platform, and conversion of archived formats
- Numeric health, capacity and performance metrics, which belong to infrastructure monitoring <!-- if not product_el_observability -->
- Code-level transaction detail and distributed traces, which belong to application performance monitoring <!-- if not product_el_apm -->
- Security detection content — correlation rules, threat intelligence matching and case management for a security operations function — unless a security module is separately in scope <!-- if not (module_stackx_security or module_stackx_soc) -->
- Data masking, tokenization or redaction of sensitive content inside log messages, beyond the field-level access restrictions agreed in design
- Legal hold, evidential chain-of-custody handling and forensic preservation of log data
- Remediating the conditions the platform detects, and acting on the alerts it raises
- Long-term archive outside the agreed retention model, and restoration of data already expired under that model

*[Confirm daily volume, the source list and retention per tier per bid.]*
