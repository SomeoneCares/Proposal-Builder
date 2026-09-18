# Network Operations Management <!-- if not vendor_names -->
# OpenText NOM <!-- if vendor_names -->

**Token:** `{{product_ot_nom}}`
**Group:** OpenText Products
**Required:** No

---

Network monitoring discovers the routed and switched estate, keeps its topology current, and reports faults and performance against it. <!-- if not vendor_names -->
OpenText NOM discovers the routed and switched estate, keeps its topology current, and reports faults and performance against it. <!-- if vendor_names -->

## What It Delivers

- Discovery of network devices and interfaces, with a topology map kept current automatically
- Fault monitoring with root-cause suppression, so a failed uplink does not alarm everything behind it
- Performance monitoring of interfaces, links, capacity and errors, with historical trends
- Threshold and baseline alerting per interface class
- Configuration capture for in-scope devices, with change history and comparison
- Reporting on availability, utilization and the devices that raise the most faults

## Build Activities <!-- if services -->

<!-- if services -->
- Deploy the platform and configure device credentials for the in-scope ranges
- Run discovery, validate the topology and agree the device and interface inventory
- Configure polling intervals, thresholds and alert routing per device class
- Configure the agreed reports and dashboards
- Forward events to the correlation console <!-- if product_ot_obm -->
<!-- endif -->

## Sizing Basis

Sizing follows the number of devices and interfaces polled, the polling interval and the retention period. The figures are recorded in the design document and confirmed against the device inventory.

*[Confirm device counts per class, polling intervals and retention per bid.]*
