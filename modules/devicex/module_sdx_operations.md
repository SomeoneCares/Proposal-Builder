# DeviceX/SDX Centralized Operations

**Token:** `{{module_sdx_operations}}`  
**Group:** DeviceX/SDX — Edge & Branch Layer  
**Required:** No (optional add-on)

---

## Solution Overview

DeviceX/SDX centralized operations cover the management, configuration and monitoring of every appliance from the central platform, keeping connectivity stable, security enforced and performance consistent across all sites.

## Core Activities

### Device Provisioning and Lifecycle

- Approval and onboarding of new appliances
- Initial provisioning and configuration, including WAN and LAN interfaces
- Secure decommissioning and removal of appliances

### Network Configuration and Routing

- Static and dynamic routing policies
- Creation and management of the SD-WAN tunnels between sites <!-- if module_sdwan -->

### Security and Policy Management

- Creation, modification and enforcement of firewall policies <!-- if module_firewall -->
- Central push of configuration updates to keep every appliance consistent

### Monitoring and Performance

- Continuous monitoring of appliance health, status and performance
- Monitoring of agent status and connectivity
- Monitoring of tunnel status and stability <!-- if module_sdwan -->

## Zero-Touch Provisioning

Zero-touch provisioning is an advantage only if it does not create a security weakness. Appliances are often unpacked and connected by staff who are neither security-cleared nor technically trained, so the provisioning model assumes the person plugging in the device is untrusted and derives trust from the hardware instead. A new site is brought into service by connecting power and a network cable, with a stronger security posture than a manually configured site.

### Provisioning Flow

1. **Pre-registration.** Before shipping, the public part of each appliance's hardware endorsement key certificate — signed permanently by the silicon manufacturer — is imported into the central inventory as a pre-authorized unit.
2. **First boot and attestation.** On power-up, the appliance locates the central registration service and generates an attestation key inside its hardware root of trust. The service issues a challenge that only the genuine hardware can decrypt, proving physical possession of the registered unit.
3. **Certificate issuance.** With its identity proven, the appliance generates its operational private keys inside the hardware root of trust — one pair for management and one for the SD-WAN tunnel — and submits standards-based signing requests. The central authority validates them against the attestation result and issues the certificates.
4. **Mesh join.** The appliance establishes its IPsec tunnels with certificate authentication and enters service under its policy template. Private keys never leave the hardware root of trust.

<!-- Diagram guidance: the four provisioning stages as a sequence between the appliance, the registration service and the certificate authority. No service or site names. -->
[[figure: ztp-flow | Zero-touch provisioning and attestation]]

## Attestation and Short-Lived Credentials

Long-lived certificates create a long-lived risk: a stolen credential can stay valid for years. The platform instead issues credentials that expire within hours and are renewed only on proof of continuing integrity.

- **Attestation cycle.** On a short recurring cycle, each appliance requests a single-use challenge, signs a statement of its current platform measurements and requests a new certificate.
- **Verification.** The central platform validates the hardware identity, the signature and the challenge, replays the boot event log and compares the result with the approved baseline for that hardware and software build.
- **Issuance.** Only on success is a new short-lived certificate issued; the cycle repeats automatically.
- **Baseline registry.** The central platform keeps the approved measurement baselines for every hardware platform and software build, so approved updates are accommodated without weakening the check.

### Response to Compromise

- **Appliance stolen.** Its identity is revoked centrally, its credentials expire within hours, and on its next connection its hardware root of trust is cleared, making its disk permanently unreadable.
- **Boot loader or operating system tampered.** Measurements no longer match the baseline, the sealed keys are not released and the appliance cannot join the network.
- **Provisioning interception attempted.** The enrollment protocol validates the central service against trust anchors held in a read-only layer of the appliance, so a substituted server is rejected.
- **Unexplained configuration drift.** An event is raised immediately in the central operations platform and flagged as possible tampering, identifying the site.
- **Diagnostics needed before service is restored.** A restricted credential can route the appliance to an isolated remediation segment for investigation.

## Delivery Model

- Appliance provisioning and lifecycle are handled centrally from the management platform.
- Technical support is provided by certified network operations engineers. <!-- if managed_services -->

---

*This module is a reusable building block. Validate the attestation model against {{customer_short}}'s security requirements before asserting specific certificate lifetimes.*
