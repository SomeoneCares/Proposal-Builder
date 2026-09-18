# Application Performance Monitoring <!-- if not named_product_el_apm -->
# Elastic APM <!-- if named_product_el_apm -->

**Token:** `{{product_el_apm}}`
**Group:** Elastic Products
**Required:** No

---

Application monitoring instruments the services in scope and shows transaction performance, dependencies and errors as users experience them. <!-- if not named_product_el_apm -->
Elastic APM instruments the services in scope and shows transaction performance, dependencies and errors as users experience them. <!-- if named_product_el_apm -->

## What It Delivers

- Transaction tracing across the instrumented services, with timing per step
- A dependency map built from the traces, showing what each service calls
- Error and exception tracking, grouped so a recurring fault is one entry
- Slow-transaction analysis down to the query or call responsible
- Alerting on latency, error rate and throughput against agreed targets
- Correlation with the logs of the same service <!-- if product_el_logs -->

## Build Activities <!-- if services -->

<!-- if services -->
- Deploy the platform and instrument the applications in scope with the development team
- Configure sampling, retention and service naming
- Configure alerts and the agreed dashboards per service
- Validate traces end to end for the agreed user journeys
- Hand over the instrumentation guide so new services can be added later
<!-- endif -->

## Scope Boundaries

Tracing covers the applications instrumented under this scope. Applications that cannot be instrumented, or whose runtime is unsupported, are monitored at infrastructure level only.

*[Confirm the applications, their runtimes and the user journeys to validate per bid.]*
