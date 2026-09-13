# Proposal Module Integration Playbook

How to fold a new source proposal into the modular template without
reintroducing client/sector specificity or gratuitous repetition.

This is a worked pattern built from merging the Telemedicine Network
Technical Proposal V1.6 into the existing 35-module system. Use it as
the template for the next integration.

## When to use

A new proposal has been uploaded and Basem wants its content folded into
the existing modules — richer detail, new capability angles, better
operating-model language — while keeping everything generic and non-
repetitive.

## Workflow

### 1. Extract + structure-read first

Extract the docx with `docx_read.py --structure` before reading text.
Get the section list, table count, and heading outline. For the
Telemedicine doc this revealed: 8 main sections, ~16 appendices, 50
tables, ~200k chars — a genuinely rich source.

Do not start patching modules before you know the source's shape.

### 2. Two-pass audit of existing modules

Pass A — client/sector grep (fast):

```
grep -rniE "EGYCash|ECMI|CPC|30-June|MOE|Ministry of Education|October|Roxy|RDH|Educational City" modules/
```

Pass B — sentence-level dedup on body text only:

Read each module's first 10-15 lines and its Out-of-Scope block. Compare
across modules. The Virtualization ↔ Business Workloads verbatim 3-sentence
intro was caught only by this pass, not by the client-name grep.

Do both passes. Pass A alone misses non-name repetition.

### 3. Triage new content into four buckets

For each piece of strong content in the new source:

- **Fold now (generic, non-repetitive, adds value)** — enrich an existing
  module in-place. Examples from this session: SD-WAN multi-path steering
  matrix, firewall micro-segmentation table, zero-touch provisioning flow,
  ITSM monitoring-to-incident workflow, OLA 4-priority model.

- **Fold now (generic, but needs a new home)** — the content is reusable
  but doesn't fit any existing module. Flag for a new module. Examples:
  platform security/attestation narrative, extended security services
  catalog, compliance-response methodology (C/S/CC/TP/AS codes).

- **Hold in reserve (proposal-specific, values-driven later)** — the
  structure is reusable but the numbers/names/scale are specific to this
  bid. Do not hard-code. Examples: hardware class A/B/C sizing table,
  training course list with attendee counts, OLA response-time numbers,
  site inventory template, deliverables-by-phase table, risk register
  format.

- **Discard / do not carry (client/sector/legal-lock-in)** — customer
  names, country names, sector framing, specific quantities, dates,
  vendor product screenshots, commercial license tables. De-sectorize
  the framing; drop the rest.

### 4. De-sectorize as you write

Do not copy-paste source sentences and clean up later. Rewrite into
generic form in the same step.

Reusable substitution patterns (from this session):

| Source phrase (strip) | Generic replacement |
| --- | --- |
| clinical / telemedicine / consultation | application / session / service |
| specialist / general practitioner | remote expert / responder |
| patient / medical records / clinical data | user / data / records |
| examination camera / medical devices | peripheral / connected device |
| Dubai / UAE / Abu Dhabi / Country 1-4 | central site / hub / data center / location |
| Africa-to-Gulf / long-haul Africa | long-haul / inter-site paths |
| clinical media / clinical quality | priority real-time media / service quality |
| clinical service hours / on-call clinical pathway | service hours / on-call pathway |
| telemedicine application / EMR | the customer's application |
| teleconsultation requirements document | the customer's requirements document |
| 27 devices / 30 endpoints / 20 servers | {{values-driven}} per bid |
| 2026-09-01 / V1.6 | {{proposal_date_iso}} / {{proposal_version}} |
| Appendix 4 / 5 / 6 / 7 / 8 | Appendix N (generic) or values-driven |

General rule: keep the *structure* and *operating logic*; drop the
*destination*, the *sector*, and the *scale*.

### 5. Maintain a repetition watch-list

When enriching existing modules from a new source, keep a running list of
overlap points and reconcile each one — do not let the new content
duplicate what's already there.

Common overlap shapes to watch for:

- **Same capability, different layer** — e.g. SD-WAN security integration
  vs Firewall security posture. Each module writes from its own layer's
  angle; do not restate the other's capability list.
- **Same narrative, different module** — e.g. a platform overview
  differentiators table could land in the exec summary OR a module. Pick
  one home.
- **Same section type, different numbers** — e.g. OLA response times
  differ across proposals. If the module is meant to be a default, pick
  one set (or make it values-driven); do not keep two conflicting sets.
- **Same section type, different length** — e.g. out-of-scope lists. Merge
  the richer generic clauses into the canonical section; keep each
  module's own block as the contractual boundary; do not maintain two
  separate out-of-scope lists.
