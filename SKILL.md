# Proposal Template — DeviceX/SDX & StackX (VertoWave)

**Use when:** issuing a new DeviceX/SDX and/or StackX technical proposal for an Egypt/GCC enterprise or government customer.

**What this skill provides:**
- A library of **modular Markdown source files**, one per capability module (DeviceX/SDX edge layer + StackX control/SOC/operations layer + cross-cutting sections).
- A **module registry** (`module_index.json`) mapping each module to its token name, source file, and group.
- A **combine script** (`combine.py`) that selects modules + a customer-values JSON and assembles a Word `.docx` — either a complete filled proposal, or a docx template with `{{module_…}}` tokens left in place for per-bid manual fill.
- A **token-based docx template** with document metadata, classification, change-history, customer slots, and `{{module_…}}` placeholders.

**Product lineage (internal):**
- **SDX** = the platform/software layer.
- **DeviceX** = SDX installed on specific hardware (branded appliance — "Branch-in-a-Box", "School-in-a-Box").
- **StackX** = the management, orchestration, observability, automation, ITSM, compliance, and SOC platform layer above/around DeviceX/SDX.

**Rule:** This is a *technical* proposal template. Pricing is out of scope — no pricing section is generated. Pricing is attached manually per Bid Office rules.

**Source material:** module content is derived from prior VertoWave proposals (EGYCash DeviceX V1, ECMI DeviceX v06, CPC DeviceX v03, 30-June Schools DeviceX v3, MOE StackX+DeviceX v3). Treat as reusable building blocks — validate against the current customer's RFP/ITB before issuing.

## Workflow

1. **Validate value-token coverage (pre-flight).** Before assembling in
   `--mode complete`, enumerate every `{{customer_*}}` token that appears in the
   selected module Markdown and confirm each has a matching key in the values
   JSON. Any token with no value key leaks as literal `{{...}}` text into the
   assembled docx. A quick scan:

   ```
   python3 - <<'PY'
   import json, re, glob
   values = json.load(open("values-<customer>.json"))
   used = sorted(set(
       m.group(1)
       for f in glob.glob("modules/**/*.md", recursive=True)
       for m in re.finditer(r"\{\{customer_(\w+)\}\}", open(f).read())
   ))
   missing = [k for k in used if k not in values]
   print(f"customer_* tokens used: {len(used)}; values keys: {len(values)}")
   print(f"MISMATCH ({len(missing)}): {missing}" if missing else "OK — all customer_* tokens resolved")
   PY
   ```

   If the scan reports a mismatch, fix the gap before assembling — add the
   missing key to the values file if the slot is intentional, or remove/neutralise
   the token if it was introduced accidentally. Do not assemble until the scan is
   clean. (This is a separate gate from module-token resolution; a missing
   `customer_*` key is not a missing module and may slip past module-only checks.)

2. Create a customer-values JSON (`values-<customer>.json`) with the slots from
   `module_index.json` → `customer_slots`.
2. Decide which modules to include (edit the module list, or pass `--modules` to the script).
3. Run the combine script to produce either a complete docx or a token-template docx.
4. Review the output docx; replace any remaining `{{...}}` tokens; validate with `docx_validate.py`.
5. Price separately (outside this skill) and attach manually.

## Combine script

`combine.py` reads:
- `module_index.json` (registry)
- one or more module markdown files (selected via `--modules` or the index default)
- a customer values JSON (`--values`)

and writes a `.docx`.

Markdown → docx is a **basic conversion**: level-1/2/3 headings, paragraphs, bullet lists, numbered lists, and simple tables. It is not a full markdown renderer — complex markup should be simplified in the source modules.

## Module authoring contract

Every module is a single Markdown file under `modules/<group>/`. The file follows a fixed two-part structure:

1. **Leading metadata block (non-negotiable, stripped on assembly)**
   The first lines after the `# <Title>` heading MUST be the token, group, and required metadata, formatted as bold inline labels followed by a colon, e.g.:

   ```md
   # SD-WAN

   **Token:** `{{module_sdwan}}`
   **Group:** DeviceX/SDX — Edge & Branch Layer
   **Required:** No (optional add-on)
   ```

   The metadata labels are: `Token`, `Group`, `Required`. Additional labels the script strips are `Present in`, `To be authored`, `Sub-components`, `Note`, `Format`, `Duration`, `Attendees`, `Audience`, `Focus`, `Overview`. Use these for module notes and placeholders.

   The metadata block is closed by a horizontal rule `---`. The combine script strips the entire metadata block (including the `---`) in **complete mode** so the module body inserts cleanly. **Do not put body content between the title and the `---`** — it will be stripped.

