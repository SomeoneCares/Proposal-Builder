---
name: proposal-template
description: >
  Assemble DeviceX/SDX & StackX proposal docx from modular markdown.
version: 1.1.0
category: productivity
metadata:
  hermes:
    tags: [proposal, template, docx, devicex, stackx, modular, vertowave]
    category: productivity
    related_skills: [docx, pdf]
author: Nous Research
license: MIT
---

# Proposal Template — DeviceX/SDX & StackX (VertoWave)

## User Preference — Conversational Proposal Workflow

For this customer (VertoWave / Basem), proposal authoring is done
**conversationally, without running tools**, unless the user explicitly asks
for a script run or file write.

**Default mode:**

- The agent gives the user structured options, numbered slots, and draft text
  inline in the chat.
- The user fills in numbers, confirms or changes the structure, and supplies
  any missing data (numbers, logos, image decisions, etc.).
- At the end, the agent constructs the final section(s) and sends them to the
  user here in the chat — as text, not as a file — unless the user asks for a
  file.

**Specifically:**

- Do **not** default to extracting docx/PDF text with scripts, running combine
  builds, or producing docx files as the first move.
- When a user says "i want to rely on my bid office", "i want to chat with
  you", or "i do not want to run commands or tools", treat this as a
  binding workflow preference: go conversational. Offer options, wait for
  selection/data, then assemble the text.
- Image extraction/embedding is **deferred by default** when the user says so,
  and the agent should instead insert **image-placement guidance blocks** into
  the relevant modules — describing what image belongs where, the inclusion
  rule, and source candidates — so the bid team can drop images in later.
- Logo insertion is also deferred behind placeholders unless the user supplies
  the actual logo image file *and* asks for embedding.

**When tools are still appropriate (explicit user ask):**

- The user explicitly asks for a script run, a file write, a build, or an
  extraction — then use the proposal-template skill's combine/build scripts or
  the docx skill's scripts as requested, and report results.
- If a task genuinely cannot be done without a tool (e.g. real image
  extraction from a binary), say so plainly and give the user options rather
  than inventing one.

This preference is about **how the work is done**, not about what the
proposal contains. The module content, token conventions, genericity rules,
and de-sectorization mappings in this skill still apply.

> Tip: if the user ever asks for tools again, that's a one-off override, not
> a change to this preference — do not re-read it as a reopening of the
> default.

- **Module registry** (`module_index.json`): 35 modules across 3 groups
  (DeviceX/SDX edge layer, StackX control/SOC/operations layer, cross-cutting
  sections), each with a token, source file path, name, required flag, and notes.
- **Markdown module sources** in `modules/devicex/`, `modules/stackx/`,
  `modules/cross_cutting/` — one `.md` per capability, reusable across bids.
- **Combine script** (`combine.py`): assembles a Word `.docx` from selected
  modules + a customer-values JSON. Two modes:
  - `--mode complete` — resolves `{{module_*}}` tokens to full module content +
    `{{customer_*}}` tokens from values → ready-to-issue proposal.
  - `--mode template` — keeps all tokens as placeholders → token-based template
    for per-bid manual fill.
- **Token-based docx template** (`templates/proposal_template.docx`): styled
  empty shell with classification header, page-number footer, document metadata,
  and all built-in styles the converter needs.
- **Image-guidance helpers** (`scripts/insert_image_guidance.py`,
  `scripts/insert_section_guidance.py`): insert **image-placement guidance
  blocks** at the center of module `.md` files. The first script handles
  module-specific guidance for DeviceX/SDX, StackX, and cross-cutting sections
  with a known candidate image; the second backfills a generic guidance block
  into any `section_*.md` still missing one. Both use
  `Path(__file__).resolve().parents[1]` for the skill root (the `parents[1]`
  fix — see pitfalls). The guidance blocks are **text-only reminders** for the
  docx-editor stage; combine.py remains text-only — actual image embedding and
  logo insertion happen when building a specific proposal, not by the script.
