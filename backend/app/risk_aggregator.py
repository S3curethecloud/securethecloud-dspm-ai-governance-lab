"""Unified executive risk aggregation for Phase 5.

The aggregator correlates posture scoring, classification, access exposure,
and AI observability into one advisory-only executive risk view.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

HIGH_DECISIONS = {"deny", "approval_required"}
CONTROL_DECISIONS = {"access_review", "redact", "dlp_recommended", "label_required", "control_required"}


def risk_level(score: int) -> str:
    if score >= 90:
        return "critical"
    if score >= 65:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


def executive_decision(score: int) -> str:
    if score >= 90:
        return "deny"
    if score >= 75:
        return "approval_required"
    if score >= 50:
        return "control_required"
    return "monitor"


def classification_signal(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "signal_type": "classification",
        "source_id": result["asset_id"],
        "score": result["classification_score"],
        "level": risk_level(result["classification_score"]),
        "decision": result["decision"],
        "reasons": [
            f"inferred sensitivity label is {result['inferred_label']}",
            f"detected sensitivity types: {', '.join(result.get('detected_types', [])) or 'none'}",
        ],
        "recommendations": [
            "Review inferred sensitivity classification and map to label, DLP, or approval workflow"
        ] if result["decision"] != "monitor" else [],
    }


def posture_signal(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "signal_type": "posture",
        "source_id": result["subject_id"],
        "score": result["score"],
        "level": result["risk_level"],
        "decision": result["decision"],
        "reasons": result.get("reasons", []),
        "recommendations": result.get("recommendations", []),
    }


def access_signal(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "signal_type": "access_exposure",
        "source_id": result["permission_id"],
        "score": result["score"],
        "level": result["exposure_level"],
        "decision": result["decision"],
        "reasons": result.get("reasons", []),
        "recommendations": result.get("recommendations", []),
        "principal_id": result.get("principal", {}).get("principal_id"),
    }


def observability_signal(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "signal_type": "ai_observability",
        "source_id": result["session_id"],
        "score": result["score"],
        "level": result["observability_level"],
        "decision": result["decision"],
        "reasons": result.get("reasons", []),
        "recommendations": result.get("recommendations", []),
        "agent_id": result.get("agent_id"),
        "actor_id": result.get("actor_id"),
    }


def dedupe(items: list[str]) -> list[str]:
    seen = set()
    output = []
    for item in items:
        if item and item not in seen:
            output.append(item)
            seen.add(item)
    return output


def aggregate_subject(subject_id: str, subject_type: str, signals: list[dict[str, Any]]) -> dict[str, Any]:
    if not signals:
        composite_score = 0
    else:
        base_score = max(signal["score"] for signal in signals)
        high_signal_count = sum(1 for signal in signals if signal["score"] >= 65 or signal["decision"] in HIGH_DECISIONS)
        control_signal_count = sum(1 for signal in signals if signal["decision"] in CONTROL_DECISIONS)
        signal_diversity_bonus = max(0, len({signal["signal_type"] for signal in signals}) - 1) * 5
        high_signal_bonus = 10 if high_signal_count >= 3 else 5 if high_signal_count >= 2 else 0
        control_bonus = 5 if control_signal_count >= 2 else 0
        composite_score = min(100, base_score + signal_diversity_bonus + high_signal_bonus + control_bonus)

    recommendations = dedupe(
        recommendation
        for signal in signals
        for recommendation in signal.get("recommendations", [])
    )
    reasons = dedupe(
        reason
        for signal in signals
        for reason in signal.get("reasons", [])
    )

    return {
        "subject_id": subject_id,
        "subject_type": subject_type,
        "composite_score": composite_score,
        "priority_level": risk_level(composite_score),
        "decision": executive_decision(composite_score),
        "signal_count": len(signals),
        "signal_types": sorted({signal["signal_type"] for signal in signals}),
        "contributing_signals": sorted(signals, key=lambda signal: signal["score"], reverse=True),
        "executive_reasons": reasons,
        "recommended_controls": recommendations,
        "authority": "advisory_only",
    }


def aggregate_unified_risk(
    asset_results: list[dict[str, Any]],
    ai_event_results: list[dict[str, Any]],
    classification_results: list[dict[str, Any]],
    access_results: list[dict[str, Any]],
    ai_observability_results: list[dict[str, Any]],
) -> dict[str, Any]:
    signals_by_subject: dict[str, list[dict[str, Any]]] = defaultdict(list)
    subject_types: dict[str, str] = {}

    for result in asset_results:
        subject_id = result["subject_id"]
        subject_types[subject_id] = "asset"
        signals_by_subject[subject_id].append(posture_signal(result))

    for result in ai_event_results:
        subject_id = result["subject_id"]
        subject_types[subject_id] = "ai_event"
        signals_by_subject[subject_id].append(posture_signal(result))

    for result in classification_results:
        subject_id = result["asset_id"]
        subject_types[subject_id] = "asset"
        signals_by_subject[subject_id].append(classification_signal(result))

    for result in access_results:
        subject_id = result["asset_id"]
        subject_types[subject_id] = "asset"
        signals_by_subject[subject_id].append(access_signal(result))

    for result in ai_observability_results:
        session_id = result["session_id"]
        subject_types[session_id] = "ai_session"
        signals_by_subject[session_id].append(observability_signal(result))
        for asset in result.get("retrieved_assets", []):
            asset_id = asset.get("asset_id")
            if asset_id:
                subject_types[asset_id] = "asset"
                signals_by_subject[asset_id].append(observability_signal(result))

    results = [
        aggregate_subject(subject_id, subject_types.get(subject_id, "unknown"), signals)
        for subject_id, signals in signals_by_subject.items()
    ]
    results.sort(key=lambda result: result["composite_score"], reverse=True)

    priority_counts = Counter(result["priority_level"] for result in results)
    decision_counts = Counter(result["decision"] for result in results)
    subject_type_counts = Counter(result["subject_type"] for result in results)

    return {
        "summary": {
            "total_subjects": len(results),
            "subject_type_counts": dict(subject_type_counts),
            "priority_counts": dict(priority_counts),
            "decision_counts": dict(decision_counts),
            "top_priority_subjects": [
                {
                    "subject_id": result["subject_id"],
                    "subject_type": result["subject_type"],
                    "composite_score": result["composite_score"],
                    "priority_level": result["priority_level"],
                    "decision": result["decision"],
                }
                for result in results[:5]
            ],
            "authority": "advisory_only",
        },
        "results": results,
    }
