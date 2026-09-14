# Module Authoring Contract

How to write a module `.md` under `modules/<group>/` so `combine.py` renders it
correctly. `write_module.py` creates a file in this shape and registers it; the
portal's Module Library refuses to save a version that breaks these rules.

## File structure

```
# <Human-readable Module Title>

**Token:** `{{module_<token>}}`
**Group:** <group label>
**Required:** Yes | No (<when to include it>)

---

<body>
```

- The title and metadata block are required. The block ends at the first `---`
  line; everything in it is dropped from the proposal.
- The `# Title` becomes the module's numbered Heading 1 (the cover hides it via
  `"show_title": false` in `module_index.json`).
- Other `---` lines are source-only rules and are not rendered.

## What the converter renders

| Markdown | In the .docx |
| --- | --- |
| `#`, `##`, `###` | Numbered Heading 1–3 (1, 1.1, 1.1.1; appendices A, A.1) |
| `#! text` | Title style — cover page only |
| `\newpage` alone on a line | Page break |
| `- item` / indented `- item` | Bullets, two levels |
| `1. item` | Indented numbered line (the number is kept as written) |
| `| a | b |` tables | Styled table; a `| --- |` separator row marks a navy header row |
| `**bold**`, `*italic*`, `` `code` `` | Bold, italic, plain text |
| `<!-- ... -->` | Never rendered — use for diagram guidance |

## Conditional content — every point appears only when it applies

```
<!-- if module_nvr -->
... a block shown only when the NVR module is selected ...
<!-- endif -->

- a single bullet <!-- if module_ipbx or module_stackx_call_center -->
| a table row | ... <!-- if devicex --> |
## A heading <!-- if managed_services -->
```

Names usable in conditions:

- any module or section token (`module_sdwan`, `section_training`, ...)
- `devicex` / `stackx` — any module of that family is selected
- the offering: `licenses`, `services`, `managed_services`, `premier_support`
- combine with `and`, `or`, `not` and parentheses

A whole module can be tied to the offering with `"requires"` in
`module_index.json` (for example `"requires": "managed_services"` on the OLA).

## Directives

| Line | Result |
| --- | --- |
| `[[figure: slug \| Caption]]` | The image uploaded as `slug` in the Module Library (or `assets/figures/slug.png`), numbered "Figure N: Caption". Without an image: a placeholder box in a draft, nothing in an issue copy. |
| `[[scope_table]]` | Table of the selected modules and their `summary` from the registry |
| `[[compliance_matrix]]` | The RFP requirement rows entered in the builder |
| `[[glossary]]` | `glossary.json` terms that appear in the built proposal |

## Bid-team material

Content for the bid team, not the customer, is removed from an issue copy and
highlighted in a draft:

- a whole paragraph in italics — `*[Note: confirm the response times per bid.]*`
- a heading containing `(for the bid team)` and everything under it

Never write customer-facing text as a whole italic paragraph.

## Wording rules

- US spelling; the brand is **Verto Wave**.
- Use `{{customer_short}}` instead of "the customer".
- No prior-customer names, sites or sectors (`banned_terms`) and no third-party
  product names (`third_party_terms`) — describe the function instead.
- Exclusions belong only in `section_out_of_scope.md`, tagged with conditions;
  modules do not carry their own out-of-scope lists.
- Each module describes its own layer; do not repeat another module's
  capability list.
- `{{slot}}` values must exist in `module_index.json` → `customer_slots` and in
  `values-example.json`.

## Placeholder modules

A module whose content is not written yet carries `"placeholder": true`; the
builder labels it and warns when it is selected.

## After editing

Portal edits: save a new version in the Module Library (it validates the text).
Repo edits: `scripts/deploy.sh --test-only`, then build a draft of the modules
you touched.