- **Image-guidance helpers** (`scripts/insert_image_guidance.py`,
  `scripts/insert_section_guidance.py`): insert **image-placement guidance
  blocks** at the center of module `.md` files. The first script handles
  module-specific guidance for DeviceX/SDX, StackX, and cross-cutting sections
  with a known candidate image; the second backfills a generic guidance block
  into any `section_*.md` still missing one. Both use
  `Path(__file__).resolve().parents[1]` for the skill root (the `parents[1]`
  fix — see pitfalls). The guidance blocks are **text-only reminders** for the
  docx-editor stage; combine.py remains text-only — actual image embedding and
  logo insertion happen when building a specific proposal, not by the script.
- **Enrichment patterns** (`references/enrichment-patterns.md`): worked
  before/after examples of folding a richer source proposal into existing
  modules — SD-WAN steering matrix, firewall micro-segmentation, NVR operating
  pattern, IP-PBX call-flows table, virtualization continuity, SDX Operations
  zero-touch + attestation, OLA enrichments, de-sectorization mappings, and the
  three deferred new-module candidates.

**Product lineage (internal):**

- **SDX** = the platform/software layer.
- **DeviceX** = SDX installed on specific hardware (branded appliance —
  "Branch-in-a-Box", "School-in-a-Box").
- **StackX** = the management, orchestration, observability, automation, ITSM,
  compliance, and SOC platform layer above/around DeviceX/SDX.

**Rule:** This is a *technical* proposal template. Pricing is excluded by design
— no pricing section is generated. Pricing is attached manually per Bid Office
rules. Never assert certifications or compliance claims not validated for the
current engagement.

**Source material:** module content is derived from prior VertoWave proposals
(EGYCash DeviceX V1, ECMI DeviceX v06, CPC DeviceX v03, 30-June Schools
DeviceX v3, MOE StackX+DeviceX v3). Treat as reusable building blocks — validate
against the current customer's RFP/ITB before issuing. Keep modules **generic**:
no client names, no sector-specific site/datacentre references, no prior-customer
history in body text.

## Workflow

1. Copy `values-example.json` → `values-<customer>.json` and fill in the slots
   (customer name, date, engagement name, exec-summary narrative, proposal
   version/status/author, etc.).
2. Decide which modules to include (edit the module list, or pass `--modules` to
   the script). All 35 are the default.
3. Run the combine script to produce either a complete docx or a token-template
   docx.
4. Review the output docx; replace any remaining `{{...}}` tokens; validate with
   `docx_validate.py` if available.
5. Pricing separately (outside this skill) and attach manually.

## Combine script

`combine.py` reads:

- `module_index.json` (registry)
- one or more module markdown files (selected via `--modules` or the index default)
- a customer values JSON (`--values`)

and writes a `.docx`.

Markdown → docx is a **basic conversion**:

- `#` / `##` / `###` → Heading 1 / 2 / 3
- `-` / `*` bullet lines → List Bullet
- `1.` numbered lines → List Number
- `|` table rows → a Word table (first row bold as header)
- blank lines separate paragraphs
- everything else → Normal paragraph

**Logo embedding:** combine.py accepts an optional `--logo <path>` flag. When given, the script embeds the logo image into the cover page — searching the assembled document for the first paragraph containing a `[VERTO WAVE LOGO` or `[LOGO` placeholder marker and replacing that paragraph with the picture (centered, max width 3.5 in). If no placeholder paragraph is found, the picture is inserted at the start of the document body. If the file does not exist or cannot be read, the embed is skipped and a status line is printed on stdout (`LOGO: ...`). This is the supported way to put the Verto Wave logo onto a built proposal cover page — the logo file should be the approved public logo (e.g. `assets/vertowave_logo.png`, downloaded from the Verto Wave website — see the logo sourcing technique in `references/image-guidance.md`), confirmed with the Verto Wave brand/marketing team before issue.

