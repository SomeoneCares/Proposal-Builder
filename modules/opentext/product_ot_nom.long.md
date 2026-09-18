# Network Operations Management <!-- if not named_product_ot_nom -->
# OpenText NOM <!-- if named_product_ot_nom -->

**Token:** `{{product_ot_nom}}`
**Group:** OpenText Products
**Required:** No

---

Network monitoring discovers the routed and switched estate, keeps its topology current, and reports faults and performance against it. <!-- if not named_product_ot_nom -->
OpenText NOM discovers the routed and switched estate, keeps its topology current, and reports faults and performance against it. <!-- if named_product_ot_nom -->

The product is a suite rather than a single server. A fault and topology component discovers the network and decides which alarm is the cause; a performance component polls and trends interface and component metrics; a traffic component reads the flow records the devices export; a synthetic-test component measures latency, jitter and loss along the paths that carry real-time traffic; and a configuration component captures device configurations, compares them over time and checks them against policy. They share one topology, so a performance problem, a traffic pattern and a configuration change can be read against the same device and interface.

## Where It Fits in This Project

{{customer_short}}'s requirement is to know the state of the network before its users report it, and to tell the difference between a failed device and the two hundred devices behind it that merely became unreachable. That distinction is what keeps a network team working on the fault instead of on the alarm list.

In this project the platform covers the routed and switched estate agreed during the design stage: its discovery, its topology, its fault and performance monitoring, and — where they are in scope — its traffic analysis, its synthetic path tests and its configuration compliance. Network faults leave this platform for the event console or the service desk rather than being worked from a second console. The device and interface quantities are held in the professional services scope and are not repeated here.

## Platform Components

<!-- if not named_product_ot_nom -->
- **Fault and topology component** — discovery of devices, interfaces and their layer 2 and layer 3 connectivity; state polling; trap and syslog handling; and the causal engine that decides which alarm is the cause and which are consequences.
- **Performance component** — metric polling, retention and trending for interfaces and device components, with static thresholds and calculated baselines, and the performance reports built on them.
- **Traffic component** — a collector for the flow records the devices export, resolving a congested interface into the applications, sources and conversations behind it.
- **Synthetic test component** — configured tests between agreed points, reporting latency, jitter, loss and call-quality scores along paths that carry real-time traffic.
- **Configuration and compliance component** — scheduled capture of device configurations, change detection and comparison, policy compliance checking and device software image records.
- **Regional and central managers** — a manager per region forwarding to a central manager, so a distributed estate is monitored locally and seen centrally.
- **Console and reporting** — the topology, incident and drill-down interface, and the scheduled availability, utilization and fault reports.
<!-- endif -->

<!-- if named_product_ot_nom -->
- **Network Node Manager i** — discovery of devices, interfaces and their layer 2 and layer 3 connectivity; state polling; trap and syslog handling; and the causal engine that decides which alarm is the root cause and which are consequences.
- **Performance for Metrics** — metric polling, retention and trending for interfaces and device components, with static thresholds and calculated baselines, and the performance reports built on them.
- **Performance for Traffic** — flow record collection, resolving a congested interface into the applications, sources and conversations behind it.
- **Performance for Quality Assurance** — synthetic tests between agreed points, reporting latency, jitter, loss and call-quality scores along paths that carry real-time traffic.
- **Network Automation** — scheduled capture of device configurations, change detection and comparison, policy compliance checking and device software image records.
- **Global network management** — regional managers forwarding to a global manager, so a distributed estate is monitored locally and seen centrally.
- **Console and reporting** — the topology, incident and drill-down interface, and the scheduled availability, utilization and fault reports.
<!-- endif -->

*[The components above have historically been separate entitlements. Confirm with the Verto Wave product team which are inside the entitlement being quoted, and remove from this module any component that is not being sold.]*

## What It Delivers

- Discovery of network devices and interfaces at layer 2 and layer 3, with a topology map kept current automatically as devices are added, moved and removed
- Fault monitoring with root-cause suppression, so a failed uplink does not alarm everything behind it
- Trap and syslog handling, with each managed alert carried through one incident lifecycle rather than a separate log to watch
- Performance monitoring of interfaces, links, capacity and errors, current and historical, with the trend behind a complaint available rather than reconstructed
- Threshold and baseline alerting per interface class, so a busy link and a quiet one are judged against their own normal
- Traffic analysis from the flow records the devices export, showing the interfaces, applications and conversations behind a congested link
- Synthetic tests between agreed points, reporting latency, jitter and loss on the paths that carry real-time traffic
- Configuration capture for in-scope devices, with change history, comparison between two points in time, and policy compliance checks that flag a device that has drifted from standard
- Device, user and tenant groups, so each team sees the part of the estate it operates
- Regional and central managers that consolidate an estate spread across locations
- Reporting on availability, utilization, capacity trend and the devices that raise the most faults


