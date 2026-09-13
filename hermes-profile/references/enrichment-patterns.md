# Enrichment Patterns — Concrete Before/After from Module Integration

Concrete enrichment patterns applied when folding a richer source proposal
(Telemedicine Network Technical Proposal V1.6) into the existing 35-module
system. Use as worked examples when enriching modules in a future integration.

Companion to `references/integration-playbook.md` — that file is the
*methodology*; this file is the *worked examples*.

## Pattern 1 — SD-WAN: add a multi-path steering matrix

**Before (module_sdwan.md):** solution overview + bullet capability list +
ZTP + link aggregation + traffic prioritization. No steering behaviour
table.

**After:** kept all existing sections; added a new `## Path Diversity &
Quality-Based Steering` section containing:

- A 2-3 sentence transport-independence paragraph (de-sectorized from the
  source's "carrier independence" differentiator).
- A `### Steering Behaviour` table with 5 rows (all paths healthy / primary
  degrades / primary fails / all paths impaired / total outage), each row a
  Condition + System Response pair.
- A `### Service Quality Targets (reference — confirm per bid)` table with
  7 metric rows using `{{ola_*_target}}` value tokens, plus a note to replace
  or remove per engagement.

**Why this pattern works:** the table gives the module a concrete operating
story it previously lacked, while the value tokens keep the numbers from
becoming a hard claim. The transport-independence paragraph is a reusable
positioning line that applies to any multi-site deployment.

**De-sectorization applied:** "consultation media" → "priority media"; "Dubai
hub" → "central hub"; "Africa-to-Gulf" → "long-haul / inter-site paths";
"geostationary satellite" → "satellite (where it is the only option)".

**Do not carry:** the 150ms-to-Dubai figure, the satellite/geostationary note
as a fixed claim, any mention of "clinical".

---

## Pattern 2 — Firewall: add a micro-segmentation table

**Before:** stateful firewall capabilities + NGFW enhancement list + template
deployment + out-of-scope.

**After:** kept all existing sections; added `## In-Site Micro-Segmentation`
with:

- A 1-sentence isolation principle.
- A bulleted list of 6 generic traffic segments (application/user, peripheral/
  device, surveillance/camera, voice, management, administrative/guest), each
  with a one-line characteristic.
- A 1-sentence rationale (least-trusted device is often the most common
  foothold; compromised peripheral/camera can reach neither application
  segment nor hub).

**De-sectorization applied:** "clinical consultation segment" → "primary
application / user segment"; "connected medical device segment" → "connected
peripheral / device segment"; "IP surveillance camera segment" → "surveillance
/ camera segment"; "clinical" dropped throughout.

**Do not carry:** the source's framing that this is "for a telemedicine room" —
the segmentation model is generic and applies to any site with mixed traffic
classes.

---

## Pattern 3 — NVR: add operating pattern + sizing-as-design-input

**Before:** two variant sub-options (A — without AI, B — with edge analytics)
+ reference parameters + out-of-scope.

**After:** kept both variants; added `## Operating Pattern` with three
sub-sections:

- `### Local recording and retention (default)` — 2 sentences: recorded
  locally, retention + alert forwarding to central platform, does not compete
  with priority wide-area traffic.
- `### Centralised monitoring array (optional, where required)` — describes
  the high-capacity monitoring arrangement as a design-time planning input,
  not a fixed product spec; sizing confirmed at design stage.
- `### NVR bandwidth consideration (planning input)` — 3 bullets: local
  recording is not a continuous WAN consumer; central archive sync scheduled
  outside critical hours and rate-limited; monitoring backbone sized against
  camera count/resolution/display config.
- Enriched `## Reference Parameters` with 2 new confirm-per-design rows
  (central monitoring array sizing, archive synchronisation schedule).
- Enriched `## Camera Support` to state IP cameras supported by default,
  analogue support is a per-engagement decision.

**De-sectorization applied:** "room security and procedure documentation" →
removed (too sector-specific); "8 display outputs, 8-camera grid" → "multiple
display outputs, each with a camera grid plus a dedicated active-focus window"
(generic structure, not a fixed number); "2 MP resolution / 160 Mbps / 250 Mbps"
→ removed (proposal-specific numbers).

**Do not carry:** the specific 8-display / 2MP / 160Mbps / 250Mbps figures.

---

## Pattern 4 — IP-PBX: add a generic call-flows table + local survivability

**Before:** solution overview + core capability bullets + value-to-distributed-
branches + out-of-scope.

**After:** kept existing sections; added `## Call Flows (generic — define per
engagement)` with 4 sub-tables (Scheduled Session / On-Demand Remote Expert
Request / Urgent Escalation / Inter-Site and Administrative), each a Flow/Trigger/
Behaviour table. Added `## Local Survivability` — 3 sentences on local call
handling during WAN outage, specialist extensions, configurable recording/
retention.

**De-sectorization applied:** the source's call-flow table was fully
de-sectorized: "Scheduled Consultation" → "Scheduled Session"; "specialist
extension" → "remote extension"; "general practitioner" → removed (the
on-demand flow just says "a user needs an opinion"); "Dubai" → "remote site";
"consultation" → "session"; "urgent escalation path to on-call specialist
group" → "urgent escalation path to the on-call group".

