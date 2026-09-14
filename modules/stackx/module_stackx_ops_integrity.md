# StackX Operations Integrity

**Token:** `{{module_stackx_ops_integrity}}`  
**Group:** StackX — Control / Orchestration / SOC / Operations Layer  
**Required:** No (optional module)

---

## Overview

StackX Operations Integrity assures that {{customer_short}}'s systems are operated as intended: that configurations match their approved baselines, that only authorized people perform operations, and that every operational action can be proven afterwards.

## Key Capabilities

### Baselines and Drift Detection

- Approved configuration baselines for in-scope systems
- Continuous comparison of running configurations against their baselines
- Immediate alerts on unapproved drift, with the difference and the affected system identified

### Controlled Access to Operations

Access to operational interfaces is brokered through an identity-aware access layer rather than trusted network locations:

- Access is granted per request after continuous evaluation of the user's identity, multi-factor authentication state and device health.
- Internal management interfaces are hidden from unauthorized users entirely.
- Access can be revoked immediately when a risk signal changes, for example when a device's security posture degrades.

### Verified Operations

- Every administrative session and action recorded against a named identity
- Operational changes matched to approved change records
- Unapproved or out-of-window actions flagged for investigation

### Integrity Case Handling

Integrity events — drift, unapproved changes, unusual administrative behavior — are raised as cases with their evidence attached, assigned to an owner and tracked to closure, with role-based access for handlers.

<!-- Diagram guidance: approved baseline vs running configuration with drift alerts; administrators reaching systems only through the identity-aware access layer; every action linked to a change record. -->
[[figure: operations-integrity | Baselines, controlled access and verified operations]]

## Value

- Configuration errors and unauthorized changes found in minutes, not at the next outage
- Excessive standing access to production systems removed
- Evidence for auditors and regulators that operations follow approved processes

## Integration

- Uses identities and roles from StackX Identity Management. <!-- if module_stackx_idm -->
- Checks operational changes against approved change records in StackX ITSM. <!-- if module_stackx_itSM -->
- Shares integrity events with StackX Security for correlation with other threats. <!-- if module_stackx_security -->

---

*This module is a reusable building block. Confirm the systems under baseline and the operational interfaces to be brokered per bid.*
