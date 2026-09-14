# Out-of-Scope Activities

**Token:** `{{section_out_of_scope}}`  
**Group:** Cross-Cutting  
**Required:** Yes

---

The following activities are out of scope unless explicitly stated otherwise in the in-scope sections of this proposal. This is the single list of exclusions for the whole proposal.

## Hardware, Cabling, Civil and Field Work

- Supplying and mounting hardware, network equipment and storage devices, and the associated cabling, other than DeviceX appliances. <!-- if devicex -->
- Supplying and mounting hardware, network equipment and storage devices, and the associated cabling. <!-- if not devicex -->
- Providing or mounting hardware for the central management and monitoring infrastructure, except devices delivered by Verto Wave.
- Civil or electrical work, and resolving power availability from UPS.
- Any activity at the sites, including delivery and mounting of devices, field support and on-site operations. <!-- if devicex -->
- Logistics tasks and direct communication with end users.
- Passive work, including mounting hardware, cabling and connecting screens.
- Replacement of existing site devices, and providing screens or display equipment. <!-- if devicex -->

## Rework, Hardware Failure and Environmental Issues

- Rework, including of the central management infrastructure, caused by hardware availability or failure, network connectivity issues, electricity instability or outages.
- Troubleshooting hardware, network or power failures, except for devices delivered by Verto Wave.

## Third-Party Systems, Integration and Migration

- Deployment, configuration, integration or troubleshooting of third-party systems, applications, services or products not named in the in-scope sections.
- Integrating with components that do not support the standard protocols used by the solution, or with end-of-life or end-of-support systems.
- Operating third-party systems, and managing systems or devices that offer no supported means of integration.
- Implementing new systems or solutions, development and debugging, and migration activities.
- Deploying or configuring third-party endpoint security products, and managing devices that cannot be integrated with StackX Endpoint Management. <!-- if module_stackx_endpoint_mgmt -->
- Migrating historical tickets, records or data from an existing service management platform. <!-- if module_stackx_itSM -->
- Onboarding log sources that offer no supported collection interface. <!-- if module_stackx_event_log_mgmt or module_stackx_security -->
- Writing or modifying application code, or fixing application defects, within the release pipeline. <!-- if module_stackx_devops or module_stackx_alm -->

## Workloads, Operating Systems and Databases <!-- if module_virtualization or module_business_workloads -->

- Deploying software on the created virtual machines or containers. <!-- if module_virtualization or module_business_workloads -->
- Configuring or troubleshooting the business workloads hosted on DeviceX. <!-- if module_virtualization or module_business_workloads -->
- Installing or upgrading operating systems or databases, and application compatibility checks or troubleshooting. <!-- if module_virtualization or module_business_workloads -->

## Changes to the Existing Environment

- Any change to existing devices or configurations (switches, routers, existing firewalls and similar).
- Any design change to the existing environment.

## Connectivity, Carriers and Access Services <!-- if devicex -->

<!-- if devicex -->
- Procurement, supply, resale, contracting or funding of any connectivity service — Internet, fiber, DSL, satellite, cellular, MPLS or other wide-area transport — at any site or at the central site. All access services are contracted directly by {{customer_short}} with its chosen providers.
- Communication, negotiation, fault escalation or SLA management with telecom operators, ISPs, carriers or satellite operators on {{customer_short}}'s behalf.
- Responsibility for the availability, throughput, latency or quality of access services provided by {{customer_short}}, and any service credit arising from their failure.
- Design, survey, installation or upgrade of last-mile access, including satellite terminal installation and commissioning.
- Customs clearance, import permits, duties, in-country logistics and delivery of equipment to site.
<!-- endif -->

## Licensing and Certificates

- Telecommunications, telephone numbering, VoIP or data-service licenses and regulatory permits in any country of operation. <!-- if module_ipbx or module_stackx_call_center -->
- Procurement of licenses that are not identified as in scope.
- Acquisition of commercial certificates.

## Surveillance <!-- if module_nvr -->

- Adding existing NVR or DVR systems to the platform NVR. <!-- if module_nvr -->
- Adding analog cameras to the platform NVR, unless confirmed in the design. <!-- if module_nvr -->

## Security Testing, Recordings and Documentation

- Penetration testing, vulnerability assessments, code reviews and forensic activities.
- Video recordings or screenshots, other than the recorded training session. <!-- if section_training -->
- Video recordings or screenshots. <!-- if not section_training -->
- Documentation other than the design documents and the agreed deliverables.

## Backup, Disaster Recovery, Network and Security Activities

- Backup, network and security activities beyond those listed as in scope or selected from the extended security services.
- Disaster recovery activities, unless a backup and continuity service is selected and separately quoted.
- Procuring backup storage capacity or media. <!-- if module_stackx_backup -->

## Other Exclusions

- Creating new SLAs or agreements with vendors for systems other than those in scope.
- Managing or monitoring endpoints or workstations, unless explicitly in scope. <!-- if not module_stackx_endpoint_mgmt -->
- Any activity not explicitly listed in the in-scope sections.

## Connectivity Boundary <!-- if devicex -->

- Wide-area access services remain {{customer_short}}'s procurement. Verto Wave supplies the platform, not the circuits, and {{customer_short}} keeps full freedom to select or change access providers at each location without redesigning the network. <!-- if devicex -->
- Where a control depends on equipment or tenancy that {{customer_short}} supplies — access-layer switching, cloud accounts, directory services — Verto Wave's commitment is to design, verify and evidence it, not to operate what it does not supply. <!-- if devicex -->

## Application Boundary

- {{customer_short}}'s business applications remain their supplier's products. Verto Wave does not write, modify or take ownership of application code; where a control lives inside an application, Verto Wave's role is independent testing, evidence and supervision.
- Supply, configuration or support of specialized application peripherals, devices or application software, application licensing, and application data migration remain {{customer_short}}'s responsibility.

---

*This is the single exclusion list for the proposal; modules do not repeat it. Confirm with Legal that no additional exclusions are needed for the current bid.*
