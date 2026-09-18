# Professional Services — Architecture, Design, Implementation and Roll-out

**Token:** `{{section_professional_services}}`  
**Group:** Cross-Cutting  
**Required:** Yes

---

## Overview

This section defines the professional services for the architecture, design, implementation and roll-out of the selected solution. The scope is quantified: every figure below bounds the work, and each in-scope line has a matching out-of-scope boundary.

*[Author per bid: fill every scope number in the proposal values with the figures confirmed for this engagement. Do not carry numbers forward from a prior engagement.]*

## Scope Numbers

| # | Dimension | Confirmed figure |
| :--- | :--- | :--- |
| 1 | Branches / sites | {{services_branches}} <!-- if devicex --> |
| 2 | Network devices to be monitored | {{services_network_devices}} <!-- if module_stackx_network_ops or module_sdx_operations or product_ot_nom --> |
| 3 | Applications to be monitored | {{services_apps_monitored}} <!-- if module_stackx_observability_apm or module_stackx_trueview or product_el_apm --> |
| 4 | Automation and orchestration workflows | {{services_workflows}} <!-- if module_stackx_automation_orchestration or product_ot_oo --> |
| 5 | Endpoints to roll out | {{services_endpoints}} <!-- if module_stackx_endpoint_mgmt --> |
| 6 | NVR cameras | {{services_nvr_cameras}} <!-- if module_nvr --> |
| 7 | IoT devices | {{services_iot_devices}} <!-- if devicex --> |
| 8 | SD-WAN tunnels / overlay connections | {{services_tunnels}} <!-- if module_sdwan --> |
| 9 | Firewall policies | {{services_firewall_policies}} <!-- if module_firewall --> |
| 10 | PBX extensions | {{services_pbx_extensions}} <!-- if module_ipbx --> |
| 11 | Virtualization workloads | {{services_virtualization_workloads}} <!-- if module_virtualization or module_business_workloads --> |
| 12 | Service catalog items and request workflows | {{services_catalog_items}} <!-- if product_ot_smax -->
| 13 | Discovery sources for the configuration model | {{services_discovery_sources}} <!-- if product_ot_ucmdb -->
| 14 | Configuration item classes in scope | {{services_ci_classes}} <!-- if product_ot_ucmdb -->
| 15 | Event sources to be integrated | {{services_event_sources}} <!-- if product_ot_obm -->
| 16 | Hosts and services to be instrumented | {{services_monitored_hosts}} <!-- if product_el_observability -->
| 17 | Log sources to be onboarded | {{services_log_sources}} <!-- if product_el_logs -->
| 18 | Integration points | {{services_integrations}} |
| 19 | User personas / roles | {{services_roles}} |
| 20 | Training attendees | {{services_training_attendees}} <!-- if section_training --> |
| 21 | Training sessions | {{services_training_sessions}} <!-- if section_training --> |
| 22 | Acceptance-test sites | {{services_acceptance_sites}} <!-- if devicex --> |
| 23 | Architecture and design workshops | {{services_arch_workshops}} |
| 24 | Architecture diagrams to be produced | {{services_arch_diagrams}} |

## Phase 1 — Architecture

### In Scope

