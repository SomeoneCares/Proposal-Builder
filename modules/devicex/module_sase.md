# SASE / Zero Trust Access

**Token:** `{{module_sase}}`  
**Group:** DeviceX/SDX — Edge & Branch Layer  
**Required:** No (optional add-on)

---

## Solution Overview

DeviceX SASE empowers total control over branch network access. Robust device visibility and profiling enable policy-driven access management. The solution implements Zero-Trust measures with on-prem edge technology, LAN/WAN conditional secure access, device health assessment, user authentication against common technologies, and protection of internal assets.

## Key Capabilities

- Robust device visibility and profiling — policy-driven access management
- Implementation of Zero-Trust measures
- On-Prem Edge Technology
- LAN/WAN Conditional Secure Access
- Assess Device Health
- Authenticate users against common technologies
- Protect Internal Assets

---

## Figure — SASE Architecture (Cloud + Edge Secure Access)

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic SASE architecture diagram showing edge nodes (branches/sites) and remote users connected to cloud-delivered security services (SWG, CASB, ZTNA, FWaaS, secure web/Internet access) over a unified overlay. No customer-specific site names, no customer-specific identity provider names, no customer-specific policy labels. -->
<!-- Suggested source: generic SASE reference model — no customer-specific content from prior proposals is carried. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic SASE architecture diagram here. See image-placement guidance notes.]*

---

## How It Fits

SASE extends the security posture of the DeviceX branch edge into a comprehensive secure-access model. Combined with the firewall (NGFW variant) and SD-WAN, it delivers a Zero Trust–aligned branch architecture in which every access request is verified regardless of user or device location.

## Out-of-Scope (explicitly)

- Any security penetration testing, vulnerability assessments, code reviews, and forensic activities
- Any backup, network, and security activities not explicitly in scope
- Any integration with components that don't support standard protocols used by DeviceX
- Acquisition of any necessary commercial certificates (unless explicitly in scope)
- Any design changes to the existing environment

---

*This module is a reusable building block. Include when SASE / Zero Trust edge access is in scope for the current engagement. Confirm with the customer.*
