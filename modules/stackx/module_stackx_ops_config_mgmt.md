# StackX Operations Monitoring & Configuration Management

**Token:** `{{module_stackx_ops_config_mgmt}}`  
**Group:** StackX — Control / Orchestration / SOC / Operations Layer  
**Required:** No (optional module)

---

## Overview

This module combines two foundations of IT operations: an accurate, automatically maintained configuration management database (CMDB), and consolidated operations monitoring that turns events from every tool into one managed view.

## Configuration Management

### Automated Discovery and Dependency Mapping

StackX discovery combines automated inventory discovery with dependency mapping. It explores assets and configuration items (CIs) from layer 2 to layer 7 of the OSI model and maps the relationships between them, providing the basis for understanding the services IT delivers — from the physical data center to the business process.

Discovery patterns capture:

- Applications and their components, including custom and legacy applications
- Database components such as tablespaces, users and jobs
- Servers and their resources: CPUs, memory, network interfaces and storage
- Network devices: routers, switches, load balancers, ports, VLANs and firewalls
- Storage arrays, logical disks and storage-network connectivity
- Virtualization platforms, including virtual file systems, disks, network interfaces and management servers
- PCs, laptops and printers
- Private and public cloud resources
- Mainframe and midrange system attributes
- The relationships between all of the above

### Automated Service Modeling

Starting from a service's entry point, such as its URL, StackX discovers the business service top-down and builds a service model that updates automatically as the environment changes. Teams can then view the layers they need — application, infrastructure or network — for each service.

### A Foundation for Configuration Management

The CMDB federates core CI data with related data held elsewhere, so information is shared across the IT ecosystem without copying it. Continuous discovery keeps the CMDB accurate, which supports faster incident diagnosis, change impact assessment and asset management.

<!-- Diagram guidance: discovery feeding the CMDB and service model; events from monitoring tools consolidated into one console with correlation and dashboards. -->
[[figure: cmdb-operations | Discovery, CMDB and consolidated operations | Diagram | Architect]]
## Operations Monitoring

Operations monitoring plays two roles. It monitors servers and applications, using agent and agentless methods to collect performance metrics and faults from hardware, operating systems, processes, databases and applications. It also acts as a manager of managers, consolidating events from its own monitoring and from other tools for event management, correlation and dashboards.

- **Secure agents** — HTTPS communication with server and client certificates, and a reverse-channel proxy for sites that are less trusted than the central site.
- **Extensibility** — open interfaces and management packs extend monitoring to virtually any component.
- **Consistency** — management policies are created once and deployed consistently across a heterogeneous estate.
- **Low overhead** — agents run with minimal impact on system resources.
- **Event correlation** — topology-based correlation reduces event noise to the incidents that matter.
- **Hybrid monitoring** — traditional, private and public cloud infrastructure monitored from one console.
- **Cross-domain reporting** — reports and dashboards built from the live service model.

## Value

- Faster diagnosis, because incidents are shown in the context of the services and components they affect
- Less time lost switching between consoles, with one view of events, metrics and topology
- More reliable changes, because impact is assessed against an accurate CMDB

## Integration

- Provides CI and service context to StackX ITSM for incident, problem and change management. <!-- if module_stackx_itSM -->
- Supplies the service model to StackX TrueView dashboards. <!-- if module_stackx_trueview -->
- Hands events to StackX Automation & Orchestration for automated remediation. <!-- if module_stackx_automation_orchestration -->

<!-- if per_product_sizing -->

## Sizing Basis

| Dimension | Counted As | Confirmed Figure |
| :--- | :--- | :--- |
| Discovery ranges | IP ranges / cloud accounts | {{sizing_stackx_ops_config_mgmt_discovery_ranges}} |
| CIs | Expected CIs | {{sizing_stackx_ops_config_mgmt_cis}} |
| Monitored servers | Agent / agentless | {{sizing_stackx_ops_config_mgmt_monitored_servers}} |
| Event sources | Third-party tools integrated | {{sizing_stackx_ops_config_mgmt_event_sources}} |
| Services modelled | Top-down service models | {{sizing_stackx_ops_config_mgmt_services_modelled}} |

*[Confirm every figure for this bid against the confirmed requirement. Do not carry numbers forward from a prior engagement.]*

<!-- endif -->

<!-- if services -->

## Acceptance Tests

The tests below are executed jointly and form part of the acceptance test plan for this module.

| Test | Method | Pass Criterion |
| :--- | :--- | :--- |
| Discovery coverage | Run discovery on agreed ranges | ≥ 95 % of in-scope ranges discovered |
| CMDB quality | Duplicate CI report | < 2 % duplicate CIs |
| Correlation | Fail an upstream device in test | One correlated event, not one per downstream CI |

<!-- endif -->

---

*This module is a reusable building block. Confirm the discovery scope, monitored domains and event sources per bid.*
