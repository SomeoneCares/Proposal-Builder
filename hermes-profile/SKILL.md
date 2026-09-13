---
name: proposal-template
description: >
  Build DeviceX/SDX & StackX technical proposals (.docx) for VertoWave from the modular template.
version: 2.0.0
category: productivity
metadata:
  hermes:
    tags: [proposal, template, docx, devicex, stackx, modular, vertowave]
    category: productivity
    related_skills: [docx, pdf]
author: VertoWave Bid Office
---

# Proposal Template — DeviceX/SDX & StackX (VertoWave)

## Ownership — read first

Since 2026-09-14 the code, modules and web builder are maintained by Basem in a git
repository on his PC and deployed to this host with `scripts/deploy.sh`. The deployed
copy lives in `/home/hermes/.hermes/skills/proposal-template/`.

- Do **not** edit, patch or add files in that folder. Changes there are overwritten by
  the next deploy and are not tracked.
- If a module's wording, the registry or the builder needs to change, draft the change
  in chat (quote the module file and the exact text) and tell Basem.
- Do not restart the `proposal-builder` service unless Basem asks.

## Working style with Basem

Proposal authoring is conversational unless Basem explicitly asks for a build, a file or
a script run: give structured options and numbered slots in chat, let him choose and
supply numbers, then assemble the text. Treat "I want to rely on my bid office" or "I do
not want to run commands" as binding for that task. A request for a build or a file is a
one-off, not a change of this preference.

## What the template contains

- 37 modules in `modules/`: 9 DeviceX/SDX, 17 StackX, 11 cross-cutting sections.
- `module_index.json`: module tokens, names, required/placeholder flags, notes, the value
  slots (`customer_slots`) and `banned_terms`.
- 9 StackX modules are placeholders and must not go into a live bid until authored and
  SME-reviewed: TrueView, IDM, Backup, Ops/Config Mgmt, Network Ops, ALM, Compliance,
  Ops Integrity, Call Center.
- Pricing is excluded by design; never add, calculate or alter pricing.

## Building a proposal

Preferred: the web builder at `http://192.168.100.178:8501` (fill values, tick modules,
choose Draft or Issue copy, download).

From the terminal (only when Basem asks):

```
cd /home/hermes/.hermes/skills/proposal-template
/home/hermes/.hermes/hermes-agent/venv/bin/python combine.py \
    --values <values.json> --modules <token,token,...> \
    --logo assets/vertowave_logo.png [--issue] --out <output.docx>
```

- **Draft** (default) keeps bid-team notes and figure placeholders, highlighted yellow;
  blank values appear as `[TO CONFIRM: key]` and are listed on a `TO CONFIRM:` line.
- **Issue copy** (`--issue`) removes all notes and refuses to build while any value used
  by the selected modules is blank.

## Reporting a build — rules

- The build checks the finished document itself and refuses to write it (exit code 3,
  `ERROR:` lines) if it contains `{{...}}` text, HTML comment text, or a banned
  prior-customer term. Report those ERROR lines verbatim; never describe a refused
  build as done.
- Never say a proposal is "clean", "complete" or "verified" unless the build printed
  `OK: wrote ...` with no `ERROR:` lines, and name any `TO CONFIRM:` keys still open.
- Report the exact output path.

## Content rules

- Modules stay generic: no prior-customer names, sites, sectors or dates. The list of
  banned terms is `banned_terms` in `module_index.json`.
- Never invent capabilities, certifications, references, prices, dates or compliance
  claims. Placeholder modules are not live content.

## References

`references/` holds the notes from the original build (integration playbook, enrichment
patterns, image guidance and logo sourcing). They describe how the content was
assembled in September 2026; where they disagree with this file, this file wins.
