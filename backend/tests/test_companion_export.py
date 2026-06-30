from backend.app.companion_export import build_companion_export, build_export_contract


EXECUTIVE_DASHBOARD = {
    "summary": {
        "total_kpis": 8,
        "kpi_severity_counts": {"critical": 5, "warning": 1, "healthy": 2},
        "top_risk_subject": {
            "subject_id": "hr-payroll-001",
            "subject_type": "asset",
            "composite_score": 100,
            "priority_level": "critical",
            "decision": "deny",
        },
    }
}

UNIFIED_RISK_SUMMARY = {
    "total_subjects": 17,
    "priority_counts": {"critical": 8, "high": 2, "medium": 6, "low": 1},
    "decision_counts": {"deny": 8, "approval_required": 2, "control_required": 5, "monitor": 2},
}

OBSERVABILITY_SUMMARY = {
    "total_sessions": 5,
    "sensitive_retrieval_sessions": 4,
    "external_destination_sessions": 1,
    "write_or_export_sessions": 2,
}

EVIDENCE_VALIDATION_SUMMARY = {
    "artifact_count": 12,
    "audit_chain_events": 12,
    "validation_status": "passed",
}


def test_export_contract_is_optional_and_advisory_only():
    contract = build_export_contract("2026-06-30T00:00:00Z")

    assert contract["authority"] == "advisory_only"
    assert contract["repo_merge_required"] is False
    assert contract["codebase_dependency_required"] is False
    assert contract["live_tenant_required"] is False


def test_companion_export_preserves_top_risk_and_evidence_health():
    export = build_companion_export(
        EXECUTIVE_DASHBOARD,
        UNIFIED_RISK_SUMMARY,
        OBSERVABILITY_SUMMARY,
        EVIDENCE_VALIDATION_SUMMARY,
        "2026-06-30T00:00:00Z",
    )

    assert export["summary"]["top_risk_subject_id"] == "hr-payroll-001"
    assert export["summary"]["top_risk_decision"] == "deny"
    assert export["summary"]["evidence_validation_status"] == "passed"
    assert export["boundary"]["no_repo_merge"] is True
    assert export["boundary"]["no_codebase_dependency"] is True


def test_companion_export_contains_ai_observability_summary():
    export = build_companion_export(
        EXECUTIVE_DASHBOARD,
        UNIFIED_RISK_SUMMARY,
        OBSERVABILITY_SUMMARY,
        EVIDENCE_VALIDATION_SUMMARY,
        "2026-06-30T00:00:00Z",
    )

    assert export["findings"]["ai_observability"]["sensitive_retrieval_sessions"] == 4
    assert export["findings"]["ai_observability"]["write_or_export_sessions"] == 2