- Conduct {{services_arch_workshops}} architecture and envisioning workshops.
- Produce a high-level architecture design covering {{services_branches}} sites. <!-- if devicex -->
- Produce the monitoring architecture covering {{services_apps_monitored}} applications. <!-- if module_stackx_observability_apm or module_stackx_trueview -->
- Produce the network monitoring architecture covering {{services_network_devices}} network devices. <!-- if module_stackx_network_ops or module_sdx_operations or product_ot_nom -->
- Produce the automation and orchestration framework design for {{services_workflows}} workflows. <!-- if module_stackx_automation_orchestration or product_ot_oo -->
- Produce the endpoint roll-out architecture for {{services_endpoints}} endpoints. <!-- if module_stackx_endpoint_mgmt -->
- Produce the NVR architecture for {{services_nvr_cameras}} cameras. <!-- if module_nvr -->
- Produce the IoT device integration architecture for {{services_iot_devices}} devices. <!-- if devicex -->
- Produce the SD-WAN overlay topology for {{services_tunnels}} tunnels. <!-- if module_sdwan -->
- Produce the firewall policy architecture for {{services_firewall_policies}} policies. <!-- if module_firewall -->
- Produce the numbering plan and call-flow design for {{services_pbx_extensions}} extensions. <!-- if module_ipbx -->
- Produce the workload architecture for {{services_virtualization_workloads}} workloads. <!-- if module_virtualization or module_business_workloads -->
- Produce the service management architecture, covering the process model and {{services_catalog_items}} catalog items and request workflows. <!-- if product_ot_smax -->
- Produce the configuration model design, covering {{services_ci_classes}} configuration item classes and {{services_discovery_sources}} discovery sources. <!-- if product_ot_ucmdb -->
- Produce the event management and correlation architecture for {{services_event_sources}} event sources. <!-- if product_ot_obm -->
- Produce the observability architecture for {{services_monitored_hosts}} hosts and services. <!-- if product_el_observability -->
- Produce the log collection architecture for {{services_log_sources}} log sources, with the retention and storage tiers. <!-- if product_el_logs -->
- Produce the application performance monitoring architecture for {{services_apps_monitored}} applications. <!-- if product_el_apm -->
- Produce the integration design for {{services_integrations}} integration points.
- Produce the role and access model for {{services_roles}} roles.
- Produce {{services_arch_diagrams}} architecture diagrams.
- Hold an architecture review and obtain sign-off.

### Out of Scope

- Any architecture, design, diagram or review not listed above.
- Detailed design (Phase 2) and implementation (Phase 3).
- The architecture of {{customer_short}}'s business applications.

### Deliverables

- Architecture design document with {{services_arch_diagrams}} architecture diagrams.
- Architecture review sign-off record.

## Phase 2 — Design

### In Scope

- Produce the detailed design for {{services_branches}} sites. <!-- if devicex -->
- Produce the detailed monitoring design for {{services_apps_monitored}} applications. <!-- if module_stackx_observability_apm or module_stackx_trueview -->
- Produce the detailed network monitoring design for {{services_network_devices}} network devices. <!-- if module_stackx_network_ops or module_sdx_operations or product_ot_nom -->
- Produce the detailed automation and orchestration design for {{services_workflows}} workflows. <!-- if module_stackx_automation_orchestration or product_ot_oo -->
- Produce the detailed endpoint roll-out design for {{services_endpoints}} endpoints. <!-- if module_stackx_endpoint_mgmt -->
- Produce the detailed NVR design for {{services_nvr_cameras}} cameras. <!-- if module_nvr -->
- Produce the detailed IoT design for {{services_iot_devices}} devices. <!-- if devicex -->
- Produce the detailed SD-WAN design for {{services_tunnels}} tunnels. <!-- if module_sdwan -->
- Produce the detailed firewall design for {{services_firewall_policies}} policies. <!-- if module_firewall -->
- Produce the detailed PBX design for {{services_pbx_extensions}} extensions. <!-- if module_ipbx -->
- Produce the detailed workload design for {{services_virtualization_workloads}} workloads. <!-- if module_virtualization or module_business_workloads -->
- Produce the detailed service management design: process configuration, {{services_catalog_items}} catalog items and request workflows, and the approval and notification rules. <!-- if product_ot_smax -->
- Produce the detailed discovery design: {{services_discovery_sources}} discovery sources, credentials, schedules and the reconciliation rules for {{services_ci_classes}} configuration item classes. <!-- if product_ot_ucmdb -->
- Produce the detailed event design: collection from {{services_event_sources}} event sources, correlation and de-duplication rules, and the alert routing model. <!-- if product_ot_obm -->
- Produce the detailed observability design for {{services_monitored_hosts}} hosts and services: agent policies, dashboards and alerting rules. <!-- if product_el_observability -->
- Produce the detailed log pipeline design for {{services_log_sources}} log sources: parsing, enrichment, index lifecycle and retention tiers. <!-- if product_el_logs -->
- Produce the detailed instrumentation design for {{services_apps_monitored}} applications, with the sampling and service dependency model. <!-- if product_el_apm -->
- Produce the detailed design for {{services_integrations}} integrations and the access design for {{services_roles}} roles.
- Produce configuration and policy design documents per component.

