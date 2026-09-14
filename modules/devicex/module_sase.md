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
[[figure: sase-access | Zero Trust access at the site edge]]

---

*This module is a reusable building block. Include it when secure edge access is in scope for the current engagement.*
