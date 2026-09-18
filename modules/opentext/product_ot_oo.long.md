# Runbook Automation and Orchestration <!-- if not named_product_ot_oo -->
# OpenText Operations Orchestration <!-- if named_product_ot_oo -->

**Token:** `{{product_ot_oo}}`
**Group:** OpenText Products
**Required:** No

---

Repeatable operational work runs as a governed flow instead of a manual procedure, started by an operator, by the service desk or by an event. <!-- if not named_product_ot_oo -->
OpenText Operations Orchestration runs repeatable operational work as a governed flow instead of a manual procedure, started by an operator, by the service desk or by an event. <!-- if named_product_ot_oo -->

The product separates three things that are usually mixed together in scripts: where a flow is written, where it is executed and governed, and where it reaches the target system from. Flows are authored in a design tool from tested building blocks, published to a central execution server that holds the credentials, the roles, the schedule and the run history, and executed by workers placed in the network zones where the target systems actually live.

## Where It Fits in This Project

{{customer_short}}'s requirement is that routine operational work stops depending on which engineer is on shift and what they remember. The same task run by two people on two days produces two results; run as a flow it produces one, with a record of who started it, against what, and what it returned.

In this project the platform is the execution layer beneath the rest of the solution: the service desk uses it to fulfil catalog requests without manual work, the event console uses it to act on known faults before they are escalated, and operators use it directly for tasks that are too frequent to keep doing by hand. Its scope is the automation scenarios agreed during the design stage; the number of flows is held in the professional services scope and is not repeated here.

## Platform Components

<!-- if not named_product_ot_oo -->
- **Central execution server** — publishes and runs flows, holds the credential store, the role model, the schedule and the complete run history, and exposes the interface other systems call to start a flow.
- **Database** — the store for published content, run history, schedules and audit records.
- **Workers** — the execution components that reach the target systems. Workers are grouped, and a flow step is directed at the group that can reach its target, so a segmented estate does not require a path from one central server to everything.
- **Flow authoring tool** — the design environment in which flows are built from supplied building blocks, tested step by step and versioned before publication.
- **Supplied content** — the maintained library of tested operations for common platforms and protocols: remote command execution, web service calls, database operations, file handling, mail, virtualization and directory operations.
- **Credential store** — the protected store of the accounts flows use, so no password is held inside a flow or passed on a command line.
- **Run history and audit** — the record of every run: who or what started it, its inputs, the path it took, the result of each step and its outcome.
<!-- endif -->

<!-- if named_product_ot_oo -->
- **Central** — publishes and runs flows, holds the credential store, the role model, the schedule and the complete run history, and exposes the REST interface other systems call to start a flow.
- **Database** — the store for published content, run history, schedules and audit records.
- **Remote Action Service workers** — the execution components that reach the target systems. Workers are grouped, and a flow step is directed at the worker group that can reach its target, so a segmented estate does not require a path from Central to everything.
- **Studio** — the design environment in which flows are built from supplied operations, debugged step by step and versioned before publication.
- **Content packs** — the maintained library of tested operations for common platforms and protocols: remote command execution, web service calls, database operations, file handling, mail, virtualization and directory operations.
- **System accounts and credential store** — the protected store of the accounts flows use, so no password is held inside a flow or passed on a command line.
- **Run history and audit** — the record of every run: who or what started it, its inputs, the path it took, the result of each step and its outcome.
<!-- endif -->

