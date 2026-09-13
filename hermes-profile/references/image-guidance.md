# Image Placement Guidance — VertoWave Proposal Template

## What this is

A reusable workflow for inserting **image-placement guidance blocks** into the modular proposal markdown sources, plus the technique used to source the Verto Wave logo from the public website.

Scope: combine.py assembles text and can embed images via the `--logo` flag when building a specific proposal docx (the logo image goes onto the cover page). Diagram and screenshot images for the body modules are still inserted in the docx-editor stage — the guidance blocks are the placeholders/reminders inserted into modules now so the right image goes in the right place later.

## Generic-only rule (class-level)

Every image placed in a proposal module must be **generic**:
- No customer name, customer-specific environment, architecture, site names, or branding.
- If reusing an image from a prior proposal, strip customer-specific labels before use.
- If an image's caption references a specific customer context (e.g. "clinic", "Dubai management plane", "October site", "telemedicine workstation", "examination camera"), that image is **not** reusable as-is — genericise the diagram or drop it.
- Vendor UI screenshots from prior proposals are composition references only — produce or source a generic / Verto-Wave-branded equivalent for the issue copy.

## Image-placement guidance block — structure

Inserted at the **center** of each module `.md` file, in a blank line, wrapped in `---` separators so it reads as a distinct figure block:

```
## Figure — <descriptive name>

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: <what kind of diagram/screenshot> -->
<!-- Suggested source: <proposal section / figure ref> — genericise, strip customer labels -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: for the logo, use `combine.py --logo <path>` when building the proposal docx — combine.py embeds the logo image into the cover-page placeholder paragraph (centered). For body-module diagram/screenshot images, insert the approved image at this location in the final docx in the docx-editor stage (combine.py is text-only for body images). -->

*[Figure placeholder — insert approved generic <name> diagram here. See image-placement guidance notes.]*
```

The block is module-specific where we know the right candidate image; otherwise a short generic variant is used.

## Suggested image candidates per module (from the proposal texts)

These are composition references — only the **generic shape** is reusable; labels must be stripped.

