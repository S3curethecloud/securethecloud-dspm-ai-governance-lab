from backend.app.scoring import score_ai_interaction, score_asset, summarize_posture


def test_broadly_shared_sensitive_asset_becomes_critical():
    asset = {
        "asset_id": "hr-payroll-001",
        "sensitivity_label": "highly_confidential",
        "sensitivity_types": ["pii", "payroll"],
        "shared_with": ["all_employees"],
        "external_sharing": False,
        "dlp_policy_present": False,
        "insider_risk_policy_present": False,
        "ai_access_allowed": True,
    }

    result = score_asset(asset)

    assert result["risk_level"] == "critical"
    assert result["decision"] in {"approval_required", "deny"}
    assert "Run access review and remove broad group access" in result["recommendations"]


def test_external_ai_destination_requires_action():
    asset = {
        "asset_id": "legal-mna-002",
        "sensitivity_label": "confidential",
        "sensitivity_types": ["legal", "financial"],
        "shared_with": ["legal_team"],
        "external_sharing": True,
        "dlp_policy_present": True,
        "insider_risk_policy_present": False,
        "ai_access_allowed": False,
    }
    event = {
        "event_id": "ai-event-002",
        "retrieved_assets": ["legal-mna-002"],
        "sensitive_data_detected": True,
        "destination": "external_partner_workspace",
    }

    result = score_ai_interaction(event, {asset["asset_id"]: asset})

    assert result["risk_level"] in {"high", "critical"}
    assert result["decision"] == "approval_required"


def test_posture_summary_returns_top_risks():
    assets = [
        {
            "asset_id": "asset-low",
            "sensitivity_label": "internal",
            "sensitivity_types": [],
            "shared_with": ["engineering_team"],
            "external_sharing": False,
            "dlp_policy_present": False,
            "insider_risk_policy_present": False,
            "ai_access_allowed": False,
        }
    ]
    events = []

    summary = summarize_posture(assets, events)

    assert summary["total_assets"] == 1
    assert summary["posture_score"] <= 100
    assert summary["top_risks"]