*[The component list follows the vendor's current packaging. Confirm the component names and which supplied content is inside the entitlement being quoted with the Verto Wave product team before issue.]*

## What It Delivers

- Runbooks for the routine tasks agreed in the design, each versioned and auditable
- Flows built from supplied content for common platforms and protocols, so a flow starts from tested building blocks rather than a blank script
- Orchestration across systems, so one flow can touch several platforms in sequence and carry the result of one step into the next
- Approval steps inside a flow where an action needs authorization before it proceeds, with the approver and the decision recorded on the run
- Triggering from the service catalog, so a request fulfils itself <!-- if product_ot_smax -->
- Triggering from an event, so a known fault is acted on before it is escalated <!-- if product_ot_obm -->
- Triggering on a schedule, and by a call from another system, so the same flow serves every route into it
- A credential store, so flows run without passwords held in the flow itself
- Role-based access to flows and to the systems they touch, separating who may author a flow from who may run it and who may approve it
- Workers placed per network zone, so a flow reaches segmented targets without opening a path from one server to the whole estate
- A run history that records who ran what, when, against which target and with what result — the evidence an auditor asks for after an automated change


[[figure: ot-oo-automation | A runbook from trigger to result]]

## Integration

The links below are configured only where both platforms are part of this proposal.

- The service management platform starts a flow when a catalog item is approved or a standard change is authorized, and the flow returns its result to the record that requested it. <!-- if product_ot_smax -->
- The event console starts a flow when a known fault is detected, under the conditions agreed for that fault, and receives the outcome so the event shows what was attempted. <!-- if product_ot_obm -->
- The configuration management database is read by a flow to select and validate its target before acting, so a flow acts on a known record rather than on a hostname typed into a field. <!-- if product_ot_ucmdb -->
- The network monitoring platform triggers flows for the agreed network faults, and is the source of the device detail a network flow acts on. <!-- if product_ot_nom -->
- Alerting rules in the server and infrastructure monitoring platform call a flow through the platform's inbound interface. <!-- if product_el_observability -->
- Alerting rules in the log platform call a flow when an agreed log condition is matched. <!-- if product_el_logs -->
- Alerting rules in the application performance platform call a flow for the agreed application conditions. <!-- if product_el_apm -->
- Alerts from the observability platform call a flow through the platform's inbound interface. <!-- if module_stackx_observability_apm -->
- Alerts from the network operations platform call a flow for the agreed network conditions. <!-- if module_stackx_network_ops -->
- The service management platform in scope starts flows for approved requests and standard changes. <!-- if module_stackx_itSM -->
- The automation and orchestration platform in scope and this platform are divided by domain during design, so one owns each automated task rather than both. <!-- if module_stackx_automation_orchestration -->

## Build Activities <!-- if services -->

<!-- if services -->
**Design confirmation**

- Agree each automation scenario with its owner: the trigger, the target systems, the pre-conditions, the expected result and what must happen when a step fails.
- Agree which scenarios may run unattended and which require an approval step, and who approves them.
- Agree the complexity band for each flow — steps, target systems and decision points — and record it, so the scope is bounded by work rather than by count alone.
- Confirm that a documented procedure exists for each scenario; where it does not, it is written and agreed before the flow is built.

**Platform deployment**

- Deploy the central execution server and its database and bring them to the supported patch level.
- Deploy workers into each network zone that holds target systems, and configure the worker groups that flow steps will be directed at.
- Install the supplied content in scope, and agree how content updates will be applied after handover.
- Configure backup of the database and the published content, and prove a restore before flows are built.
- Configure the platform's published name and certificate for the interface other systems will call.

**Access, credentials and governance**

- Configure the credential store and load a service account per target system, each holding the least privilege its task needs.
- Configure the role model: who authors, who publishes, who runs, who approves and who may only read the run history.
- Configure the audit and retention settings for the run history, to the period agreed in the design stage.

**Flow build and test**

- Build each agreed flow from supplied content, with its pre-checks, its decision points and its logging.
- Build the failure handling for each flow: what it does when a step fails, what it reports, and the rollback path where the target system supports one.
- Configure the approval gates, the scheduling and the input validation for each flow.
- Test each flow step by step against the agreed test targets, including the failure path, by forcing a failure rather than assuming it.
- Run each flow end to end against its test target and record the expected result.

**Integration build**

- Integrate with the service catalog so an approved request runs its flow and receives the result. <!-- if product_ot_smax -->
- Integrate with the event console so a matching event runs its flow under the agreed conditions, and the outcome returns to the event. <!-- if product_ot_obm -->
- Configure the read from the configuration record used for target selection. <!-- if product_ot_ucmdb -->
- Configure the inbound calls from the monitoring and log platforms in scope. <!-- if product_el_observability or product_el_logs or product_el_apm or module_stackx_observability_apm or module_stackx_network_ops -->

**Production introduction and handover**

- Run each flow in production under supervision before it is released to run unattended, and record the result of each supervised run.
- Review the run history with {{customer_short}} after the supervised period and confirm which flows may run unattended.
- Hand over the flow inventory, the flow documentation, the credential register, the run history and the administration guide.
<!-- endif -->

## Hardware Requirements

The specifications below are this product's own components. They are the vendor's recommended figures for the deployment sizes shown, are indicative, and are confirmed against the flow count, concurrency and run-history retention recorded in the design document.

| Component | Small — up to ~10 concurrent flow executions | Medium — up to ~50 concurrent | Large — above ~50 concurrent |
| :--- | :--- | :--- | :--- |
| Central execution server | 4 vCPU / 8 GB RAM / 100 GB SSD | 8 vCPU / 16 GB RAM / 200 GB SSD | 16 vCPU / 32 GB RAM / 500 GB SSD |
| Database | 4 vCPU / 16 GB RAM / 200 GB SSD | 8 vCPU / 32 GB RAM / 500 GB SSD | 8 vCPU / 32 GB RAM / 1 TB SSD |
| Worker, per network zone | 2 vCPU / 4 GB RAM / 50 GB SSD | 4 vCPU / 8 GB RAM / 100 GB SSD | 4 vCPU / 8 GB RAM / 100 GB SSD per worker |
| Second execution server for high availability, where in scope | Matched pair at the tier specification, behind a load balancer | Same | Same |
| Flow authoring workstation | 4 vCPU / 8 GB RAM / 50 GB SSD | Same | Same |

- Concurrency drives this platform, not flow count: a hundred flows that run once a week size smaller than five that run every minute.
- Database storage is set by the run-history retention period; a flow that logs large outputs on every step will grow it faster than the flow count suggests.
- One worker is required per network zone that cannot be reached from the execution server, and additional workers where concurrency inside a zone requires them.
- The authoring workstation is only required where {{customer_short}}'s team will author flows after handover.

*[Hardware figures are indicative and are confirmed during the design stage. Confirm with the Verto Wave product team which release the figures are drawn from, and re-check them against that release's sizing guide before issue.]*

## What Automation Needs

- A supported interface on every target system — a documented API, a command-line session over a secure transport, a remote management interface or database access
- A service account per target system, holding the least privilege the task needs, with a named owner and an agreed rotation process
- Network paths open from the workers to their target systems, on the protocols recorded in the design document
- Test targets, or an agreed window on production targets, so each flow can be proven before it is trusted
- A documented current procedure per scenario, and a named owner who can approve what the flow is allowed to do unattended
- Name resolution, time synchronization and a certificate for the platform's published name

## Scope Boundaries

The number of flows is agreed in the design and recorded in the scope, and each flow is bounded by the complexity band recorded with it — the number of steps, target systems and decision points it may contain. A scenario that turns out to exceed its band is handled as a change request. Each flow is limited to systems that expose a supported interface and a working credential. A flow automates the procedure as it is agreed and documented; where no agreed procedure exists, defining it is design work that is completed before the flow is built.

### Not Covered by This Product's Scope

- Target systems that expose no supported interface, and automation by driving a graphical interface or screen-scraping a terminal session where no programmatic interface exists.
- Flows that require a person to interpret an intermediate result and decide, beyond the approval steps agreed in the design.
- Rollback of actions the target system cannot reverse; the flow records what it did, and the compensating step exists only where the target supports one.
- Development of new supplied content for platforms the content library does not cover.
- Maintaining flows against changes made to the target systems after handover, unless a managed service covering them is separately in scope.
- Automating a procedure that is not agreed and documented, or that differs between teams or sites.
- The correctness of the outcome inside the target system: the flow performs the agreed actions and reports what the target returned.

## Acceptance <!-- if services -->

<!-- if services -->
Automation is accepted when, for every flow in the agreed inventory:

- The flow executes end to end against its agreed test target and produces the result recorded for it in the design document.
- Its failure path is demonstrated by forcing a failure, and the flow reports the failure rather than stopping silently or leaving the target half-changed.
- Its approval step, where it has one, blocks execution until the nominated approver decides, and the decision is recorded on the run.
- Its trigger is demonstrated from the route agreed for it — the service catalog, an event, a schedule or a call from another system.
- Its run record shows the executor, the target, the inputs, the path taken and the outcome.

Acceptance covers the flows delivered under this scope and their behavior as built. It does not extend to the behavior of the target systems, and no restoration or resolution time is committed on the basis of an automated flow.
<!-- endif -->

*[Confirm the automation scenarios, their target systems, the trigger for each one and its complexity band per bid.]*

*[Verify with the Verto Wave product team before issue: the current product and component names, which supplied content is included in the entitlement being quoted, and the licensing basis — it has historically been counted by managed node or by flow execution, and that changes the commercial answer.]*
