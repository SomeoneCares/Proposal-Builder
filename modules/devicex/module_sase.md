# SASE / Zero Trust Access

**Token:** `{{module_sase}}`  
**Group:** DeviceX/SDX — Edge & Branch Layer  
**Required:** No (optional add-on)

---

## Solution Overview

DeviceX SASE gives {{customer_short}} control over who and what can access the network at each site. Devices are identified and profiled, users are authenticated, device health is assessed, and access to internal resources is granted per request rather than by network location.

## Key Capabilities

- Device visibility and profiling for policy-driven access
- Zero Trust enforcement at the site edge
- Conditional secure access on LAN and WAN
- Device health assessment before access is granted
- User authentication against standard directory and identity protocols
- Protection of internal resources from unauthorized devices and users

## How It Fits

SASE extends the site edge into a Zero Trust access model: every access request is verified regardless of the user's or device's location. Combined with the SD-WAN overlay and the firewall, it gives each site a consistent, centrally managed access policy. <!-- if module_firewall or module_sdwan -->

<!-- Diagram guidance: users and devices at a site and remote users, each access request passing identity, device-health and policy checks before reaching internal resources. -->
[[figure: sase-access | Zero Trust access at the site edge | Diagram | Architect]]
<!-- if per_product_sizing -->

## Sizing Basis

| Dimension | Counted As | Confirmed Figure |
| :--- | :--- | :--- |
| Remote users | Named users with secure access | {{sizing_sase_remote_users}} |
| Access policies | Policies in the access model | {{sizing_sase_access_policies}} |
| Protected applications | Applications published through the access service | {{sizing_sase_protected_applications}} |

*[Confirm every figure for this bid against the confirmed requirement. Do not carry numbers forward from a prior engagement.]*

<!-- endif -->

<!-- if services -->

## Acceptance Tests

The tests below are executed jointly and form part of the acceptance test plan for this module.

| Test | Method | Pass Criterion |
| :--- | :--- | :--- |
| Access | Connect as a test user from outside the estate | Only the published applications are reachable |
| Policy | Attempt access outside the agreed policy | Denied and logged |
| Revocation | Disable the test user | Session ends and reconnection is refused |

<!-- endif -->

---

*This module is a reusable building block. Include it when secure edge access is in scope for the current engagement.*
