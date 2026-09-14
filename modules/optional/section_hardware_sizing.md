# DeviceX Hardware Specifications and Sizing

**Token:** `{{section_hardware_sizing}}`  
**Group:** Optional Proposal Sections  
**Required:** No

---

## DeviceX Appliance Specifications

DeviceX appliances are standard Verto Wave hardware running the SDX platform. Every class runs the complete module set; the class determines capacity, not capability.

| Reference configuration | Processor | Memory | Storage | Network interfaces |
| :--- | :--- | :--- | :--- | :--- |
| DeviceX Mid-Range | Multi-core x86 processor | 64 GB DDR4 | 2 × 4 TB SATA and 2 × 256 GB NVMe | 8 × 1 GbE RJ45 and 2 × 10 GbE SFP+ |
| DeviceX High-Capacity | 24-core server-class x86 processor | 128 GB | 512 GB SSD and 2 TB HDD | 8 × 1 GbE and 4 × 10 GbE, with 4G/5G connectivity |

*[Confirm the current model names and specifications with the Verto Wave product team before issue. Specifications are indicative and may be superseded by equivalent or higher configurations.]*

## Site Sizing Classes

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

## Central Management Infrastructure

The DeviceX central management components run on virtual machines provided by {{customer_short}} at the central site:

| Role | Specification | Quantity |
| :--- | :--- | :--- |
| Hub | 12 vCPU, 32 GB memory, 150 GB disk | 1 |
| Backend | 4 vCPU, 12 GB memory, 250 GB disk | 3 |
| Management console | 4 vCPU, 8 GB memory, 250 GB disk | 1 |
| Load balancer for the backend | HTTPS load balancing with a TLS certificate for the console and backend addresses | 1 |

## StackX Platform Infrastructure <!-- if stackx -->

<!-- if stackx -->
Indicative sizing for the StackX components in scope, confirmed during the design stage against data volumes and retention:

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

---

*This section is reusable product and sizing data. Keep specifications current with the Verto Wave product team.*
