"""Generate synthetic DSPM posture evidence artifacts.

This script converts the lab's synthetic asset, AI interaction, classification,
access, and observability fixtures into reviewable evidence outputs for architecture walkthroughs and phase closure.
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

from backend.app.access_analyzer import analyze_access_exposure
from backend.app.classifier import classify_documents, summarize_classification_results
from backend.app.observability import analyze_ai_observability
from backend.app.scoring import score_ai_interaction, score_asset, summarize_posture

ASSETS_PATH = ROOT / "data" / "assets" / "sample_assets.json"
ADDITIONAL_ASSETS_PATH = ROOT / "data" / "assets" / "phase2_additional_assets.json"
EVENTS_PATH = ROOT / "data" / "events" / "ai_interactions.json"
PATTERNS_PATH = ROOT / "data" / "classification_patterns" / "sensitivity_patterns.json"
DOCUMENTS_PATH = ROOT / "data" / "content_samples" / "synthetic_documents.json"
IDENTITIES_PATH = ROOT / "data" / "access" / "identities.json"
GROUPS_PATH = ROOT / "data" / "access" / "groups.json"
PERMISSIONS_PATH = ROOT / "data" / "access" / "permissions.json"
AI_SESSIONS_PATH = ROOT / "data" / "observability" / "ai_sessions.json"
RETRIEVAL_TRACES_PATH = ROOT / "data" / "observability" / "retrieval_traces.json"
TOOL_CALLS_PATH = ROOT / "data" / "observability" / "tool_calls.json"
OUTPUT_DIR = ROOT / "evidence" / "generated"


def load_json(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_all_assets() -> list[dict[str, Any]]:
    assets = load_json(ASSETS_PATH)
    if ADDITIONAL_ASSETS_PATH.exists():
        assets.extend(load_json(ADDITIONAL_ASSETS_PATH))
    return assets


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def write_markdown(
    path: Path,
    summary: dict[str, Any],
    classification_summary: dict[str, Any],
    access_summary: dict[str, Any],
    observability_summary: dict[str, Any],
) -> None:
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
        "## Classification Overview",
        "",
        f"- Total classified documents: **{classification_summary['total_documents']}**",
        f"- Label counts: `{classification_summary['label_counts']}`",
        f"- Type counts: `{classification_summary['type_counts']}`",
        f"- Decision counts: `{classification_summary['decision_counts']}`",
        "",
        "## Access Exposure Overview",
        "",
        f"- Total permissions: **{access_summary['total_permissions']}**",
        f"- Exposure level counts: `{access_summary['level_counts']}`",
        f"- Decision counts: `{access_summary['decision_counts']}`",
        f"- External exposures: **{access_summary['external_exposures']}**",
        f"- Broad group exposures: **{access_summary['broad_group_exposures']}**",
        f"- AI access exposures: **{access_summary['ai_access_exposures']}**",
        "",
        "## AI Interaction Observability Overview",
        "",
        f"- Total observed sessions: **{observability_summary['total_sessions']}**",
        f"- Sensitive retrieval sessions: **{observability_summary['sensitive_retrieval_sessions']}**",
        f"- External destination sessions: **{observability_summary['external_destination_sessions']}**",
        f"- Write or export sessions: **{observability_summary['write_or_export_sessions']}**",
        f"- Observability level counts: `{observability_summary['level_counts']}`",
        f"- Decision counts: `{observability_summary['decision_counts']}`",
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
    all_assets = load_all_assets()
    events = load_json(EVENTS_PATH)
    patterns = load_json(PATTERNS_PATH)
    documents = load_json(DOCUMENTS_PATH)
    identities = load_json(IDENTITIES_PATH)
    groups = load_json(GROUPS_PATH)
    permissions = load_json(PERMISSIONS_PATH)
    ai_sessions = load_json(AI_SESSIONS_PATH)
    retrieval_traces = load_json(RETRIEVAL_TRACES_PATH)
    tool_calls = load_json(TOOL_CALLS_PATH)
    asset_index = {asset["asset_id"]: asset for asset in assets}

    asset_results = [score_asset(asset) for asset in assets]
    event_results = [score_ai_interaction(event, asset_index) for event in events]
    classification_results = classify_documents(documents, patterns)
    classification_summary = summarize_classification_results(classification_results)
    access_exposure = analyze_access_exposure(all_assets, permissions, identities, groups)
    ai_observability = analyze_ai_observability(ai_sessions, retrieval_traces, tool_calls, all_assets)
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

    for result in classification_results:
        if result["decision"] in {"approval_required", "dlp_recommended", "label_required"}:
            recommendation_register.append(
                {
                    "subject_id": result["asset_id"],
                    "risk_level": result["inferred_label"],
                    "decision": result["decision"],
                    "recommendation": "Review inferred sensitivity classification and map to label, DLP, or approval workflow",
                    "authority": "advisory_only",
                }
            )

    for result in access_exposure["results"]:
        for recommendation in result.get("recommendations", []):
            recommendation_register.append(
                {
                    "subject_id": result["asset_id"],
                    "risk_level": result["exposure_level"],
                    "decision": result["decision"],
                    "recommendation": recommendation,
                    "authority": "advisory_only",
                }
            )

    for result in ai_observability["results"]:
        for recommendation in result.get("recommendations", []):
            recommendation_register.append(
                {
                    "subject_id": result["session_id"],
                    "risk_level": result["observability_level"],
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
            "classification_results.json",
            "classification_summary.json",
            "access_exposure_results.json",
            "access_exposure_summary.json",
            "ai_observability_results.json",
            "ai_observability_summary.json",
            "recommendation_register.json",
            "evidence_manifest.json",
            "executive_summary.md",
        ],
    }

    return {
        "posture_summary": posture_summary,
        "asset_risk_results": asset_results,
        "ai_interaction_risk_results": event_results,
        "classification_results": classification_results,
        "classification_summary": classification_summary,
        "access_exposure_results": access_exposure["results"],
        "access_exposure_summary": access_exposure["summary"],
        "ai_observability_results": ai_observability["results"],
        "ai_observability_summary": ai_observability["summary"],
        "recommendation_register": recommendation_register,
        "manifest": manifest,
    }


def main() -> int:
    evidence = build_evidence()

    write_json(OUTPUT_DIR / "posture_summary.json", evidence["posture_summary"])
    write_json(OUTPUT_DIR / "asset_risk_results.json", evidence["asset_risk_results"])
    write_json(OUTPUT_DIR / "ai_interaction_risk_results.json", evidence["ai_interaction_risk_results"])
    write_json(OUTPUT_DIR / "classification_results.json", evidence["classification_results"])
    write_json(OUTPUT_DIR / "classification_summary.json", evidence["classification_summary"])
    write_json(OUTPUT_DIR / "access_exposure_results.json", evidence["access_exposure_results"])
    write_json(OUTPUT_DIR / "access_exposure_summary.json", evidence["access_exposure_summary"])
    write_json(OUTPUT_DIR / "ai_observability_results.json", evidence["ai_observability_results"])
    write_json(OUTPUT_DIR / "ai_observability_summary.json", evidence["ai_observability_summary"])
    write_json(OUTPUT_DIR / "recommendation_register.json", evidence["recommendation_register"])
    write_json(OUTPUT_DIR / "evidence_manifest.json", evidence["manifest"])
    write_markdown(
        OUTPUT_DIR / "executive_summary.md",
        evidence["posture_summary"],
        evidence["classification_summary"],
        evidence["access_exposure_summary"],
        evidence["ai_observability_summary"],
    )

    print(f"Generated synthetic DSPM evidence in {OUTPUT_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
