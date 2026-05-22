# Data Dictionary

## Source Data

| Table | Grain | Purpose |
|---|---|---|
| `data/mobile_requests.csv` | Mobile commerce request | Synthetic request intake, value, risk, readiness, and handoff attributes. |

## Generated Outputs

| Table | Grain | Purpose |
|---|---|---|
| `analysis/outputs/priority_queue.csv` | Ranked request | Explainable prioritization output used by the studio queue. |
| `analysis/outputs/intake_triage_summary.csv` | Triage lane | Counts, average score, and operating question for each intake lane. |
| `analysis/outputs/integration_risk_register.csv` | High-risk request | Vendor and data dependencies that need owner resolution before delivery. |
| `analysis/outputs/handoff_packages.csv` | Top request | PRD-style package with problem statement, acceptance criteria, edge cases, QA focus, vendor dependency, and launch gate. |

## Key Fields

| Field | Meaning |
|---|---|
| `triage_lane` | Intake routing: actionable, discovery, blocked, or monitor. |
| `business_value` | Modeled impact on commercial or operating priorities. |
| `customer_impact` | Modeled customer experience impact. |
| `urgency` | Time sensitivity for grooming and delivery. |
| `delivery_effort` | Relative implementation complexity. |
| `dependency_risk` | Vendor, platform, integration, or ownership risk. |
| `qa_complexity` | Breadth of test paths, failure states, and regression exposure. |
| `privacy_complexity` | Consent, identity, profile, or data retention complexity. |
| `confidence` | Confidence that the request is understood well enough to size. |
| `omnichannel_fit` | Relevance to app, store, profile, POS, QR, or clienteling workflows. |
| `acceptance_readiness` | Completeness of requirements and acceptance criteria. |
