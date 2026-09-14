# Assumptions, Dependencies and Risks

**Token:** `{{section_assumptions}}`  
**Group:** Cross-Cutting  
**Required:** Yes

---

## General Assumptions

- Verto Wave operates on a standard forty (40) hour work week, with resources working an eight (8) hour schedule from Sunday to Thursday, or other mutually agreed local working days. Working hours are 9 AM to 5 PM local time, excluding official local holidays ("working days").
- Any modification or additional requirement beyond the stated scope is handled through a change request. <!-- if services or managed_services -->
- Scope is limited to the solutions described in this document and does not include any other solution, even those in the same portfolio.
- {{customer_short}} provides reliable, stable connectivity, including Internet connectivity, at every site and at the central site for all systems contributing to this project.
- No security policy or firewall blocks the communication or replication required between the solution's components.

## Licenses and Acceptance

- Software licenses are deemed delivered when the license keys or entitlements are delivered to {{customer_short}}, and are not subject to acceptance. <!-- if licenses -->
- The license term, quantities and editions are those stated in the commercial proposal. <!-- if licenses -->
- Professional services are accepted against acceptance criteria agreed during the designing and planning stage; each phase or site is accepted on successful completion of its acceptance test. <!-- if services -->
- Managed services are not subject to acceptance; service performance is measured and reported against the Operations Level Agreement. <!-- if managed_services -->

<!-- if services -->
## Delivery Assumptions

- The project is delivered remotely, and remote access is required throughout its lifecycle.
- Build and implementation activities cover implementing and configuring the systems according to the agreed design, and apply only to systems and configurations that meet all requirements identified in the designing and planning stage.
- Integration with third-party applications is provided where the system is healthy, supported by its vendor, and offers a supported integration method according to the vendor's guidelines and supportability matrix.
- Hardware, operating system and database specifications are recommended by Verto Wave during the design workshop.
- {{customer_short}} dedicates stakeholders to participate effectively in requirement gathering and system design.
- Delays in responses or feedback from {{customer_short}}'s resources lead to corresponding delays in the project schedule.
<!-- endif -->

- Managed operations activities follow the allocation defined in the Operations Level Agreement and are delivered from Verto Wave's central operations site. <!-- if managed_services -->

<!-- if services -->
## {{customer_short}} Responsibilities

- Provide Verto Wave with the required credentials and access, including remote access, at all locations.
- Address all requirements and recommendations identified during envisioning and recorded in the design document before build activities begin.
- Open the network ports requested during implementation within one business day of the request.
- Maintain a complete backup (full, incremental, differential) of the implemented solutions from the date of installation.
- Provide all required information about the environment so that Verto Wave resources can work effectively on site or remotely.
- Prepare and hand over the administrative accounts for the services in scope before deployment begins.
- Provide full administrative access to the existing servers and services, where applicable.
- Ensure the solution servers meet all prerequisites in the design documents before deployment.
- Finalize the detailed design with Verto Wave during the designing and planning stage, before the building stage starts.
- Provide any certificates required to secure the solution.
- Purchase any required operating system, database or application subscription licenses for the supporting infrastructure.
- Agree the naming convention during the designing and planning stage.
- Designate stakeholders for project meetings and facilitate the information-gathering sessions.
<!-- endif -->

<!-- if devicex -->
## DeviceX/SDX Assumptions

- The solution is deployed once, in a single production environment.
- Where selected, operations activities cover only the Verto Wave-implemented solution. <!-- if managed_services -->
- Video retention period, camera recording resolution, frame rate and bitrate are confirmed during design and recorded in the design document. <!-- if module_nvr -->
<!-- endif -->

## Multi-Location and Regulatory Assumptions (where applicable)

*[Include this subsection where the engagement spans multiple operating locations or jurisdictions; delete it otherwise. Do not assert regulatory positions that have not been confirmed.]*

- {{customer_short}} holds, or will obtain, all licenses and regulatory approvals required to operate the service and to carry voice and data traffic in each operating location.
- {{customer_short}} confirms that the intended flow of data to the central site is permitted under the data protection and sector regulations of each country of operation.
- {{customer_short}} is responsible for equipment import, customs clearance and in-country delivery of appliances to each site. <!-- if devicex -->
- Where encryption, lawful interception or numbering restrictions apply in a location, {{customer_short}} notifies Verto Wave during envisioning so that the design can accommodate them.
- {{customer_short}} has at least one access service meeting the minimum characteristics active at each site and at the central site before that site's build begins, and procures a second independent service where resilience requires it. <!-- if module_sdwan -->

## Dependencies

- Delivery of the backend and management infrastructure at {{customer_short}}'s data center, according to the design. <!-- if services -->
- Secure communication channels (for example VPN or encrypted connections) for internal and external data exchange.
- Availability of {{customer_short}}'s technical team for requirement gathering, system design and knowledge transfer. <!-- if services -->
- Availability of administrative credentials and access. <!-- if services or managed_services -->
- Data center readiness at the central site (power, cooling, rack space, physical security).

## Risks (elaborated per bid in the RAID log)

*[The risk themes below are starting points for the per-bid RAID log, not a committed risk register. Validate, add, remove and re-weight per engagement.]*

- **Access quality below service-quality thresholds** — mitigated by publishing minimum access characteristics, validating each site during design, multi-path design with quality-based steering, and recording a per-site quality baseline before go-live. <!-- if module_sdwan -->
- **Customs or import delay for appliances** — mitigated by an early hardware forecast at design sign-off, building the central platform in parallel, and sequencing roll-out by clearance readiness. <!-- if devicex -->
- **Delay in access, credentials or permits** — mitigated by an access checklist issued at kick-off with named owners and dates, tracked in weekly governance. <!-- if services -->
- **Stakeholder availability for call-flow design** — mitigated by scheduling the design workshop in the first two weeks and pre-designing default flows. <!-- if module_ipbx or module_stackx_call_center -->
- **Theft or tampering of appliances at sites** — mitigated by hardware-bound encryption, continuous attestation that removes a tampered node automatically, and central revocation and remote wipe. <!-- if devicex -->
- **Regulatory restriction on cross-border data** — mitigated by confirmation per location during envisioning and segmentation that supports in-country retention where required.

## Mutual Cooperation

The parties acknowledge that the successful completion of the services requires full and mutual good-faith cooperation. Any agreement, approval, consent or similar action required by either party under this proposal will not be unreasonably delayed or withheld. {{customer_short}} agrees that if its failure to meet its responsibilities causes a delay or failure in Verto Wave's performance, Verto Wave is not liable for that delay or failure.

---

*This section is a reusable building block. Validate and tailor it per bid. The acceptance clauses follow the offering selected in the builder; confirm them with Legal before issue.*
