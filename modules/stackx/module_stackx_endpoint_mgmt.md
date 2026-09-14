# StackX Endpoint Management & Analytics

**Token:** `{{module_stackx_endpoint_mgmt}}`  
**Group:** StackX — Control / Orchestration / SOC / Operations Layer  
**Required:** No (optional module)

---

## Overview

StackX Endpoint Management is built on a data-centric, modular architecture with an open database, so {{customer_short}}'s IT teams can integrate it with their own tools. Its server components run on virtual machines or physical servers on premises. A lightweight local agent on each endpoint gives management reach regardless of the endpoint's location or connectivity.

## Data Collection and Monitoring

Data collection uses system and network tools and the endpoint agents to discover detailed information on endpoints, network nodes and topology:

- End-user analytics
- Hardware and software inventory
- Operating system and application versions, licenses and update status
- Start-up items and services
- Endpoint details: name, uptime, IP addresses, last seen, last logged-in user and domain
- Executables launched, by user
- Logged errors

Live or on-demand monitoring covers:

- Network device details through SNMP and SNMP traps
- Network traffic statistics from major network platforms
- Print jobs: user, file name, page count, size and color
- Resource performance: CPU, memory and storage activity per process
- File operations: creation, modification and deletion

## Management Actions

- Find endpoints by software, hardware or user-assigned tags
- Maintain ready-to-install software packages and pre- and post-installation configuration
- Install and uninstall software
- Manage operating system update cycles: scan, download and install
- Create, edit and delete registry keys
- Start, stop and restart services
- Initiate backups, including to cloud storage
- Run or terminate executables, commands and scripts
- Transfer files
- Shut down or restart endpoints remotely
- Activate operating system and productivity-suite licenses remotely
- Shape bandwidth per process
- Close idle applications after a configurable period
- Access an endpoint's desktop remotely, without additional tools
- Control printing by user quota, printer or color option
- Define role-based administrator privileges

<!-- Diagram guidance: managed endpoints reporting through agents to the central server, with dashboards for inventory, compliance and alerts. No endpoint or site names. -->
[[figure: endpoint-management | Endpoint management overview]]

## Analytics

The analytics engine correlates collected data to give behavior, performance and cost insight — for example, renewing licenses only for the users who actually need them:

- Proactive performance analysis
- Network traffic insight
- Endpoint change and crash tracking
- User behavior analytics

## Print Management

StackX Print Management centralizes control of the printing estate:

- Secure print release and mobile printing
- Print job tracking and reporting, with live and historical detail
- Print quotas and enforcement
- Usage analytics that identify savings
- Sustainability through enforced duplex printing and less paper and toner waste

## Integration

- Provides configuration-item context and endpoint tickets to StackX ITSM. <!-- if module_stackx_itSM -->
- Shares endpoint telemetry with the StackX security modules. <!-- if module_stackx_security or module_stackx_soc -->

---

*This module is a reusable building block. Confirm which sub-capabilities and the number of endpoints are in scope per bid.*
