from backend.app.observability import analyze_ai_observability, evaluate_session


ASSETS = [
    {
        "asset_id": "legal-mna-002",
        "name": "Confidential Acquisition Notes",
        "sensitivity_label": "confidential",
        "sensitivity_types": ["legal", "financial"],
    },
    {
        "asset_id": "eng-prompts-004",
        "name": "Internal Prompt Library",
        "sensitivity_label": "internal",
        "sensitivity_types": [],
    },
]


def test_sensitive_retrieval_to_external_destination_requires_denial():
    session = {
        "session_id": "ai-session-test-001",
        "started_at": "2026-06-29T18:20:00Z",
        "actor_id": "user-legal-counsel-001",
        "actor_department": "legal",
        "agent_id": "agent-contract-review-001",
        "agent_type": "contract_review_agent",
        "use_case": "acquisition review",
        "prompt_intent": "summarize acquisition notes",
        "prompt_risk_signals": ["legal", "financial"],
        "approval_status": "not_requested",
        "response_destination": {
            "destination_id": "external_partner_workspace",
            "destination_type": "workspace",
            "scope": "external_partner",
            "external": True,
        },
    }
    retrievals = [
        {
            "trace_id": "trace-test-001",
            "session_id": "ai-session-test-001",
            "asset_id": "legal-mna-002",
            "retrieval_action": "summarize",
            "policy_decision": "approval_required",
        }
    ]
    tool_calls = [
        {
            "tool_call_id": "tool-test-001",
            "session_id": "ai-session-test-001",
            "tool_name": "export_response",
            "tool_category": "egress",
            "action": "export",
            "target_asset_id": "legal-mna-002",
            "decision": "approval_required",
            "write_action": True,
            "external_call": True,
        }
    ]

    result = evaluate_session(session, retrievals, tool_calls, {asset["asset_id"]: asset for asset in ASSETS})

    assert result["observability_level"] == "critical"
    assert result["decision"] == "deny"
    assert "sensitive retrieval path targets external destination without approval" in result["reasons"]


def test_internal_non_sensitive_lookup_is_monitor():
    session = {
        "session_id": "ai-session-test-002",
        "started_at": "2026-06-29T18:40:00Z",
        "actor_id": "user-platform-admin-001",
        "actor_department": "platform_engineering",
        "agent_id": "agent-dev-assistant-001",
        "agent_type": "developer_assistant",
        "use_case": "prompt library lookup",
        "prompt_intent": "retrieve internal prompt examples",
        "prompt_risk_signals": [],
        "approval_status": "not_required",
        "response_destination": {
            "destination_id": "internal_engineering_chat",
            "destination_type": "chat",
            "scope": "internal",
            "external": False,
        },
    }
    retrievals = [
        {
            "trace_id": "trace-test-002",
            "session_id": "ai-session-test-002",
            "asset_id": "eng-prompts-004",
            "retrieval_action": "read",
            "policy_decision": "monitor",
        }
    ]
    tool_calls = []

    result = evaluate_session(session, retrievals, tool_calls, {asset["asset_id"]: asset for asset in ASSETS})

    assert result["observability_level"] == "low"
    assert result["decision"] == "monitor"


def test_ai_observability_summary_counts_sensitive_external_and_write_sessions():
    sessions = [
        {
            "session_id": "ai-session-test-001",
            "started_at": "2026-06-29T18:20:00Z",
            "actor_id": "user-legal-counsel-001",
            "actor_department": "legal",
            "agent_id": "agent-contract-review-001",
            "agent_type": "contract_review_agent",
            "use_case": "acquisition review",
            "prompt_intent": "summarize acquisition notes",
            "prompt_risk_signals": ["legal"],
            "approval_status": "not_requested",
            "response_destination": {
                "destination_id": "external_partner_workspace",
                "destination_type": "workspace",
                "scope": "external_partner",
                "external": True,
            },
        }
    ]
    retrievals = [
        {
            "trace_id": "trace-test-001",
            "session_id": "ai-session-test-001",
            "asset_id": "legal-mna-002",
            "retrieval_action": "summarize",
            "policy_decision": "approval_required",
        }
    ]
    tool_calls = [
        {
            "tool_call_id": "tool-test-001",
            "session_id": "ai-session-test-001",
            "tool_name": "export_response",
            "tool_category": "egress",
            "action": "export",
            "target_asset_id": "legal-mna-002",
            "decision": "approval_required",
            "write_action": True,
            "external_call": True,
        }
    ]

    observability = analyze_ai_observability(sessions, retrievals, tool_calls, ASSETS)

    assert observability["summary"]["total_sessions"] == 1
    assert observability["summary"]["sensitive_retrieval_sessions"] == 1
    assert observability["summary"]["external_destination_sessions"] == 1
    assert observability["summary"]["write_or_export_sessions"] == 1
