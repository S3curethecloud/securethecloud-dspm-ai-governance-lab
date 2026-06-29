"""Risk scoring logic for the synthetic DSPM AI governance lab.

The scoring model is intentionally transparent and deterministic so it can be
reviewed during interviews, audits, and architecture walkthroughs.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

SENSITIVITY_WEIGHTS = {
    "public": 0,
    "internal": 15,
    "confidential": 35,
    "highly_confidential": 50,
    "regulated": 60,
}

TYPE_WEIGHTS = {
    "pii": 15,
    "phi": 25,
    "pci": 25,
    "payroll": 20,
    "legal": 20,
    "credential": 30,
    "customer_record": 20,
    "financial": 20,
}

BROAD_ACCESS_GROUPS = {"all_employees", "everyone", "company_all", "domain_users"}


def risk_level(score: int) -> str:
    if score >= 90:
        return "critical"
    if score >= 65:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


def decision_for(score: int, *, external_sharing: bool = False, ai_access: bool = False) -> str:
    if score >= 95 or (external_sharing and score >= 80):
        return "deny"
    if score >= 70 or ai_access:
        return "approval_required"
    if score >= 40:
        return "redact"
    return "allow"


def score_asset(asset: dict[str, Any]) -> dict[str, Any]:
    score = 0
    reasons: list[str] = []
    recommendations: list[str] = []

    label = str(asset.get("sensitivity_label", "internal")).lower()
    score += SENSITIVITY_WEIGHTS.get(label, 15)
    if label in {"confidential", "highly_confidential", "regulated"}:
        reasons.append(f"sensitivity label is {label}")

    sensitivity_types = [str(item).lower() for item in asset.get("sensitivity_types", [])]
    for sensitivity_type in sensitivity_types:
        score += TYPE_WEIGHTS.get(sensitivity_type, 5)
    if sensitivity_types:
        reasons.append("sensitive data types detected: " + ", ".join(sorted(set(sensitivity_types))))

    shared_with = {str(item).lower() for item in asset.get("shared_with", [])}
    if shared_with & BROAD_ACCESS_GROUPS:
        score += 25
        reasons.append("asset is broadly shared")
        recommendations.append("Run access review and remove broad group access")

    if asset.get("external_sharing"):
        score += 30
        reasons.append("external sharing is enabled")
        recommendations.append("Block external sharing for sensitive assets or require approval")

    if asset.get("ai_access_allowed"):
        score += 20
        reasons.append("AI access is allowed for this asset")
        recommendations.append("Require AI access policy review before retrieval or summarization")

    if not asset.get("dlp_policy_present") and score >= 40:
        score += 15
        reasons.append("DLP policy coverage is missing")
        recommendations.append("Create or update DLP policy for detected sensitivity types")

    if not asset.get("insider_risk_policy_present") and score >= 65:
        score += 10
        reasons.append("Insider Risk policy coverage is missing")
        recommendations.append("Map asset to Insider Risk review workflow")

    score = min(score, 100)

    return {
        "subject_id": asset.get("asset_id", "unknown_asset"),
        "score": score,
        "risk_level": risk_level(score),
        "decision": decision_for(
            score,
            external_sharing=bool(asset.get("external_sharing")),
            ai_access=bool(asset.get("ai_access_allowed")),
        ),
        "reasons": reasons or ["no material posture risk detected"],
        "recommendations": recommendations or ["Continue monitoring posture and access scope"],
    }


def score_ai_interaction(event: dict[str, Any], asset_index: dict[str, dict[str, Any]]) -> dict[str, Any]:
    base_score = 10
    reasons: list[str] = ["AI interaction observed"]
    recommendations: list[str] = []

    if event.get("sensitive_data_detected"):
        base_score += 25
        reasons.append("prompt or response path includes sensitive data")
        recommendations.append("Inspect prompt, retrieved content, and response handling")

    if str(event.get("destination", "internal")).lower() != "internal":
        base_score += 30
        reasons.append("AI interaction targets a non-internal destination")
        recommendations.append("Apply DLP control for risky destination")

    retrieved_assets = event.get("retrieved_assets", [])
    linked_asset_results = []
    for asset_id in retrieved_assets:
        asset = asset_index.get(asset_id)
        if not asset:
            continue
        asset_result = score_asset(asset)
        linked_asset_results.append(asset_result)
        if asset_result["risk_level"] in {"high", "critical"}:
            base_score += 20
            reasons.append(f"retrieved high-risk asset {asset_id}")

    score = min(base_score, 100)
    return {
        "subject_id": event.get("event_id", "unknown_event"),
        "score": score,
        "risk_level": risk_level(score),
        "decision": decision_for(score, ai_access=bool(retrieved_assets)),
        "reasons": reasons,
        "recommendations": recommendations or ["Retain AI interaction evidence and continue monitoring"],
        "linked_asset_results": linked_asset_results,
    }


def summarize_posture(assets: list[dict[str, Any]], events: list[dict[str, Any]]) -> dict[str, Any]:
    asset_index = {asset["asset_id"]: asset for asset in assets}
    asset_results = [score_asset(asset) for asset in assets]
    event_results = [score_ai_interaction(event, asset_index) for event in events]

    all_results = asset_results + event_results
    risk_counts = Counter(result["risk_level"] for result in all_results)
    avg_score = round(sum(result["score"] for result in all_results) / max(len(all_results), 1), 2)

    posture_score = max(0, 100 - avg_score)

    return {
        "posture_score": posture_score,
        "average_risk_score": avg_score,
        "total_assets": len(assets),
        "total_ai_interactions": len(events),
        "risk_counts": dict(risk_counts),
        "top_risks": sorted(all_results, key=lambda result: result["score"], reverse=True)[:5],
    }
