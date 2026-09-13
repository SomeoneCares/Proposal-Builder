# Module Skeleton — DeviceX/SDX & StackX Proposal Module

<!--skill: proposal-template-->

Copy this file, rename it, fill in the metadata and body, and register it in `module_index.json`.

```md
# <Module Title>

**Token:** `{{module_<token>}}`
**Group:** <group label>
**Required:** Yes | No (<notes>)

---

## Solution Overview

<What the module delivers, in proposal language.>

## Key Capabilities

- <capability 1>
- <capability 2>
- <capability 3>

## Value / How It Fits

<Why the customer cares and where the module sits in the architecture.>

## Deployment / Build Notes

<How the module is delivered or configured, if relevant.>

*[Note: <per-bid confirmation needed, e.g. scope depth, variants, prerequisites.>]*

## Out-of-Scope (explicitly)

- <exclusion 1>
- <exclusion 2>
- <exclusion 3>

---

*This module is a reusable building block. Validate against the current customer's RFP/ITB before issuing.*
```

## Registration checklist

1. Place the file at `modules/<group>/module_<token>.md`.
2. Add an entry to `module_index.json` under the correct group, including `token`, `file`, `name`, `required`, and `notes`.
3. Run one complete-mode assembly with the new module included and inspect the output for metadata leaks.
4. Run one template-mode assembly with the new module and confirm the placeholder line renders.
