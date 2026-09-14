# StackX Network Operations

**Token:** `{{module_stackx_network_ops}}`  
**Group:** StackX — Control / Orchestration / SOC / Operations Layer  
**Required:** No (optional module)

---

## Overview

StackX Network Operations brings network fault, availability, performance and service monitoring into a single operations console. Continuous discovery, a single polling engine and common causal analysis keep administrative overhead low, while workflow-based navigation helps the network team move quickly from an alert to its cause.

It manages physical, virtual, hybrid and cloud network environments, and extends to a wide range of devices, services and protocols.

## Key Capabilities

- **Continuous discovery and monitoring** — the network topology is discovered and kept current automatically.
- **Unified polling** — one correlated, optimized polling engine and a single configuration point.
- **Root-cause analysis** — service-impacting incidents are identified in the context of the network topology, rather than as isolated alarms.
- **Workflow-based navigation** — a network-wide status view with drill-down to device, component and incident detail.
- **Path health** — traffic trends and congestion analysis, bottleneck isolation and synthetic path tests.
- **Performance monitoring** — interface and component health, flow records and service-level quality, with incidents raised from static or adaptive thresholds and dynamically calculated baselines.
- **Configuration and compliance** — configuration changes are correlated with performance, so a degradation caused by a new configuration is visible immediately.
- **Multi-tenancy** — node, user and security groups partition the network logically.
- **Regional scale** — global and regional managers consolidate information across locations.

<!-- Diagram guidance: live network topology with health status, traffic heatmap and a drill-down from an incident to the affected interface. No device names or addressing. -->
[[figure: network-operations | Network operations console and topology]]

## Reporting and Dashboards

- Performance reports scheduled and shared with stakeholders
- Traffic reporting by interface, with drill-down to top applications and conversations
- Time filters that let teams correlate events across panels
- Usage trend and forecast reports for capacity planning

## Value

- Lower mean time to resolution through topology-aware root-cause analysis
- Fewer outages caused by configuration errors, because changes are correlated with their impact
- One tool for fault, performance and configuration, instead of separate consoles

## Integration

- Monitors the DeviceX appliances and overlay alongside the rest of the network. <!-- if devicex -->
- Raises incidents automatically in StackX ITSM. <!-- if module_stackx_itSM -->
- Shares network topology with the CMDB. <!-- if module_stackx_ops_config_mgmt -->

---

*This module is a reusable building block. Confirm the number and types of devices to be monitored per bid.*
