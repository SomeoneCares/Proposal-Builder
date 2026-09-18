# Application Performance Monitoring <!-- if not named_product_el_apm -->
# Elastic APM <!-- if named_product_el_apm -->

**Token:** `{{product_el_apm}}`
**Group:** Elastic Products
**Required:** No

---

Application monitoring instruments the services in scope and shows transaction performance, dependencies and errors as users experience them. <!-- if not named_product_el_apm -->
Elastic APM instruments the services in scope and shows transaction performance, dependencies and errors as users experience them. <!-- if named_product_el_apm -->

## What It Delivers

- Distributed transaction tracing across the instrumented services, with timing per step and the trace carried across service boundaries
- A dependency map built from the traces, showing what each service calls, how often and how each call performs
- Error and exception tracking, grouped so a recurring fault is one entry with a count and a first-seen time, rather than a flood
- Slow-transaction analysis down to the query, remote call or method responsible, with the parameters of the slow path where the runtime exposes them
- Aggregated service metrics — throughput, latency distribution and error rate per service, version and environment — retained far longer than the traces themselves
- Alerting on latency, error rate and throughput against agreed targets, including comparison against the same service's own normal behavior
- Service level objectives tracked against agreed indicators such as latency and error rate, with the error budget shown against the target
- Comparison across deployments, so the effect of a release on latency or error rate is visible
- Correlation with the logs of the same service, from the same trace identifier <!-- if product_el_logs -->
- Correlation with the host and container metrics underneath the service <!-- if product_el_observability -->

The operational benefit is that a performance complaint is answered with evidence — which service, which call, which release — instead of with a round of mutual elimination between teams. The development benefit is that a regression is attributed to a change while the change is still recent.

## Platform Components

The platform is assembled from the following functional parts. Each is deployed and configured as part of the work described below.

| Component | Function |
| :--- | :--- |
| Instrumentation library | A language-specific library loaded into each application process; it times transactions, records spans and errors, and propagates the trace identifier to the next service. |
| Trace context propagation | The standard headers that carry a trace identifier between services, so calls made by one service join the trace started by another. |
| Intake endpoint | Receives trace, error and metric events from the instrumented applications, validates and enriches them, and writes them to storage. |
| Collector management service | Central enrollment, policy assignment and version upgrade for the intake components and any host-side collectors. |
| Sampling controller | Decides which traces are kept in full, by a fixed rate before the trace runs or by a decision taken once the trace is complete, so that unusual and failing traces survive while routine ones are aggregated. |
| Aggregation pipeline | Produces the per-service throughput, latency and error-rate series from the full trace stream, so service-level views stay accurate even where traces are sampled. |
| Distributed storage and search engine | Indexes and holds traces, errors and aggregated metrics across the tiers, and serves the queries behind every view and alert. |
| Lifecycle controller | Applies a separate retention to full traces and to the aggregated data, and expires each at the end of its agreed period. |
| Alerting and anomaly-detection service | Evaluates the agreed rules, learns each service's normal behavior where anomaly detection is enabled, and routes notifications. |
| Application performance console | Service inventory, transaction and trace views, the dependency map, error grouping, service level objective tracking and case handling. |
| Security and access layer | Authentication, role-based access control, encrypted transport and audit logging for the platform itself. |

<!-- if named_product_el_apm -->
In product terms, instrumentation is delivered through OpenTelemetry wherever the runtime supports it, using the Elastic distributions of the OpenTelemetry language agents and collector, with the native Elastic APM agents used for the runtimes where a supported OpenTelemetry route is not yet available. Trace, error and metric events are received on the managed intake endpoint, stored in Elasticsearch alongside the rest of the telemetry, and presented in the Kibana application performance views. Sampling is configured either as a fixed rate applied at the start of a trace or as a decision taken once the trace is complete, so that slow and failing traces are retained in preference to routine ones.

