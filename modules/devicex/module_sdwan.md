# SD-WAN

**Token:** `{{module_sdwan}}`  
**Group:** DeviceX/SDX — Edge & Branch Layer  
**Required:** Yes (core — appears in every DeviceX proposal)

---

## Solution Overview

The DeviceX/SDX SD-WAN delivers comprehensive networking capabilities to empower branch agility and resilience. Intelligent traffic load balancing optimizes performance by dynamically routing traffic across multiple WAN links. Automated connection failover ensures business continuity with seamless failover, while granular traffic shaping prioritizes mission-critical applications. These features create a reliable, high-performance, and adaptable wide-area network for branch locations.

## Key Capabilities

- Intelligent traffic load balancing across multiple WAN links
- Automated connection failover with seamless continuity
- Granular traffic shaping to prioritize mission-critical applications
- Application-aware intelligent routing
- Multi-WAN load balancing and failover
- IPSec and SSL VPN encryption for secure tunnels
- Quality of Service (QoS) optimization
- Centralized policy management
- Real-time network monitoring and analytics
- Cloud and on-premises connectivity
- Bandwidth optimization and compression

## Path Diversity & Quality-Based Steering

Multi-path bonding aggregates diverse underlays — fiber, DSL, cellular and satellite where required — into a single encrypted overlay. The platform is transport-agnostic: it requires access services to meet certain characteristics, not any particular carrier or technology, so the customer retains full commercial freedom to select or change access providers at each location without redesigning the network or renegotiating the engagement.

Live quality measurement runs continuously per path (one-way latency, jitter and packet loss under load), not on link state alone. Secondary paths are kept measured and warm, so a path that becomes the best alternative is already proven and ready. The overlay steers priority traffic on live quality measurement, protecting the sessions that matter most rather than treating all traffic identically.

### Steering Behaviour

| Condition | System Response |
|-----------|-----------------|
| All paths healthy | Priority media pinned to the lowest-latency, lowest-jitter path. Secondary paths remain measured and warm. |
| Primary path degrades | Quality thresholds breached on jitter or loss trigger steering of live priority media to the best alternative path without dropping the session. |
| Primary path fails | Sub-second failover to the standby underlay. Active sessions continue; users experience a brief quality dip rather than a disconnection. |
| All paths impaired | Bandwidth is reclaimed by throttling general, management and bulk traffic so priority media retains capacity. Optional graceful degradation from media to audio-only preserves the conversation. |
| Total outage | Site continues on local services — internal voice, local recording, cached workloads. Queued data and recordings synchronise automatically on restoration. |

### Service Quality Targets (reference — confirm per bid)

The following targets are representative reference values for prioritised real-time media and are used to validate overlay design and to configure quality-based steering. They are confirmed per engagement against the customer's traffic profile and access services, and are not a warranty of end-to-end performance, which also depends on the customer-provided underlay.

| Metric | Representative Target | Purpose |
|--------|----------------------|---------|
| One-way latency | ≤ {{ola_latency_target}} | Preserves natural turn-taking during real-time interaction. |
| Jitter | ≤ {{ola_jitter_target}} | Keeps de-jitter buffering within limits that avoid audible and visible artefacts. |
| Packet loss (priority media) | ≤ {{ola_loss_target}} | Below the threshold at which loss concealment becomes noticeable. |
| Voice quality | MOS ≥ {{ola_mos_target}} | Sustains clear dialogue without repetition. |
| Session video | {{ola_video_target}} | Sufficient fidelity for visual assessment at the primary session camera. |
| Overlay failover | < {{ola_failover_target}} | A path change is perceived as a brief quality dip, not a dropped session. |
| Site bring-up (zero-touch) | ≤ {{ola_bringup_target}} | From power-on to adopted, policy-compliant and in service. |

*[Enter the service-quality targets agreed for the current engagement in the proposal values, or remove this table where the customer has not specified quality targets.]*

---

## Figure — SD-WAN Architecture (Hub-and-Spoke / Mesh Overlay)

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic SD-WAN topology showing a central hub (or dual hubs) with multiple remote/branch sites connected over an encrypted overlay, with diverse underlays (fiber, DSL, cellular) converging at each site. Transport-agnostic — no carrier branding, no customer site names, no customer-specific IP addressing. -->
<!-- Alternative: a path-diversity / quality-based steering decision diagram showing primary path, standby underlay, and steering logic (latency/jitter/loss thresholds). -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic SD-WAN architecture / path-diversity diagram here. See image-placement guidance notes.]*

---

## Zero-Touch Provisioning (ZTP)

DeviceX enables instant onboarding and rapid site bring-up for branches. Through the cloud orchestration plane and StackX, new configurations, updates, and policies can be pushed instantly to thousands of DeviceX units. The Branch-in-a-Box model allows for full remote management and updates, eliminating the need for on-site IT staff for provisioning.

## Link Aggregation Resilience

DeviceX utilizes Link Aggregation, allowing the customer to combine fiber, 4G/5G, and even satellite links. If one connection fails, traffic moves to the remaining links and active sessions continue, as described in the steering behaviour above.

## Traffic Prioritization

DeviceX recognizes the importance of mission-critical applications. It ensures that critical traffic — such as business transactions, ERP updates or real-time voice and video — is always prioritized over routine background data, even during peak congestion.

## Deployment Architecture Options

Select one or more architecture patterns as applicable:

- Point-to-Point
- Hub & Spoke
- Site-to-Site VPN

## Security Integration with Firewall

The SD-WAN tunnels integrate with the branch firewall to provide layered security, where encrypted transport-level tunnels are complemented by policy-based traffic inspection at the edge. Firewall policy enforcement and SD-WAN traffic steering work together to ensure that traffic reaching the branch is both routed optimally and filtered according to security policy.

## Out-of-Scope (explicitly)

- Any communication with the telco operators
- Procurement and infrastructure readiness (including hardware, network, storage, cabling, security firewalls, load balancers, commercial certificates, virtualization platforms, operating systems, antivirus, backup) — unless explicitly in scope
- Any rework for the centralized management infrastructure related to hardware availability/hardware failure issues, network connectivity issues, electricity instability or electricity outages
- The availability, throughput, latency or quality of customer-provided access services, and any service credit arising from their failure
- Design, survey, installation or upgrade of last-mile access, including satellite terminal installation, alignment and commissioning
- Any communication, negotiation, fault escalation or SLA management with ISPs, carriers or satellite operators on the customer's behalf

---

*This module is a reusable building block. Validate scope, architecture options, performance framing, and quality targets against the current customer's RFP/ITB before issuing.*
