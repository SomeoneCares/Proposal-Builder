"""
Insert image-placement guidance blocks at the center of each module .md file.
Guidance blocks are module-specific where we know the right image; otherwise generic.
Preserves all existing content — only inserts a block at the center.
"""

import re
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
MODULES_DIR = SKILL_ROOT / "modules"

# Module-specific image-placement guidance.
# Key = module file path relative to MODULES_DIR (e.g. "devicex/module_sdwan.md").
# Value = guidance block text to insert at center.
GUIDANCE = {
    # ---- DeviceX/SDX ----
    "devicex/module_sdwan.md": """---

## Figure — SD-WAN Architecture (Hub-and-Spoke / Mesh Overlay)

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic SD-WAN topology showing a central hub (or dual hubs) with multiple remote/branch sites connected over an encrypted overlay, with diverse underlays (fiber, DSL, cellular) converging at each site. Transport-agnostic — no carrier branding, no customer site names, no customer-specific IP addressing. -->
<!-- Suggested source: Telemedicine proposal §3.1 / §3.2 (architecture tiers + SD-WAN architecture) — reuse only the generic topology/fabric shape; strip any "clinic", "Dubai", or site-name labels before use. -->
<!-- Alternative: a path-diversity / quality-based steering decision diagram showing primary path, standby underlay, and steering logic (latency/jitter/loss thresholds). -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic SD-WAN architecture / path-diversity diagram here. See image-placement guidance notes.]*

---""",

    "devicex/module_firewall.md": """---

## Figure — Firewall Security Zones / In-Site Micro-Segmentation

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic in-site micro-segmentation diagram showing distinct security zones (e.g. untrusted/guest, user/application, peripheral/device, surveillance/camera, voice, management) with explicit allow-list boundaries and no unwanted egress between zones. No customer-specific device names, no customer site names, no customer IP addressing. -->
<!-- Suggested source: Telemedicine proposal §4.3.3 (in-clinic micro-segmentation, 6 segments) — reuse only the generic zone model; strip any "telemedicine room", "consultation station", "medical device", "examination camera" labels before use. -->
<!-- Alternative: a network-perimeter firewall policy / zone-based firewall diagram (e.g.Guest Wi-Fi vs Corporate Core) — EGYCash-style zone-based firewall concept, genericised. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic firewall / micro-segmentation diagram here. See image-placement guidance notes.]*

---""",

    "devicex/module_nvr.md": """---

## Figure — NVR Recording & Monitoring Architecture

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic NVR architecture diagram showing camera streams recorded locally on the appliance, with only alerts/metadata/thumbnails/operator-requested playback traversing the wide-area link to a central monitoring array. No customer-specific camera names, no site names, no customer-specific retention figures. -->
<!-- Suggested source: Telemedicine proposal NVR section (local recording as default, centralised monitoring array as design input, NVR bandwidth consideration) — genericise the diagram. -->
<!-- Alternative: a camera layout / per-site camera-count diagram (generic — show N cameras per site as a variable, not a fixed customer number). -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic NVR architecture / camera-layout diagram here. See image-placement guidance notes.]*

---""",

    "devicex/module_ipbx.md": """---

## Figure — IP-PBX Call Flows / Telephony Topology

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic IP-PBX call-flow diagram showing the four standard flows (scheduled / on-demand / urgent / inter-site) and local survivability (site continues on local services when the wide-area link is down). No customer-specific extension numbers, no customer site names, no customer-specific telephony licensing/numbering details. -->
<!-- Suggested source: Telemedicine proposal §3.4 (Clinical Communication Flows, 4 flows) — genericise the diagram and labels. -->
<!-- Alternative: a PBX topology diagram showing endpoints, trunks, voicemail, and survivability path. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic IP-PBX call-flow / topology diagram here. See image-placement guidance notes.]*

---""",

    "devicex/module_sase.md": """---

## Figure — SASE Architecture (Cloud + Edge Secure Access)

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic SASE architecture diagram showing edge nodes (branches/sites) and remote users connected to cloud-delivered security services (SWG, CASB, ZTNA, FWaaS, secure web/Internet access) over a unified overlay. No customer-specific site names, no customer-specific identity provider names, no customer-specific policy labels. -->
<!-- Suggested source: generic SASE reference model — no customer-specific content from prior proposals is carried. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic SASE architecture diagram here. See image-placement guidance notes.]*

---""",

    "devicex/module_network_services.md": """---

## Figure — Network Services Topology (DNS / NTP / DHCP / Edge Services)

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic network-services topology diagram showing DNS, NTP, DHCP, and other edge/network services distributed across sites with central authority where required. No customer-specific server names, no customer site names, no customer-specific IP addressing. -->
<!-- Suggested source: generic network-services reference model — no customer-specific content from prior proposals is carried. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic network-services topology diagram here. See image-placement guidance notes.]*

---""",

    "devicex/module_virtualization.md": """---

## Figure — Virtualization Architecture / Workload Placement

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic virtualization architecture diagram showing the hypervisor stack, virtual machines / containers, and per-site workload placement, with a continuity-by-design note (local survivability, workload counts per site as a variable). No customer-specific VM names, no customer-specific application names, no customer site names. -->
<!-- Suggested source: Telemedicine proposal DeviceX Virtualization section (§3.3.1) — genericise the diagram. -->
<!-- Alternative: a workload-capacity / per-site workload-count diagram (generic — show N workloads per site as a variable). -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic virtualization / workload-placement diagram here. See image-placement guidance notes.]*

---""",

    "devicex/module_business_workloads.md": """---

## Figure — Business Workload Architecture / Application Placement

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic business-workload architecture diagram showing application tiers, data tiers, and integration points across sites, with workload placement aligned to the customer's deployment goal (to be confirmed per bid). No customer-specific application names, no customer data classifications, no customer site names. -->
<!-- Suggested source: generic business-workloads reference model — no customer-specific content from prior proposals is carried. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic business-workload / application-placement diagram here. See image-placement guidance notes.]*

---""",

    "devicex/module_sdx_operations.md": """---

## Figure — Zero-Touch Provisioning Flow / Attestation & Credentials

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic zero-touch provisioning sequence diagram showing the four stages — pre-registration, first boot & attestation, certificate issuance, mesh join — and an attestation / short-lived-credentials flow showing compromise-response scenarios. No customer-specific registration-service names, no customer-specific CA names, no customer site names. -->
<!-- Suggested source: Telemedicine proposal §3.6 / §3.6.1 (Centralized Management And Zero-Touch Provisioning, ZTP in a multi-country deployment) — genericise the diagram and labels; strip any country/site names. -->
<!-- Alternative: a device-adoption / mesh-join diagram showing a new site brought into service by a non-technical person connecting power and a network cable. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic ZTP / attestation flow diagram here. See image-placement guidance notes.]*

---""",

    # ---- StackX ----
    "stackx/module_stackx_endpoint_mgmt.md": """---

## Figure — Endpoint Management Dashboard / Endpoint Topology

<!-- IMAGE PLACEHOLDER — insert approved generic image here -->
<!-- Recommended image: a generic endpoint-management dashboard or endpoint-topology diagram showing managed endpoints, device status, policy compliance, and alerting. Vendor names cleaned to "major vendor platforms" in the text already; the image must likewise be generic — no specific vendor product screenshot unless approved for the current bid, no customer-specific endpoint names, no customer site names. -->
<!-- Suggested source: EGYCash/Telemedicine "Endpoint Management" screenshot references — these are vendor UI screenshots; use only as a composition reference, and produce or source a generic / Verto-Wave-branded equivalent for the final proposal. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic endpoint-management dashboard / topology diagram here. See image-placement guidance notes.]*

---""",

    "stackx/module_stackx_automation_orchestration.md": """---

## Figure — Automation & Orchestration Pipeline / Workflow

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic automation/orchestration pipeline diagram showing workflow definition, trigger, execution, approval/gating, and reporting — aligned to the "how many workflows" scope-number slot ({{services_workflows}}) in the Professional Services module. No customer-specific workflow names, no customer-specific system names, no customer site names. -->
<!-- Suggested source: generic automation/orchestration reference model — no customer-specific content from prior proposals is carried. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic automation/orchestration pipeline diagram here. See image-placement guidance notes.]*

---""",

    "stackx/module_stackx_observability_apm.md": """---

## Figure — Observability / APM Dashboards & Traces

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic observability/APM dashboard image showing metrics, logs, traces, alerting, and dashboard-oriented visibility — aligned to the "how many apps monitored" scope-number slot ({{services_apps_monitored}}) in the Professional Services module. No customer-specific application names, no customer-specific metric labels that reveal the customer's business, no customer site names. -->
<!-- Suggested source: Telemedicine proposal §3.12 (StackX Observability) + EGYCash "Figure 1: Change-Correlated Performance Views" — use only as a composition reference; strip any customer-specific labels; produce or source a generic / Verto-Wave-branded equivalent for the final proposal. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic observability/APM dashboard diagram here. See image-placement guidance notes.]*

---""",

    "stackx/module_stackx_trueview.md": """---

## Figure — TrueView Dashboard / Visualisation

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic TrueView-style dashboard / visualisation diagram showing consolidated visibility, status, and reporting across the managed estate. No customer-specific entity names, no customer-specific dashboard labels that reveal the customer's business, no customer site names. -->
<!-- Suggested source: generic TrueView reference model — no customer-specific content from prior proposals is carried. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic TrueView dashboard / visualisation diagram here. See image-placement guidance notes.]*

---""",

    "stackx/module_stackx_idm.md": """---

## Figure — Identity & Access Management Architecture / SSO-MFA Flow

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic identity/access-management architecture diagram showing authentication, MFA, SSO, role-based access control, and identity lifecycle, plus an SSO/MFA login flow diagram. No customer-specific identity provider names, no customer-specific role names, no customer site names. -->
<!-- Suggested source: generic IDM reference model — no customer-specific content from prior proposals is carried. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic IDM architecture / SSO-MFA flow diagram here. See image-placement guidance notes.]*

---""",

    "stackx/module_stackx_backup.md": """---

## Figure — Backup Architecture / Backup Policy Flow

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic backup architecture diagram showing backup sources, backup repository/target, backup policies (full/incremental/differential), retention, and recovery path — with recovery targets agreed per bid (not assumed). No customer-specific data-source names, no customer-specific retention figures, no customer site names. -->
<!-- Suggested source: generic backup reference model — no customer-specific content from prior proposals is carried. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic backup architecture / policy-flow diagram here. See image-placement guidance notes.]*

---""",

    "stackx/module_stackx_ops_config_mgmt.md": """---

## Figure — Configuration Management Workflow / Change Flow

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic configuration-management workflow diagram showing baseline configuration, change control, drift detection, compliance check, and remediation — aligned to the change-management cross-reference ({{section_change_mgmt}}). No customer-specific configuration item names, no customer-specific system names, no customer site names. -->
<!-- Suggested source: generic configuration-management reference model — no customer-specific content from prior proposals is carried. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic configuration-management / change-flow diagram here. See image-placement guidance notes.]*

---""",

    "stackx/module_stackx_network_ops.md": """---

## Figure — Network Operations Dashboard / Topology Map

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic network-operations dashboard / interactive topology-map diagram showing live network topology, port utilisation heatmaps, bandwidth traffic graphs, and link-flap alerts — aligned to the "how many network devices to be monitored" scope-number slot ({{services_network_devices}}) in the Professional Services module. No customer-specific device names, no customer-specific interface descriptions that reveal the customer's business (e.g. "Telemedicine Workstation", "Examination Camera"), no customer site names. -->
<!-- Suggested source: Telemedicine proposal §3.8 / §3.9 (StackX Network Monitoring, SNMP LLD, topology mapping, traffic heatmaps, network alarm escalation) — genericise the diagram; strip any "clinic", "telemedicine workstation", "examination camera", "WAN uplink" labels that reveal a specific customer environment. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic network-operations dashboard / topology-map diagram here. See image-placement guidance notes.]*

---""",

    "stackx/module_stackx_itSM.md": """---

## Figure — ITSM Service Desk / Incident & Request Workflow

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic ITSM service-desk dashboard image showing ticket counts, open-ticket lists, navigation structure, and dashboard-oriented visibility — plus an incident-to-resolution workflow diagram (monitoring → alert → triage → investigation → resolution → closure) and a request-fulfilment / change / major-incident operating workflow. No customer-specific service-desk configuration, no customer-specific category/workflow/asset names, no customer site names. -->
<!-- Suggested source: Telemedicine proposal §3.9 (StackX ITSM) "Figure 2. STACKX product overview reference image" and "Figure 3. STACKX ticket timeline reference screenshot" — these are explicit "official STACKX reference screenshots"; use only as a composition reference, and produce or source a generic / Verto-Wave-branded equivalent configured with the customer's entities for the final proposal. Also EGYCash "Figure 1: Smart Service Desk" — composition reference only. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic ITSM service-desk / incident-workflow diagram here. See image-placement guidance notes.]*

---""",

    "stackx/module_stackx_alm.md": """---

## Figure — Asset Lifecycle / Asset Inventory Dashboard

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic asset-lifecycle diagram showing procurement/onboarding, deployment, maintenance, renewal/replacement, and decommissioning — plus an asset-inventory dashboard showing asset register, status, and ownership. No customer-specific asset names, no customer-specific serial numbers, no customer site names. -->
<!-- Suggested source: generic ALM reference model — no customer-specific content from prior proposals is carried. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic asset-lifecycle / asset-inventory diagram here. See image-placement guidance notes.]*

---""",

    "stackx/module_stackx_compliance.md": """---

## Figure — Compliance Framework / Audit-Trail Diagram

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic compliance-framework diagram showing compliance domains, controls, evidence, and audit trail — aligned to the customer's compliance framework confirmed per bid. No customer-specific control names that reveal the customer's regulatory regime beyond what is agreed, no customer site names. -->
<!-- Suggested source: generic compliance reference model — no customer-specific content from prior proposals is carried. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic compliance-framework / audit-trail diagram here. See image-placement guidance notes.]*

---""",

    "stackx/module_stackx_ops_integrity.md": """---

## Figure — Operations Integrity / Integrity-Check Flow

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic operations-integrity diagram showing integrity monitoring, baseline comparison, anomaly detection, and integrity-check/remediation flow. No customer-specific integrity-check targets, no customer-specific system names, no customer site names. -->
<!-- Suggested source: generic operations-integrity reference model — no customer-specific content from prior proposals is carried. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic operations-integrity / integrity-check-flow diagram here. See image-placement guidance notes.]*

---""",

    "stackx/module_stackx_call_center.md": """---

## Figure — Call-Center Architecture / Call Flow

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic call-center architecture diagram showing inbound/outbound routing, queues, agents, and reporting — plus a call-flow diagram. No customer-specific queue names, no customer-specific agent roles, no customer site names. -->
<!-- Suggested source: generic call-center reference model — no customer-specific content from prior proposals is carried. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic call-center architecture / call-flow diagram here. See image-placement guidance notes.]*

---""",

    "stackx/module_stackx_event_log_mgmt.md": """---

## Figure — Event Log Management Architecture / Log Flow

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic event-log-management architecture diagram showing log sources, collection, normalisation, storage, correlation, retention, and reporting/forensics access. No customer-specific log-source names, no customer-specific retention figures, no customer site names. -->
<!-- Suggested source: generic event-log-management reference model — no customer-specific content from prior proposals is carried. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic event-log-management architecture / log-flow diagram here. See image-placement guidance notes.]*

---""",

    "stackx/module_stackx_soc.md": """---

## Figure — SOC Architecture / Security Operations Workflow

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic SOC architecture diagram showing the security-operations delivery model (Native / Integrated / Assured), security services areas, monitoring, detection, triage, investigation, response, and escalation — plus a SOC tiers / shift-model diagram where relevant. No customer-specific SOC tooling names beyond what is agreed, no customer-specific threat intel feeds, no customer site names. -->
<!-- Suggested source: Telemedicine proposal §3.7 (StackX Security) + the security-model-at-a-glance concept — genericise the diagram; strip any "clinic", "Dubai management plane", or site-specific labels. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic SOC architecture / security-operations-workflow diagram here. See image-placement guidance notes.]*

---""",

    "stackx/module_stackx_devops.md": """---

## Figure — DevOps Pipeline / CI-CD Flow

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic DevOps pipeline / CI-CD flow diagram showing source, build, test, security scanning, release, deploy, and monitor stages — aligned to the delivery-phasing note in the PM methodology module. No customer-specific repository names, no customer-specific pipeline stage names that reveal the customer's business, no customer site names. -->
<!-- Suggested source: generic DevOps reference model — no customer-specific content from prior proposals is carried. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic DevOps pipeline / CI-CD flow diagram here. See image-placement guidance notes.]*

---""",

    "stackx/module_stackx_security.md": """---

## Figure — Security Architecture / Defence-in-Depth

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic defence-in-depth / layered security architecture diagram showing the security capability layers (external boundary, internal visibility & control, identity shield, data & system integrity, continuity & recovery, assurance & oversight) and the delivery-mode framing (Native / Integrated / Assured). No customer-specific control names that reveal the customer's regulatory regime beyond what is agreed, no customer site names. -->
<!-- Suggested source: Telemedicine proposal §3.7 (StackX Security) + the security-model-at-a-glance concept — genericise the diagram; strip any "clinic", "Dubai management plane", or site-specific labels. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic security / defence-in-depth architecture diagram here. See image-placement guidance notes.]*

---""",

    # ---- Cross-cutting ----
    "cross_cutting/section_professional_services.md": """---

## Figure — Architecture & Engagement Diagram (Design Phase Input)

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic engagement architecture diagram showing the Architecture, Design, Implementation & Roll-out engagement flow — architecture workshops ({{services_arch_workshops}} sessions), architecture diagrams produced ({{services_arch_diagrams}} diagrams), design outputs, and the handover into implementation/roll-out. No customer-specific architecture names, no customer-specific environment depiction, no customer site names. -->
<!-- Suggested source: generic professional-services engagement model — no customer-specific content from prior proposals is carried. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic professional-services engagement / architecture diagram here. See image-placement guidance notes.]*

---""",

    "cross_cutting/section_change_mgmt.md": """---

## Figure — Change Request Process Flow

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic change-request process flow diagram showing request submission, impact assessment, approval gate, implementation, validation, and closure — aligned to the change request procedure in this section. No customer-specific committee/approver names, no customer-specific system names, no customer site names. -->
<!-- Suggested source: generic change-management reference model — no customer-specific content from prior proposals is carried. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic change-request process-flow diagram here. See image-placement guidance notes.]*

---""",

    "cross_cutting/section_pm_methodology.md": """---

## Figure — Delivery Phasing / Project Stages Diagram

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic delivery-phasing / project-stages diagram showing the phases (from the delivery phasing subsection: Phase 1 … through optional Phase 6 managed ops) and the 5-stage PMI-mapped PM methodology + RAID log. No customer-specific milestone names, no customer-specific dates, no customer site names. -->
<!-- Suggested source: EGYCash "Fig. 1. Verto Wave Project Management Stages" — use only as a composition reference for the PM stages shape; genericise labels; strip any customer-specific milestone names/dates. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic delivery-phasing / project-stages diagram here. See image-placement guidance notes.]*

---""",

    "cross_cutting/section_training.md": """---

## Figure — Training Programme / Training Matrix Visual

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic training-programme diagram or training-matrix visual (course / attendees / duration format) showing the training approach for the roll-out — aligned to the "how many training attendees" and "how many training sessions" scope-number slots ({{services_training_attendees}}, {{services_training_sessions}}) in the Professional Services module. No customer-specific course names that reveal the customer's business, no customer-specific attendee names, no customer site names. -->
<!-- Suggested source: generic training reference model — no customer-specific content from prior proposals is carried. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic training-programme / training-matrix visual here. See image-placement guidance notes.]*

---""",
}