| Module | Candidate image | Source reference | Genericisation note |
|--------|-----------------|------------------|---------------------|
| module_sdwan | SD-WAN hub-and-spoke / mesh overlay topology; path-diversity / quality-based steering decision diagram | Telemedicine §3.1, §3.2 (architecture tiers, SD-WAN architecture, consultation path behavior) | Strip any site/country names, "clinic" labels |
| module_firewall | In-site micro-segmentation (6-segment model); zone-based firewall (guest vs corporate core) | Telemedicine §4.3.3 (in-clinic micro-segmentation); EGYCash zone-based firewall concept | Strip "telemedicine room", "consultation station", "medical device", "examination camera" labels |
| module_nvr | NVR recording & monitoring architecture (local recording + central monitoring array); per-site camera-count diagram | Telemedicine NVR section (local recording default, centralised monitoring array, NVR bandwidth) | Strip site/camera names; show N cameras per site as a variable |
| module_ipbx | IP-PBX call flows (4 flows: scheduled / on-demand / urgent / inter-site); telephony topology with local survivability | Telemedicine §3.4 (Clinical Communication Flows) | Strip extension numbers, site names |
| module_sase | SASE architecture (edge + remote users → cloud security services: SWG/CASB/ZTNA/FWaaS) | Generic SASE reference model | No customer-specific identity provider names |
| module_network_services | Network services topology (DNS/NTP/DHCP/edge services) | Generic reference model | No customer-specific server names |
| module_virtualization | Virtualization architecture / workload placement (per-site workload count as variable); continuity-by-design | Telemedicine §3.3.1 (DeviceX Virtualization) | Strip VM/application names, site names |
| module_business_workloads | Business workload architecture / application placement (tiers, data, integration) | Generic reference model | Strip application/data classification names |
| module_sdx_operations | Zero-touch provisioning flow (4 stages: pre-registration → first boot & attestation → certificate issuance → mesh join); attestation & short-lived credentials flow; device-adoption diagram | Telemedicine §3.6, §3.6.1 (ZTP, multi-country deployment) | Strip country/site names, registration-service/CA names |
| module_stackx_endpoint_mgmt | Endpoint management dashboard / endpoint topology | EGYCash/Telemedicine "Endpoint Management" screenshot refs (composition only — vendor UI screenshots) | Use generic / Verto-Wave-branded equivalent; strip vendor product screenshot unless approved |
| module_stackx_automation_orchestration | Automation/orchestration pipeline (workflow definition → trigger → execution → approval → reporting) | Generic reference model; ties to `{{services_workflows}}` scope slot | Strip workflow/system names |
| module_stackx_observability_apm | Observability/APM dashboards (metrics/logs/traces/alerting) | Telemedicine §3.12 (StackX Observability); EGYCash "Figure 1: Change-Correlated Performance Views" (composition only) | Strip customer-specific app/metric labels that reveal the customer's business |
| module_stackx_trueview | TrueView dashboard / visualisation (consolidated visibility/status/reporting) | Generic TrueView reference model | Strip entity/dashboard labels |
| module_stackx_idm | IAM architecture (authentication/MFA/SSO/RBAC/identity lifecycle); SSO-MFA login flow | Generic IDM reference model | Strip identity provider/role names |
| module_stackx_backup | Backup architecture (sources/repository/policies/retention/recovery) | Generic backup reference model | Strip data-source/retention names; recovery targets agreed per bid |
| module_stackx_ops_config_mgmt | Configuration management workflow (baseline → change control → drift detection → compliance → remediation) | Generic reference model; ties to `{{section_change_mgmt}}` | Strip configuration item/system names |
| module_stackx_network_ops | Network operations dashboard / interactive topology map (live topology, port utilisation heatmaps, bandwidth graphs, link-flap alerts) | Telemedicine §3.8, §3.9 (StackX Network Monitoring, SNMP LLD, topology mapping, traffic heatmaps, alarm escalation) | Strip "clinic", "telemedicine workstation", "examination camera", "WAN uplink" labels |
| module_stackx_itSM | ITSM service-desk dashboard (ticket counts, open-ticket lists, navigation, dashboard visibility); incident-to-resolution workflow (monitoring → alert → triage → investigation → resolution → closure); request-fulfilment/change/major-incident operating workflows | Telemedicine §3.9 (StackX ITSM) "Figure 2" (STACKX product overview reference image) & "Figure 3" (ticket timeline reference screenshot) — explicit "official STACKX reference screenshots"; EGYCash "Figure 1: Smart Service Desk" | Composition references only — produce/source a generic / Verto-Wave-branded equivalent configured with the customer's entities |
| module_stackx_alm | Asset lifecycle (procurement/onboarding → deployment → maintenance → renewal/replacement → decommissioning); asset-inventory dashboard | Generic ALM reference model | Strip asset/serial-number names |
| module_stackx_compliance | Compliance framework (domains/controls/evidence/audit trail) | Generic compliance reference model | Strip control names that reveal the customer's regulatory regime beyond what is agreed |
| module_stackx_ops_integrity | Operations integrity (monitoring → baseline comparison → anomaly detection → integrity check/remediation) | Generic reference model | Strip integrity-check target/system names |
| module_stackx_call_center | Call-center architecture (inbound/outbound routing, queues, agents, reporting); call-flow diagram | Generic call-center reference model | Strip queue/agent-role names |
| module_stackx_event_log_mgmt | Event log management architecture (sources/collection/normalisation/storage/correlation/retention/reporting) | Generic reference model | Strip log-source/retention names |
| module_stackx_soc | SOC architecture (delivery model Native/Integrated/Assured, security services areas, monitoring/detection/triage/investigation/response/escalation); SOC tiers/shift model | Telemedicine §3.7 (StackX Security) + security-model-at-a-glance concept | Strip "clinic", "Dubai management plane", site-specific labels |
| module_stackx_devops | DevOps pipeline / CI-CD flow (source → build → test → security scanning → release → deploy → monitor) | Generic DevOps reference model; ties to delivery-phasing note in PM methodology | Strip repository/pipeline-stage names that reveal the customer's business |
| module_stackx_security | Defence-in-depth / layered security architecture (external boundary → internal visibility & control → identity shield → data & system integrity → continuity & recovery → assurance & oversight); delivery-mode framing (Native/Integrated/Assured) | Telemedicine §3.7 (StackX Security) + security-model-at-a-glance concept | Strip "clinic", "Dubai management plane", site-specific labels |
| section_professional_services | Engagement architecture diagram (architecture workshops → architecture diagrams → design outputs → handover into implementation/roll-out) | Generic professional-services engagement model; ties to `{{services_arch_workshops}}`, `{{services_arch_diagrams}}` scope slots | Strip architecture/environment names |
| section_change_mgmt | Change request process flow (request → impact assessment → approval gate → implementation → validation → closure) | Generic change-management reference model; ties to change request procedure in this section | Strip committee/approver/system names |
| section_pm_methodology | Delivery-phasing / project-stages diagram (phases incl. optional Phase 6 managed ops) + 5-stage PMI-mapped PM methodology + RAID log | EGYCash "Fig. 1. Verto Wave Project Management Stages" (composition only) | Strip milestone names/dates |
| section_training | Training programme diagram / training-matrix visual (course/attendees/duration format) | Generic training reference model; ties to `{{services_training_attendees}}`, `{{services_training_sessions}}` scope slots | Strip course/attendee names |
| section_assumptions | (generic — diagram optional; assumptions are text-led) | — | If a diagram is used, it must be generic |
| section_cover_execsummary | Cover visual (generic Verto Wave platform/network visual, no customer environment) | Generic cover visual | Must not depict any specific customer environment/architecture/naming |
| section_document_control | (generic — document-control is text-led; deliverables-by-phase table may have a small visual) | — | If a visual is used, generic only |
| section_ola | (generic — OLA is text/table-led; coverage-options framing may have a small visual) | — | If a visual is used, generic only |
| section_out_of_scope | (generic — out-of-scope is text-led) | — | If a visual is used, generic only |
| section_roles | (generic — roles is table-led; role-structure diagram optional) | — | If a visual is used, generic only |
| section_validity | (generic — validity is text-led) | — | If a visual is used, generic only |

