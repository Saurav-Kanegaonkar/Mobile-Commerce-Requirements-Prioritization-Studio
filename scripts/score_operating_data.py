import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "analysis" / "outputs"


REQUESTS = [
    {
        "request_id": "MCR-101",
        "request_name": "Loyalty wallet with QR redemption",
        "stakeholder": "CRM",
        "platform_area": "Loyalty",
        "request_type": "Enhancement",
        "business_goal": "Let app shoppers earn and redeem rewards across app and store visits.",
        "triage_lane": "Discovery",
        "business_value": 94,
        "customer_impact": 91,
        "urgency": 88,
        "delivery_effort": 34,
        "dependency_risk": 82,
        "qa_complexity": 76,
        "privacy_complexity": 69,
        "confidence": 74,
        "omnichannel_fit": 97,
        "acceptance_readiness": 61,
        "vendor_dependency": "Tapcart blocks, loyalty provider, POS customer lookup",
        "data_dependency": "Unified customer id, points balance, redemption ledger",
        "edge_cases": "Expired rewards, split tender, offline store scan, duplicate wallet pass",
        "qa_focus": "Reward balance accuracy, QR scan failure states, store associate lookup",
    },
    {
        "request_id": "MCR-102",
        "request_name": "Guest checkout payment failure recovery",
        "stakeholder": "Ecommerce",
        "platform_area": "Checkout",
        "request_type": "Issue",
        "business_goal": "Reduce abandoned checkout when payment authorization fails.",
        "triage_lane": "Actionable",
        "business_value": 91,
        "customer_impact": 86,
        "urgency": 93,
        "delivery_effort": 18,
        "dependency_risk": 38,
        "qa_complexity": 58,
        "privacy_complexity": 41,
        "confidence": 86,
        "omnichannel_fit": 53,
        "acceptance_readiness": 88,
        "vendor_dependency": "Payment gateway and checkout SDK",
        "data_dependency": "Payment error reason, cart state, retry event",
        "edge_cases": "Card decline, address mismatch, wallet timeout, duplicate order prevention",
        "qa_focus": "Retry path, saved cart persistence, analytics event continuity",
    },
    {
        "request_id": "MCR-103",
        "request_name": "Personalized occasion shop modules",
        "stakeholder": "Merchandising",
        "platform_area": "Personalization",
        "request_type": "New capability",
        "business_goal": "Tailor mobile collections by upcoming occasion, size preference, and browsing behavior.",
        "triage_lane": "Discovery",
        "business_value": 89,
        "customer_impact": 84,
        "urgency": 70,
        "delivery_effort": 30,
        "dependency_risk": 66,
        "qa_complexity": 63,
        "privacy_complexity": 72,
        "confidence": 67,
        "omnichannel_fit": 74,
        "acceptance_readiness": 58,
        "vendor_dependency": "Tapcart conditional content and recommendation feed",
        "data_dependency": "Customer segments, product tags, browsing consent, inventory feed",
        "edge_cases": "Cold start, no size history, out of stock recommendations, consent opt out",
        "qa_focus": "Segment rules, fallback modules, inventory suppression",
    },
    {
        "request_id": "MCR-104",
        "request_name": "Wishlist contest enrollment",
        "stakeholder": "Marketing",
        "platform_area": "Wishlist",
        "request_type": "Enhancement",
        "business_goal": "Convert wishlist creation into a measurable weekly engagement loop.",
        "triage_lane": "Actionable",
        "business_value": 76,
        "customer_impact": 78,
        "urgency": 72,
        "delivery_effort": 16,
        "dependency_risk": 34,
        "qa_complexity": 42,
        "privacy_complexity": 47,
        "confidence": 82,
        "omnichannel_fit": 49,
        "acceptance_readiness": 91,
        "vendor_dependency": "Tapcart wishlist event and marketing automation",
        "data_dependency": "Wishlist id, weekly eligibility flag, notification opt in",
        "edge_cases": "Duplicate entries, deleted wishlist, underage account, opt out status",
        "qa_focus": "Eligibility logic, event dedupe, notification trigger",
    },
    {
        "request_id": "MCR-105",
        "request_name": "Store associate clienteling notes",
        "stakeholder": "Stores",
        "platform_area": "Clienteling",
        "request_type": "New capability",
        "business_goal": "Give associates useful app and order context for high-intent store visits.",
        "triage_lane": "Discovery",
        "business_value": 83,
        "customer_impact": 82,
        "urgency": 61,
        "delivery_effort": 38,
        "dependency_risk": 88,
        "qa_complexity": 81,
        "privacy_complexity": 86,
        "confidence": 54,
        "omnichannel_fit": 95,
        "acceptance_readiness": 44,
        "vendor_dependency": "Clienteling partner, POS profile, Tapcart account surface",
        "data_dependency": "Customer profile, consent flag, recent orders, store visit context",
        "edge_cases": "Shared devices, associate role access, customer deletion request, stale notes",
        "qa_focus": "Permissioning, profile match accuracy, data retention rules",
    },
    {
        "request_id": "MCR-106",
        "request_name": "Push campaign quiet hours",
        "stakeholder": "Marketing",
        "platform_area": "Messaging",
        "request_type": "Enhancement",
        "business_goal": "Protect app retention by enforcing send windows and frequency limits.",
        "triage_lane": "Actionable",
        "business_value": 74,
        "customer_impact": 80,
        "urgency": 68,
        "delivery_effort": 12,
        "dependency_risk": 24,
        "qa_complexity": 33,
        "privacy_complexity": 31,
        "confidence": 90,
        "omnichannel_fit": 42,
        "acceptance_readiness": 95,
        "vendor_dependency": "Push messaging provider",
        "data_dependency": "Time zone, opt in status, campaign send log",
        "edge_cases": "Traveling users, daylight saving time, campaign override, transactional push",
        "qa_focus": "Suppression logic, local time conversion, override audit",
    },
    {
        "request_id": "MCR-107",
        "request_name": "Order tracking account refresh",
        "stakeholder": "Customer Care",
        "platform_area": "Account",
        "request_type": "Issue",
        "business_goal": "Reduce support contacts by making app order status easier to trust.",
        "triage_lane": "Actionable",
        "business_value": 82,
        "customer_impact": 88,
        "urgency": 84,
        "delivery_effort": 22,
        "dependency_risk": 46,
        "qa_complexity": 54,
        "privacy_complexity": 43,
        "confidence": 81,
        "omnichannel_fit": 64,
        "acceptance_readiness": 83,
        "vendor_dependency": "Order management API and Tapcart account surface",
        "data_dependency": "Order id, fulfillment status, shipment tracking, return status",
        "edge_cases": "Split shipments, canceled line item, guest order claim, delayed carrier update",
        "qa_focus": "Status mapping, empty states, support deflection events",
    },
    {
        "request_id": "MCR-108",
        "request_name": "In-store app install QR attribution",
        "stakeholder": "Stores",
        "platform_area": "Omnichannel",
        "request_type": "Measurement",
        "business_goal": "Attribute app installs and first purchases to store QR placements.",
        "triage_lane": "Blocked",
        "business_value": 77,
        "customer_impact": 58,
        "urgency": 66,
        "delivery_effort": 24,
        "dependency_risk": 79,
        "qa_complexity": 61,
        "privacy_complexity": 64,
        "confidence": 48,
        "omnichannel_fit": 93,
        "acceptance_readiness": 39,
        "vendor_dependency": "QR provider, analytics SDK, app store attribution",
        "data_dependency": "Store id, QR campaign id, install event, first purchase event",
        "edge_cases": "App already installed, delayed install, shared QR, privacy restricted attribution",
        "qa_focus": "Campaign mapping, duplicate install handling, reporting latency",
    },
    {
        "request_id": "MCR-109",
        "request_name": "Product detail size confidence prompt",
        "stakeholder": "Merchandising",
        "platform_area": "Product Detail",
        "request_type": "Enhancement",
        "business_goal": "Reduce fit hesitation on occasionwear product detail pages.",
        "triage_lane": "Actionable",
        "business_value": 79,
        "customer_impact": 83,
        "urgency": 73,
        "delivery_effort": 20,
        "dependency_risk": 36,
        "qa_complexity": 45,
        "privacy_complexity": 38,
        "confidence": 78,
        "omnichannel_fit": 57,
        "acceptance_readiness": 84,
        "vendor_dependency": "Size guide content feed and Tapcart product block",
        "data_dependency": "Product category, size chart, return reason labels",
        "edge_cases": "One size items, missing chart, international size labels, final sale messaging",
        "qa_focus": "Category mapping, fallback content, accessibility labels",
    },
    {
        "request_id": "MCR-110",
        "request_name": "Returns eligibility self-service",
        "stakeholder": "Customer Care",
        "platform_area": "Post Purchase",
        "request_type": "New capability",
        "business_goal": "Let customers confirm return eligibility before contacting support.",
        "triage_lane": "Discovery",
        "business_value": 81,
        "customer_impact": 85,
        "urgency": 63,
        "delivery_effort": 29,
        "dependency_risk": 71,
        "qa_complexity": 72,
        "privacy_complexity": 51,
        "confidence": 62,
        "omnichannel_fit": 67,
        "acceptance_readiness": 53,
        "vendor_dependency": "Returns platform and order management API",
        "data_dependency": "Order line, return window, final sale flag, store purchase flag",
        "edge_cases": "Gift returns, store purchase lookup, partial return, final sale override",
        "qa_focus": "Eligibility rules, message clarity, support handoff",
    },
    {
        "request_id": "MCR-111",
        "request_name": "App inbox launch calendar",
        "stakeholder": "Brand Marketing",
        "platform_area": "Messaging",
        "request_type": "Enhancement",
        "business_goal": "Coordinate collection launch stories without overloading push notifications.",
        "triage_lane": "Monitor",
        "business_value": 68,
        "customer_impact": 66,
        "urgency": 55,
        "delivery_effort": 18,
        "dependency_risk": 41,
        "qa_complexity": 37,
        "privacy_complexity": 33,
        "confidence": 72,
        "omnichannel_fit": 39,
        "acceptance_readiness": 76,
        "vendor_dependency": "Tapcart inbox or marketing suite",
        "data_dependency": "Launch date, segment, message priority, expiration date",
        "edge_cases": "Expired content, overlapping launches, customer segment exclusion",
        "qa_focus": "Message priority, expiration behavior, deep link routing",
    },
    {
        "request_id": "MCR-112",
        "request_name": "Store pickup promise visibility",
        "stakeholder": "Operations",
        "platform_area": "Fulfillment",
        "request_type": "Enhancement",
        "business_goal": "Show customers realistic store pickup timing before checkout.",
        "triage_lane": "Blocked",
        "business_value": 87,
        "customer_impact": 89,
        "urgency": 76,
        "delivery_effort": 35,
        "dependency_risk": 90,
        "qa_complexity": 78,
        "privacy_complexity": 39,
        "confidence": 46,
        "omnichannel_fit": 96,
        "acceptance_readiness": 36,
        "vendor_dependency": "Inventory availability service, POS, Tapcart checkout configuration",
        "data_dependency": "Store inventory, pickup capacity, cutoff time, reservation state",
        "edge_cases": "Inventory mismatch, store closed, cart with mixed fulfillment, reservation expiry",
        "qa_focus": "Availability latency, cutoff logic, checkout handoff",
    },
]


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def score_request(row):
    upside = (
        row["business_value"] * 0.26
        + row["customer_impact"] * 0.21
        + row["urgency"] * 0.16
        + row["omnichannel_fit"] * 0.11
        + row["confidence"] * 0.12
    )
    drag = (
        row["delivery_effort"] * 0.17
        + row["dependency_risk"] * 0.12
        + row["qa_complexity"] * 0.07
        + row["privacy_complexity"] * 0.04
    )
    return max(0, min(100, round(upside - drag + 17, 1)))