### Out of Scope

- Any detailed design, configuration or policy document not listed above.
- Implementation (Phase 3), and design changes to the existing environment.

### Deliverables

- Detailed design documents per site and per component; configuration, policy and integration design documents.
- Design sign-off record.

## Phase 3 — Implementation and Roll-out

### In Scope

- Implement and roll out the design across {{services_branches}} sites. <!-- if devicex -->
- Deploy monitoring for {{services_apps_monitored}} applications. <!-- if module_stackx_observability_apm or module_stackx_trueview -->
- Deploy network monitoring for {{services_network_devices}} network devices. <!-- if module_stackx_network_ops or module_sdx_operations or product_ot_nom -->
- Implement {{services_workflows}} automation and orchestration workflows. <!-- if module_stackx_automation_orchestration or product_ot_oo -->
- Roll out {{services_endpoints}} endpoints. <!-- if module_stackx_endpoint_mgmt -->
- Deploy NVR for {{services_nvr_cameras}} cameras. <!-- if module_nvr -->
- Integrate {{services_iot_devices}} IoT devices. <!-- if devicex -->
- Deploy the SD-WAN overlay for {{services_tunnels}} tunnels. <!-- if module_sdwan -->
- Implement {{services_firewall_policies}} firewall policies. <!-- if module_firewall -->
- Deploy the PBX for {{services_pbx_extensions}} extensions. <!-- if module_ipbx -->
- Deploy {{services_virtualization_workloads}} workloads. <!-- if module_virtualization or module_business_workloads -->
- Deploy the service management platform and configure {{services_catalog_items}} catalog items and request workflows. <!-- if product_ot_smax -->
- Deploy discovery, onboard {{services_discovery_sources}} discovery sources and populate {{services_ci_classes}} configuration item classes. <!-- if product_ot_ucmdb -->
- Integrate {{services_event_sources}} event sources and implement the correlation and routing rules. <!-- if product_ot_obm -->
- Instrument {{services_monitored_hosts}} hosts and services, and publish the agreed dashboards and alerts. <!-- if product_el_observability -->
- Onboard {{services_log_sources}} log sources and apply the parsing, enrichment and retention configuration. <!-- if product_el_logs -->
- Instrument {{services_apps_monitored}} applications and publish the trace and service dependency views. <!-- if product_el_apm -->
- Implement {{services_integrations}} integrations and the access model for {{services_roles}} roles.
- Test and validate each component and site.
- Execute acceptance testing at {{services_acceptance_sites}} sites. <!-- if devicex -->

### Out of Scope

- Any implementation, deployment, roll-out, testing or validation not listed above.
- The general exclusions in the Out-of-Scope Activities section.

### Deliverables

- Implemented and validated solution; test and validation reports.
- Acceptance test records for {{services_acceptance_sites}} sites. <!-- if devicex -->
- As-built documentation.


[[figure: services-scope-overview | Scope at a glance]]

## Acceptance

Each phase is accepted against the acceptance criteria agreed in the design stage. Acceptance tests are executed jointly, and the signed acceptance record closes the phase or site.

## Professional Services Assumptions

- The figures in the scope-numbers table are confirmed in the design stage and bound the work.
- Architecture is signed off before detailed design begins, and detailed design is signed off before implementation begins.
- Implementation is performed remotely; on-site work is added only by change request.

---

*Include this section when professional services are part of the offering. Fill every scope number per bid.*
