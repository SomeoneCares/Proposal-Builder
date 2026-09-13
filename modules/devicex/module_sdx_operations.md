# DeviceX/SDX Centralized Operations (Edge Management)

**Token:** `{{module_sdx_operations}}`  
**Group:** DeviceX/SDX — Edge & Branch Layer  
**Required:** No (optional add-on)

---

## Solution Overview

The SDX Backend Operations function is responsible for the centralized management, configuration, and monitoring of the SD-WAN infrastructure, ensuring stable connectivity, security enforcement, and optimal network performance across all managed devices.

## Core Operations Activities

### Device Provisioning and Lifecycle Management

- Approval and onboarding of new SD-WAN devices
- Initial device provisioning and configuration
- Assignment and configuration of WAN and LAN interfaces
- Secure decommissioning and removal of devices when required

### Network Configuration and Routing

- Configuration and management of network routing, including static and dynamic routing policies
- Creation and management of SD-WAN tunnels between sites

### Security and Policy Management

- Creation, modification, and enforcement of firewall policies
- Centralized deployment and push of configuration updates to SD-WAN devices to ensure consistency across the infrastructure

### Monitoring and Performance Management

- Continuous monitoring of device health, operational status, and system performance
- Monitoring of SD-WAN agent status and connectivity
- Monitoring of tunnel status and stability

## Zero-Touch Provisioning

Zero-touch provisioning is a deployment advantage only if it does not create a security weakness. Across multiple locations, appliances will be unpacked and connected by staff who are not security-cleared and not technically trained. The provisioning model therefore assumes the person plugging in the device is untrusted, and derives trust from the hardware instead.

The operational result is that a new site is brought into service by a non-technical person connecting power and a network cable, while the security posture is stronger than a manually configured site would achieve.

### Provisioning Flow

**Stage 1 — Pre-Registration**

Before shipping, the public portion of each appliance's hardware endorsement key certificate — permanently signed by the silicon manufacturer — is imported into the central inventory as a pre-authorised hardware unit.

**Stage 2 — First Boot and Attestation**

On power-up the node locates the central registration service and generates an attestation key inside its hardware root of trust. The central service issues a challenge encrypted specifically to that node's endorsement key. Only the genuine hardware can decrypt it, proving physical possession of the registered hardware.

**Stage 3 — Certificate Issuance**

With identity proven, the node generates its operational private keys inside the hardware root of trust — one pair for management, one for the SD-WAN tunnel — and submits standards-based signing requests over a secure enrolment protocol. The central authority validates them against the attestation result and issues the operational certificates.

**Stage 4 — Mesh Join**

The node establishes its IPsec tunnels using certificate authentication and enters service under its assigned policy template. The private keys never leave the hardware root of trust at any point — not during generation, not during renewal, not during signing.

---

## Figure — Zero-Touch Provisioning Flow / Attestation & Credentials

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic zero-touch provisioning sequence diagram showing the four stages — pre-registration, first boot & attestation, certificate issuance, mesh join — and an attestation / short-lived-credentials flow showing compromise-response scenarios. No customer-specific registration-service names, no customer-specific CA names, no customer site names. -->
<!-- Alternative: a device-adoption / mesh-join diagram showing a new site brought into service by a non-technical person connecting power and a network cable. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic ZTP / attestation flow diagram here. See image-placement guidance notes.]*

---

## Attestation and Short-Lived Credentials

Long-lived certificates create a long-lived problem: a credential stolen today may remain valid for years, and containing it depends on someone noticing and acting. The platform inverts this by issuing credentials that expire in hours and are renewed only on proof of continuing integrity.

### How It Operates

- **Attestation cycle.** On a short recurring cycle, each node requests a single-use challenge from the central service, generates a signed statement of its current platform measurements, and submits it together with a request for a new certificate.
- **Verification.** The central platform validates the hardware identity, verifies the signature and challenge, replays the boot event log to confirm the measurements are internally consistent, and compares the result against the approved baseline for that hardware and software build.
- **Issuance.** Only on success is a new short-lived certificate issued — operational lifetime in hours, configurable — and the cycle repeats automatically in the background.
- **Baseline registry.** The central platform maintains the approved measurement baselines for every hardware platform and software build in the estate, so approved updates are accommodated without weakening the check.

### Response to Compromise

- **Node stolen from a site.** The node's identity is revoked centrally. Its current credentials expire within hours, removing it from the network. On next connection it receives a command that clears its hardware root of trust, destroying the disk encryption key and rendering the drive permanently unrecoverable.
- **Bootloader or operating system tampered.** Platform measurements no longer match the approved baseline. The hardware root of trust refuses to release the sealed keys and attestation fails, so the node cannot join the network at all.
- **Attempted interception of provisioning.** The enrolment protocol requires validation of the central service against trust anchors held in a read-only layer of the node's operating system, so a substituted server is rejected.
- **Unexplained configuration drift.** Failure is raised immediately as an event in the central operations platform, flagged as possible physical tampering, with the affected site identified.
- **Diagnostics required before restoring service.** Rather than flat refusal, the platform can issue a restricted credential that routes the node only to an isolated remediation segment for investigation.

## Delivery Model

- Provide SDX-Edge Technical Support through Certified NOC Engineers operating from regional / network operations centres
- Device provisioning and lifecycle management handled centrally from the management platform

## Out-of-Scope (explicitly)

- Providing/Mounting Hardware, network, and storage devices including cabling
- Any field support activities
- Any logistical work and direct communication with the end user
- Any rework related to hardware availability or hardware failure issues
- Any activity in the branches including Delivery and mounting of devices
- Any communication with the telco operators
- Any migration activities
- Integration with any other third-party products except for what is mentioned under scope of work

---

*This module is a reusable building block. Present in prior proposals for branch operations scope. Confirm with the customer whether centralized SDX / edge operations are in scope for the current engagement. The attestation and short-lived credential model is platform capability framing; validate against the current customer's security requirements before asserting any specific certificate lifetimes or baseline-registry behaviour.*
