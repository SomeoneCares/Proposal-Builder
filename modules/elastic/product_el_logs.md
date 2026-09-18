# Log Management and Analytics <!-- if not named_product_el_logs -->
# Elastic Log Management <!-- if named_product_el_logs -->

**Token:** `{{product_el_logs}}`
**Group:** Elastic Products
**Required:** No

---

Logs from the estate are collected centrally, parsed into a common structure, retained in tiers and made searchable for operations and investigation. <!-- if not named_product_el_logs -->
Elastic Log Management collects logs from the estate centrally, parses them into a common structure, retains them in tiers and makes them searchable for operations and investigation. <!-- if named_product_el_logs -->

## What It Delivers

- Central collection from servers, network devices, applications and platforms
- Parsing into a consistent structure, so fields mean the same thing across sources
- Retention tiers, so recent data stays fast and older data stays affordable
- Search and correlation across sources during an investigation
- Alerting on patterns, including the absence of an expected message
- Dashboards per source type and per service


[[figure: el-logs-pipeline | Log pipeline and retention tiers]]

## Build Activities <!-- if services -->

<!-- if services -->
- Deploy the platform and size the storage tiers to the agreed volume and retention
- Onboard the agreed log sources, with parsing validated per source type
- Configure retention, lifecycle and access control
- Configure the agreed alerts and dashboards
- Hand over the source inventory and the administration guide
<!-- endif -->

## Sizing Basis

Sizing follows the daily ingest volume, the number of sources and the retention held in each tier. The figures are recorded in the design document and confirmed against a sample measurement.

*[Confirm daily volume, the source list and retention per tier per bid.]*
