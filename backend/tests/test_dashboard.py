from backend.app.dashboard import build_executive_dashboard, build_kpis, build_top_risk_cards


POSTURE_SUMMARY = {
    "posture_score": 21.25,
    "average_risk_score": 78.75,
    "total_assets": 5,
    "total_ai_interactions": 3,
}

CLASSIFICATION_SUMMARY = {
    "total_documents": 9,
    "decision_counts": {"approval_required": 8, "monitor": 1},
}

ACCESS_SUMMARY = {
    "ai_access_exposures": 6,
    "external_exposures": 1,
    "broad_group_exposures": 4,
}

OBSERVABILITY_SUMMARY = {
    "sensitive_retrieval_sessions": 4,
    "external_destination_sessions": 1,
    "write_or_export_sessions": 2,
}

UNIFIED_SUMMARY = {
    "total_subjects": 17,
    "priority_counts": {"critical": 8, "high": 2, "medium": 6, "low": 1},
    "decision_counts": {"deny": 8, "approval_required": 2, "control_required": 5, "monitor": 2},
}

EVIDENCE_VALIDATION_SUMMARY = {
    "artifact_count": 12,
    "audit_chain_events": 12,
    "validation_status": "passed",
}

UNIFIED_RESULTS = [
    {
        "subject_id": "hr-payroll-001",
        "subject_type": "asset",
        "composite_score": 100,
        "priority_level": "critical",
        "decision": "deny",
        "signal_count": 4,
        "signal_types": ["posture", "classification", "access_exposure", "ai_observability"],
        "executive_reasons": ["sensitive data", "AI access allowed"],
        "recommended_controls": ["Require AI access policy review before retrieval or summarization"],
    },
    {
        "subject_id": "ai-session-004",
        "subject_type": "ai_session",
        "composite_score": 10,
        "priority_level": "low",
        "decision": "monitor",
        "signal_count": 1,
        "signal_types": ["ai_observability"],
        "executive_reasons": [],
        "recommended_controls": [],
    },
]


def test_dashboard_kpis_include_evidence_validation_status():
    kpis = build_kpis(
        POSTURE_SUMMARY,
        CLASSIFICATION_SUMMARY,
        ACCESS_SUMMARY,
        OBSERVABILITY_SUMMARY,
        UNIFIED_SUMMARY,
        EVIDENCE_VALIDATION_SUMMARY,
    )

    evidence_kpi = next(kpi for kpi in kpis if kpi["kpi_id"] == "evidence_validation")
    posture_kpi = next(kpi for kpi in kpis if kpi["kpi_id"] == "posture_score")

    assert evidence_kpi["value"] == "passed"
    assert evidence_kpi["severity"] == "healthy"
    assert posture_kpi["severity"] == "critical"


def test_top_risk_cards_are_limited_and_preserve_controls():
    cards = build_top_risk_cards(UNIFIED_RESULTS, limit=1)

    assert len(cards) == 1
    assert cards[0]["subject_id"] == "hr-payroll-001"
    assert cards[0]["recommended_controls"] == ["Require AI access policy review before retrieval or summarization"]


def test_executive_dashboard_has_summary_cards_and_control_feed():
    dashboard = build_executive_dashboard(
        POSTURE_SUMMARY,
        CLASSIFICATION_SUMMARY,
        ACCESS_SUMMARY,
        OBSERVABILITY_SUMMARY,
        UNIFIED_SUMMARY,
        UNIFIED_RESULTS,
        EVIDENCE_VALIDATION_SUMMARY,
        "2026-06-30T00:00:00Z",
    )

    assert dashboard["authority"] == "advisory_only"
    assert dashboard["summary"]["total_kpis"] == 8
    assert dashboard["top_risk_cards"][0]["subject_id"] == "hr-payroll-001"
    assert dashboard["control_recommendations"][0]["subject_id"] == "hr-payroll-001"