- **Two different frameworks that look similar** — e.g. PM methodology
  (how we manage) vs delivery phasing (how we sequence the build). These
  are complementary, not duplicate; label them clearly so the reader is
  not confused.

### 6. Patch the SKILL.md if the integration reveals a new pattern

If the integration surfaces a reusable technique not yet in SKILL.md,
add it to the relevant section (usually "Keeping modules generic" or
"Avoiding repetition" or a new subsection). This session's integration
did not surface new techniques beyond what is already captured — the
cleanup path bug, TOC wiring gap, and repetition audit technique were
all already in SKILL.md. What *was* missing was the integration workflow
itself and the de-sectorization mappings — that is what the reference
file captures.

## Cleanup helper

`scripts/cleanup_notes.py` handles the note-level genericization
(module final-italic notes and StackX placeholder notes). It does NOT
touch body text — body-text fixes are separate targeted patches.

Known bug (already fixed in the script): `SKILL_ROOT` must be
`Path(__file__).resolve().parents[1]`, not `.parent`. The wrong setting
resolves to `scripts/` and produces a false CLEAN on an empty glob.

Always run from the skill root and always print the paths the script
operates on, plus a final contamination scan using the actual glob.

## Content integration decisions log (this session)

These are the decisions made during the Telemedicine integration. Use as
a reference for the next integration's decision points, not as fixed
rules.

- SD-WAN: enrich with multi-path steering matrix + transport independence.
  Biggest single win.
- Firewall: enrich with micro-segmentation table.
- NVR: enrich with local-recording pattern + centralized monitoring sizing
  as a design input (not a fixed claim).
- IP-PBX: enrich with generic call-flows table + local survivability.
- Virtualization: add continuity-by-design one-liner.
- SDX Operations: add zero-touch provisioning flow + attestation narrative
  (or create a new platform security module — decision deferred to Basem).
- Orchestration: add central-management-stack framing + vendor-agnostic
  integration builder positioning.
- Endpoint Management: substantial enrich from the Telemedicine section
  (data collection / management actions / analytics). Watch vendor product
  names (Cisco, F5, Palo Alto, Forcepoint) — keep generic or flag.
- Observability: major expansion (ELK log management + APM + synthetic +
  profiling). Decision deferred: one module or split into log-management
  + APM.
- Security: enrich with SIEM/correlation/forensics + delivery-modes table.
- ITSM: enrich with monitoring-to-incident workflow + operating workflows
  + third-party-screenshot note.
- IDM: add entity-hierarchy multi-site model (currently a placeholder).
- PM methodology: add pilot-then-parallel delivery phasing as a separate
  framework from the PM methodology (label clearly).
- OLA: enrich with 4-priority model + response times (values-driven) +
  OLA conditions + reporting note.
- Assumptions: merge Telemedicine generic assumptions + customer
  responsibility + multi-location/regulatory assumptions + discovery
  checklist.
- Out-of-scope: merge Telemedicine generic clauses into canonical section.
- Exec summary: add values-driven service-quality-targets table + generic
  platform differentiators.
- Training: add training-matrix format example (no specific courses).
- Document control: add deliverables-by-phase table + screenshot-note
  guidance.

New modules flagged for Basem's decision (do not create without approval):
- Platform security architecture / attestation module, OR fold into SDX
  Operations.
- Extended security services catalog + three delivery modes module.
- Compliance-response methodology module (C/S/CC/TP/AS codes).

Held in reserve (do not hard-code):
- Hardware class A/B/C sizing framework — reusable structure, platform-
  specific. Ask Basem whether to add as a generic device-sizing section.
- OLA response-time numbers — make values-driven, do not hardcode one set.
- Training course list — format only, no specific courses.
- Deliverables-by-phase table — generic structure, keep.
- Risk register format — generic structure, keep; drop the Telemedicine-
  specific risk wording.

Standard clauses confirmed across multiple proposals (likely VertoWave
defaults, keep generic, flag for legal/Basem review):
- "Services that include configured/installed/upgraded/implemented software
  are not subject to customer acceptance."
- 12-month expiry from Effective Date unless extended by mutual agreement.
- Customer provides all access, credentials, connectivity, backend hardware,
  licenses, regulatory approvals, customs/clearance/logistics.
- Vendor not accountable for access-service availability/performance.
- Wide-area access is a customer procurement; selecting any service does
  not alter that boundary.

## Verification after integration

After enriching modules from a new source, re-run both passes of the
audit:

1. Client/sector grep — should still be CLEAN.
2. Repetition scan — check the enriched modules do not now duplicate each
   other or the canonical sections.
3. Rebuild both modes, validate token resolution, confirm 0 unresolved
   non-section tokens.
4. If a new module was added, confirm it is registered in
   `module_index.json` and that the combine script picks it up.
