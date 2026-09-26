# Virtualization / Container Platform

**Token:** `{{module_virtualization}}`  
**Group:** DeviceX/SDX — Edge & Branch Layer  
**Required:** No (optional add-on)

---

## Solution Overview

The DeviceX virtualization and container platform runs virtual machines and containers at the site edge, so {{customer_short}} can consolidate site workloads onto the appliance instead of separate compute hardware.

## Platform Capabilities

- Hypervisor-based virtual machine hosting
- Container deployment and management
- Container orchestration
- Multi-tenant workload isolation
- Resource allocation and scaling
- Application lifecycle management
- Load balancing and service discovery
- Persistent storage management
- Network policy enforcement
- Monitoring and logging integration

## Continuity by Design

The platform can host local copies of key workloads — application front ends, document viewers, directory services and similar — so a site remains functional through a wide-area outage. The number of workloads per site is a design input: a small site does not carry capacity it does not use, and capacity can be added later without redesign.

<!-- Diagram guidance: the appliance's hypervisor with VMs and containers alongside the network functions; workload count per site shown as N. -->
[[figure: virtualization-stack | Workloads hosted on the DeviceX appliance | Product photo | Marketing]]
## Value to Sites

The compact, low-power appliance needs minimal space and cooling, and only the required functions are enabled, which suits space-constrained sites.

<!-- if per_product_sizing -->

## Sizing Basis

| Dimension | Counted As | Confirmed Figure |
| :--- | :--- | :--- |
| Hosted workloads | Virtual machines and containers per site | {{sizing_virtualization_hosted_workloads}} |
| Workload allowance | vCPU and RAM reserved for workloads per site | {{sizing_virtualization_workload_allowance}} |
| Persistent storage | Storage allocated to workloads per site | {{sizing_virtualization_persistent_storage}} |

*[Confirm every figure for this bid against the confirmed requirement. Do not carry numbers forward from a prior engagement.]*

<!-- endif -->

<!-- if services -->

## Acceptance Tests

The tests below are executed jointly and form part of the acceptance test plan for this module.

| Test | Method | Pass Criterion |
| :--- | :--- | :--- |
| Provisioning | Create the agreed VMs from template | VMs running with reserved resources |
| Isolation | Workload attempts to reach management zone | Blocked |

<!-- endif -->

---

*This module is a reusable building block. Define the workload set, capacity and continuity scope against the current RFP/ITB.*
