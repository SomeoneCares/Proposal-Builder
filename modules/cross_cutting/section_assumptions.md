# Assumptions, Dependencies & Risks

**Token:** `{{section_assumptions}}`  
**Group:** Cross-Cutting  
**Required:** Yes

---

## General Assumptions

- VertoWave operates on a standard forty (40) hour work week, with resources adhering to an eight (8) hour schedule from Sunday to Thursday, or other mutually agreed local working days. Working hours are from 9 AM to 5 PM local time, excluding official local holidays. Any other standard local business hours can be mutually agreed upon, referred to as "working days".
- The entire project will be delivered remotely, and remote access is mandatory throughout its lifecycle. The customer will provide Verto Wave with the required credentials and access, including any required remote access.
- Build/implementation activities are only concerned with implementing and configuring the systems as per the agreed-upon design, and apply only to systems and configurations that meet all the requirements mentioned in the designing and planning stage.
- Implementation activities will be performed remotely. Where the optional managed operations service is selected, operations activities and the operations team will follow the allocation provided in the OLA and will be delivered from the central site.
- Integration with third-party applications will be provided if applicable — meaning that the system is healthy, supported by the involved system vendors, and provides supported integration methodology and compatibility scenarios per the involved systems vendors' guidelines and supportability matrix.
- The customer should ensure the dedication of stakeholders to effectively participate in the requirement gathering and in system design.
- Delays in responses or feedback from the customer's resources will lead to corresponding delays in the project schedule.
- The customer will provide Verto Wave with the needed credentials and access, including any needed remote access, in all locations.
- All requirements and recommendations raised during the envisioning phase will be addressed by the customer before kick-off of build activities.
- All required network communication ports requested during the implementation phase will be opened in firewalls within one working day of the request.
- Hardware, operating system and database specifications will be recommended by Verto Wave during the design workshop.
- Any modification or additional requirements beyond the stated scope will be handled through a change request.
- Scope is limited to solutions mentioned in this document and not any other solution, even those in the same portfolio.
- The customer will provide reliable, stable connectivity at every site and in the central data center for all systems contributing to this project.
- The customer will hold a full backup of the solutions from the installation date onward.
- The customer technical team will make all required environment information available to Verto Wave resources for work to be completed successfully.
- During the analysis and design phase, the customer and Verto Wave will finalize the detailed design before starting the deployment phase.
- There is no security policy or firewall blocking required communication or replication between servers.
- The parties acknowledge that the successful completion of the Services requires their full and mutual good faith cooperation. Where agreement, approval, acceptance, consent or similar action by either party is required by any provision of this proposal, such action will not be unreasonably delayed or withheld. The customer agrees that to the extent its failure to meet its responsibilities results in a failure or delay by Verto Wave in performing its obligations, Verto Wave will not be liable for such failure or delay.
- If an engagement end date is not stated, the terms and conditions of this proposal expire twelve months from the Effective Date. If either party wishes to extend, both parties may mutually agree to extend before the expiration date. If the expiration date has been exceeded, a new and independent contractual agreement will need to be drawn up and agreed by both parties.
- Services identified in this proposal which include configured, installed, upgraded or implemented software are not subject to customer acceptance.

## Customer Responsibilities

- The customer will provide Verto Wave with the required credentials and access, including any required remote access, in all locations.
- All requirements and recommendations identified during the envisioning stage and outlined in the design document must be addressed by the customer before the kick-off of build activities.
- All required network communication ports requested during the building/implementation stage should be opened in the firewall within one business day of the request.
- The customer should ensure reliable, stable connectivity with all systems involved in this project.
- The customer should maintain a complete backup (full, incremental, differential, etc.) of the implemented solutions under this scope from the date of installation.
- The customer's technical team should provide all required information about the environment to ensure Verto Wave resources can work effectively both onsite or offsite.
- All administrative accounts for the services specified within the scope of this engagement must be prepared and handed over to the Verto Wave team prior to the commencement of deployment.
- The customer should provide full administrative access to the existing servers and services, where applicable.
- The solution servers must meet all prerequisites outlined in the design documents before deployment.
- There is no security policy or firewalls blocking required communication or replication between servers.
- During the designing and planning stage, the customer and Verto Wave must finalize the detailed design prior to starting the building stage.
- All the implemented firewalls and security policies should allow the required communication or replication between servers.
- Any required certificates for securing the solution will be provided by the customer.
- The customer will purchase any required operating system, database, or application subscription licenses, where applicable.
- The naming convention will be established and agreed upon during the designing and planning stage.
- The customer will ensure dedication of stakeholders to participate effectively in the requirement gathering and system design.
- Designate stakeholders to participate in meetings.
- Facilitate the information-gathering sessions.
- Ensure that stakeholders are committed to actively participate in requirement gathering and system design.
---

