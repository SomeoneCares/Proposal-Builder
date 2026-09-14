# Network Services (DNS, DHCP, LDAP, RADIUS)

**Token:** `{{module_network_services}}`  
**Group:** DeviceX/SDX — Edge & Branch Layer  
**Required:** No (optional add-on)

---

## Solution Overview

DeviceX on-demand services provide the core network services every site needs, directly on the appliance, without separate servers or additional license layers.

## Services

| Service | What it provides at the site |
| :--- | :--- |
| DNS | Local name resolution, with forwarding to {{customer_short}}'s central DNS |
| DHCP | IP address management for each segment |
| LDAP | Local directory lookups for site services |
| RADIUS | Authentication for network access |

## Value

Running these services on the appliance removes the need for separate site servers, keeps them available during a wide-area outage and brings them under the same central management as the rest of the site. <!-- if devicex -->

<!-- Diagram guidance: DNS, DHCP, LDAP and RADIUS on the site appliance, with central authority where required. No server names or addressing. -->
[[figure: network-services | Site network services on DeviceX]]

---

*This module is a reusable building block. Include it when site network services are in scope for the current engagement.*