## Logo sourcing technique (Verto Wave website)

The Verto Wave public website (`https://www.vertowave.com/`) is a **Framer single-page site** — the logo is not in static HTML; it is rendered by JavaScript into the nav ("Logo/Menu Items" component). To find and download it:

1. Fetch the homepage HTML with a browser-like User-Agent.
2. Locate the nav component: search the HTML for `data-framer-name="Logo/Menu Items"`.
3. Inside that component, the logo `<img>` tag carries `width="307" height="65"` and a `src` pointing to a `framerusercontent.com` image (e.g. `https://framerusercontent.com/images/9aSgY9nMAwJbNTDBJAJzimNEE.png`).
4. Download that image directly (it is a public, hotlinkable asset on framerusercontent.com).
5. Verify with a vision check that it is the actual Verto Wave logo (dark teal background, "VERTO WAVE" text + sound-wave icon) before using it in a proposal.
6. Save to the skill's `assets/` directory (e.g. `assets/vertowave_logo.png`).

Caveats:
- Direct guesses at `/images/logo.png`, `/logo.svg`, `/public/logo.png`, `/assets/logo.png` return 404 — the logo is referenced by a hashed filename in the nav component, not by a stable logo path.
- The homepage also carries many `framerusercontent.com/images/*.png` section photos (hero, customers, etc.) — most are decorative section imagery, not the logo. Confirm by vision before using any of them as a logo.
- Third-party pages (e.g. OpenText customer spotlight) carry their own logos, not Verto Wave's official logo — use only as a brand reference, not as the logo file.

## Where the guidance blocks live

- Script that inserts module-specific guidance at center: `scripts/insert_image_guidance.py` (operates on `modules/devicex/*.md`, `modules/stackx/*.md`, `modules/cross_cutting/section_*.md` that are in its dict; generic fallback for the rest).
- Script that backfills generic guidance into any `section_*.md` still missing one: `scripts/insert_section_guidance.py`.
- Both scripts use `Path(__file__).resolve().parents[1]` for the skill root (the `parents[1]` fix — see the pitfall below).
- Guidance block text is module-specific where known (dict in `insert_image_guidance.py`), generic otherwise.

## Pitfall — script path resolution

A script that sets `SKILL_ROOT = Path(__file__).resolve().parent` resolves to `scripts/`, not the skill root. Modules were skipped (wrong directory) and the final scan reported a false "CLEAN" on an empty glob. Fix: `SKILL_ROOT = Path(__file__).resolve().parents[1]`. Always print the paths the script operates on and a final scan with the actual glob it used.

## Pitfall — verify the logo, don't trust the filename

A `framerusercontent.com` image that looks like it could be a logo (nav component, 307×65) still needs a vision check. Some nav images could be menu icons rather than the logo. Confirm the actual "VERTO WAVE" wordmark + icon before committing it to a proposal cover page.

## Cover page logo placement

The cover page module (`section_cover_execsummary`) carries:
- A primary logo placeholder line: `[VERTO WAVE LOGO — INSERT LOGO IMAGE HERE]`
- An optional secondary-logo placeholder line
- Logo placement notes telling the bid team to insert the approved logo image (e.g. `assets/vertowave_logo.png` or the brand-team-approved file) before issue. The supported way to put the logo onto a built proposal cover page is the `combine.py --logo <path>` flag — it embeds the image into the cover-page placeholder paragraph (centered). The logo can still be dropped in manually in the docx editor if preferred.
- A rule: do not use a logo image that is not the approved Verto Wave logo; do not carry a logo from a prior proposal's customer-specific cover page; logo images are embedded via `combine.py --logo` (or inserted manually per bid).
- **Verification pitfall:** before embedding, confirm with a vision check that the file is the actual Verto Wave logo (dark teal background, "VERTO WAVE" wordmark + sound-wave icon). Some nav images on the Verto Wave site are menu icons, not the logo. Also confirm with the Verto Wave brand/marketing team that the downloaded public logo is the approved version before issue — the public-website logo is a composition reference, not necessarily the brand-approved asset.

When building a specific proposal, drop the approved logo file into the cover-page logo slot in the docx. The logo file in `assets/vertowave_logo.png` is the downloaded public logo — confirm with the Verto Wave brand/marketing team that it is the approved version before issue.
