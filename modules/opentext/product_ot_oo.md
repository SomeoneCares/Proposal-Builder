# Runbook Automation and Orchestration <!-- if not named_product_ot_oo -->
# OpenText Operations Orchestration <!-- if named_product_ot_oo -->

**Token:** `{{product_ot_oo}}`
**Group:** OpenText Products
**Required:** No

---

Repeatable operational work runs as a governed flow instead of a manual procedure, started by an operator, by the service desk or by an event. <!-- if not named_product_ot_oo -->
OpenText Operations Orchestration runs repeatable operational work as a governed flow instead of a manual procedure, started by an operator, by the service desk or by an event. <!-- if named_product_ot_oo -->

## What It Delivers

- Runbooks for the routine tasks agreed in the design, each versioned and auditable
- Orchestration across systems, so one flow can touch several platforms in sequence
- Approval steps inside a flow where an action needs authorization before it proceeds
- Triggering from the service catalog, so a request fulfils itself <!-- if product_ot_smax -->
- Triggering from an event, so a known fault is acted on before it is escalated <!-- if product_ot_obm -->
- A credential store, so flows run without passwords held in the flow itself

## Build Activities <!-- if services -->

<!-- if services -->
- Deploy the platform and connect it to the systems in scope
- Build and test the agreed automation flows, each with its pre-checks and rollback path
- Configure approval gates, scheduling and error handling
- Integrate with the service catalog and the event console as selected
- Hand over the flow inventory, the run history and the administration guide
<!-- endif -->

## Scope Boundaries

The number of flows is agreed in the design and recorded in the scope. Each flow is limited to systems that expose a supported interface and a working credential.

*[Confirm the automation scenarios and their target systems per bid.]*
