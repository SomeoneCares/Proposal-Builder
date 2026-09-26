# Business Workloads Hosting Platform

**Token:** `{{module_business_workloads}}`  
**Group:** DeviceX/SDX — Edge & Branch Layer  
**Required:** No (optional add-on)

---

## Solution Overview

The DeviceX business workloads hosting platform runs {{customer_short}}'s business-critical applications and services on managed infrastructure, with monitoring, protection and room to grow — so application teams can focus on the application rather than the infrastructure beneath it.

## Platform Capabilities

- Managed infrastructure for business-critical applications
- Advanced monitoring and management of hosted workloads
- Scalability to meet growing demand
- High availability and performance assurance
- Protection of hosted workloads

## Build Activities

- Create the required virtual machines according to the design
- Configure monitoring and management of the hosted workloads in the backend infrastructure

<!-- Diagram guidance: application and data tiers hosted on the platform with their integration points; no application names or data classifications. -->
[[figure: business-workloads | Business workload placement | Diagram | Architect]]
<!-- if per_product_sizing -->

## Sizing Basis

| Dimension | Counted As | Confirmed Figure |
| :--- | :--- | :--- |
| Hosted applications | Business applications running at the edge | {{sizing_business_workloads_hosted_applications}} |
| Workload footprint | vCPU, RAM and storage per application | {{sizing_business_workloads_workload_footprint}} |
| Sites hosting workloads | Sites where the applications run | {{sizing_business_workloads_sites_hosting}} |

*[Confirm every figure for this bid against the confirmed requirement. Do not carry numbers forward from a prior engagement.]*

<!-- endif -->

<!-- if services -->

## Acceptance Tests

The tests below are executed jointly and form part of the acceptance test plan for this module.

| Test | Method | Pass Criterion |
| :--- | :--- | :--- |
| Provisioning | Deploy the agreed applications from template | Running within the agreed footprint |
| Isolation | Attempt to reach the management zone from a workload | Blocked and logged |
| Survivability | Disconnect the wide-area link | Application continues to serve local users |

<!-- endif -->

---

*This module is a reusable building block. Include it when business workload hosting is in scope for the current engagement.*