def find_center(path: Path) -> int:
    """Return the 0-based line index closest to the center of the file,
    skipping pure-metadata header lines."""
    lines = path.read_text(encoding="utf-8").split("\n")
    total = len(lines)
    # center index
    return total // 2


def insert_guidance(path: Path, guidance: str) -> bool:
    lines = path.read_text(encoding="utf-8").split("\n")
    center = find_center(path)

    # Find a good insertion point: the first blank line at or after center,
    # or the center line itself if no blank nearby.
    insert_at = center
    # search forward for a blank line within 15 lines
    for i in range(center, min(center + 15, len(lines))):
        if lines[i].strip() == "":
            insert_at = i
            break
    else:
        # search backward
        for i in range(center, max(center - 15, -1), -1):
            if lines[i].strip() == "":
                insert_at = i
                break

    # Build the new content
    before = lines[:insert_at]
    after = lines[insert_at:]
    new_lines = before + [guidance, ""] + after
    path.write_text("\n".join(new_lines), encoding="utf-8")
    return True


def main():
    count = 0
    skipped = []
    for rel, guidance in GUIDANCE.items():
        path = MODULES_DIR / rel
        if not path.exists():
            skipped.append(rel)
            continue
        insert_guidance(path, guidance)
        count += 1
        print(f"inserted: {rel}")

    # Generic fallback for modules not in GUIDANCE dict:
    # insert a short generic guidance at center.
    generic_guidance = """---

## Figure — <Insert approved generic diagram / screenshot here>

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic diagram or screenshot relevant to this module's content (architecture, flow, dashboard, or topology as appropriate). No customer-specific names, environment, architecture, site names, or branding. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic image here. See image-placement guidance notes.]*

---"""

    for md_file in sorted(MODULES_DIR.rglob("module_*.md")):
        rel = md_file.relative_to(MODULES_DIR).as_posix()
        if rel in GUIDANCE:
            continue
        # also skip cross_cutting section_*.md that already got specific guidance
        if rel in GUIDANCE:
            continue
        if md_file.is_file():
            # check if already has an IMAGE PLACEMENT GUIDANCE block
            text = md_file.read_text(encoding="utf-8")
            if "IMAGE PLACEMENT GUIDANCE" in text:
                continue
            insert_guidance(md_file, generic_guidance)
            count += 1
            print(f"inserted (generic): {rel}")

    print(f"\nTotal modules updated: {count}")
    if skipped:
        print(f"Skipped (not found): {skipped}")


if __name__ == "__main__":
    main()
