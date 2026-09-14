# StackX TrueView

**Token:** `{{module_stackx_trueview}}`  
**Group:** StackX — Control / Orchestration / SOC / Operations Layer  
**Required:** No (optional module)

---

## Overview

StackX TrueView is a technical and business service dashboard. It consolidates and correlates data from IT infrastructure monitoring, correlation engines and business systems into one place, so that {{customer_short}} can see how technical conditions affect business services and act on that insight — with strong attention to data privacy.

## How It Works

TrueView aggregates real-time information from diverse sources — enterprise applications, HR systems and user access logs — to give a comprehensive view of organizational activity. Through its integration with infrastructure monitoring, it also brings in availability, resource utilization and performance data, so teams can identify issues that could affect business operations before they escalate.

Its analytics correlate data across systems to find patterns, anomalies and potential privacy risks, helping {{customer_short}} refine policies and workflows and put the right controls around sensitive information.

<!-- Diagram guidance: data sources (infrastructure monitoring, applications, HR and access systems) feeding TrueView, which presents business-service and technical dashboards to different audiences. Generic labels only. -->
[[figure: trueview-dashboard | Business and technical service dashboard]]

## Key Capabilities

- **Comprehensive data aggregation** — integrates infrastructure monitoring, HR systems, access logs and enterprise applications into one dashboard.
- **Analytics and correlation** — identifies patterns and potential data privacy risks across infrastructure and business processes.
- **Visualization and reporting** — intuitive visualizations, custom dashboards and reports for each audience.
- **Data-driven decisions** — stakeholders act on insight aligned with {{customer_short}}'s strategic objectives.
- **Cross-functional collaboration** — one shared view helps departments identify and address issues together.
- **Scalable architecture** — new data sources and dashboards are added as requirements grow.

## Integration

- Receives service health and performance data from StackX Observability & APM. <!-- if module_stackx_observability_apm -->
- Uses the discovered service model from StackX Operations Monitoring & Configuration Management. <!-- if module_stackx_ops_config_mgmt -->
- Shows open incidents and service requests from StackX ITSM against each business service. <!-- if module_stackx_itSM -->

---

*This module is a reusable building block. Confirm the data sources and dashboards in scope for the current engagement.*
