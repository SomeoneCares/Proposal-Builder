# Event Correlation and Root-Cause Analysis <!-- if not vendor_names -->
# OpenText OBM <!-- if vendor_names -->

**Token:** `{{product_ot_obm}}`
**Group:** OpenText Products
**Required:** No

---

Events from every monitoring source arrive in one console, where correlation removes duplicates and symptoms and leaves the operator with a probable cause. <!-- if not vendor_names -->
OpenText OBM collects events from every monitoring source into one console, where correlation removes duplicates and symptoms and leaves the operator with a probable cause. <!-- if vendor_names -->

## What It Delivers

- One event console for infrastructure, network, application and platform sources
- Deduplication and suppression, so a single fault does not arrive as fifty alerts
- Topology-based correlation that uses the service model to separate cause from symptom
- Automatic ticket creation and update in the service management platform <!-- if product_ot_smax -->
- Automatic runbook execution for known faults <!-- if product_ot_oo -->
- Operator views per service, with the event history that led to the current state

## Build Activities <!-- if services -->

<!-- if services -->
- Deploy the platform and connect the in-scope monitoring sources
- Configure deduplication, suppression and maintenance windows
- Configure correlation rules against the modelled services <!-- if product_ot_ucmdb -->
- Configure ticketing and notification, including severity mapping
- Tune the rules over an agreed observation period so the console stays readable
<!-- endif -->

## How Correlation Is Judged

Correlation is assessed on how far it reduces the events an operator must read, measured before and after tuning across the agreed observation period. A probable cause is presented for the operator to validate; it is not warranted to be the actual cause.

*[Confirm the sources in scope, the observation period and the noise-reduction baseline per bid.]*
