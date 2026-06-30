"""Synthetic AI interaction observability for Phase 4.

The observability engine correlates AI sessions, retrieval traces, tool calls,
and synthetic asset sensitivity to produce advisory-only evidence.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

SENSITIVE_LABELS = {"confidential", "highly_confidential", "regulated"}
SENSITIVE_TYPES = {"pii", "phi", "pci", "payroll", "legal", "credential", "customer_record", "financial"}
DENY_TOOL_DECISIONS = {"deny", "blocked"}
APPROVAL_STATUSES = {"approved", "pre_approved", "approval_granted"}
SENSITIVE_AGENT_TYPES = {"service_agent", "autonomous_agent", "agentic_workflow"}


def index_assets(assets: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {asset["asset_id"]: asset for asset in assets}


def group_by(items: list[dict[str, Any]], key: str) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        grouped[item[key]].append(item)
    return dict(grouped)


def asset_is_sensitive(asset: dict[str, Any] | None) -> bool:
    if not asset:
        return False
    label = asset.get("sensitivity_label", "public")
    types = set(asset.get("sensitivity_types", []))
    return label in SENSITIVE_LABELS or bool(types & SENSITIVE_TYPES)


def asset_sensitivity(asset: dict[str, Any] | None) -> dict[str, Any]:
    if not asset:
        return {
            "sensitive": False,
            "sensitivity_label": "unknown",
            "sensitivity_types": [],
        }
    return {
        "sensitive": asset_is_sensitive(asset),
        "sensitivity_label": asset.get("sensitivity_label", "public"),
        "sensitivity_types": asset.get("sensitivity_types", []),
    }


def observability_level(score: int) -> str:
    if score >= 90:
        return "critical"
    if score >= 65:
        return "high"
    if score >= 35:
        return "medium"
    return "low"


def observability_decision(score: int) -> str:
    if score >= 90:
        return "deny"
    if score >= 65:
        return "approval_required"
    if score >= 35:
        return "redact"
    return "monitor"


def build_timeline(
    session: dict[str, Any],
    retrievals: list[dict[str, Any]],
    tool_calls: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = [
        {
            "event_type": "session_started",
            "session_id": session["session_id"],
            "actor_id": session["actor_id"],
            "agent_id": session["agent_id"],
            "started_at": session["started_at"],
        }
    ]

    for trace in retrievals:
        events.append(
            {
                "event_type": "retrieval_trace",
                "trace_id": trace["trace_id"],
                "asset_id": trace["asset_id"],
                "retrieval_action": trace["retrieval_action"],
                "policy_decision": trace.get("policy_decision", "unknown"),
            }
        )

    for call in tool_calls:
        events.append(
            {
                "event_type": "tool_call",
                "tool_call_id": call["tool_call_id"],
                "tool_name": call["tool_name"],
                "action": call["action"],
                "target_asset_id": call.get("target_asset_id"),
                "decision": call.get("decision", "unknown"),
            }
        )

    events.append(
        {
            "event_type": "response_destination",
            "destination": session["response_destination"],
        }
    )
    return events


def evaluate_session(
    session: dict[str, Any],
    retrievals: list[dict[str, Any]],
    tool_calls: list[dict[str, Any]],
    assets_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    score = 10
    reasons = ["AI interaction session observed"]
    recommendations: list[str] = []

    prompt_risk_signals = session.get("prompt_risk_signals", [])
    if prompt_risk_signals:
        score += 15
        reasons.append("prompt contains risk signals")
        recommendations.append("Review prompt intent and ensure least-data response generation")

    destination = session.get("response_destination", {})
    external_destination = bool(destination.get("external")) or destination.get("scope") not in {"internal", "private"}
    if external_destination:
        score += 25
        reasons.append("response destination is external or partner-scoped")
        recommendations.append("Require destination approval before response release")

    sensitive_retrievals = []
    retrieved_assets = []
    for trace in retrievals:
        asset = assets_by_id.get(trace["asset_id"])
        retrieved_assets.append(
            {
                "asset_id": trace["asset_id"],
                "retrieval_action": trace["retrieval_action"],
                "policy_decision": trace.get("policy_decision", "unknown"),
                **asset_sensitivity(asset),
            }
        )
        if asset_is_sensitive(asset):
            sensitive_retrievals.append(trace)

    if sensitive_retrievals:
        score += 30
        reasons.append("session retrieved sensitive or regulated assets")
        recommendations.append("Map retrieved assets to label, DLP, and AI access policy requirements")

    if len(sensitive_retrievals) > 1:
        score += 15
        reasons.append("session retrieved multiple sensitive assets")
        recommendations.append("Review multi-asset retrieval blast radius")

    write_or_export_calls = [call for call in tool_calls if call.get("write_action") or call.get("external_call")]
    if write_or_export_calls:
        score += 20
        reasons.append("session included write, export, ticketing, or external tool action")
        recommendations.append("Require tool-use approval for write or egress actions")

    denied_tool_calls = [call for call in tool_calls if call.get("decision") in DENY_TOOL_DECISIONS]
    if denied_tool_calls:
        score += 20
        reasons.append("one or more tool calls were denied by policy")
        recommendations.append("Investigate denied tool calls and preserve evidence trail")

    if sensitive_retrievals and external_destination and session.get("approval_status") not in APPROVAL_STATUSES:
        score += 25
        reasons.append("sensitive retrieval path targets external destination without approval")
        recommendations.append("Block response release until approval is granted")

    if sensitive_retrievals and session.get("agent_type") in SENSITIVE_AGENT_TYPES:
        score += 15
        reasons.append("sensitive retrieval was performed by service or agentic workflow")
        recommendations.append("Require agent identity and tool scope review")

    score = min(score, 100)

    return {
        "session_id": session["session_id"],
        "actor_id": session["actor_id"],
        "actor_department": session.get("actor_department"),
        "agent_id": session["agent_id"],
        "agent_type": session["agent_type"],
        "use_case": session["use_case"],
        "response_destination": destination,
        "approval_status": session.get("approval_status", "unknown"),
        "retrieved_assets": retrieved_assets,
        "tool_calls": tool_calls,
        "timeline": build_timeline(session, retrievals, tool_calls),
        "score": score,
        "observability_level": observability_level(score),
        "decision": observability_decision(score),
        "reasons": reasons,
        "recommendations": recommendations,
        "authority": "advisory_only",
    }


def analyze_ai_observability(
    sessions: list[dict[str, Any]],
    retrieval_traces: list[dict[str, Any]],
    tool_calls: list[dict[str, Any]],
    assets: list[dict[str, Any]],
) -> dict[str, Any]:
    assets_by_id = index_assets(assets)
    retrievals_by_session = group_by(retrieval_traces, "session_id")
    tools_by_session = group_by(tool_calls, "session_id")

    results = [
        evaluate_session(
            session,
            retrievals_by_session.get(session["session_id"], []),
            tools_by_session.get(session["session_id"], []),
            assets_by_id,
        )
        for session in sessions
    ]

    level_counts = Counter(result["observability_level"] for result in results)
    decision_counts = Counter(result["decision"] for result in results)
    sensitive_sessions = sum(
        1 for result in results if any(asset["sensitive"] for asset in result["retrieved_assets"])
    )
    external_destination_sessions = sum(
        1 for result in results if result["response_destination"].get("external")
    )
    write_or_export_sessions = sum(
        1 for result in results if any(call.get("write_action") or call.get("external_call") for call in result["tool_calls"])
    )

    return {
        "summary": {
            "total_sessions": len(results),
            "sensitive_retrieval_sessions": sensitive_sessions,
            "external_destination_sessions": external_destination_sessions,
            "write_or_export_sessions": write_or_export_sessions,
            "level_counts": dict(level_counts),
            "decision_counts": dict(decision_counts),
            "authority": "advisory_only",
        },
        "results": sorted(results, key=lambda result: result["score"], reverse=True),
    }
