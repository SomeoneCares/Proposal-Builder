# SD-WAN

**Token:** `{{module_sdwan}}`  
**Group:** DeviceX/SDX — Edge & Branch Layer  
**Required:** Yes (core — appears in every DeviceX proposal)

---

## Solution Overview

DeviceX/SDX SD-WAN gives each site resilient, high-performance wide-area connectivity. Intelligent load balancing routes traffic dynamically across multiple WAN links, automated failover keeps the business running when a link fails, and granular traffic shaping prioritizes business-critical applications.

## Key Capabilities

- Application-aware routing and traffic shaping for business-critical applications
- Multi-WAN load balancing and automated failover
- IPsec and SSL VPN encryption for all inter-site tunnels
- Quality of Service (QoS) optimization
- Centralized policy management
- Real-time network monitoring and analytics
- Connectivity to cloud and on-premises destinations
- Bandwidth optimization and compression

## Path Diversity and Quality-Based Steering

Multi-path bonding combines diverse underlays — fiber, DSL, cellular and, where required, satellite — into a single encrypted overlay. The platform is transport-agnostic: it requires access services to meet defined characteristics, not any particular carrier or technology, so {{customer_short}} keeps full commercial freedom to select or change access providers at each location.

Each path is measured continuously for one-way latency, jitter and packet loss under load, not just link state. Secondary paths are kept measured and warm, so the best alternative path is already proven when it is needed.

### Steering Behavior

| Condition | System response |
| :--- | :--- |
| All paths healthy | Priority traffic is pinned to the lowest-latency, lowest-jitter path; secondary paths stay measured and warm. |
| Primary path degrades | When jitter or loss thresholds are breached, live priority traffic moves to the best alternative path without dropping the session. |
| Primary path fails | Sub-second failover to the standby underlay; active sessions continue with a brief quality dip rather than a disconnection. |
| All paths impaired | General, management and bulk traffic is throttled so priority traffic keeps its capacity; media can gracefully degrade to audio only. |
| Total outage | The site continues on local services — internal voice, local recording, locally hosted workloads — and queued data synchronizes when the link returns. |

<!-- Diagram guidance: hub (or dual hubs) with sites connected over an encrypted overlay; diverse underlays converging at each site; optionally the steering decision logic. No carrier branding, site names or addressing. -->
[[figure: sdwan-topology | SD-WAN overlay with diverse underlays]]

### Service-Quality Targets

The targets below are used to validate the overlay design and to configure quality-based steering. They are confirmed against {{customer_short}}'s traffic profile and access services; end-to-end performance also depends on the access services {{customer_short}} provides.

| Metric | Target | Purpose |
| :--- | :--- | :--- |
| One-way latency | ≤ {{ola_latency_target}} | Preserves natural turn-taking in real-time interaction |
| Jitter | ≤ {{ola_jitter_target}} | Keeps buffering within limits that avoid audible and visible artifacts |
| Packet loss (priority traffic) | ≤ {{ola_loss_target}} | Below the level at which loss concealment becomes noticeable |
| Voice quality | MOS ≥ {{ola_mos_target}} | Clear dialogue without repetition |
| Session video | {{ola_video_target}} | Sufficient fidelity for the intended use |
| Overlay failover | < {{ola_failover_target}} | A path change is a brief quality dip, not a dropped session |
| Site bring-up (zero-touch) | ≤ {{ola_bringup_target}} | From power-on to adopted, policy-compliant and in service |

*[Enter the service-quality targets agreed for this engagement in the proposal values, or remove this table where {{customer_short}} has not specified targets.]*

## Zero-Touch Site Bring-Up

New sites are brought into service without on-site IT staff: configurations, updates and policies are pushed centrally to every appliance, so a site can be operational within hours of the appliance being connected. The provisioning and attestation model is described in the DeviceX/SDX Centralized Operations section. <!-- if module_sdx_operations -->

## Traffic Prioritization

DeviceX recognizes business-critical applications and keeps their traffic — such as business transactions, ERP updates or real-time voice and video — ahead of routine background data, even during peak congestion.

## Deployment Topologies

Point-to-point, hub-and-spoke and site-to-site topologies are supported and selected per requirement during design.

## Integration with the Firewall <!-- if module_firewall -->

SD-WAN tunnels work together with the DeviceX firewall: encrypted transport is complemented by policy-based inspection at the edge, so traffic reaching each site is both routed optimally and filtered according to security policy. <!-- if module_firewall -->

---

*This module is a reusable building block. Validate the architecture options, performance framing and quality targets against the current RFP/ITB before issue.*
