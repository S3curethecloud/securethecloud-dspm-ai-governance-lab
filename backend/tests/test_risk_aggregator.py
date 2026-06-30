from backend.app.risk_aggregator import aggregate_subject, aggregate_unified_risk


def test_aggregate_subject_escalates_multiple_high_signals_to_critical():
    signals = [
        {
            "signal_type": "posture",
            "source_id": "asset-001",
            "score": 85,
            "level": "high",
            "decision": "approval_required",
            "reasons": ["high posture risk"],
            "recommendations": ["review posture"],
        },
        {
            "signal_type": "access_exposure",
            "source_id": "perm-001",
            "score": 80,
            "level": "high",
            "decision": "approval_required",
            "reasons": ["broad access"],
            "recommendations": ["remove broad access"],
        },
        {
            "signal_type": "ai_observability",
            "source_id": "session-001",
            "score": 75,
            "level": "high",
            "decision": "approval_required",
            "reasons": ["sensitive retrieval"],
            "recommendations": ["require AI approval"],
        },
    ]

    result = aggregate_subject("asset-001", "asset", signals)

    assert result["priority_level"] == "critical"
    assert result["decision"] == "deny"
    assert result["composite_score"] == 100
    assert result["signal_count"] == 3


def test_unified_risk_links_ai_observability_back_to_asset():
    aggregate = aggregate_unified_risk(
        asset_results=[
            {
                "subject_id": "asset-001",
                "score": 100,
                "risk_level": "critical",
                "decision": "deny",
                "reasons": ["asset is risky"],
                "recommendations": ["fix asset"],
            }
        ],
        ai_event_results=[],
        classification_results=[],
        access_results=[],
        ai_observability_results=[
            {
                "session_id": "session-001",
                "score": 90,
                "observability_level": "critical",
                "decision": "deny",
                "reasons": ["sensitive retrieval"],
                "recommendations": ["block response"],
                "retrieved_assets": [{"asset_id": "asset-001", "sensitive": True}],
            }
        ],
    )

    asset_result = next(result for result in aggregate["results"] if result["subject_id"] == "asset-001")
    session_result = next(result for result in aggregate["results"] if result["subject_id"] == "session-001")

    assert asset_result["decision"] == "deny"
    assert "ai_observability" in asset_result["signal_types"]
    assert session_result["subject_type"] == "ai_session"


def test_low_single_signal_remains_monitor():
    result = aggregate_subject(
        "asset-low",
        "asset",
        [
            {
                "signal_type": "classification",
                "source_id": "asset-low",
                "score": 10,
                "level": "low",
                "decision": "monitor",
                "reasons": [],
                "recommendations": [],
            }
        ],
    )

    assert result["priority_level"] == "low"
    assert result["decision"] == "monitor"