## Figure — <Insert approved generic diagram / screenshot here>

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic diagram or screenshot relevant to this section's content (architecture, flow, dashboard, or topology as appropriate). No customer-specific names, environment, architecture, site names, or branding. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic image here. See image-placement guidance notes.]*

---


## Assumptions Specific to DeviceX/SDX Solution

- The solution will be deployed once in a single production environment.
- Video retention period, camera recording resolution, frame rate, and video bitrate assumptions (where NVR is in scope) — confirm per bid and document in the design stage. Do not carry forward assumptions from a prior engagement without validation.
- The customer should avail reliable stable/high connectivity with all systems contributing to this project and Internet Connectivity.
- Where selected, operations activities will take place only on the Verto Wave-implemented solution.

## Multi-Location / Regulatory Assumptions (where applicable)

*Include this subsection where the engagement spans multiple operating locations or jurisdictions. De-sectorize the wording to match the current engagement; do not assert regulatory positions that have not been confirmed.*

- The customer holds, or will obtain, all licenses and regulatory approvals required to operate the service and to carry voice and data traffic in each operating location.
- The customer confirms that the intended cross-border flow of data to the central data center is permitted under the data protection and relevant sector regulations of each country of operation.
- The customer is responsible for equipment import, customs clearance and in-country delivery of appliances to each site.
- Where encryption, lawful interception or numbering restrictions apply in a location, the customer will notify Verto Wave during the envisioning phase so the design can accommodate them.
- The customer will procure and have active at each site, and in the central data center, at least one access service meeting the minimum characteristics, before the site build for that location begins. Where a second independent service is required for resilience, the customer will procure it.

## Dependencies

- Delivery of backend and management infrastructure in the customer datacentre as per the design.
- Secure communication channels (e.g., VPN, encrypted connections) for internal and external data exchange.
- Availability of required network communication ports opened in the firewall per the timelines above.
- Availability of customer technical team for requirement gathering, system design, and knowledge transfer.
- Availability of customer administrative credentials and access.
- Customer datacentre readiness (power, cooling, rack space, physical security) — note: civil/electrical/power/UPS work is out of scope.

## Risks (to be elaborated per bid in the RAID log)

The following are representative risk themes drawn from prior multi-location deployments. They are starting points for the per-bid RAID log, not a committed risk register. Validate, add, remove and re-weight per engagement.

- Customer-provided access quality below service-quality thresholds for priority traffic — mitigate via minimum access characteristics published per bid and validated per site during design; multi-path design so a second customer service can be added where the first is insufficient; quality-based steering and adaptive media degradation; per-site quality baseline recorded before go-live commitment.
- Customs or import delay for appliances — mitigate via early hardware forecast issued at design sign-off; core built on temporary or cloud infrastructure so the central side proceeds in parallel; location rollout sequenced by clearance readiness.
- Regulatory restriction on cross-border data — mitigate via confirmation per location during envisioning; segmentation model supports in-country retention of designated data classes where required.
- Delay in customer-side access, credentials or permits — mitigate via access checklist issued at kick-off with named owners and dates; tracked as a standing item in weekly governance.
- Stakeholder availability for call flow / operating-model design — mitigate via design workshop scheduled in the first two weeks; default flows pre-designed so absence delays refinement rather than the build.
- Physical theft or tampering of appliances at sites — mitigate via hardware-bound encryption rendering a stolen node unreadable; continuous attestation removing a tampered node from the network automatically; central revocation and remote wipe available on report of loss.

## Mutual Cooperation

The parties acknowledge that the successful completion of the services requires full and mutual good faith cooperation. Any agreement, approval, acceptance, consent, or similar action required by either party under this proposal will not be unreasonably delayed or withheld. The customer agrees that if its failure to meet its responsibilities causes a delay or failure in Verto Wave's performance under the agreement, Verto Wave will not be liable for such delay or failure.

---

*This section is a reusable building block. The assumptions above are derived from prior VertoWave proposals and reflect standard engagement conditions. Validate and tailor per bid — do not assert facts about the current customer's environment that have not been confirmed. The "not subject to customer acceptance" clause and the 12-month expiry clause are standard commercial clauses; confirm with Legal/Solution before issuing.*