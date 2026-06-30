"""Repository contract validation for the DSPM AI Governance Lab."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "README.md",
    "AGENTS.md",
    "GOVERNANCE.md",
    "backend/__init__.py",
    "backend/app/__init__.py",
    "backend/app/main.py",
    "backend/app/models.py",
    "backend/app/scoring.py",
    "backend/app/classifier.py",
    "backend/app/access_analyzer.py",
    "backend/app/observability.py",
    "backend/app/risk_aggregator.py",
    "backend/app/evidence_package.py",
    "backend/app/dashboard.py",
    "backend/app/companion_export.py",
    "backend/tests/test_scoring.py",
    "backend/tests/test_classifier.py",
    "backend/tests/test_access_analyzer.py",
    "backend/tests/test_observability.py",
    "backend/tests/test_risk_aggregator.py",
    "backend/tests/test_evidence_package.py",
    "backend/tests/test_dashboard.py",
    "backend/tests/test_companion_export.py",
    "frontend/README.md",
    "frontend/index.html",
    "frontend/styles.css",
    "frontend/app.js",
    "data/assets/sample_assets.json",
    "data/assets/phase2_additional_assets.json",
    "data/content_samples/synthetic_documents.json",
    "data/classification_patterns/sensitivity_patterns.json",
    "data/access/identities.json",
    "data/access/groups.json",
    "data/access/permissions.json",
    "data/observability/ai_sessions.json",
    "data/observability/retrieval_traces.json",
    "data/observability/tool_calls.json",
    "data/events/ai_interactions.json",
    "policies/dspm_policy_rules.yaml",
    "docs/sot/PROJECT_SOURCE_OF_TRUTH.md",
    "docs/architecture/DSPM_AI_GOVERNANCE_ARCHITECTURE.md",
]

REQUIRED_BOUNDARY_PHRASES = [
    "synthetic",
    "advisory",
    "no live",
    "no production enforcement",
]

BLOCKED_AFFIRMATIVE_CLAIMS = [
    "production enforcement enabled",
    "live tenant mutation enabled",
    "autonomous approval enabled",
    "real tenant write access enabled",
]


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def read_json(relative_path: str):
    return json.loads(read_text(relative_path))


def validate_required_paths() -> list[str]:
    errors = []
    for relative_path in REQUIRED_PATHS:
        if not (ROOT / relative_path).exists():
            errors.append(f"missing required path: {relative_path}")
    return errors


def validate_json(relative_path: str) -> list[str]:
    try:
        read_json(relative_path)
    except Exception as exc:  # pragma: no cover - diagnostic path
        return [f"invalid json in {relative_path}: {exc}"]
    return []


def validate_classifier_fixture_contract() -> list[str]:
    errors = []
    patterns = read_json("data/classification_patterns/sensitivity_patterns.json")
    documents = read_json("data/content_samples/synthetic_documents.json")

    required_pattern_keys = {
        "pattern_id",
        "name",
        "sensitivity_type",
        "inferred_label",
        "regex",
        "risk_points",
        "confidence",
    }
    for pattern in patterns:
        missing = required_pattern_keys - set(pattern)
        if missing:
            errors.append(f"classification pattern {pattern.get('pattern_id', '<unknown>')} missing keys: {sorted(missing)}")

    for document in documents:
        if not document.get("asset_id") or not document.get("content"):
            errors.append("classification document fixture requires asset_id and content")

    return errors


def validate_access_fixture_contract() -> list[str]:
    errors = []
    identities = read_json("data/access/identities.json")
    groups = read_json("data/access/groups.json")
    permissions = read_json("data/access/permissions.json")
    assets = read_json("data/assets/sample_assets.json") + read_json("data/assets/phase2_additional_assets.json")

    identity_ids = {identity.get("identity_id") for identity in identities}
    group_ids = {group.get("group_id") for group in groups}
    asset_ids = {asset.get("asset_id") for asset in assets}

    for group in groups:
        for member in group.get("members", []):
            if member not in identity_ids:
                errors.append(f"group {group.get('group_id')} references unknown identity member: {member}")

    required_permission_keys = {
        "permission_id",
        "asset_id",
        "principal_id",
        "principal_type",
        "access_level",
        "roles",
        "inherited",
        "external",
        "ai_tool_access_allowed",
        "source",
    }
    for permission in permissions:
        missing = required_permission_keys - set(permission)
        if missing:
            errors.append(f"permission {permission.get('permission_id', '<unknown>')} missing keys: {sorted(missing)}")
        if permission.get("asset_id") not in asset_ids:
            errors.append(f"permission {permission.get('permission_id')} references unknown asset: {permission.get('asset_id')}")
        principal_id = permission.get("principal_id")
        principal_type = permission.get("principal_type")
        if principal_type == "group" and principal_id not in group_ids:
            errors.append(f"permission {permission.get('permission_id')} references unknown group: {principal_id}")
        if principal_type in {"user", "guest", "service_principal"} and principal_id not in identity_ids:
            errors.append(f"permission {permission.get('permission_id')} references unknown identity: {principal_id}")

    return errors


def validate_observability_fixture_contract() -> list[str]:
    errors = []
    sessions = read_json("data/observability/ai_sessions.json")
    retrieval_traces = read_json("data/observability/retrieval_traces.json")
    tool_calls = read_json("data/observability/tool_calls.json")
    assets = read_json("data/assets/sample_assets.json") + read_json("data/assets/phase2_additional_assets.json")

    session_ids = {session.get("session_id") for session in sessions}
    asset_ids = {asset.get("asset_id") for asset in assets}

    required_session_keys = {
        "session_id",
        "started_at",
        "actor_id",
        "actor_department",
        "agent_id",
        "agent_type",
        "use_case",
        "prompt_intent",
        "prompt_risk_signals",
        "approval_status",
        "response_destination",
    }
    for session in sessions:
        missing = required_session_keys - set(session)
        if missing:
            errors.append(f"AI session {session.get('session_id', '<unknown>')} missing keys: {sorted(missing)}")
        destination = session.get("response_destination", {})
        if not {"destination_id", "destination_type", "scope", "external"}.issubset(destination):
            errors.append(f"AI session {session.get('session_id')} has incomplete response_destination")

    for trace in retrieval_traces:
        if trace.get("session_id") not in session_ids:
            errors.append(f"retrieval trace {trace.get('trace_id')} references unknown session: {trace.get('session_id')}")
        if trace.get("asset_id") not in asset_ids:
            errors.append(f"retrieval trace {trace.get('trace_id')} references unknown asset: {trace.get('asset_id')}")

    for call in tool_calls:
        if call.get("session_id") not in session_ids:
            errors.append(f"tool call {call.get('tool_call_id')} references unknown session: {call.get('session_id')}")
        target_asset_id = call.get("target_asset_id")
        if target_asset_id and target_asset_id not in asset_ids:
            errors.append(f"tool call {call.get('tool_call_id')} references unknown asset: {target_asset_id}")

    return errors


def validate_boundary_claims() -> list[str]:
    errors = []
    markdown_content = "\n".join(
        path.read_text(encoding="utf-8").lower() for path in ROOT.rglob("*.md")
    )

    for phrase in REQUIRED_BOUNDARY_PHRASES:
        if phrase not in markdown_content:
            errors.append(f"missing required boundary phrase: {phrase}")

    for claim in BLOCKED_AFFIRMATIVE_CLAIMS:
        if claim in markdown_content:
            errors.append(f"blocked affirmative boundary claim found: {claim}")

    return errors


def main() -> int:
    errors = []
    errors.extend(validate_required_paths())
    errors.extend(validate_json("data/assets/sample_assets.json"))
    errors.extend(validate_json("data/assets/phase2_additional_assets.json"))
    errors.extend(validate_json("data/content_samples/synthetic_documents.json"))
    errors.extend(validate_json("data/classification_patterns/sensitivity_patterns.json"))
    errors.extend(validate_json("data/access/identities.json"))
    errors.extend(validate_json("data/access/groups.json"))
    errors.extend(validate_json("data/access/permissions.json"))
    errors.extend(validate_json("data/observability/ai_sessions.json"))
    errors.extend(validate_json("data/observability/retrieval_traces.json"))
    errors.extend(validate_json("data/observability/tool_calls.json"))
    errors.extend(validate_json("data/events/ai_interactions.json"))
    errors.extend(validate_classifier_fixture_contract())
    errors.extend(validate_access_fixture_contract())
    errors.extend(validate_observability_fixture_contract())
    errors.extend(validate_boundary_claims())

    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("VALIDATION PASSED: DSPM lab contract is intact.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
