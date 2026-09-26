# StackX Identity Management (IDM)

**Token:** `{{module_stackx_idm}}`  
**Group:** StackX — Control / Orchestration / SOC / Operations Layer  
**Required:** No (optional module)

---

## Overview

StackX Identity Management provides secure access control, authentication and authorization across {{customer_short}}'s systems from one governance platform. It manages who has access to what, why they have it, and whether they should keep it.

## Key Capabilities

### Identity Lifecycle Management

Identities are provisioned when people join, updated when they move and deprovisioned when they leave, automatically. Periodic access reviews and self-service requests keep access current without adding administrative load.

### Role-Based Access Control

Access is granted through roles rather than individual assignments, with privileged access management, policy enforcement and dynamic access controls for sensitive systems.

### Directory Services Integration

StackX IDM integrates with enterprise directory services, LDAP directories and cloud identity providers, so identities stay consistent across on-premises and cloud systems.

### Authentication

- Multi-factor authentication for users and administrators
- Single sign-on to connected applications
- Secure authentication for users, devices and services

<!-- Diagram guidance: identity sources and the IDM platform provisioning accounts to target systems, with access reviews and an SSO/MFA login flow. No identity provider or role names. -->
[[figure: identity-lifecycle | Identity lifecycle and access governance | Diagram | Architect]]
## Value

- One governance platform for identity and access
- Stronger security through automated access controls and monitoring
- Less administrative effort through automated provisioning and self-service
- Easier compliance through access certification and audit trails

## Integration

- Provides role and identity data to StackX Operations Integrity for access to operations. <!-- if module_stackx_ops_integrity -->
- Manages access to the StackX modules themselves through the same roles. <!-- if stackx -->

<!-- if per_product_sizing -->

## Sizing Basis

| Dimension | Counted As | Confirmed Figure |
| :--- | :--- | :--- |
| Identities | Employees + contractors + service accounts | {{sizing_stackx_idm_identities}} |
| Target systems | Connected applications | {{sizing_stackx_idm_target_systems}} |
| Roles | Business roles | {{sizing_stackx_idm_roles}} |

*[Confirm every figure for this bid against the confirmed requirement. Do not carry numbers forward from a prior engagement.]*

<!-- endif -->

<!-- if services -->

## Acceptance Tests

The tests below are executed jointly and form part of the acceptance test plan for this module.

| Test | Method | Pass Criterion |
| :--- | :--- | :--- |
| Leaver | Terminate a test user in HR | All target access removed within target |
| SoD | Request a conflicting role | Request blocked or escalated |

<!-- endif -->

---

*This module is a reusable building block. Confirm directories, target systems and the number of identities per bid.*
