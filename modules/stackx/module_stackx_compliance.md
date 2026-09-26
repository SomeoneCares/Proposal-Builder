# StackX Compliance Assurance

**Token:** `{{module_stackx_compliance}}`  
**Group:** StackX — Control / Orchestration / SOC / Operations Layer  
**Required:** No (optional module)

---

## Overview

StackX Compliance Assurance continuously measures {{customer_short}}'s estate against the standards and regulations that apply to it, and keeps the evidence needed to prove it. It turns compliance from a periodic audit exercise into a continuously maintained position.

## Key Capabilities

### Continuous Assessment

- Active and passive scanning of the internal network and external attack surface to find missing patches, insecure configurations and default passwords
- Authenticated and unauthenticated scanning, with automated asset discovery
- Configuration assessment against security benchmarks such as the CIS benchmarks

### Standards and Regulatory Mapping

- Compliance dashboards for standards such as CIS and PCI-DSS, and for {{customer_short}}'s applicable regulations: {{compliance_frameworks}}
- Monitoring of where data resides and whether encryption at rest is in place

### Evidence and Audit Readiness

- Automated compliance reports for standards and regulatory requirements
- Collection and retention of compliance evidence for audits
- A complete trail of findings, remediation actions and exceptions

### Remediation Tracking

- Findings assigned to owners with target dates
- Progress and aging of open findings visible to management
- Accepted exceptions recorded with their justification and review date

<!-- Diagram guidance: assessment sources (scans, configuration checks) → findings mapped to controls → remediation tracking → audit evidence and reports. -->
[[figure: compliance-assurance | Continuous compliance assessment and evidence | Diagram | Architect]]
## Value

- A smaller attack surface and actionable metrics for patching teams
- Continuous regulatory compliance instead of point-in-time audits
- Audit preparation in days rather than weeks, with evidence already collected

## Integration

- Uses retained logs from StackX Event & Log Management as audit evidence. <!-- if module_stackx_event_log_mgmt -->
- Feeds vulnerability findings to StackX Security for exploitation-based prioritization. <!-- if module_stackx_security -->
- Tracks remediation tasks as tickets in StackX ITSM. <!-- if module_stackx_itSM -->

<!-- if per_product_sizing -->

## Sizing Basis

| Dimension | Counted As | Confirmed Figure |
| :--- | :--- | :--- |
| Assets scanned | IPs / hosts | {{sizing_stackx_compliance_assets_scanned}} |
| External IPs | Internet-facing | {{sizing_stackx_compliance_external_ips}} |
| Frameworks | Mapped | {{sizing_stackx_compliance_frameworks}} |

*[Confirm every figure for this bid against the confirmed requirement. Do not carry numbers forward from a prior engagement.]*

<!-- endif -->

<!-- if services -->

## Acceptance Tests

The tests below are executed jointly and form part of the acceptance test plan for this module.

| Test | Method | Pass Criterion |
| :--- | :--- | :--- |
| Scan coverage | Compare scanned assets to CMDB | ≥ 95 % of in-scope assets |
| Reports | Generate framework reports | All selected frameworks produced |

<!-- endif -->

---

*This module is a reusable building block. Confirm the standards, regulations and scanning scope per bid. Do not claim certification or attestation on {{customer_short}}'s behalf.*