**Limitations:**

- No inline formatting beyond stripping `**bold**` markers (no real bold runs).
- Complex markdown (nested lists, blockquotes, images, links) is not rendered.
- Tables are basic pipe tables only.
- If a referenced module file is missing in `--mode complete`, the token is left
  unresolved and a warning is printed — the docx is still produced.

## Module groups

- **devicex_sdx** — DeviceX/SDX edge & branch layer modules (SD-WAN, Firewall,
  NVR variant A/B, IP-PBX, SASE, Network Services, Virtualization, Business
  Workloads, SDX Operations). SD-WAN is the core; others are optional add-ons.
- **stackx** — StackX control/orchestration/SOC/operations modules (16 modules
  from the MOE license coverage list: Endpoint Mgmt, Automation/Orchestration,
  Observability/APM, TrueView, IDM, Backup, Ops/Config Mgmt, Network Ops, ITSM,
  ALM, Compliance, Ops Integrity, Call Center, Event/Log Mgmt, SOC composite,
  DevOps).
- **cross_cutting** — reusable sections: cover/exec summary scaffolding,
  assumptions, dependencies, out-of-scope, change request procedure, PM
  methodology, OLA template, training, roles & responsibilities, validity clause,
  document control.

## Tokens

Two token families:

- **Customer/value tokens** e.g. `{{customer_name}}`, `{{rfp_reference}}`,
  `{{proposal_date}}` — filled from the values JSON or left for manual fill.
- **Module tokens** e.g. `{{module_sdwan}}`, `{{module_stackx_soc}}` — replaced by
  the assembled module content in complete mode; left as placeholders in template
  mode.

## Exec-summary narrative slots (complete mode)

The exec-summary module (`section_cover_execsummary`) carries `[PROSE]` narrative
fill-in slots that the combine script resolves from the values JSON where possible
(`esg_footprint`, `esg_value_1`, `esg_value_2`, `esg_outcome`, `esg_example_a`,
`esg_example_b`, `scope_services_description`, `deployment_context`, `objective_1`,
`objective_4`, `objective_5`). Any slot not in the values JSON stays as a
`{{...}}` placeholder. The proposal author must still write the genuine narrative
prose per bid — the scaffolding does not auto-generate the executive summary.

## TOC (Table of Contents)

Both assemble modes insert a Word auto-updating **Table of Contents field**
(`TOC \o "1-3" \h \z \u`) plus a `w:updateFields val="true"` settings flag so
Word refreshes fields on open. The TOC collects Heading 1..3 entries with page
numbers. If entries are missing on open, right-click the table and choose "Update
Field" → "Update entire table".

Note: the TOC field placeholder text shows until the field is updated in Word.
PDF preview or non-Word viewers will show the placeholder, not a populated TOC.

## Directories

- `modules/devicex/` — DeviceX/SDX modules (9 `.md` files).
- `modules/stackx/` — StackX modules (17 `.md` files — includes `module_stackx_security.md`).
- `modules/cross_cutting/` — cross-cutting sections (10 `.md` files — includes `section_professional_services.md`).
- `templates/proposal_template.docx` — the token-based docx template shell.
- `scripts/cleanup_notes.py` — batch-cleanup helper for module notes.
- `scripts/insert_image_guidance.py` — insert module-specific image-placement
  guidance blocks at the center of module `.md` files (DeviceX/SDX, StackX,
  cross-cutting sections with a known candidate image).
- `scripts/insert_section_guidance.py` — backfill a generic image-placement
  guidance block into any `section_*.md` still missing one.
- `write_module.py` — scaffold + register a new module.
- `references/integration-playbook.md` — audit workflow, de-sectorization
  mappings, repetition watch-list, enrichment priorities, new-module decision
  points.
