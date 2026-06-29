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
    "backend/tests/test_scoring.py",
    "backend/tests/test_classifier.py",
    "data/assets/sample_assets.json",
    "data/assets/phase2_additional_assets.json",
    "data/content_samples/synthetic_documents.json",
    "data/classification_patterns/sensitivity_patterns.json",
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


def validate_required_paths() -> list[str]:
    errors = []
    for relative_path in REQUIRED_PATHS:
        if not (ROOT / relative_path).exists():
            errors.append(f"missing required path: {relative_path}")
    return errors


def validate_json(relative_path: str) -> list[str]:
    try:
        json.loads(read_text(relative_path))
    except Exception as exc:  # pragma: no cover - diagnostic path
        return [f"invalid json in {relative_path}: {exc}"]
    return []


def validate_classifier_fixture_contract() -> list[str]:
    errors = []
    patterns = json.loads(read_text("data/classification_patterns/sensitivity_patterns.json"))
    documents = json.loads(read_text("data/content_samples/synthetic_documents.json"))

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
    errors.extend(validate_json("data/events/ai_interactions.json"))
    errors.extend(validate_classifier_fixture_contract())
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