[[figure: ot-nom-topology | Network topology and fault monitoring]]

## Integration

The links below are configured only where both platforms are part of this proposal.

- The event console receives network faults with their root-cause result already applied, so the network is polled once and judged once, and network events correlate alongside server and application events. <!-- if product_ot_obm -->
- The configuration management database receives the discovered network topology, devices and interfaces, so the network is not discovered twice by two products. <!-- if product_ot_ucmdb -->
- The service management platform receives incidents for network faults directly, where no event console is in scope. <!-- if product_ot_smax and not product_ot_obm -->
- The automation platform runs a flow against a device when an agreed fault is detected, and is the route by which a configuration change is pushed under approval. <!-- if product_ot_oo -->
- Device syslog is forwarded in parallel to the log platform, where long-term search and retention of raw device logs live there rather than here. <!-- if product_el_logs -->
- Device syslog is forwarded in parallel to the event and log management platform for long-term search and retention. <!-- if module_stackx_event_log_mgmt -->
- The network operations platform in scope and this platform are aligned during design so that one of the two polls each device, not both. <!-- if module_stackx_network_ops -->
- The operations configuration management platform receives the discovered network topology as configuration item data. <!-- if module_stackx_ops_config_mgmt -->
- The service management platform in scope receives incidents for network faults. <!-- if module_stackx_itSM and not product_ot_obm -->

## Build Activities <!-- if services -->

<!-- if services -->
**Design confirmation**

- Agree the device inventory: management address, vendor, model, role and site per device, and the device classes those roles map to.
- Agree the discovery seed list and the discovery boundaries, so discovery does not walk into networks that are out of scope.
- Agree the polling intervals, thresholds and baseline behavior per device class, and the interfaces that are monitored as opposed to merely discovered.
- Agree the alert routing map, the maintenance windows and the incident lifecycle.

**Platform deployment**

- Deploy the platform components in scope and bring them to the supported patch level.
- Deploy regional managers where the estate requires them, and configure forwarding to the central manager.
- Configure the access model, including the device, user and tenant groups that partition the estate.
- Configure backup of the platform's databases and configuration, and prove a restore before discovery starts.

**Discovery and topology**

- Load the management protocol credentials for the in-scope ranges and devices.
- Run discovery against the agreed seed list and boundaries, in stages.
- Validate the topology against {{customer_short}}'s own network documentation, and resolve the differences — the differences are usually the useful part.
- Agree and record the final device and interface inventory, including the interfaces excluded from polling and why.

**Fault and performance configuration**

- Configure device and interface groups per class, and the polling intervals, thresholds and baselines that go with each.
- Configure trap and syslog reception, the trap definitions for the device types in scope, and the mapping from trap to managed alert.
- Configure the incident lifecycle, the root-cause behavior and the alert routing per device class.
- Configure the maintenance windows during which polling is quietened.
- Tune the alarm set across an agreed observation period, so the console the team inherits is one they will read.

**Traffic, synthetic tests and configuration compliance**

- Enable flow export on the interfaces where traffic analysis is in scope, direct it at the collector and validate that records arrive and resolve correctly.
- Configure the synthetic tests between the agreed source and target points, and confirm each test reports against a known-good path before it is trusted.
- Configure scheduled configuration capture for the in-scope devices, with the credentials it requires.
- Configure the compliance policies to be checked, the comparison reports and the change notifications.

**Integration and handover**

- Forward events to the correlation console, and confirm the root-cause result survives the forwarding. <!-- if product_ot_obm -->
- Publish the network topology to the configuration record. <!-- if product_ot_ucmdb -->
- Configure incident creation in the service management platform. <!-- if product_ot_smax and not product_ot_obm -->
- Configure the agreed reports and dashboards, including the scheduled distribution list for each.
- Hand over the device inventory, the polling configuration, the credential register and the administration guide.
<!-- endif -->

## Hardware Requirements

The specifications below are this product's own components. They are the vendor's recommended figures for the deployment sizes shown, are indicative, and are confirmed against the device and interface counts recorded in the design document.