- `references/enrichment-patterns.md` — worked before/after enrichment examples.
- `references/image-guidance.md` — generic-only rule, guidance-block structure,
  per-module candidate-image table (with source refs + genericisation notes),
  Verto Wave logo sourcing technique, cover-page logo placement, script-path
  pitfall.

## Avoiding repetition

- Each module owns its own **Out-of-Scope** block — this is the standard
  exclusion boundary and is intentionally repeated across modules (near-verbatim
  across all 25 modules). Do not delete these; they are the contractual boundary.
- **Do not duplicate capability descriptions across modules.** If two modules
  cover overlapping surface area (e.g. SD-WAN security integration vs Firewall
  security posture), write each from its own layer's angle and avoid restating the
  other's capability list.
- **Module intros must be distinct.** Do not copy the same 3-sentence intro
  paragraph across modules (this was a bug — Virtualization and Business
  Workloads once shared a verbatim intro).
- The **canonical Out-of-Scope list** lives in
  `modules/cross_cutting/section_out_of_scope.md`. When writing a new module's
  out-of-scope block, mirror it rather than inventing a variant — but keep the
  module's own block (the contract is per-module).

## Keeping modules generic

- No client names (EGYCash, ECMI, CPC, 30-June Schools, MOE) in body text.
- No sector-specific site/datacentre references (October, Roxy, RDH, Educational
  City) in body text.
- No prior-customer history ("Present in EGYCash/ECMI/CPC/30-June/MOE proposals")
  — replace with generic "Include when X is in scope for the current engagement."
- Module final italic notes should say **when to include**, not **where it came
  from**.
- StackX placeholder modules (to-be-authored) should reference "a prior proposal
  appendix" generically, not "MOE proposal Appendix 5.x".
- The working-week assumption should be "mutually agreed local working days"
  rather than hard-coded to a specific country's Sunday-Thursday/Egypt-holidays
  pattern, unless the bid is country-specific.
- NVR reference parameters (retention days, MP, FPS, Kbps) should be framed as
  "confirm per design", not carried from a prior engagement.

## Verification

- **Complete build (all 35 modules):** confirm ~109k chars, ~1000+ paragraphs,
  ~7 tables, **0 unresolved non-section tokens**.
- **Template build:** confirm ~46 intentional placeholders, all correct.
- **All required modules present** in the complete build.
- **No client/sector contamination:** grep all module files for client/sector
  names — should be CLEAN (internal sub-option labels like "Variant A/B" are
  fine; they are not client references).
- **TOC field present** in the docx settings (check `w:updateFields` and the
  `TOC` instrText).

## Adding a new module

Use `write_module.py`:

```
python write_module.py --token module_foo --name "Module Foo" \
    --group stackx [--required] [--notes "optional notes"]
```

The script creates `modules/<group>/module_foo.md` with a minimal skeleton
(token/group/required/notes header + placeholder Overview + Out-of-Scope) and
registers the token in `module_index.json`.

For content-backed modules (especially StackX placeholders that should be authored
from a prior proposal appendix), replace the skeleton body with the sourced
content and remove the "to be authored" markers before including in a live bid.

## Cleanup helper

`scripts/cleanup_notes.py` batch-rewrites:

- DeviceX module final italic notes → generic "Include when X is in scope."
- StackX placeholder "MOE proposal Appendix 5.x" references → generic "a prior
  proposal appendix" framing.

Run from the skill root:

```
python scripts/cleanup_notes.py
```

It prints a final contamination scan; should report CLEAN.

## Image-guidance workflow

When a proposal module should carry a diagram or screenshot, insert an
**image-placement guidance block** at the center of the module `.md` file
(before issue). The block is a text-only reminder for the docx-editor stage —
combine.py assembles text only; actual image embedding is done when building the
specific proposal docx.

Standard guidance-block structure:

