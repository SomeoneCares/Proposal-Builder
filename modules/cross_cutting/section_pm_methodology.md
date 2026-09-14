# Project Management Methodology

**Token:** `{{section_pm_methodology}}`  
**Group:** Cross-Cutting  
**Required:** Yes

---

## Overview

The Verto Wave project management methodology has five stages, mapped to the PMI project management process groups. A RAID log (risks, actions, issues and decisions) is maintained throughout the project.

| PMI Process Group | Verto Wave Project Stage |
| :--- | :--- |
| Initiating | Envisioning |
| Planning | Designing and Planning |
| Executing | Building (deployment, stabilization and testing) |
| Monitoring and Controlling | Monitoring and Controlling |
| Closing | Closure |

<!-- Diagram guidance: the five stages as a left-to-right flow, with Monitoring and Controlling spanning underneath. -->
[[figure: pm-stages | Verto Wave project management stages]]

## Project Stages

### Envisioning

The project is formally approved and assigned to a project manager and technical lead. The project charter is developed and the key stakeholders are identified. A series of technical workshops establishes what is already in place at {{customer_short}} and aligns stakeholders with the project's objectives, constraints and timeline.

### Designing and Planning

The project plan is developed and the timeframe and risks are evaluated. The plan is used to monitor project performance throughout the lifecycle. The key outcomes are a confirmed scope document with the detailed scope of work, and confirmed project management deliverables.

### Building

The work defined in the approved project plan is carried out, coordinating all resources so the project keeps delivering its objectives. Deliverables are built, tested and stabilized in line with the plan. Only changes approved by the steering committee or change control board are implemented.

### Monitoring and Controlling

Project work is tracked and reviewed throughout all stages to regulate progress and performance, identify where the plan must change, and initiate those changes. The RAID log records:

- **Risks** — potential challenges, their causes and effects, and the mitigation strategy
- **Actions** — planned tasks, their owners and timelines
- **Issues** — problems encountered, how they arose and how they were resolved
- **Decisions** — choices made, by whom and when

### Closure

The project is completed and authorized by {{customer_short}}'s designated authority. The handover and acceptance activities defined in the scope documentation are carried out, and the solution is handed over to {{customer_short}}.

## Delivery Phasing

The stages above describe how the project is managed; the phasing below describes how delivery is sequenced. The central platform is proven before site roll-out begins, and the first site validates the model end to end before the remaining sites are delivered in parallel. <!-- if devicex -->

| Phase | Focus | Key outcomes |
| :--- | :--- | :--- |
| Envisioning and design | Requirements gathered, site profiles and classes assigned, traffic and security models agreed, design signed off | Signed-off design document and hardware forecast |
| Core build | Central platform components built, integrated and validated | Central platform in service and validated |
| Pilot | First site provisioned through zero-touch provisioning and validated against the service-quality targets | Site template hardened from real-world findings <!-- if devicex --> |
| Parallel roll-out | Remaining sites deployed from the hardened template, each closed with the standard acceptance test | All sites accepted <!-- if devicex --> |
| StackX implementation | StackX modules configured, integrated with {{customer_short}}'s systems and tested | StackX modules accepted <!-- if stackx --> |
| Training and handover | Administration training, documentation and operational handover | Training delivered and handover pack issued <!-- if section_training --> |
| Managed operations | Managed operations start under the Operations Level Agreement | Operations running under the OLA <!-- if managed_services --> |

## Deliverables by Phase

| Phase | Deliverables |
| :--- | :--- |
| Envisioning and design | Design document for each solution; security baseline; configuration and policy design |
| Envisioning and design | Site profile and class assignment per site; traffic classification, QoS and segmentation model; access service validation record per site <!-- if devicex --> |
| Envisioning and design | Numbering plan and call-flow design <!-- if module_ipbx or module_stackx_call_center --> |
| Build | Implemented and validated solution; as-built documentation |
| Build | Per-site acceptance test record <!-- if devicex --> |
| Training and handover | Training delivered; training documentation and recorded session; operational handover pack <!-- if section_training --> |
| Managed operations | Operations reports and enhancement recommendations <!-- if managed_services --> |

---

*This section is a reusable building block. Confirm stage gating, milestone definitions and the RAID review cadence per bid.*