*[Confirm with the Verto Wave product team, per runtime in scope, which instrumentation route is proposed and that it is generally available in the release being quoted. Elastic's agent strategy has moved toward OpenTelemetry and the support position differs by language — do not assume parity across runtimes. Confirm separately whether tail-based sampling, browser monitoring or continuous profiling is being offered; none of them is included in this module as written.]*
<!-- endif -->

## Fit to {{customer_short}}'s Scope

This module covers the application layer of {{customer_short}}'s estate: the services named in the agreed inventory, instrumented so that their transaction performance, their dependencies on each other and their errors are visible as a user experiences them. It answers the requirement to know whether a business service is performing, and where the time goes when it is not — a question infrastructure monitoring cannot answer, because a host can be healthy while the service on it is slow. It is bounded at the services instrumented under this scope: systems that cannot be instrumented remain visible at infrastructure level only. Where infrastructure monitoring or log management is also in scope, they run on the same platform, so a slow transaction, the host it ran on and the log lines it wrote are read together.

*[Restate the specific requirement this module answers in {{customer_short}}'s own terms per bid, naming the business services the requirement is really about. Do not leave this paragraph generic in a competitive bid.]*

[[figure: el-apm-traces | Transaction traces and service dependencies]]

## Deployment Model

The platform is deployed either on infrastructure under {{customer_short}}'s control or consumed as a managed cloud service. The choice is made in the design stage and it determines the licensing basis, the node sizing below, and which party operates the platform itself. The proposal assumes one production deployment; instrumenting a non-production environment as well is a separate line of scope, and is normally worth doing because it is where a regression is cheapest to find.

*[Confirm the deployment model, the licensing basis that follows from it, and whether non-production environments are to be instrumented per bid.]*

## What the Environment Must Provide

- Compute, memory and storage for the platform nodes, to the sizing recorded in the design document
- Network paths and firewall rules from every instrumented application host to the intake endpoint
- A supported runtime version for each application in scope, confirmed against the vendor support matrix during design
- The ability to add the instrumentation library or collector to each application's build or runtime configuration, and a release or restart window in which to apply it
- Application team availability for service naming, environment naming and the user journeys to be validated
- Access to the application's deployment pipeline or configuration management, so instrumentation is applied the same way on every instance rather than by hand
- Certificates for the intake and platform endpoints
- An agreed sampling decision per service before instrumentation begins, because it governs both the data volume and what is visible in an investigation
- A repository for the platform's own snapshots, separate from the data nodes

## Hardware Requirements

The figures below are the hardware requirements for this module — the application performance monitoring workload and the nodes that carry it. They are the platform vendor's recommended specifications for a self-managed deployment, expressed per node role, and they are sized by this module's own drivers: the peak transaction rate across the instrumented services, the sampling rate agreed per service, the number of spans in a typical trace, and the separate retention held for full traces and for aggregated data. They are indicative: the final node counts and disk sizes are calculated from the agreed figures and recorded in the design document. Where the platform is consumed as a managed cloud service, these roles still exist but are sized by the service rather than provisioned as machines.

### Node Roles and Indicative Specifications

| Node role | vCPU | Memory | Disk | Disk type | Minimum count |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Master-eligible | 4–8 | 16 GB | 200 GB | SSD | 3 |
| Hot data | 8–16 | 64 GB | 2–4 TB | NVMe SSD | 2 |
| Warm data | 8 | 64 GB | 8–10 TB | SSD or high-throughput SAS | 2 |
| Intake endpoint | 4–8 | 8–16 GB | 100 GB | SSD | 2 |
| Ingest / coordinating | 8 | 32 GB | 200 GB | SSD | 2 |
| Application performance console | 4–8 | 16 GB | 100 GB | SSD | 2 |
| Collector management service | 4 | 8 GB | 100 GB | SSD | 2 |
| Machine learning | 8–16 | 64 GB | 500 GB | SSD | 2 |

Minimum counts are the counts that give resilience, not the counts that give capacity. The intake endpoint is placed behind a load-balanced address so that instrumented applications keep sending during a node restart.

The instrumentation libraries themselves run inside the application processes and consume a share of each application host's own processor and memory. That overhead is a property of the monitored estate, not of the platform, and is measured on the pilot service before the wider rollout rather than assumed.

### Ratio Guidance

The ratios below govern this cluster more than any single specification does:

- Java heap is set to at most half of a node's memory, and to no more than approximately 30 GB per node, because above that threshold the runtime loses compressed object pointers and the larger heap performs worse than the smaller one.
- Memory-to-storage ratio per tier is approximately 1:30 on the hot tier, and approximately 1:160 on the warm tier. A 64 GB hot node therefore carries roughly 2 TB of data, and a 64 GB warm node roughly 10 TB.
- At least three master-eligible nodes are required so that a quorum survives the loss of one, and at least two data nodes per active tier before a replica can be placed on a different node from its primary.
- Usable capacity is planned below 85 percent of disk, because the engine stops allocating shards to a node at that level, stops relocating at 90 percent and enforces a read-only block at 95 percent.
- Intake capacity scales with events received per second, not with the number of services. Intake nodes are added horizontally as the peak event rate rises.
- Trace data is short-lived and aggregated data is long-lived. Full traces are commonly held on the hot tier for days, while the per-service aggregated metrics are held for months on the warm tier at a fraction of the volume. Sizing the two together at the same retention is the commonest way an application monitoring cluster is over-specified.
- Where a sampling decision is taken only once a trace is complete, the spans of an in-flight trace are buffered before the decision, which adds memory and local disk to the intake tier. This is confirmed in design if that sampling mode is selected.

### Worked Reference Points

These reference points are for application performance data only. They assume a moderate span count per trace, full traces held for seven days on the hot tier, aggregated service metrics held for ninety days on the warm tier, and one replica. They exist so a reader can scale from a stated transaction rate, not as a quotation.

| Peak transaction rate | Sampling | Hot nodes | Warm nodes | Intake nodes | Master | Console | Machine learning |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Up to 500 transactions per second | Full sampling | 2 × (8 vCPU / 64 GB / 2 TB NVMe) | 2 × (8 vCPU / 64 GB / 8 TB) | 2 × (4 vCPU / 8 GB / 100 GB) | 3 × (4 vCPU / 16 GB / 200 GB) | 2 × (4 vCPU / 16 GB / 100 GB) | Not required |
| Around 5,000 transactions per second | Reduced rate per service | 4 × (16 vCPU / 64 GB / 4 TB NVMe) | 3 × (8 vCPU / 64 GB / 10 TB) | 3 × (8 vCPU / 16 GB / 100 GB) | 3 × (8 vCPU / 16 GB / 200 GB) | 2 × (8 vCPU / 16 GB / 100 GB) | 1 × (8 vCPU / 64 GB / 500 GB) |
| Around 25,000 transactions per second | Low rate, with unusual and failing traces retained in preference | 8 × (16 vCPU / 64 GB / 4 TB NVMe) | 5 × (8 vCPU / 64 GB / 10 TB) | 4 × (8 vCPU / 16 GB / 200 GB) | 3 × (8 vCPU / 32 GB / 200 GB) | 3 × (8 vCPU / 16 GB / 100 GB) | 2 × (8 vCPU / 64 GB / 500 GB) |

The sampling column is what holds the node counts down as the transaction rate rises. The same transaction rate at full sampling instead of a reduced rate multiplies the stored trace volume by the inverse of the sampling rate, and the hot tier grows with it. Stored volume is calculated as the retained event rate multiplied by the average event size multiplied by the seconds held in the tier, multiplied by one plus the number of replicas, and then divided by the planned utilization ceiling. The average event size depends on the span count per trace and on how much context each instrumented service attaches, and is measured on the pilot service rather than assumed.

### Where Other Products Share the Same Platform

The figures above size this module on its own, and are complete for a bid in which application performance monitoring is the only product. Where infrastructure monitoring or log management is also in scope, those products run on the same cluster as this one: their node roles are these node roles, with the intake tier added for this module. The combined solution is therefore sized once against the combined data volume and retention, not by adding a second and third cluster to this one. The combined figures are the ones recorded in the design document.

*[Hardware figures are indicative and are drawn from the platform vendor's published sizing and ratio guidance for a self-managed deployment. Confirm with the Verto Wave product team which product release the figures are taken from, and have them restated against that release before issue. Confirm the assumed span count and event size against a measured pilot service before these node counts are quoted.]*

## How It Fits With the Rest of the Platform

- Traces share the platform with the metric and log data, so a slow transaction, the logs it wrote and the host it ran on are seen together rather than assembled by hand from three tools. <!-- if product_el_observability or product_el_logs -->
- Platform capacity is sized once against the combined data, not once per product; the sizing figures in this proposal are the combined figures. <!-- if product_el_observability or product_el_logs -->
- Infrastructure metrics supply the host and container context underneath a slow service, so latency can be attributed to contention on the host rather than to the code, or the other way round. <!-- if product_el_observability -->
- The trace identifier written into the application's own log lines links a failing transaction to the log output it produced, so the trace view and the log search are two views of one event. <!-- if product_el_logs -->
- Application alerts are forwarded to the central event console for correlation and routing, so an application symptom is correlated with the infrastructure events around it before an operator sees it. <!-- if product_ot_obm -->
- Application alerts raise and update tickets in the service management platform, with the severity mapping agreed in design. <!-- if product_ot_smax or module_stackx_itSM -->
- Service and dependency information from the traces can inform the configuration model, within the reconciliation rules agreed for it. <!-- if product_ot_ucmdb -->
- Instrumentation is applied through the release pipeline, so a newly deployed service arrives instrumented rather than being added afterwards. <!-- if module_stackx_devops -->

## Build Activities <!-- if services -->

<!-- if services -->
**Platform build**

- Confirm the sizing inputs, then finalize the cluster topology, the node roles and the tier layout against the hardware requirements above
- Prepare the operating system on each platform node: file descriptor and memory map limits, swap disabled or memory locked, data volumes mounted and separated from the system volume, and the platform's own service account created
- Install the engine across the nodes, configure node roles and discovery, and form the cluster on a dedicated master quorum
- Generate and deploy the certificate set, enable encrypted transport between nodes and encrypted client traffic, and verify that no unencrypted path remains
- Configure the authentication realm, the role model and the access rules for the application performance views
- Deploy the intake endpoint behind a load-balanced address and its certificate, and the collector management service
- Configure the snapshot repository and the backup schedule for the platform's own data, and restore one snapshot to prove the path works
- Configure the separate retention for full traces and for aggregated service data, with the lifecycle policy for each
- Deploy the console tier and verify the application performance views against a test service

**Instrumentation**

- Agree the service inventory, the runtime of each service, and which services are instrumented in which phase
- Agree the service and environment naming convention before any instrumentation is applied, because renaming afterwards breaks the history
- Agree the sampling model per service, and the user journeys that will be validated at acceptance
- Instrument a pilot service first: apply the library, deploy it through {{customer_short}}'s normal release process, and measure the overhead on the application host and the event volume it produces
- Review the pilot result with {{customer_short}}'s development team, adjust the sampling rate and the captured context, and confirm the sizing assumptions against the measured figures
- Instrument the remaining services in agreed phases, one release cycle at a time, with the development team applying each change through the pipeline
- Configure trace context propagation across service boundaries, including at the entry point, so a journey appears as one trace rather than several
- Validate that traces join correctly at every boundary between instrumented services, and record where a journey crosses an uninstrumented system
- Configure the capture of database and remote-call detail per service, within the limits agreed for sensitive parameters

**Configuration and handover**

- Configure the alert rules agreed per service — latency, error rate and throughput — with their notification connectors and routing
- Configure the service level objectives agreed for the services in scope, with their indicators, targets and reporting period
- Configure anomaly-detection jobs where they are agreed, and tune them across an agreed observation period
- Build the agreed dashboards per service and the views the operations and development teams will use during an incident
- Configure the access model so each team sees the services agreed for it
- Validate the agreed user journeys end to end across the instrumented services, and record the result
- Hand over the instrumentation guide, the naming convention, the sampling model and the runbook, so {{customer_short}}'s teams can instrument a new service later without Verto Wave
<!-- endif -->

## Sizing Basis

Sizing follows the figures below, and all of them are confirmed before the design is signed off:

- The number of instrumented services and their runtimes
- The transaction rate per service at peak, not at average, because trace volume follows the peak
- The sampling rate agreed per service, which is the single largest lever on both the data volume and the platform cost
- The number of spans in a typical trace and the context each service attaches, which together set the average event size
- The retention held for full traces, and separately for the aggregated performance and error data, which is normally retained far longer than the traces themselves

Trace volume is driven by transaction rate and sampling rate, not by the number of services. A fully sampled high-traffic service can produce more data than the rest of the estate combined, so the sampling model is agreed per service during design and recorded in the design document. A sustained change in transaction rate or sampling rate beyond the agreed figures is handled through the change process.

*[Confirm the service list with runtimes, peak transaction rate per service, the sampling model and the retention per data type per bid. Do not carry sampling assumptions forward from a prior engagement.]*

## Acceptance Criteria <!-- if services -->

<!-- if services -->
Acceptance is demonstrated against the criteria agreed in the design stage, and is expected to cover, per instrumented service:

- Transactions appearing under the agreed service name, environment name and version
- The service appearing on the dependency map with its downstream calls and their timing
- Slow-transaction detail resolving to the query or remote call responsible, on a live sample
- An induced error appearing as a grouped entry with its stack detail, where the runtime exposes it
- The agreed sampling rate applied and verifiable on the service's own data
- Each agreed alert rule firing on a deliberately induced test condition and routing to the agreed destination
- Each agreed service level objective calculating against live data
- Each agreed user journey appearing as a single joined trace across the services instrumented under this scope
- The access model enforced, demonstrated by signing in as a role and seeing only the services agreed for it
- Full traces and aggregated data expiring on their separate retention schedules, demonstrated on a shortened test policy
<!-- endif -->

## Scope Boundaries

Tracing covers the applications instrumented under this scope. Applications that cannot be instrumented, or whose runtime has no supported instrumentation route, are monitored at infrastructure level only and are recorded in the design document. A journey that crosses an uninstrumented service is visible up to that boundary and resumes beyond it. Where sampling is applied, a given individual transaction may not have been retained; service-level throughput, latency and error rate remain accurate because they are aggregated from the full stream before sampling. The platform reports latency, errors and their probable location for the application team to act on; correcting the application behavior is not part of this scope.

## Product Exclusions

The following are outside what this module delivers. They are technical boundaries of the product and the configuration built on it; the proposal's commercial and legal exclusions are held in the single exclusion list elsewhere in this document and are not repeated here.

- Applications whose runtime has no supported instrumentation route, and development of a custom instrumentation library for such a runtime
- Modifying application source code beyond adding the instrumentation library and its configuration, and any custom in-code instrumentation of specific business methods unless separately agreed
- Packaged or third-party applications that do not permit their runtime or startup configuration to be changed
- Deploying the instrumented application build; instrumentation is applied through {{customer_short}}'s own release process and release windows
- Browser, mobile and synthetic end-user experience monitoring, and continuous code profiling, unless separately agreed and quoted
- Database performance tuning, query optimization and schema analysis; the platform identifies the slow query, it does not fix it
- Load testing, performance benchmarking and capacity testing of the instrumented applications
- Diagnosing or correcting the application defects the platform surfaces, and any change to application behavior
- Retention or reconstruction of individual transactions that sampling did not retain
- Masking, tokenization or redaction of sensitive values captured in transaction parameters, beyond the capture limits and access restrictions agreed in design
- Host, container and infrastructure metrics, which belong to infrastructure monitoring <!-- if not product_el_observability -->
- Application log collection, parsing and log-based search, which belong to log management <!-- if not product_el_logs -->
- Instrumentation of non-production environments, unless confirmed in the design as in scope

*[Confirm the applications, their runtimes and the user journeys to validate per bid. Confirm which, if any, browser or synthetic end-user monitoring is included — it is not covered by this module as written.]*