```
## Figure — <descriptive name>

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: <what kind of diagram/screenshot> -->
<!-- Suggested source: <proposal section / figure ref> — genericise, strip customer labels -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: use combine.py --logo <path> when building the proposal docx; combine.py embeds the image into this figure block's paragraph (centered). Do not embed vendor product screenshots unless the current bid explicitly uses that product. -->

*[Figure placeholder — insert approved generic <name> diagram here. See image-placement guidance notes.]*
```

Insert at the center of the file: find the line closest to the middle, then pick
the nearest blank line within ~12 lines (forward first, then backward) and insert
the block there.

Run from the skill root:

```
python scripts/insert_image_guidance.py
python scripts/insert_section_guidance.py
```

The first script covers DeviceX/SDX + StackX + the cross-cutting sections that
have a known candidate image; the second fills any `section_*.md` still missing
one with a generic block.

### Generic-only rule

Every image placed in a proposal module must be **generic**:

- No customer name, customer-specific environment, architecture, site names, or
  branding.
- If reusing an image from a prior proposal, strip customer-specific labels before
  use.
- If an image's caption references a specific customer context (e.g. "clinic",
  "Dubai management plane", "October site", "telemedicine workstation",
  "examination camera"), that image is **not** reusable as-is — genericise the
  diagram or drop it.
- Vendor UI screenshots from prior proposals are composition references only —
  produce or source a generic / Verto-Wave-branded equivalent for the issue copy.

### Candidate images per module

The full per-module candidate-image table — with source references and
genericisation notes for each — lives in `references/image-guidance.md`. When
inserting guidance for a module, use that table to pick the recommended image and
the stripping note.

### Logo sourcing (Verto Wave website)

The Verto Wave public website (`https://www.vertowave.com/`) is a **Framer
single-page site** — the logo is not in static HTML; it is rendered by JavaScript
into the nav ("Logo/Menu Items" component). To find and download it:

1. Fetch the homepage HTML with a browser-like User-Agent.
2. Locate the nav component: search the HTML for `data-framer-name="Logo/Menu Items"`.
3. Inside that component, the logo `<img>` tag carries `width="307" height="65"`
   and a `src` pointing to a `framerusercontent.com` image (e.g.
   `https://framerusercontent.com/images/9aSgY9nMAwJbNTDBJAJzimNEE.png`).
4. Download that image directly (it is a public, hotlinkable asset on
   framerusercontent.com).
5. Verify with a vision check that it is the actual Verto Wave logo (dark teal
   background, "VERTO WAVE" text + sound-wave icon) before using it in a proposal.
6. Save to the skill's `assets/` directory (e.g. `assets/vertowave_logo.png`).

Caveats:

- Direct guesses at `/images/logo.png`, `/logo.svg`, `/public/logo.png`,
  `/assets/logo.png` return 404 — the logo is referenced by a hashed filename in
  the nav component, not by a stable logo path.
- The homepage also carries many `framerusercontent.com/images/*.png` section
  photos (hero, customers, etc.) — most are decorative section imagery, not the
  logo. Confirm by vision before using any of them as a logo.
- Third-party pages (e.g. OpenText customer spotlight) carry their own logos, not
  Verto Wave's official logo — use only as a brand reference, not as the logo file.

### Cover-page logo placement

The cover page module (`section_cover_execsummary`) carries:

- A primary logo placeholder line: `[VERTO WAVE LOGO — INSERT LOGO IMAGE HERE]`
- An optional secondary-logo placeholder line
- Logo placement notes telling the bid team to insert the approved logo image
  (e.g. `assets/vertowave_logo.png` or the brand-team-approved file) manually
  before issue.
- A rule: do not use a logo image that is not the approved Verto Wave logo; do
  not carry a logo from a prior proposal's customer-specific cover page; logo
  images are inserted manually per bid (not auto-embedded by combine.py).

When building a specific proposal, drop the approved logo file into the
cover-page logo slot in the docx. The logo file in `assets/vertowave_logo.png`
is the downloaded public logo — confirm with the Verto Wave brand/marketing team
that it is the approved version before issue.

