# Data Sources

This project uses synthetic, role-shaped mobile commerce product operations data. It does not represent real company performance.

## Files

- `mobile_requests.csv`: 12 modeled mobile app and ecommerce requests at request grain.
- `analysis/outputs/priority_queue.csv`: Weighted queue generated from request value, customer impact, urgency, delivery effort, dependency risk, confidence, and acceptance readiness.
- `analysis/outputs/intake_triage_summary.csv`: Request counts and operating questions by intake lane.
- `analysis/outputs/integration_risk_register.csv`: Highest dependency risk items with vendor and data contract mitigation.
- `analysis/outputs/handoff_packages.csv`: PRD-style handoff packages for top-ranked requests.

## Synthesis Logic

The dataset is modeled on common retail mobile commerce operating patterns:

- Intake lanes include actionable, discovery, blocked, and monitor.
- Mobile surfaces include checkout, loyalty, personalization, account, clienteling, messaging, product detail, post purchase, and fulfillment.
- Dependency fields reflect common Tapcart, payment, order management, POS, CRM, loyalty, analytics, and marketing automation coordination points.
- Scores use bounded 0 to 100 scales for business value, customer impact, urgency, effort, dependency risk, QA complexity, privacy complexity, confidence, omnichannel fit, and acceptance readiness.
- Edge cases and QA focus areas are written to resemble a product analyst handoff, not production test evidence.
