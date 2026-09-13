# NVR / Video Surveillance

**Token:** `{{module_nvr}}`  
**Group:** DeviceX/SDX — Edge & Branch Layer  
**Required:** No (optional add-on)

---

## Solution Overview

Providing robust surveillance capabilities over IP networks. The value lies in offering remote access, scalability, and advanced analytics, which enhance security and operational efficiency for organizations.

## Two NVR Sub-Options

This module has two variants. Select the variant that matches the current customer's requirements. Do not assume one or the other without validating against the RFP/ITB.

### Variant A — NVR Without AI

- Configure and deploy the NVR system without AI capabilities as per the design
- Set up video recording parameters including resolution, frame rate, and bitrate as per the design
- Camera-based retention policies
- Centralized archiving with WAN optimization
- Remote access and management

### Variant B — NVR with Edge Analytics

- AI-powered surveillance with edge analytics
- ONVIF-compliant camera integration
- AI-powered object detection and recognition
- Motion detection and behavioral analytics
- Facial recognition and people counting
- License plate recognition (LPR)
- Real-time alerts and notifications
- Video recording and playback
- Remote access and mobile viewing
- Integration with access control systems
- Forensic search and investigation tools

## Operating Pattern

### Local recording and retention (default)
---

## Figure — NVR Recording & Monitoring Architecture

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic NVR architecture diagram showing camera streams recorded locally on the appliance, with only alerts/metadata/thumbnails/operator-requested playback traversing the wide-area link to a central monitoring array. No customer-specific camera names, no site names, no customer-specific retention figures. -->
<!-- Suggested source: Telemedicine proposal NVR section (local recording as default, centralised monitoring array as design input, NVR bandwidth consideration) — genericise the diagram. -->
<!-- Alternative: a camera layout / per-site camera-count diagram (generic — show N cameras per site as a variable, not a fixed customer number). -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic NVR architecture / camera-layout diagram here. See image-placement guidance notes.]*

---


Surveillance is recorded locally at the edge, with retention policy and alert forwarding configured to the central platform. Recording locally means surveillance does not compete with priority wide-area traffic for the link — a key property for deployments where the wide-area link also carries sensitive real-time traffic.

### Centralised monitoring array (optional, where required)

Where the customer requires a centralised monitoring array, the platform can be configured with a high-capacity monitoring arrangement — for example, multiple display outputs, each featuring a camera grid plus a dedicated active-focus window. The configuration is optimised for a reference resolution and requires a recommended minimum backbone bandwidth at the monitoring location to maintain high-quality real-time streaming. Sizing is confirmed at design stage against the camera count, resolution and site count; it is presented here as a design-time planning input, not as a fixed product specification.

### NVR bandwidth consideration (planning input)

- Surveillance recorded locally is not a continuous consumer of the wide-area link.
- Where central archive synchronisation is required, it is scheduled outside critical hours and rate-limited so it can never contend with live priority traffic.
- The monitoring-location backbone bandwidth is sized against the agreed camera count, resolution and display configuration, and confirmed during design.

## Camera Support

- IP cameras are supported by default.
- Analogue camera support, if required, is a per-engagement decision and is confirmed against the customer's existing camera estate during design. (Do not assume analogue support without validating.)

## Reference Parameters (optional — confirm per bid)

The following parameters are provided as generic reference values only. Do **not** carry them into a new proposal without validating against the current design and customer requirements:

- Video retention period — confirm per design
- Camera recording resolution — confirm per design
- Video frame rate — confirm per design
- Average video bitrate per stream — confirm per design
- Central monitoring array sizing (display outputs, camera grid, backbone bandwidth) — confirm per design
- Archive synchronisation schedule and rate limiting — confirm per design

## Out-of-Scope (explicitly)

- Any video recordings or screenshots
- Adding any NVR or DVR to the platform-NVR
- Adding any analogue cameras to the platform-NVR, unless confirmed per design
- On-site or field operations

---

*This module is a reusable building block. Validate scope, camera support, retention and monitoring-array sizing against the current customer's RFP/ITB before issuing.*