## Content integration

Folding a new source proposal into the module system while keeping
everything generic and non-repetitive — audit workflow, de-sectorization
mappings, repetition watch-list, enrichment priorities, and new-module
decision points — is captured in `references/integration-playbook.md`.

## Sample values file

`values-example.json` is a working sample with all currently-used customer/value
slots filled. Copy it and edit per bid. Slot set includes:

- `customer_name`, `customer_short`, `rfp_reference`, `proposal_date`,
  `prepared_by`, `customer_primary_contact`, `engagement_name`, `site_count`,
  `compliance_frameworks`, `validity_period_months`, `effective_date`,
  `devicex_qty_note`
- Exec-summary narrative slots: `esg_footprint`, `esg_value_1`, `esg_value_2`,
  `esg_outcome`, `esg_example_a`, `esg_example_b`, `scope_services_description`,
  `deployment_context`, `objective_1`, `objective_4`, `objective_5`
- Document-control slots: `proposal_version`, `proposal_status`,
  `proposal_date_iso`, `author_name`

## Pitfalls captured from this session

**cleanup_notes.py path bug:** the script set `SKILL_ROOT = Path(__file__).resolve().parent`, which resolved to `scripts/` instead of the skill root. Result: DeviceX modules were skipped (wrong dir) and the final scan reported a false "CLEAN" on an empty glob. Fix: `SKILL_ROOT = Path(__file__).resolve().parents[1]`. Always print the paths the script operates on and a final scan with the actual glob it used.

**insert_image_guidance.py path bug:** same root cause — `SKILL_ROOT = Path(__file__).resolve().parent` resolves to `scripts/`, not the skill root, so the module glob matched nothing and the script reported "Total modules updated: 0". Fix: `SKILL_ROOT = Path(__file__).resolve().parents[1]`. Always print `SKILL_ROOT` and the glob at the top of the script when debugging a "didn't touch anything" result.

**Repetition audit technique:** a good repetition scan is (1) grep for client/sector names first (fast, catches the obvious contamination), then (2) a sentence-level dedup scan on body text only (catches accidental copy-paste intros and duplicate capability blocks). Do both — client-name grep alone misses non-name repetition like the Virtualization ↔ Business Workloads verbatim intro.

**TOC wiring:** the `add_toc_field` + `set_update_fields_on_open` helpers existed but weren't called in either assembler or `main()`. When adding both-hands-needed helpers (insert field + set settings flag), wire both in one pass into each call site: complete assembler, template assembler, and `main()` before save. Verify by inspecting the saved docx XML for `w:updateFields` and the `TOC` instrText — don't assume the call landed.

**"Present in X proposals" notes vs body text:** client/sector contamination comes in two forms — body-text references (must be removed, e.g. MOE SOC overview, Educational City NOC example) and module-note references (should be genericized, e.g. "Present in EGYCash/30-June proposals" → "Include when X is in scope"). Both need the same class of cleanup, but body-text fixes are content rewrites while note fixes are one-line replacements. The cleanup script only handled notes; body-text fixes were done by separate targeted patches. Keep both paths documented.

**TOC for non-Word viewers:** the TOC field shows placeholder text until updated in Word. PDF preview / non-Word viewers show the placeholder, not a populated TOC. If a proposal must ship with a visible TOC in all viewers, the TOC needs to be rendered/updated externally (e.g. LibreOffice headless update) — not just the field inserted.

**Image guidance insertion — center-point tolerance:** "at center" means the blank line nearest the file's midpoint, within a ~12-line forward-then-backward window. If a module has no blank line in that window, insert at the midpoint line itself. Don't require an exact center line — that produces awkward splits mid-paragraph. Always re-scan after insertion to confirm every module got exactly one guidance block (a duplicate means the insertion point landed on a line that already had one).
