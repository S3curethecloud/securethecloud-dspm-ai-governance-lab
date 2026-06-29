"""Repository contract validation for the DSPM AI Governance Lab."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "README.md",
    "AGENTS.md",
    "GOVERNANCE.md",
    "backend/app/main.py",
    "backend/app/models.py",
    "backend/app/scoring.py",
    "backend/tests/test_scoring.py",
    "data/assets/sample_assets.json",
    "data/events/ai_interactions.json",
    "policies/dspm_policy_rules.yaml",
    "docs/sot/PROJECT_SOURCE_OF_TRUTH.md",
    "docs/architecture/DSPM_AI_GOVERNANCE_ARCHITECTURE.md",
]

BLOCKED_TERMS = [
    "real customer data",
    "production enforcement enabled",
    "live tenant mutation enabled",
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


def validate_boundary_language() -> list[str]:
    errors = []
    for path in ROOT.rglob("*.md"):
        content = path.read_text(encoding="utf-8").lower()
        for term in BLOCKED_TERMS:
            if term in content:
                errors.append(f"blocked boundary language in {path.relative_to(ROOT)}: {term}")
    return errors


def main() -> int:
    errors = []
    errors.extend(validate_required_paths())
    errors.extend(validate_json("data/assets/sample_assets.json"))
    errors.extend(validate_json("data/events/ai_interactions.json"))
    errors.extend(validate_boundary_language())

    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("VALIDATION PASSED: DSPM lab contract is intact.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
