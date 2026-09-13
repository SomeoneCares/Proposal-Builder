# Orphan Value Tokens — coverage trap and pre-flight check

When a module or a reworded module introduces a `{{customer_*}}` or
`{{training_*}}`-style token that has no matching key in the values JSON,
the combine script's "0 unresolved non-section tokens" check may still
pass — because a missing value key is not a missing module. The result is
literal `{{...}}` text leaking into the assembled docx, which is easy to
miss in a review unless you specifically look for it.

This reference captures the trap, the pre-flight scan that catches it, and
the concrete before/after from this session.

## The trap

The combine script checks two things:

- Is the module file referenced by a `{{module_*}}` token present on disk?
- Can a `{{customer_*}}` token be filled from the values JSON?

What it does **not** (automatically) check is: *does every `{{customer_*}}`
token that appears in the selected modules actually have a key in the
values file?*

If a module was edited to add a new `{{customer_foo}}` reference and the
values file was not updated, the assemble step may still produce a docx
and the only hint is literal `{{customer_foo}}` text in the output. In
this session the training module's matrix used `{{training_attendees_*}}`
and `{{training_duration_*}}` tokens that were not in
`values-example.json` — they would have rendered as literal placeholders.

## Pre-flight scan

Run this before any `--mode complete` assemble. It enumerates every
`{{customer_*}}` token in the selected markdown and compares against the
keys in the values JSON.

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

Generalise the scan for any token family the skill uses (for example
`{{training_*}}`) by changing the regex.

Rules of thumb:

- If the token is intentional and reusable across bids, add the key to the
  values JSON and document it under `customer_slots` in `module_index.json`.
- If the token is an accidental reference or a placeholder that should not
  be in a reusable template, neutralise it — replace with plain descriptive
  text, a values-driven slot the author fills per bid, or a `[PROSE]`
  author-writing note. Do not ship a reusable template that depends on a
  values key the author has to invent per bid.
- Do not assemble until the scan is clean.

## This session's concrete case

### Symptom

After a sibling rewrote `section_training.md`, the module's example
training matrix used eight `{{training_*}}` tokens:

- `{{training_attendees_devicex}}`, `{{training_duration_devicex}}`
- `{{training_attendees_netmon}}`, `{{training_duration_netmon}}`
- `{{training_attendees_logmgmt}}`, `{{training_duration_logmgmt}}`
- `{{training_attendees_secmon}}`, `{{training_duration_secmon}}`
- `{{training_attendees_obs}}`, `{{training_duration_obs}}`
- `{{training_attendees_orch}}`, `{{training_duration_orch}}`
- `{{training_attendees_itSM}}`, `{{training_duration_itSM}}`
- `{{training_attendees_epm}}`, `{{training_duration_epm}}`

None of these were in `values-example.json`.

### Resolution option A (values-driven, reusable across bids)

Add the keys to the values file and to `customer_slots` in
`module_index.json`. This is the right call when the matrix is meant to be
a real, reused catalogue whose numbers vary per bid.

This session chose not to do that — the matrix is explicitly a *format
example*, not a default catalogue, so inventing eight reusable value slots
would over-specify the template.

### Resolution option B (neutralise to descriptive placeholder, chosen)

Replace each `{{training_*}}` token with a plain descriptive placeholder
that does not depend on a values key, and make clear in the note that the
matrix is a format example to be tailored per bid.

Before:

```
| DeviceX / SDX Administration | Up to {{training_attendees_devicex}} | {{training_duration_devicex}} |
```

After:

```
| DeviceX / SDX Administration | Up to ~5 technical staff | ~3 days |
```

The note already said: *replace the `{{training_*}}` slots or remove courses
as appropriate for the current engagement.* Changing the cells to descriptive
placeholders keeps the format example readable without creating hidden value
dependencies.

### Secondary effect — new module added this session

This session also created `module_stackx_security.md`. That module's token
was registered in `module_index.json`, but the values file was not changed
because the module introduces no new `{{customer_*}}` keys. That is fine —
the pre-flight scan above only flags tokens that *are* in the markdown but
*not* in the values file. A new module with no value tokens is not a
mismatch.

## How to detect the leak after the fact

If you already assembled and suspect a leak, grep the docx's extracted text
for literal `{{`:

- Extract the docx text with `docx_read.py --text`.
- Grep for `{{` — any hit is an unresolved token.
- Cross-reference each hit against the values JSON.

Do not rely on the combine script's WARN/NOTE output alone. A missing
`customer_*` key can produce a clean-looking assemble with no warning and a
docx full of literal `{{...}}` in the affected module.

## Relationship to module-token checks

This is a different class of problem from a missing module file:

- Missing module file → token stays unresolved, script warns, docx still
  written. Caught by module-resolution checks.
- Missing value key → token is not a module token, so module-resolution
  checks do not see it. Caught only by the pre-flight value-token scan or
  by a post-asmble `{{` grep.

Treat them as two separate gates.
