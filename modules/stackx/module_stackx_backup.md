# StackX Backup

**Token:** `{{module_stackx_backup}}`  
**Group:** StackX — Control / Orchestration / SOC / Operations Layer  
**Required:** No (optional module)

---

## Overview

StackX Backup protects {{customer_short}}'s critical data and supports business continuity through a unified backup and recovery platform for physical and virtual environments. It protects data against hardware failure, accidental deletion and cyber threats.

## Key Capabilities

- **Automated scheduled backups** — hourly, daily or weekly schedules run without manual intervention.
- **Incremental capture** — only changes since the last backup are captured, saving storage and bandwidth.
- **Recovery point discovery** — browse historical versions and restore specific files or data points in a few steps.
- **Immutable copies** — isolated, immutable backup copies allow a return to a clean state even if primary systems are compromised.
- **Organized, searchable archives** — support for retention and privacy requirements.

<!-- Diagram guidance: protected sources → backup policies (full, incremental) → immutable repository → recovery path. Retention and recovery targets shown as agreed values, not fixed figures. -->
[[figure: backup-architecture | Backup and recovery architecture | Diagram | Architect]]
## Value

- **Minimized downtime** — fast restoration so operations resume in minutes rather than days.
- **Ransomware resilience** — immutable copies provide a clean recovery point.
- **Storage efficiency** — incremental capture and scalable storage grow only as data grows.
- **Regulatory compliance** — organized archives support data retention and privacy obligations.

## Recovery Targets

Recovery point and recovery time objectives are agreed with {{customer_short}} during the design stage for each protected system; no figure is assumed in advance.

<!-- if per_product_sizing -->

## Sizing Basis

| Dimension | Counted As | Confirmed Figure |
| :--- | :--- | :--- |
| Protected data | Front-end TB | {{sizing_stackx_backup_protected_data}} |
| Protected systems | VMs / physical / databases | {{sizing_stackx_backup_protected_systems}} |
| Daily change rate | % | {{sizing_stackx_backup_daily_change}} |

*[Confirm every figure for this bid against the confirmed requirement. Do not carry numbers forward from a prior engagement.]*

<!-- endif -->

<!-- if services -->

## Acceptance Tests

The tests below are executed jointly and form part of the acceptance test plan for this module.

| Test | Method | Pass Criterion |
| :--- | :--- | :--- |
| Restore | Restore one VM and one database | Within RTO; data verified |
| Immutability | Attempt deletion of an immutable copy | Deletion refused |

<!-- endif -->

---

*This module is a reusable building block. Confirm the protected systems, schedules, retention and recovery targets per bid.*