| Component | Small — up to ~250 devices | Medium — up to ~3,000 devices | Large — above ~3,000 devices |
| :--- | :--- | :--- | :--- |
| Fault and topology server | 4 vCPU / 16 GB RAM / 150 GB SSD | 8 vCPU / 32 GB RAM / 300 GB SSD | 16 vCPU / 64 GB RAM / 500 GB SSD |
| Performance component | 4 vCPU / 16 GB RAM / 250 GB SSD | 8 vCPU / 32 GB RAM / 500 GB SSD | 16 vCPU / 64 GB RAM / 1 TB SSD, high IOPS |
| Traffic collector, where in scope | 4 vCPU / 16 GB RAM / 250 GB SSD | 8 vCPU / 32 GB RAM / 500 GB SSD | 8 vCPU / 32 GB RAM / 1 TB SSD per collector |
| Synthetic test component, where in scope | 2 vCPU / 8 GB RAM / 100 GB SSD | 4 vCPU / 8 GB RAM / 150 GB SSD | 4 vCPU / 16 GB RAM / 250 GB SSD |
| Configuration and compliance component, where in scope | 4 vCPU / 16 GB RAM / 200 GB SSD | 8 vCPU / 16 GB RAM / 300 GB SSD | 8 vCPU / 32 GB RAM / 500 GB SSD |
| Regional manager, where the estate requires one | 4 vCPU / 16 GB RAM / 150 GB SSD each | 8 vCPU / 32 GB RAM / 300 GB SSD each | 8 vCPU / 32 GB RAM / 300 GB SSD each |
| Central manager, where regional managers are deployed | 8 vCPU / 32 GB RAM / 300 GB SSD | 16 vCPU / 64 GB RAM / 500 GB SSD | 16 vCPU / 96 GB RAM / 1 TB SSD |

- Polled interface count drives the performance component more than device count does; a few large chassis switches can size it higher than several hundred branch routers.
- The performance component's storage is latency-sensitive: it writes continuously and reports off the same volume, so SSD-class storage with headroom for the agreed retention is required.
- Traffic collection is sized on flow records per second and the retention held; one collector per region is the usual arrangement where regional managers are deployed.
- Storage for all components grows with the retention period agreed in the design stage.

*[Hardware figures are indicative and are confirmed during the design stage. Confirm with the Verto Wave product team which release the figures are drawn from, and re-check them against that release's sizing guide — the suite's tier boundaries have moved between releases — before issue.]*

## What the Platform Needs

- Read access by the agreed management protocol on every in-scope device, with community strings or user credentials supplied by a named owner
- Management pings permitted from the pollers to the managed addresses
- Trap and syslog forwarding configured on the devices to the platform's addresses
- Flow export enabled on the interfaces where traffic analysis is in scope, directed at the collector address
- Privileged read credentials for configuration capture, and write credentials only where automated configuration change is agreed to be in scope
- A management address per device, and the maintenance windows during which polling may be quietened
- {{customer_short}}'s current network documentation, for the topology validation step
- Name resolution, time synchronization and the network paths recorded in the design document

## Sizing Basis

Sizing follows the number of devices and interfaces polled, the polling interval, the volume of flow records collected, the number of synthetic tests and the retention period. The figures are recorded in the design document and confirmed against the device inventory.

The polling interval per device class sets how quickly a fault is detected, and is recorded in the design document. Restoring a failed device or circuit is not part of this platform's scope, and no restoration or resolution time is committed on the basis of it.

## Scope Boundaries

### Not Covered by This Product's Scope

- Devices that do not respond to the agreed management protocol, or that expose only a proprietary interface the platform does not support.
- Packet capture and payload inspection: the platform reads counters, flow records and device state, not the contents of traffic.
- Per-client wireless visibility beyond what the wireless controllers in scope expose to the platform.
- Networks beyond the demarcation point with a carrier or service provider; a provider circuit is monitored from {{customer_short}}'s side of it only.
- Automated configuration change and device software image upgrades, unless those are explicitly agreed as in scope, and never without an approval step.
- Repairing, reconfiguring or replacing the devices whose faults the platform reports.
- Monitoring of servers, applications and endpoints, which the platform sees as network endpoints only.

## Acceptance <!-- if services -->

<!-- if services -->
The platform is accepted when, in a session run jointly with {{customer_short}}:

- Every device in the agreed inventory appears in the topology with its in-scope interfaces polled, and the exceptions are listed with their reason.
- A fault raised on a nominated test device appears in the console within one polling cycle for its class and routes to the agreed group.
- A downstream device behind that test device is shown as a consequence rather than as a separate cause.
- A trap sent from a nominated device produces the mapped managed alert.
- The agreed performance reports render with data for the agreed period, and a threshold breach on a nominated interface produces its alert.
- Where traffic analysis is in scope, a congested or loaded interface resolves to its top applications and conversations.
- Where synthetic tests are in scope, each configured test reports latency, jitter and loss for its path.
- Where configuration compliance is in scope, a deliberate configuration change on a nominated device is captured, shown in comparison and flagged against its policy.

Acceptance covers detection, reporting and routing. It does not extend to the behavior of the network devices themselves, and no restoration or resolution time is committed.
<!-- endif -->

*[Confirm device counts per class, polling intervals, retention, and whether flow-based traffic analysis, synthetic path testing and configuration compliance are in scope per bid.]*

*[Verify with the Verto Wave product team before issue: the current suite and component names, and which of the traffic, synthetic-test and configuration-compliance components are inside the entitlement being quoted — they have historically been separate line items.]*