def next_step(row, score):
    if row["triage_lane"] == "Blocked":
        return "Resolve integration owner and data contract before sprint grooming"
    if row["triage_lane"] == "Discovery":
        return "Draft strawman PRD and validate assumptions with stakeholder"
    if score >= 82:
        return "Move to sprint-ready handoff with QA and vendor review"
    if row["triage_lane"] == "Monitor":
        return "Keep in operating review and watch signal movement"
    return "Groom with delivery lead and confirm release slice"


def launch_gate(row):
    if row["triage_lane"] == "Blocked":
        return "Blocked until dependency contract is signed off"
    if row["acceptance_readiness"] < 65:
        return "Needs PRD clarification before estimation"
    if row["dependency_risk"] > 70:
        return "Needs vendor checkpoint before sprint start"
    return "Ready for delivery and QA sizing"


def build_outputs():
    request_fields = list(REQUESTS[0].keys())
    write_csv(DATA_DIR / "mobile_requests.csv", REQUESTS, request_fields)

    priority_rows = []
    for row in REQUESTS:
        score = score_request(row)
        priority_rows.append(
            {
                "request_id": row["request_id"],
                "request_name": row["request_name"],
                "platform_area": row["platform_area"],
                "stakeholder": row["stakeholder"],
                "triage_lane": row["triage_lane"],
                "priority_score": score,
                "business_value": row["business_value"],
                "customer_impact": row["customer_impact"],
                "urgency": row["urgency"],
                "delivery_effort": row["delivery_effort"],
                "dependency_risk": row["dependency_risk"],
                "confidence": row["confidence"],
                "acceptance_readiness": row["acceptance_readiness"],
                "recommended_next_step": next_step(row, score),
            }
        )

    priority_rows.sort(key=lambda item: item["priority_score"], reverse=True)
    for index, row in enumerate(priority_rows, start=1):
        row["rank"] = index

    priority_fields = [
        "rank",
        "request_id",
        "request_name",
        "platform_area",
        "stakeholder",
        "triage_lane",
        "priority_score",
        "business_value",
        "customer_impact",
        "urgency",
        "delivery_effort",
        "dependency_risk",
        "confidence",
        "acceptance_readiness",
        "recommended_next_step",
    ]
    write_csv(OUTPUT_DIR / "priority_queue.csv", priority_rows, priority_fields)

    handoff_rows = []
    request_lookup = {row["request_id"]: row for row in REQUESTS}
    for ranked in priority_rows[:8]:
        source = request_lookup[ranked["request_id"]]
        handoff_rows.append(
            {
                "request_id": source["request_id"],
                "request_name": source["request_name"],
                "problem_statement": source["business_goal"],
                "acceptance_criteria": (
                    f"Business outcome is measurable; {source['data_dependency']}; "
                    f"customer-facing states cover success, empty, and failure paths"
                ),
                "edge_cases": source["edge_cases"],
                "qa_focus": source["qa_focus"],
                "vendor_dependency": source["vendor_dependency"],
                "launch_gate": launch_gate(source),
            }
        )

    handoff_fields = [
        "request_id",
        "request_name",
        "problem_statement",
        "acceptance_criteria",
        "edge_cases",
        "qa_focus",
        "vendor_dependency",
        "launch_gate",
    ]
    write_csv(OUTPUT_DIR / "handoff_packages.csv", handoff_rows, handoff_fields)

    lane_counts = Counter(row["triage_lane"] for row in REQUESTS)
    lane_rows = []
    for lane in ["Actionable", "Discovery", "Blocked", "Monitor"]:
        lane_set = [row for row in REQUESTS if row["triage_lane"] == lane]
        avg_score = sum(score_request(row) for row in lane_set) / len(lane_set)
        lane_rows.append(
            {
                "triage_lane": lane,
                "request_count": lane_counts[lane],
                "avg_priority_score": round(avg_score, 1),
                "primary_operating_question": {
                    "Actionable": "Can this be groomed into a delivery-ready slice now?",
                    "Discovery": "Which assumptions must be validated before estimation?",
                    "Blocked": "Which dependency owner must unblock the path?",
                    "Monitor": "What signal would make this worth promoting?",
                }[lane],
            }
        )
    write_csv(
        OUTPUT_DIR / "intake_triage_summary.csv",
        lane_rows,
        ["triage_lane", "request_count", "avg_priority_score", "primary_operating_question"],
    )

    risk_rows = []
    for row in sorted(REQUESTS, key=lambda item: item["dependency_risk"], reverse=True)[:7]:
        risk_rows.append(
            {
                "request_id": row["request_id"],
                "request_name": row["request_name"],
                "dependency_risk": row["dependency_risk"],
                "vendor_dependency": row["vendor_dependency"],
                "data_dependency": row["data_dependency"],
                "mitigation": next_step(row, score_request(row)),
            }
        )
    write_csv(
        OUTPUT_DIR / "integration_risk_register.csv",
        risk_rows,
        ["request_id", "request_name", "dependency_risk", "vendor_dependency", "data_dependency", "mitigation"],
    )

    return priority_rows, lane_rows, handoff_rows


if __name__ == "__main__":
    priority, lanes, handoffs = build_outputs()
    print("Top 5 mobile commerce requirements")
    for row in priority[:5]:
        print(
            f"{row['rank']}. {row['request_id']} {row['request_name']} "
            f"score={row['priority_score']} lane={row['triage_lane']}"
        )
    print()
    print("Triage lanes")
    for row in lanes:
        print(f"{row['triage_lane']}: {row['request_count']} requests, avg score {row['avg_priority_score']}")
    print()
    print(f"Generated {len(handoffs)} handoff packages")
