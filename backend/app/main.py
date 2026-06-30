"""Local API for the SecureTheCloud DSPM AI Governance Lab."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from fastapi import FastAPI

from backend.app.access_analyzer import analyze_access_exposure
from backend.app.classifier import classify_documents, summarize_classification_results
from backend.app.evidence_package import build_evidence_package
from backend.app.observability import analyze_ai_observability
from backend.app.risk_aggregator import aggregate_unified_risk
from backend.app.scoring import score_ai_interaction, score_asset, summarize_posture

ROOT = Path(__file__).resolve().parents[2]
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

app = FastAPI(
    title="SecureTheCloud DSPM AI Governance Lab",
    version="0.6.0",
    description="Synthetic DSPM posture scoring, classification, access exposure, AI observability, unified risk, and evidence package API.",
)


def load_json(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_all_assets() -> list[dict]:
    assets = load_json(ASSETS_PATH)
    if ADDITIONAL_ASSETS_PATH.exists():
        assets.extend(load_json(ADDITIONAL_ASSETS_PATH))
    return assets


def build_risk_context() -> dict:
    assets = load_json(ASSETS_PATH)
    all_assets = load_all_assets()
    events = load_json(EVENTS_PATH)
    asset_index = {asset["asset_id"]: asset for asset in assets}
    patterns = load_json(PATTERNS_PATH)
    documents = load_json(DOCUMENTS_PATH)

    asset_results = [score_asset(asset) for asset in assets]
    ai_event_results = [score_ai_interaction(event, asset_index) for event in events]
    classification_results = classify_documents(documents, patterns)
    classification_summary = summarize_classification_results(classification_results)
    access_exposure = analyze_access_exposure(
        all_assets,
        load_json(PERMISSIONS_PATH),
        load_json(IDENTITIES_PATH),
        load_json(GROUPS_PATH),
    )
    observability = analyze_ai_observability(
        load_json(AI_SESSIONS_PATH),
        load_json(RETRIEVAL_TRACES_PATH),
        load_json(TOOL_CALLS_PATH),
        all_assets,
    )
    unified_risk_result = aggregate_unified_risk(
        asset_results,
        ai_event_results,
        classification_results,
        access_exposure["results"],
        observability["results"],
    )

    return {
        "asset_results": asset_results,
        "ai_event_results": ai_event_results,
        "classification_results": classification_results,
        "classification_summary": classification_summary,
        "access_results": access_exposure["results"],
        "access_summary": access_exposure["summary"],
        "observability_results": observability["results"],
        "observability_summary": observability["summary"],
        "unified_risk_results": unified_risk_result["results"],
        "unified_risk_summary": unified_risk_result["summary"],
    }


def build_evidence_artifacts() -> dict:
    context = build_risk_context()
    assets = load_json(ASSETS_PATH)
    events = load_json(EVENTS_PATH)
    posture_summary_result = summarize_posture(assets, events)

    return {
        "posture_summary.json": posture_summary_result,
        "asset_risk_results.json": context["asset_results"],
        "ai_interaction_risk_results.json": context["ai_event_results"],
        "classification_results.json": context["classification_results"],
        "classification_summary.json": context["classification_summary"],
        "access_exposure_results.json": context["access_results"],
        "access_exposure_summary.json": context["access_summary"],
        "ai_observability_results.json": context["observability_results"],
        "ai_observability_summary.json": context["observability_summary"],
        "unified_risk_results.json": context["unified_risk_results"],
        "unified_risk_summary.json": context["unified_risk_summary"],
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "platform": "securethecloud-dspm-ai-governance-lab",
        "data_mode": "synthetic",
        "authority": "advisory_only",
    }


@app.get("/assets")
def list_assets() -> list[dict]:
    return load_all_assets()


@app.get("/ai-interactions")
def list_ai_interactions() -> list[dict]:
    return load_json(EVENTS_PATH)


@app.get("/classification/patterns")
def classification_patterns() -> list[dict]:
    return load_json(PATTERNS_PATH)


@app.get("/classification/assets")
def classify_assets() -> dict:
    documents = load_json(DOCUMENTS_PATH)
    patterns = load_json(PATTERNS_PATH)
    results = classify_documents(documents, patterns)
    return {
        "summary": summarize_classification_results(results),
        "results": results,
    }


@app.get("/access/exposure")
def access_exposure() -> dict:
    return analyze_access_exposure(
        load_all_assets(),
        load_json(PERMISSIONS_PATH),
        load_json(IDENTITIES_PATH),
        load_json(GROUPS_PATH),
    )


@app.get("/observability/ai-interactions")
def ai_interaction_observability() -> dict:
    return analyze_ai_observability(
        load_json(AI_SESSIONS_PATH),
        load_json(RETRIEVAL_TRACES_PATH),
        load_json(TOOL_CALLS_PATH),
        load_all_assets(),
    )


@app.get("/risk/unified")
def unified_risk() -> dict:
    context = build_risk_context()
    return {
        "summary": context["unified_risk_summary"],
        "results": context["unified_risk_results"],
    }


@app.get("/evidence/package")
def evidence_package() -> dict:
    return build_evidence_package(
        build_evidence_artifacts(),
        datetime.now(UTC).replace(microsecond=0).isoformat(),
    )


@app.get("/risk/assets")
def asset_risk_results() -> list[dict]:
    return [score_asset(asset) for asset in load_json(ASSETS_PATH)]


@app.get("/risk/ai-interactions")
def ai_interaction_risk_results() -> list[dict]:
    assets = load_json(ASSETS_PATH)
    events = load_json(EVENTS_PATH)
    asset_index = {asset["asset_id"]: asset for asset in assets}
    return [score_ai_interaction(event, asset_index) for event in events]


@app.get("/posture/summary")
def posture_summary() -> dict:
    return summarize_posture(load_json(ASSETS_PATH), load_json(EVENTS_PATH))
