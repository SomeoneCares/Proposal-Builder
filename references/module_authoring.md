# Module Authoring Contract

How to write a module `.md` under `modules/<group>/` so `combine.py` renders it
correctly. `write_module.py` creates a file in this shape and registers it.

## File structure

```
# <Human-readable Module Title>

**Token:** `{{module_<token>}}`
**Group:** <group label>
**Required:** Yes | No (<when to include it>)
<optional: **Note:** / **Present in:** / **To be authored:** ...>

---

<body>
```

- The title line and the metadata block are required. The block ends at the first
  `---` line; everything in it is dropped from the proposal.
- The `# Title` becomes the module's Heading 1 (the cover module hides it via
  `"show_title": false` in `module_index.json`).
- Other `---` lines are horizontal rules in the source only; they are not rendered.

## What the converter renders

| Markdown | In the .docx |
| --- | --- |
| `#`, `##`, `###` | Heading 1–3 (these build the table of contents) |
| `#! text` | Title style — cover page only |
| `\newpage` alone on a line | Page break |
| `- item` / indented `- item` | Bullets, two levels |
| `1. item` | Indented numbered line (the number is kept as written) |
| `| a | b |` tables | Word table; a `| --- |` separator row marks the first row as a bold header |
| `**bold**`, `*italic*`, `` `code` `` | Bold, italic, plain text |
| `> text` | Plain paragraph |
| `<!-- ... -->` | Never rendered (use for image guidance and author comments) |

Links, images, nested tables and deeper list levels are not supported.

## Bid-team material

Content meant for the bid team, not the customer, must be marked so that an issue copy
removes it (a draft keeps it, highlighted yellow):

- **Notes:** a whole paragraph in italics — `*[Note: confirm the response times per bid.]*`
  or a closing `*This module is a reusable building block ...*` line. A whole
  paragraph in `**[...]**` also counts.
- **Sections:** a heading containing `(for the bid team)`, e.g.
  `## Logo Placement Notes (for the bid team)`; everything under it up to the next
  heading of the same or higher level is bid-team material.
- **Figure placeholders:** a `## Figure — <name>` heading followed by `<!-- -->`
  guidance and a `*[Figure placeholder — ...]*` note. Place it at a section boundary,
  never between a heading or a "the following ...:" sentence and its content.

Never write customer-facing text in italics as a whole paragraph — it would be removed
from the issue copy.

## Values and cross-references

- `{{slot}}` is filled from the proposal values. Every slot used in a module must exist
  in `module_index.json` → `customer_slots` and in `values-example.json` (the tests
  enforce this). Blank values render as `[TO CONFIRM: slot]` in a draft and block an
  issue copy.
- `{{module_...}}` / `{{section_...}}` in body text renders as that module's name.
  Prefer writing the name in plain words.
- Only letters, digits and underscores inside `{{ }}`; `{{training_*}}`-style
  wildcards are not tokens and will block the build.

## Keeping modules generic

- No prior-customer names, sites, sectors or dates anywhere in the file — comments
  included. `banned_terms` in `module_index.json` lists the known ones; the tests scan
  every module line and every build scans the finished document.
- Final italic notes say when to include the module, not where the text came from.
- Do not duplicate another module's capability list; write from this module's layer.
- End each module with an `## Out-of-Scope (explicitly)` list that mirrors
  `modules/cross_cutting/section_out_of_scope.md`.

## Placeholder modules

A module whose content is not authored yet carries `"placeholder": true` in
`module_index.json`. The builder labels it and warns when it is selected. Remove the flag
only after the content is written and SME-reviewed.

## After editing

Run `scripts/deploy.sh --test-only` (tests on the host) and build a draft of the modules
you touched to read the result.
