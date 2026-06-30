"""Executive posture dashboard model for Phase 7.

The dashboard module converts synthetic evidence summaries and unified risk
results into executive-facing KPIs, top-risk cards, evidence health, and
control recommendation feeds.
"""

from __future__ import annotations

from collections import Counter
from typing import Any


def severity_from_value(value: int | float, warning: int | float, critical: int | float) -> str:
    if value >= critical:
        return "critical"
    if value >= warning:
        return "warning"
    return "healthy"


def posture_severity(posture_score: int | float) -> str:
    if posture_score < 40:
        return "critical"
    if posture_score < 70:
        return "warning"
    return "healthy"


def build_kpis(
    posture_summary: dict[str, Any],
    classification_summary: dict[str, Any],
    access_summary: dict[str, Any],
    observability_summary: dict[str, Any],
    unified_summary: dict[str, Any],
    evidence_validation_summary: dict[str, Any],
) -> list[dict[str, Any]]:
    priority_counts = unified_summary.get("priority_counts", {})
    decision_counts = unified_summary.get("decision_counts", {})

    return [
        {
            "kpi_id": "posture_score",
            "label": "DSPM posture score",
            "value": posture_summary.get("posture_score"),
            "severity": posture_severity(posture_summary.get("posture_score", 0)),
            "description": "Overall synthetic DSPM posture score. Lower scores indicate higher governance concern.",
        },
        {
            "kpi_id": "critical_subjects",
            "label": "Critical risk subjects",
            "value": priority_counts.get("critical", 0),
            "severity": severity_from_value(priority_counts.get("critical", 0), warning=1, critical=3),
            "description": "Assets, AI sessions, or AI events prioritized as critical by the unified risk model.",
        },
        {
            "kpi_id": "deny_decisions",
            "label": "Deny decisions",
            "value": decision_counts.get("deny", 0),
            "severity": severity_from_value(decision_counts.get("deny", 0), warning=1, critical=3),
            "description": "Unified executive decisions requiring block or no-go handling in a real control workflow.",
        },
        {
            "kpi_id": "approval_required",
            "label": "Approval-required decisions",
            "value": decision_counts.get("approval_required", 0),
            "severity": severity_from_value(decision_counts.get("approval_required", 0), warning=1, critical=5),
            "description": "Risk subjects requiring human review before release, retrieval, or action.",
        },
        {
            "kpi_id": "sensitive_retrieval_sessions",
            "label": "Sensitive AI retrieval sessions",
            "value": observability_summary.get("sensitive_retrieval_sessions", 0),
            "severity": severity_from_value(observability_summary.get("sensitive_retrieval_sessions", 0), warning=1, critical=3),
            "description": "Observed AI sessions that retrieved sensitive or regulated synthetic assets.",
        },
        {
            "kpi_id": "ai_access_exposures",
            "label": "AI access exposures",
            "value": access_summary.get("ai_access_exposures", 0),
            "severity": severity_from_value(access_summary.get("ai_access_exposures", 0), warning=1, critical=4),
            "description": "Permission paths where AI access is allowed to synthetic assets.",
        },
        {
            "kpi_id": "classified_documents",
            "label": "Classified documents",
            "value": classification_summary.get("total_documents", 0),
            "severity": "healthy",
            "description": "Synthetic documents classified by the deterministic sensitivity classifier.",
        },
        {
            "kpi_id": "evidence_validation",
            "label": "Evidence validation status",
            "value": evidence_validation_summary.get("validation_status", "unknown"),
            "severity": "healthy" if evidence_validation_summary.get("validation_status") == "passed" else "critical",
            "description": "Evidence package validation status from the audit-chain package summary.",
        },
    ]


def build_top_risk_cards(unified_risk_results: list[dict[str, Any]], limit: int = 5) -> list[dict[str, Any]]:
    cards = []
    for result in unified_risk_results[:limit]:
        cards.append(
            {
                "subject_id": result["subject_id"],
                "subject_type": result["subject_type"],
                "composite_score": result["composite_score"],
                "priority_level": result["priority_level"],
                "decision": result["decision"],
                "signal_count": result.get("signal_count", 0),
                "signal_types": result.get("signal_types", []),
                "executive_reasons": result.get("executive_reasons", [])[:5],
                "recommended_controls": result.get("recommended_controls", [])[:5],
            }
        )
    return cards


def build_control_recommendation_feed(unified_risk_results: list[dict[str, Any]], limit: int = 10) -> list[dict[str, Any]]:
    feed = []
    seen = set()
    for result in unified_risk_results:
        for control in result.get("recommended_controls", []):
            key = (result["subject_id"], control)
            if key in seen:
                continue
            seen.add(key)
            feed.append(
                {
                    "subject_id": result["subject_id"],
                    "subject_type": result["subject_type"],
                    "priority_level": result["priority_level"],
                    "decision": result["decision"],
                    "recommended_control": control,
                }
            )
            if len(feed) >= limit:
                return feed
    return feed


def build_dashboard_summary(kpis: list[dict[str, Any]], top_risk_cards: list[dict[str, Any]]) -> dict[str, Any]:
    severity_counts = Counter(kpi["severity"] for kpi in kpis)
    top_card = top_risk_cards[0] if top_risk_cards else None
    return {
        "total_kpis": len(kpis),
        "kpi_severity_counts": dict(severity_counts),
        "top_risk_subject": top_card,
        "authority": "advisory_only",
    }


def build_executive_dashboard(
    posture_summary: dict[str, Any],
    classification_summary: dict[str, Any],
    access_summary: dict[str, Any],
    observability_summary: dict[str, Any],
    unified_summary: dict[str, Any],
    unified_risk_results: list[dict[str, Any]],
    evidence_validation_summary: dict[str, Any],
    generated_at: str,
) -> dict[str, Any]:
    kpis = build_kpis(
        posture_summary,
        classification_summary,
        access_summary,
        observability_summary,
        unified_summary,
        evidence_validation_summary,
    )
    top_risk_cards = build_top_risk_cards(unified_risk_results)
    control_recommendations = build_control_recommendation_feed(unified_risk_results)

    return {
        "dashboard_title": "SecureTheCloud DSPM AI Governance Executive Dashboard",
        "generated_at": generated_at,
        "authority": "advisory_only",
        "summary": build_dashboard_summary(kpis, top_risk_cards),
        "kpis": kpis,
        "top_risk_cards": top_risk_cards,
        "control_recommendations": control_recommendations,
        "decision_breakdown": unified_summary.get("decision_counts", {}),
        "priority_breakdown": unified_summary.get("priority_counts", {}),
        "evidence_health": evidence_validation_summary,
    }
