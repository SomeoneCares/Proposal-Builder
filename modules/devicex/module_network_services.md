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
[[figure: network-services | Site network services on DeviceX | Diagram | Architect]]
<!-- if per_product_sizing -->

## Sizing Basis

| Dimension | Counted As | Confirmed Figure |
| :--- | :--- | :--- |
| Sites served | Sites taking local network services | {{sizing_network_services_sites_served}} |
| DNS zones and forwarders | Zones hosted locally and upstream forwarders | {{sizing_network_services_dns_zones}} |
| DHCP scopes | Scopes across all zones per site | {{sizing_network_services_dhcp_scopes}} |
| RADIUS clients | Switches and access points authenticating | {{sizing_network_services_radius_clients}} |

*[Confirm every figure for this bid against the confirmed requirement. Do not carry numbers forward from a prior engagement.]*

<!-- endif -->

<!-- if services -->

## Acceptance Tests

The tests below are executed jointly and form part of the acceptance test plan for this module.

| Test | Method | Pass Criterion |
| :--- | :--- | :--- |
| Local resolution | Query a local and an upstream name from a site client | Both resolve; upstream forwarding works |
| Address allocation | Connect a client in each zone | Correct scope, gateway and options issued |
| Time synchronisation | Compare site and central clocks | Within the agreed tolerance |
| Network authentication | Authenticate a test device | Accepted, with the session logged centrally |

<!-- endif -->

---

*This module is a reusable building block. Include it when site network services are in scope for the current engagement.*