**Why a table per flow:** the source used a 3-column table (Flow / Trigger /
Behaviour) for each call flow. Replicating that structure gives the module
operating detail without asserting any specific queue structure or routing.

**Do not carry:** specialist/GP/Dubai/clinical framing; specific queue names;
the source's "click-to-specialist dialing" as a fixed feature.

---

## Pattern 5 — Virtualization: add a continuity-by-design one-liner

**Before:** solution overview + platform capabilities + value to branch
locations + out-of-scope.

**After:** kept existing; added `## Continuity by Design` — 2 sentences: the
platform can host cached copies of key workloads (app front-ends, imaging/
documentation viewers, directory services) so a site remains functional through
a wide-area outage; number of workloads per site is a per-engagement design
input; small site not charged for unused capacity; capability can be added
later without redesign.

**De-sectorization applied:** the source framed this as "keeps clinical
applications, imaging gateway and directory services running" — genericized to
"application front-ends, imaging or documentation viewers, directory services,
and similar".

---

## Pattern 6 — SDX Operations: add zero-touch provisioning flow + attestation narrative

**Before:** solution overview + 4 activity sub-sections (provisioning, network
config, security/policy, monitoring) + delivery model + out-of-scope.

**After:** kept existing; added:

- `## Zero-Touch Provisioning` — 2 paragraphs: ZTP is a deployment advantage only
  if it does not create a security weakness; the provisioning model assumes the
  person plugging in the device is untrusted and derives trust from the hardware;
  operational result: a new site is brought into service by a non-technical person
  connecting power and a network cable, with stronger security posture than a
  manually configured site.
- `### Provisioning Flow` — 4 staged sub-sections (Pre-Registration / First Boot
  and Attestation / Certificate Issuance / Mesh Join), each a short paragraph.
- `## Attestation and Short-Lived Credentials` — 2 sub-sections:
  - `### How It Operates` — 4 bullets (attestation cycle / verification / issuance /
    baseline registry).
  - `### Response to Compromise` — 5 bullets (node stolen / bootloader tampered /
    attempted interception of provisioning / unexplained configuration drift /
    diagnostics required before restoring service).

**De-sectorization applied:** "telemedicine room" → "site"; "clinic" → "site";
"four countries" → "multiple locations"; "Dubai" → removed; "clinical" →
removed where it appeared in the compromise-response bullets.

**Why this is the biggest single enrichment:** the zero-touch + attestation
content is the strongest, most reusable security narrative across all six source
proposals. It currently has no other home in the 35-module system. If a dedicated
platform-security module is created later, this content should move there and be
removed from SDX Operations to avoid duplication (see the repetition watch-list
in the integration playbook).

**Module note updated:** the old note said "Present in prior proposals for branch
operations scope" — kept, since it is already generic ("prior proposals", not
named customers).

---

## Pattern 7 — OLA: enrich priority examples + OLA conditions + reporting

**Before:** 4 priority definitions with generic IT examples (network outage /
application failure / user issue / general enquiry) + response-time table +
8x5 availability + authority matrix + RACI + escalation + reporting + OLA
conditions (somewhat duplicated).

**After:** kept all existing structure; enriched:

- Priority 1-4 **examples** with the source's more concrete-style examples,
  de-sectorized: P1 = "loss of overlay connectivity for a location; central
  platform unavailable; hub down; no session possible at multiple sites"; P2 =
  "single site offline; session quality persistently below target at a site; NVR
  not recording; queue misrouting"; P3 = "single extension fault; monitoring
  dashboard error; intermittent minor quality degradation on a secondary path";
  P4 = "general enquiries, routine service requests, report additions, cosmetic
  issues".
- Reporting line: "per-location availability, service quality trend and incident
  summary" (de-sectorized from "consultation quality trend").
- OLA conditions: cleaned up the duplicated pause clauses into two clean bullets
  (clock paused if outside coverage or dispatched to customer team; critical/
  major requests must be raised by phone or email to be eligible for KPIs).
