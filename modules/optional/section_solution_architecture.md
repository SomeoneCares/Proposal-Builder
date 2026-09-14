# Solution Architecture

**Token:** `{{section_solution_architecture}}`  
**Group:** Optional Proposal Sections  
**Required:** No

---

## Architecture Overview

The proposed solution is a centrally governed architecture in which policy, identity, monitoring and logging are controlled from {{customer_short}}'s central site, while services run as close as possible to the users and systems that depend on them.

<!-- if devicex -->
Each site is served by a DeviceX/SDX appliance. SDX is the platform software; DeviceX is SDX installed on standard Verto Wave hardware. The appliances connect to the central site over an encrypted overlay and are provisioned, configured and monitored centrally.
<!-- endif -->

<!-- if stackx -->
StackX provides the operations layer: it collects telemetry from infrastructure, applications and security controls into shared data, and uses that data to drive monitoring, service management, automation and security operations.
<!-- endif -->

<!-- Diagram guidance: layered view — sites with DeviceX at the bottom, the encrypted overlay, the central site with the DeviceX backend and StackX platform, and integrations with the customer's systems. Generic labels only. -->
[[figure: solution-architecture | Solution architecture overview]]

## Architecture Layers

| Layer | Components | Role |
| :--- | :--- | :--- |
| Site edge | DeviceX/SDX appliance | Connectivity, security and local services at each site <!-- if devicex --> |
| Wide-area overlay | DeviceX SD-WAN | Encrypted, quality-steered connectivity between sites and the central site <!-- if module_sdwan --> |
| Central management | DeviceX backend and hub | Provisioning, policy, configuration and monitoring of every appliance <!-- if devicex --> |
| Operations platform | StackX | Monitoring, service management, automation and analytics <!-- if stackx --> |
| Security operations | StackX security modules | Detection, investigation and response across the estate <!-- if module_stackx_security or module_stackx_soc --> |
| Integration | Standard interfaces | Exchange with {{customer_short}}'s existing systems through supported protocols and APIs |

## Design Principles

- **Priority traffic first.** Business-critical and real-time traffic is the protected class; all other flows yield to it under contention. <!-- if module_sdwan -->
- **Assume the link will fail.** Each site keeps its local functions running independently of the wide-area network. <!-- if devicex -->
- **Centralize control, distribute function.** Policy, identity, monitoring and logging are governed centrally; processing stays close to where it is needed.
- **Standardize.** One appliance family, one configuration template per site class and one policy baseline — variation is the main cost of remote operations at scale. <!-- if devicex -->
- **Secure by default.** Segmentation, encryption, hardware-anchored identity, least-privilege administration and full logging are part of the base build, not a later phase.
- **Transport agnostic.** No assumption is made about which access service a site receives; every path is treated as untrusted, measured and steered. <!-- if module_sdwan -->

## Logical Traffic Model <!-- if module_sdwan -->

<!-- if module_sdwan -->
Traffic is classified into a small set of classes that are enforced identically at every site:

- **Priority real-time media** — voice and video carried on the best available path and protected against loss and jitter. <!-- if module_ipbx or module_nvr or module_stackx_call_center -->
- **Business application data** — application traffic between sites and the central site, segmented from all other traffic.
- **Surveillance** — camera streams recorded locally; only alerts, metadata and requested playback cross the wide-area link. <!-- if module_nvr -->
- **Telephony signaling** — registration and call control, marked as protected control traffic. <!-- if module_ipbx -->
- **Management and telemetry** — orchestration, configuration, monitoring and log shipping over a dedicated, mutually authenticated channel.
- **General and guest** — administrative browsing and updates, isolated and rate-limited so they never contend with business services.
<!-- endif -->

---

*This section is generated from the selected modules. Confirm the layer table and principles against the final design before issue.*
