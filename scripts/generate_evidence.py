"""Generate synthetic DSPM posture evidence artifacts.

This script converts the lab's synthetic asset and AI interaction fixtures into
reviewable evidence outputs for architecture walkthroughs and phase closure.
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.scoring import score_ai_interaction, score_asset, summarize_posture

ASSETS_PATH = ROOT / "data" / "assets" / "sample_assets.json"
EVENTS_PATH = ROOT / "data" / "events" / "ai_interactions.json"
OUTPUT_DIR = ROOT / "evidence" / "generated"


def load_json(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def write_markdown(path: Path, summary: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    top_risks = summary.get("top_risks", [])
    lines = [
        "# DSPM Synthetic Evidence Summary",
        "",
        f"Generated at: `{summary['generated_at']}`",
        "",
        "## Posture Overview",
        "",
        f"- Posture score: **{summary['posture_score']}**",
        f"- Average risk score: **{summary['average_risk_score']}**",
        f"- Total assets: **{summary['total_assets']}**",
        f"- Total AI interactions: **{summary['total_ai_interactions']}**",
        "",
        "## Risk Counts",
        "",
    ]

    for level, count in sorted(summary.get("risk_counts", {}).items()):
        lines.append(f"- {level}: {count}")

    lines.extend(["", "## Top Risks", ""])
    for risk in top_risks:
        lines.append(f"### {risk['subject_id']}")
        lines.append("")
        lines.append(f"- Score: {risk['score']}")
        lines.append(f"- Risk level: {risk['risk_level']}")
        lines.append(f"- Decision: {risk['decision']}")
        lines.append("- Reasons:")
        for reason in risk.get("reasons", []):
            lines.append(f"  - {reason}")
        lines.append("- Recommendations:")
        for recommendation in risk.get("recommendations", []):
            lines.append(f"  - {recommendation}")
        lines.append("")

    lines.extend(
        [
            "## Boundary",
            "",
            "This evidence is synthetic, advisory-only, and not derived from a live Microsoft tenant or production data source.",
            "",
        ]
    )

    path.write_text("\n".join(lines), encoding="utf-8")


def build_evidence() -> dict[str, Any]:
    assets = load_json(ASSETS_PATH)
    events = load_json(EVENTS_PATH)
    asset_index = {asset["asset_id"]: asset for asset in assets}

    asset_results = [score_asset(asset) for asset in assets]
    event_results = [score_ai_interaction(event, asset_index) for event in events]
    posture_summary = summarize_posture(assets, events)

    generated_at = datetime.now(UTC).replace(microsecond=0).isoformat()
    posture_summary["generated_at"] = generated_at
    posture_summary["evidence_mode"] = "synthetic"
    posture_summary["authority"] = "advisory_only"

    recommendation_register = []
    for result in asset_results + event_results:
        for recommendation in result.get("recommendations", []):
            recommendation_register.append(
                {
                    "subject_id": result["subject_id"],
                    "risk_level": result["risk_level"],
                    "decision": result["decision"],
                    "recommendation": recommendation,
                    "authority": "advisory_only",
                }
            )

    manifest = {
        "generated_at": generated_at,
        "lab": "securethecloud-dspm-ai-governance-lab",
        "evidence_mode": "synthetic",
        "authority": "advisory_only",
        "artifacts": [
            "posture_summary.json",
            "asset_risk_results.json",
            "ai_interaction_risk_results.json",
            "recommendation_register.json",
            "evidence_manifest.json",
            "executive_summary.md",
        ],
    }

    return {
        "posture_summary": posture_summary,
        "asset_risk_results": asset_results,
        "ai_interaction_risk_results": event_results,
        "recommendation_register": recommendation_register,
        "manifest": manifest,
    }


def main() -> int:
    evidence = build_evidence()

    write_json(OUTPUT_DIR / "posture_summary.json", evidence["posture_summary"])
    write_json(OUTPUT_DIR / "asset_risk_results.json", evidence["asset_risk_results"])
    write_json(OUTPUT_DIR / "ai_interaction_risk_results.json", evidence["ai_interaction_risk_results"])
    write_json(OUTPUT_DIR / "recommendation_register.json", evidence["recommendation_register"])
    write_json(OUTPUT_DIR / "evidence_manifest.json", evidence["manifest"])
    write_markdown(OUTPUT_DIR / "executive_summary.md", evidence["posture_summary"])

    print(f"Generated synthetic DSPM evidence in {OUTPUT_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