- 24x7 availability note: added a bracketed note that 24x7 is aligned to service
  hours across all locations and the central site, and applies where the customer
  selects the extended operations option.

**Do not carry:** "consultation quality trend" (sector-specific); the source's
telemedicine examples verbatim (specialty queues, consultation media) — only the
de-sectorized forms above.

---

## Pattern 8 — Out-of-scope: merge richer generic clauses

**Before:** 33 out-of-scope bullets, near-verbatim across prior proposals.

**After:** merged in additional generic clauses from the source without
duplicating existing ones. New/extended bullets added:

- "The availability, throughput, latency or quality of customer-provided access
  services, and any service credit arising from their failure."
- "Design, survey, installation or upgrade of last-mile access, including satellite
  terminal installation, alignment and commissioning."
- "Any communication, negotiation, fault escalation or SLA management with ISPs,
  carriers or satellite operators on the customer's behalf."
- "Adding any NVR or DVR to the platform-NVR."
- "Adding any analogue cameras to the platform-NVR, unless confirmed per design."
- "Procurement of any telephony numbering, VoIP or data-service licenses and
  regulatory permits."

**Watch for:** the source's out-of-scope list had some bullets that overlap
verbatim with existing bullets (e.g. "any activity not mentioned explicitly in
the in-scope activities"). When merging, keep one copy, not two.

---

## Pattern 9 — Assumptions: merge Telemedicine generic clauses

**Before:** general assumptions + customer responsibilities + DeviceX-specific
assumptions + dependencies + risks + mutual cooperation.

**After:** the source's assumptions are largely already present in generic form.
The main additions were:

- The mutual-cooperation clause was already present — confirmed consistent.
- The "configured software not subject to customer acceptance" clause was already
  implied — flag for Basem/legal as a likely standard VertoWave clause.
- The 12-month expiry clause — already present in validity module; confirmed
  consistent.
- The source's multi-location/regulatory assumptions (customer holds all licenses
  and regulatory approvals per location; confirms cross-border data flow is
  permitted; responsible for customs/clearance/logistics; notifies vendor of
  encryption/lawful-interception/numbering restrictions during envisioning; procures
  at least one access service per site before build, second independent service for
  resilience) — these are generic enough to fold in as a "multi-location
  assumptions" sub-section, de-sectorized from "four countries / Dubai / clinical
  data".

**Held in reserve:** the source's full customer-responsibility list and risk
register — the structure is reusable; the specific wording is proposal-flavoured.
Recommend folding the structure into the RAID-log / customer-responsibility area
as a format example, not copying the Telemedicine-specific risk wording.

---

## Pattern 10 — New module candidates (deferred to Basem)

Three content blocks from the source are reusable but don't fit any existing
module. Do not create these without Basem's approval:

1. **Platform security architecture / attestation module** — the zero-trust /
   hardware root of trust / secure boot / FDE / machine MFA / continuous
   attestation / short-lived credentials / cryptographic standards summary /
   security posture comparison content. Currently folded into SDX Operations
   (Pattern 6) as a holding position.

2. **Extended security services catalog + three delivery modes module** — the
   IAM/PAM/WAF-DDoS/KMS-Vault/CSPM/DLP/backup-DR/EDR/penetration-testing/
   security-assurance catalog, plus the Native/Integrated/Assured delivery-modes
   table and the scope-boundary bullets. Reusable as an optional-services
   catalog; do not hard-code it as included.

3. **Compliance-response methodology module (C/S/CC/TP/AS codes)** — the
   5-code response framework (Compliant–DeviceX / Compliant–StackX / Compliant
   on Configuration / Compliant–Third-Party Integration / Compliant–Assurance &
   Supervision), the "delivery mechanism for every control" principle, and the
   two universal dependencies (customer's application; carrier contracts) that fall
   outside any compliance code. Reusable as a compliance-response template; actual
   C/S/CC/TP/AS counts per bid must come from the real requirements document.

---

## Verification after applying enrichment patterns

After enriching modules using these patterns:

1. Re-run the two-pass audit from the integration playbook (client/sector grep
   + sentence-level dedup).
2. For each enriched module, confirm the new content is generic and non-
   repetitive with other modules.
3. Rebuild both modes; confirm 0 unresolved non-section tokens.
4. If a new module was created, confirm it is registered in
   `module_index.json` and picked up by the combine script.
5. Confirm the TOC field is still wired (enrichment edits are in module .md
   files, not in combine.py, so the TOC wiring should be unaffected — but
   confirm after rebuild).
