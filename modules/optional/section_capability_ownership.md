# Capability Ownership

**Token:** `{{section_capability_ownership}}`  
**Group:** Optional Sections  
**Required:** No

---

Several capabilities in this proposal could plausibly be delivered by more than one component. Each is owned by exactly one, and the others consume it. {{customer_short}} therefore reads each capability once and pays for it once, and there is no ambiguity about which component is accountable when it fails.

Only the components selected for this proposal appear below.

[[figure: capability-ownership | Which component owns which capability | Diagram | Architect]]

## Platform Boundary <!-- if devicex and stackx -->

<!-- if devicex and stackx -->
The edge platform enforces; the operations platform observes, records and governs.

| Capability | Edge Platform | Operations Platform |
| :--- | :--- | :--- |
| Connectivity and overlay | Establishes and steers the encrypted overlay at each site. | Monitors path health, utilization and alarm state across the estate. |
| Security enforcement | Enforces firewall policy, filtering and segmentation at the site. | Detects, correlates and investigates security events. <!-- if module_stackx_security --> |
| Configuration | Applies the agreed template to the appliance. | Authors, versions, pushes and audits the template. <!-- if module_stackx_automation_orchestration --> |
| Appliance health | Reports its own health and attestation state. | The single source of truth for appliance and network health. <!-- if module_stackx_network_ops --> |
| Workload hosting | Hosts the agreed workloads on reserved capacity. <!-- if module_virtualization or module_business_workloads --> | Monitors workload performance and collects their logs. <!-- if module_stackx_observability_apm --> |
| Surveillance | Records, retains and analyzes video at the site. <!-- if module_nvr --> | Receives alerts, tracks recorder health and holds the audit record. <!-- if module_nvr and module_stackx_network_ops --> |
| Logs | Emits logs. | Collects and retains them. <!-- if module_stackx_event_log_mgmt --> |
| Incidents | Generates the event. | Creates, assigns, tracks and closes the ticket. <!-- if module_stackx_itSM --> |
<!-- endif -->

## Shared Capabilities <!-- if stackx -->

<!-- if stackx -->
Within the operations platform, each shared capability has one owning module. Where that module is not part of this proposal, the fallback column states what happens instead, so no capability is assumed to be present when it has not been sold.

| Capability | Owner In This Proposal | Where It Is Not Selected |
| :--- | :--- | :--- |
| Cross-domain event consolidation and correlation | Operations Monitoring and Configuration Management <!-- if module_stackx_ops_config_mgmt --> | Each domain correlates its own events; there is no single cross-domain view. <!-- if not module_stackx_ops_config_mgmt --> |
| Configuration record and service model | Operations Monitoring and Configuration Management <!-- if module_stackx_ops_config_mgmt --> | The service desk holds a manually maintained asset register. <!-- if not module_stackx_ops_config_mgmt --> |
| Change and release record | Service management <!-- if module_stackx_itSM --> | Each delivery pipeline keeps its own record. <!-- if not module_stackx_itSM --> |
| Network and appliance health | Network operations <!-- if module_stackx_network_ops --> | Health is reported per component without a consolidated view. <!-- if not module_stackx_network_ops --> |
| Log collection and retention | Event and log management <!-- if module_stackx_event_log_mgmt --> | Logs remain on their source systems under their own retention. <!-- if not module_stackx_event_log_mgmt --> |
| Security correlation and detection | Security operations <!-- if module_stackx_security --> | Not in scope; log data is collected but not correlated for detection. <!-- if not module_stackx_security --> |
| Identity lifecycle, single sign-on and multi-factor authentication | Identity management <!-- if module_stackx_idm --> | Each platform uses {{customer_short}}'s existing directory directly. <!-- if not module_stackx_idm --> |
| Privileged access and session recording | Operations integrity <!-- if module_stackx_ops_integrity --> | Available as an extended security service, quoted separately. <!-- if not module_stackx_ops_integrity --> |
| Vulnerability and configuration assessment | Compliance assurance <!-- if module_stackx_compliance --> | Not in scope; assessment remains with {{customer_short}}. <!-- if not module_stackx_compliance --> |
| Backup and recovery | Backup <!-- if module_stackx_backup --> | Backup of the delivered platform remains {{customer_short}}'s responsibility. <!-- if not module_stackx_backup --> |
<!-- endif -->

## Third-Party Products <!-- if opentext or elastic -->

<!-- if opentext or elastic -->
Where a third-party product delivers a capability that a platform module could also deliver, the design records which one is in scope so the function is built once.

| Capability | Owner In This Proposal |
| :--- | :--- |
| Service management and the service catalog | The third-party service management platform. <!-- if product_ot_smax and not module_stackx_itSM --> |
| Service management and the service catalog | Agreed in design; both a platform module and a third-party product are in scope. <!-- if product_ot_smax and module_stackx_itSM --> |
| Configuration record and discovery | The third-party discovery platform. <!-- if product_ot_ucmdb and not module_stackx_ops_config_mgmt --> |
| Event correlation | The third-party event platform. <!-- if product_ot_obm --> |
| Network fault and performance monitoring | Agreed in design; one platform polls each device. <!-- if product_ot_nom and module_stackx_network_ops --> |
| Runbook automation | Agreed in design, split by domain. <!-- if product_ot_oo and module_stackx_automation_orchestration --> |
| Log collection and retention | The third-party log platform. <!-- if product_el_logs and not module_stackx_event_log_mgmt --> |
| Infrastructure and application monitoring | The third-party observability platform. <!-- if product_el_observability or product_el_apm --> |

*[Confirm each overlapping capability with the product team before issue, and delete any row that does not apply to this bid.]*
<!-- endif -->

---

*Include this section wherever two or more components could deliver the same capability. It exists to stop a capability being sold, described or priced twice.*
