# Hardware Specifications and Sizing

**Token:** `{{section_hardware_sizing}}`  
**Group:** Optional Proposal Sections  
**Required:** No

---

## DeviceX Appliance Specifications <!-- if devicex -->

<!-- if devicex -->
Every class runs the complete module set; the class determines capacity, not capability.

[[figure: hardware-site-classes | Site classes and platform sizing]]


| Reference configuration | Processor | Memory | Storage | Network interfaces |
| :--- | :--- | :--- | :--- | :--- |
| DeviceX Mid-Range | Multi-core x86 processor | 64 GB DDR4 | 2 × 4 TB SATA and 2 × 256 GB NVMe | 8 × 1 GbE RJ45 and 2 × 10 GbE SFP+ |
| DeviceX High-Capacity | 24-core server-class x86 processor | 128 GB | 512 GB SSD and 2 TB HDD | 8 × 1 GbE and 4 × 10 GbE, with 4G/5G connectivity |

*[Confirm the current model names and specifications with the Verto Wave product team before issue. Specifications are indicative and may be superseded by equivalent or higher configurations.]*

## Site Sizing Classes <!-- if devicex -->

Each site is assigned to a standard class during the design stage, based on the number of concurrent priority real-time sessions and the workloads it hosts.

| Class | Concurrent priority sessions | Recommended symmetric bandwidth | Typical site |
| :--- | :--- | :--- | :--- |
| Class A | Up to 2 | 25 Mbps | Small site with a limited number of users and services |
| Class B | Up to 4 | 50 Mbps | Standard branch with local workloads |
| Class C | Up to 8 | 100 Mbps | Large or regional site with higher data volumes and local recording |

- Upstream bandwidth is the binding constraint for real-time media; asymmetric access services must be sized on the upstream figure.
- The class assignment per site is recorded in the design document and confirmed against the site survey.

## Quantities

- Sites in scope: {{site_count}}
- Quantity basis: {{devicex_qty_note}}
<!-- endif -->

## Central Management Infrastructure <!-- if devicex -->

<!-- if devicex -->
Virtual machines at the central site for the DeviceX central management components:

| Role | Specification | Quantity |
| :--- | :--- | :--- |
| Hub | 12 vCPU, 32 GB memory, 150 GB disk | 1 |
| Backend | 4 vCPU, 12 GB memory, 250 GB disk | 3 |
| Management console | 4 vCPU, 8 GB memory, 250 GB disk | 1 |
| Load balancer for the backend | HTTPS load balancing with a TLS certificate for the console and backend addresses | 1 |
<!-- endif -->

## StackX Platform Infrastructure <!-- if stackx -->

<!-- if stackx -->
Virtual machines for the StackX components in scope. Sizing is indicative and confirmed during the design stage against data volumes and retention:

| Component | Indicative sizing |
| :--- | :--- |
| Network monitoring — application, interface and database components | 2 nodes each × 4 vCPU / 4–8 GB RAM / 30–50 GB SSD <!-- if module_stackx_network_ops --> |
| Log and event platform — data nodes | 2 nodes × 16 vCPU / 64 GB RAM / 3.75 TB SSD <!-- if module_stackx_event_log_mgmt or module_stackx_security or module_stackx_observability_apm --> |
| Log and event platform — master nodes | 3 nodes × 8 vCPU / 16 GB RAM / 250 GB SSD <!-- if module_stackx_event_log_mgmt or module_stackx_security or module_stackx_observability_apm --> |
| Log and event platform — visualization, agent management and ingest nodes | 4 nodes × 8 vCPU / 16 GB RAM / 250 GB SSD <!-- if module_stackx_event_log_mgmt or module_stackx_security or module_stackx_observability_apm --> |
| Application performance monitoring node | 1 node × 8 vCPU / 16 GB RAM / 250 GB SSD <!-- if module_stackx_observability_apm --> |
| Endpoint management node | 1 node × 32 vCPU / 128 GB RAM / 1 TB SSD <!-- if module_stackx_endpoint_mgmt --> |
| Automation and orchestration node | 1 node × 32 vCPU / 128 GB RAM / 1 TB SSD <!-- if module_stackx_automation_orchestration --> |
| Service management nodes | 6 nodes × 4 vCPU / 16 GB RAM / 50 GB SSD <!-- if module_stackx_itSM --> |
<!-- endif -->

*[Sizing is indicative. Final sizing depends on the number of monitored devices, event and log volumes, retention periods and user counts, and is confirmed in the design document.]*

## Site and Data Center Requirements

The environment must meet the following before deployment:

- Rack space and mounting for the appliances at each site in scope <!-- if devicex -->
- Power at each site, with a protected supply for the appliance <!-- if devicex -->
- Power and cooling at the central site sized for the virtual infrastructure above
- Redundant power feed and redundant network connectivity at the central site
- Stable internet or WAN access at each site, at or above the class bandwidth stated above <!-- if devicex -->
- Stable network connectivity between the monitored estate and the StackX platform <!-- if stackx -->
- Physical security for the equipment rooms housing the appliances and central infrastructure
- Structured cabling and switch ports for the interfaces listed in the specifications
- Virtualization capacity, storage and backup for the virtual machines listed above
- Time synchronization and name resolution available to every deployed component
- Network paths and firewall rules for the flows documented in the design

*[Confirm quantities, power and rack details against the site survey before issue.]*

---

*This section is reusable product and sizing data. Keep specifications current with the Verto Wave product team.*
