# Project Management Methodology

**Token:** `{{section_pm_methodology}}`  
**Group:** Cross-Cutting  
**Required:** Yes

---

## Overview

Verto Wave Project Management Methodology consists of five stages. The methodology is mapped to the PMI standard Project Management Process Groups, and RAID (Risks, Assumptions, Issues, Dependencies) logging is used throughout the project lifecycle.

## Project Management Stages

The overall project lifecycle and their interrelations are depicted in the project management stages diagram.

- **Envisioning**
- **Designing & Planning**
- **Building (Deployment, Stabilization and Testing)**
- **Monitoring & Controlling**
- **Closure**

## PMI Process Group Mapping

| PMI Process Group | Verto Wave Project Stage |
| :--- | :--- |
| Initiating Process Group | Envisioning |
| Planning Process Group | Designing & Planning |
| Executing Process Group | Building |
| Monitoring & Controlling Process Group | Monitoring & Controlling |
| Closing Process Group | Closure |

## Stage 1 — Envisioning

Envisioning stage is generally when a project is formally approved and assigned to a Project Manager and Tech Lead. Two main activities should be completed during this project stage: developing the project charter and identifying key project stakeholders.

The main objective of this stage is launching the project, getting the required data regarding the customer's environment, and aligning the currently identified stakeholders with the project's objectives, constraints, and timeline.

During this stage, a consecutive series of technical workshops should be held so the project management team deeply goes inside what is already on the ground at the customer side. This can serve as an early form of planning; it sets the stage for the more formal planning process that will take place during the project's Designing & Planning stage.

## Stage 2 — Designing & Planning

In this stage, the project management team will start the planning process to build a solid ground for the project. The planning stage is where they evaluate and manage the timeframe, and the possible risks of the project.

The most important task here is to develop the project plan which will be used for Project Performance Monitoring throughout the project life cycle in the Monitoring and Controlling stage.

The most important outcomes of this stage are:

- A confirmed Scope document, which includes the project detailed scope of work
- Confirmed project management deliverables

## Stage 3 — Building (Deployment, Stabilization and Testing)
---

## Figure — Delivery Phasing / Project Stages Diagram

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic delivery-phasing / project-stages diagram showing the phases (from the delivery phasing subsection: Phase 1 … through optional Phase 6 managed ops) and the 5-stage PMI-mapped PM methodology + RAID log. No customer-specific milestone names, no customer-specific dates, no customer site names. -->
<!-- Suggested source: EGYCash "Fig. 1. Verto Wave Project Management Stages" — use only as a composition reference for the PM stages shape; genericise labels; strip any customer-specific milestone names/dates. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic delivery-phasing / project-stages diagram here. See image-placement guidance notes.]*

---


This stage is focused on completing the work defined in the Project Plan, which is completed and approved by the stakeholders at the end of the project planning stage. It involves coordinating all the resources to get the work done efficiently and effectively so that the project keeps delivering the promised objective.

This stage is where most of the work is carried out, and where products and deliverables are built, assembled, constructed, and created.

The most important output here is the Deliverable, which is produced in line with the defined Project Plan.

During this stage, Changes will also be implemented but only those which are Approved by the management or change control board or by the steering committee.

## Stage 4 — Monitoring & Controlling

Project monitoring activities are performed throughout all project stages. In this stage, project work is required to be tracked, reviewed, in order to regulate the progress and performance of the project; identify any areas in which changes to the plan are required; and initiate the corresponding changes.

RAID technique is used to evaluate the effectiveness of a work assignment. RAID log is created and updated throughout project lifecycle.

The term RAID is an acronym that represents the following terms that apply to project management:

- **Risks:** Risks represent potential challenges that can interfere with the success of the assignment. The RAID log explains the risks and their causes; discusses the effects they can have on the project's goals and develops strategies for avoiding and overcoming them.
- **Actions:** Actions are the tasks team members plan to work on to deliver a quality final product. In this section, project managers identify the employees responsible for the tasks and the timeline for finishing them.
- **Issues:** Issues are hardships project management teams have encountered along the project. The log explains how the issue transpired, who contributed to its occurrence and what team members did to resolve it.
- **Decisions:** Decisions are choices the group made throughout the course of the project, which allow employees to track changes to their objectives. In the log, project managers may write what they decided on, who made the decision and when they agreed on the choice.

## Stage 5 — Closure

Project closure is the final stage of project management methodology. It is when the project has been completed and finished successfully and authorized by the designated customer authority.

At this stage, the handover and acceptance activities outlined in the scope documentation will be implemented. The key focus of the project closeout is the handover of the product, good, or service to the customer, whether physical or virtual.

## Change Procedures

Change management is handled per the Change Management Procedure section of this proposal. See `{{section_change_mgmt}}`.

## Delivery Phasing (separate from the PM methodology above)

The PM stages above describe how we manage the project. The phasing below describes how we sequence the delivery. They are complementary, not the same thing.

Delivery is phased so that the central/core is proven before location rollout begins, and so the first location validates the model end to end before the remaining locations are executed in parallel.

The pilot-then-parallel sequence is deliberate. The first location is where unknowns surface — carrier behaviour, customs, power, user workflow. Absorbing them once, into a template, is what allows the remaining locations to be delivered at pace rather than repeating the same discovery multiple times.

| Phase | Focus | Key Outcomes |
| :--- | :--- | :--- |
| Phase 1 — Envisioning & Design | Requirements gathered, site profiles completed, classes assigned, traffic and security models agreed, call flows designed, design document signed off, hardware forecast issued. | Requirements gathered; site profiles completed; traffic and security models agreed; design document signed off; hardware forecast issued. |
| Phase 2 — Core Build | Backend, hub, certificate authority, monitoring and log management, central platform and remote-room edge in service and validated. | Core platform components in service and validated. |
| Phase 3 — Pilot Rollout | First location's sites provisioned via zero-touch, end-to-end session validated against the service quality targets, template hardened from real-world findings. | First location validated end to end; template hardened. |
| Phase 4 — Parallel Rollout | Remaining locations deployed against the hardened template, each site closed out with the standard acceptance test. | Remaining locations delivered at pace against a proven template. |
| Phase 5 — Training & Handover | Administration training delivered, documentation issued, operational handover completed. This is the final phase of the base scope. | Training delivered; documentation issued; handover completed. |
| Phase 6 (Optional) — Managed Operations | Only if the managed service option is selected. Remote managed service commences under the OLA. Where the customer self-operates, the engagement concludes at Phase 5. | Managed operations commenced under the OLA, or self-operation concluded at handover. |

---

*This section is a reusable building block. The methodology above is near-verbatim across prior VertoWave proposals. Confirm per bid whether any stage gating, milestone definitions, or RAID review cadence require tailoring for the current engagement. The delivery phasing is platform-agnostic; tailor the phase count, pilot location and parallel-location count to the current engagement.*