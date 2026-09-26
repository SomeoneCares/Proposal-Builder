# NVR / Video Surveillance

**Token:** `{{module_nvr}}`  
**Group:** DeviceX/SDX — Edge & Branch Layer  
**Required:** No (optional add-on)

---

## Solution Overview

The DeviceX NVR module records and manages IP video surveillance at each site, with remote access, central visibility and, where selected, analytics at the edge.

## Variants

*[Choose the variant that matches the current requirement; do not assume one without validating it against the RFP/ITB.]*

### NVR Without Analytics

- Recording configured to the resolution, frame rate and bitrate agreed in the design
- Camera-based retention policies
- Central archiving with WAN optimization
- Remote access and management

### NVR With Edge Analytics

- ONVIF-compliant camera integration
- Object detection and recognition
- Motion detection and behavioral analytics
- Facial recognition and people counting
- License plate recognition
- Real-time alerts and notifications
- Recording, playback, remote and mobile viewing
- Integration with access control systems
- Forensic search and investigation tools

## Operating Pattern

### Local Recording and Retention

Video is recorded locally on the appliance, with the retention policy and alert forwarding configured to the central platform. Recording locally means surveillance never competes with priority wide-area traffic.

### Central Monitoring (Optional)

Where {{customer_short}} requires central monitoring, the platform can present multiple display outputs, each with a camera grid and a focus window. Sizing — displays, camera count and monitoring-site bandwidth — is confirmed in the design against the camera count, resolution and number of sites.

### Bandwidth Planning

- Local recording is not a continuous consumer of the wide-area link.
- Where central archive synchronization is required, it is scheduled outside critical hours and rate-limited so it never contends with live priority traffic.
- Monitoring-site bandwidth is sized against the agreed camera count, resolution and display configuration.

<!-- Diagram guidance: cameras recording locally on the appliance; only alerts, metadata and requested playback crossing the WAN to a central monitoring view. Show camera count as N. -->
[[figure: nvr-architecture | Local recording with central monitoring | Diagram | Architect]]
## Camera Support

- IP cameras are supported by default.
- Analog camera support is decided per engagement against {{customer_short}}'s existing camera estate during design.

## Parameters Confirmed in Design

- Video retention period
- Camera recording resolution and frame rate
- Average bitrate per stream
- Central monitoring sizing (displays, camera grid, bandwidth)
- Archive synchronization schedule and rate limits

<!-- if per_product_sizing -->

## Sizing Basis

| Dimension | Counted As | Confirmed Figure |
| :--- | :--- | :--- |
| Cameras | Per site and total | {{sizing_nvr_cameras}} |
| Recording profile | Resolution / fps / codec / Mbps | {{sizing_nvr_recording_profile}} |
| Retention | Days, continuous or motion | {{sizing_nvr_retention}} |

*[Confirm every figure for this bid against the confirmed requirement. Do not carry numbers forward from a prior engagement.]*

<!-- endif -->

<!-- if services -->

## Acceptance Tests

The tests below are executed jointly and form part of the acceptance test plan for this module.

| Test | Method | Pass Criterion |
| :--- | :--- | :--- |
| Recording | Review 24 h of footage from each camera | No gaps above 1 minute |
| Retention | Check calculated vs configured retention | Configured ≥ agreed days |
| Alert forwarding | Trigger a motion or analytic event | Alert visible centrally |

<!-- endif -->

---

*This module is a reusable building block. Validate camera support, retention and monitoring sizing against the current RFP/ITB before issue.*
