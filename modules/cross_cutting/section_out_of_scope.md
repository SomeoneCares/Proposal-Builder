# Out-of-Scope Activities

**Token:** `{{section_out_of_scope}}`  
**Group:** Cross-Cutting  
**Required:** Yes

---

The following activities are out of scope, unless explicitly stated otherwise in the in-scope section of this proposal:

### Hardware, cabling, civil and field work

- Supplying and mounting hardware, network equipment and storage devices, along with the necessary cabling, other than DeviceX.
- Providing or mounting hardware, network and storage devices, including cabling, for the backend management and monitoring infrastructure, except devices delivered by Verto Wave.
- Any civil or electrical work, or resolving power availability from UPS to proceed with implementation.
- Any activity at the branches/sites, including delivery and mounting of devices.
- Any field support, on-site or field operations.
- Any logistical tasks and direct communication with the end user.
- Any passive work, including mounting hardware, cabling and connecting screens.
- Replacement of customer site devices.
- Providing any screens or display equipment.

### Rework, hardware failure and environmental issues

- Any rework, including of the centralized management infrastructure, caused by hardware availability or hardware failure, network connectivity issues, electricity instability or electricity outages.
- Troubleshooting and investigating any issues related to hardware, network or power failures, except for devices delivered by Verto Wave.

### Third-party systems, integration and migration

- Any deployment, configuration, integration or troubleshooting of third-party systems, applications, services or products not mentioned in the in-scope section.
- Integration with any other third-party products except those explicitly mentioned under the scope of work.
- Integrating with components that do not support the standard protocols used by DeviceX/SDX.
- Integrating with end-of-life (EOL) / end-of-support (EOS) systems and solutions.
- Operating third-party systems aside from the systems included in this scope.
- Managing and supporting systems and devices that do not allow a means of integration, including with StackX Endpoint Management.
- Any deployment or configuration of third-party endpoint security products not included in this proposal scope.
- Any implementation of new systems or solutions, unless explicitly in scope.
- Any development and debugging activities, unless explicitly in scope.
- Any migration activities.

### Virtualization, OS/DB and compatibility

- Deploying any software on the created virtual machines, unless explicitly in scope.
- Configuring or troubleshooting the business virtual machines hosted on DeviceX, unless explicitly in scope.
- Setting up or upgrading to newer versions of operating systems or databases, unless explicitly in scope.
- Application compatibility checks or troubleshooting with operating systems.

### Changes to the existing environment

- Any change to existing customer devices or configurations (switches, routers, existing firewalls and similar).
- Any design changes to the existing environment.

---

## Figure — <Insert approved generic diagram / screenshot here>

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic diagram or screenshot relevant to this section's content (architecture, flow, dashboard, or topology as appropriate). No customer-specific names, environment, architecture, site names, or branding. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (combine.py embeds the cover logo only). -->

*[Figure placeholder — insert approved generic image here. See image-placement guidance notes.]*

---

### Connectivity, carriers and access services

- Procurement, supply, resale, contracting or funding of any connectivity service — internet, fiber, DSL, satellite, cellular, MPLS or any other wide-area transport — at any site or in the central data center. All access services are contracted directly by the customer with its chosen providers.
- Any communication, negotiation, fault escalation or SLA management with telco operators, ISPs, carriers or satellite operators on the customer's behalf.
- Any responsibility for the availability, throughput, latency or quality of customer-provided access services, and any service credit arising from their failure.
- Design, survey, installation or upgrade of last-mile access, including satellite terminal installation, alignment and commissioning.

### Customs, import and logistics

- Customs clearance, import permits, duties, in-country logistics and equipment delivery to site.

### Licensing, certificates and telecom permissions

- Obtaining telecommunications, telephony numbering, VoIP or data-service licenses and regulatory permits in any country of operation.
- Procurement of any extra licenses that are not identified as in scope.
- Acquisition of any necessary commercial certificates, unless explicitly in scope.

### Security testing, video and documentation

- Conducting security penetration testing, vulnerability assessments, code reviews and forensic activities, unless explicitly stated as in scope.
- Any video recordings or screenshots, unless explicitly in scope.
- Any documentation other than the design documents and agreed deliverables.

### Backup, disaster recovery, network and security activities

- Any backup, network and security activities beyond those explicitly listed as in scope or explicitly selected from the extended security services.
- Any disaster recovery (DR) activities, unless the backup and continuity service is selected and separately quoted.

### Other exclusions

- Creating new SLAs and/or agreements with vendors for systems aside from those explicitly included in this scope.
- Adding any NVR or DVR to the platform NVR.
- Adding any analogue cameras to the platform NVR, unless confirmed in the design.
- Managing or monitoring any endpoint or workstation, unless explicitly in scope.
- Any activity that is not explicitly mentioned in the in-scope activities.

### Connectivity boundary (explicit)

- Wide-area access services remain a customer procurement. Verto Wave supplies the platform and not the circuits. The customer keeps full commercial freedom to select or change access providers at each location without redesigning the network or renegotiating the engagement.
- Where a control depends on equipment or tenancy the customer supplies — access-layer switching, cloud accounts, directory services — Verto Wave's commitment is to design, verify and evidence it, not to operate what it does not supply.

### Application layer boundary (explicit)

- The customer's application / application layer remains its supplier's product. Verto Wave does not write, modify or assume ownership of the application's code. Where a control lives inside that application, Verto Wave's role is independent testing, evidencing and supervision.
- Supply, configuration or support of specialised application peripherals, devices, or application software of any kind remains the customer's domain.
- Supply or licensing of the customer's core application, and any application data migration, are out of scope.

---

*This section is a reusable building block and represents the standard exclusion boundary, extended with the generic connectivity- and application-layer boundary clauses. Confirm with Legal/Solution that no additional exclusions or inclusions are needed for the current bid. Do not carry forward customer-specific or sector-specific exclusions from a prior engagement without validation.*