2. **Body content (assembled into the docx)**
   After the `---`, write the actual proposal content in clean markdown. Keep it bid-validatable: flag assumptions, placeholders, and "confirm per bid" notes explicitly. Use `*[Note: ...]*` italic paragraphs for per-bid guidance.

3. **Out-of-Scope subsection (recommended for every module)**
   End each module with an explicit `## Out-of-Scope (explicitly)` list drawn from the relevant prior proposal. This keeps scope boundaries consistent across assembled proposals.

**Inline formatting limit:** the converter renders `**bold**` by stripping the markers (the text becomes clean, not bold — a known limitation). Do not depend on inline bold for meaning in assembled output. If emphasis matters, use a heading or a labeled paragraph instead.

**Placeholder modules:** modules whose source content has not yet been authored from the MOE appendix (e.g. `module_stackx_trueview`, `module_stackx_idm`, `module_stackx_backup`, `module_stackx_ops_config_mgmt`, `module_stackx_network_ops`, `module_stackx_alm`, `module_stackx_compliance`, `module_stackx_ops_integrity`, `module_stackx_call_center`) are shipped as placeholders with the `**Present in**` and `**To be authored**` metadata. Do not include a placeholder in a live proposal without completing the content and an SME review.

## Assembly modes

`combine.py --mode` selects one of two outputs:

- **`--mode complete`**: each selected module's body is inserted in place of its token. Customer-value tokens (`{{customer_name}}`, `{{proposal_date}}`, etc.) are filled from the values JSON. Module metadata blocks are stripped. Use this to produce a near-final technical proposal for review.

- **`--mode template`**: each selected module appears as a bold placeholder line `{{module_…}}  <!-- replace with module content -->` under a "Module: <name>" heading, plus a Module Selection Checklist appendix. Customer-value tokens are also left in place. Use this to produce a reusable token-based docx template that a bid writer fills per bid.

If `--modules` is omitted, all 36 tokens in `module_index.json` are used (9 DeviceX/SDX + 17 StackX + 10 cross-cutting). Required modules omitted from `--modules` trigger a NOTE (not a failure). Unknown tokens trigger a WARNING. A module whose source file is missing in complete mode leaves the token unresolved and produces a WARNING; the docx is still written.

## Module groups

- **devicex_sdx** — DeviceX/SDX edge & branch layer modules (SD-WAN, Firewall, NVR, IP-PBX, SASE, Network Services, Virtualization, Business Workloads, SDX Operations).
- **`stackx`** — StackX control/orchestration/SOC/operations modules (the 17 modules from the MOE license coverage list, including the standalone `module_stackx_security` module added post-integration).
- **cross_cutting** — reusable sections: cover/exec summary scaffolding, assumptions, dependencies, out-of-scope, change request procedure, PM methodology, OLA template, training, roles & responsibilities, validity clause, document control.

## Tokens

Two token families:
- **Customer/value tokens** e.g. `{{customer_name}}`, `{{rfp_reference}}`, `{{proposal_date}}` — filled from the values JSON or left for manual fill.
- **Module tokens** e.g. `{{module_sdwan}}`, `{{module_stackx_soc}}` — replaced by the assembled module content when building a complete proposal; left as placeholders when building a template.

## Directories

- `modules/devicex/` — DeviceX/SDX modules (Markdown).
- `modules/stackx/` — StackX modules (Markdown).
- `modules/cross_cutting/` — cross-cutting sections (Markdown).
- `templates/proposal_template.docx` — the token-based docx template.
- `references/module_authoring.md` — module authoring contract and metadata-block rules.
- `references/enrichment-patterns.md` — worked before/after examples from folding a richer source proposal into existing modules.
- `references/integration-playbook.md` — how to fold a new source proposal into the modular template without reintroducing client/sector specificity or repetition.
- `references/orphan-value-tokens.md` — worked analysis of the value-token coverage trap: how missing `{{customer_*}}` keys leak as literal text into assembled docx, with the pre-flight scan and this session's concrete before/after.
- `combine.py` — the assembly script (complete and template modes).
- `module_index.json` — module registry (tokens, files, groups, required flags, notes).
