# Module Authoring Contract

<!--skill: proposal-template-->

Quick reference for authoring a new module `.md` under `modules/<group>/`.

## File structure

```
# <Human-readable Module Title>

**Token:** `{{module_<token>}}`
**Group:** <group label, matches module_index.json>
**Required:** Yes | No (<notes, e.g. "optional add-on">)
<optional extra labels: Present in / To be authored / Note / etc.>
---
<body content>
```

- The metadata block (title + `**Token:**` / `**Group:**` / `**Required:**` lines) is REQUIRED.
- Close the metadata block with a `---` line. Nothing substantive goes between the title and the `---` — it will be stripped in complete mode.
- After `---`, write the proposal body in clean markdown.

## Metadata labels the script strips

`Token`, `Group`, `Required` — core.

Also stripped (use for notes/placeholders): `Present in`, `To be authored`, `Sub-components`, `Note`, `Format`, `Duration`, `Attendees`, `Audience`, `Focus`, `Overview`.

## Recommended module sections

1. **Solution Overview** — what the module delivers, in proposal language.
2. **Key Capabilities** — bullet list of capabilities.
3. **Value / How it fits** — why the customer cares, where it sits in the architecture.
4. **Deployment / Build notes** — how it is delivered or configured (if relevant).
5. **Per-bid notes** — `*[Note: …]*` paragraphs flagging what must be confirmed for the current bid.
6. **Out-of-Scope (explicitly)** — scope boundary list, drawn from the relevant prior proposal.

## Inline formatting

- The converter strips `**bold**` markers (text becomes clean, not bold). Do not rely on inline bold for meaning in assembled output.
- Use headings or labeled paragraphs for emphasis that matters.

## Placeholder modules

If the MOE appendix content hasn't been authored yet, ship the module as a placeholder with `**Present in**` and `**To be authored**` metadata, and an explicit out-of-scope / to-be-authored body. Do NOT include a placeholder in a live proposal without completing the content and an SME review.

## Per-bid validation rule

Every module must carry enough "confirm per bid" notes that a reviewer can tell what was assumed vs. confirmed. Do not issue a module verbatim from a prior proposal without validating it against the current customer's RFP/ITB.

## Example module skeleton

See `templates/module_skeleton.md`.
