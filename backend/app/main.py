"""Local API for the SecureTheCloud DSPM AI Governance Lab."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI

from backend.app.access_analyzer import analyze_access_exposure
from backend.app.classifier import classify_documents, summarize_classification_results
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

app = FastAPI(
    title="SecureTheCloud DSPM AI Governance Lab",
    version="0.3.0",
    description="Synthetic DSPM posture scoring, classification, access exposure, and AI data interaction governance API.",
)


def load_json(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_all_assets() -> list[dict]:
    assets = load_json(ASSETS_PATH)
    if ADDITIONAL_ASSETS_PATH.exists():
        assets.extend(load_json(ADDITIONAL_ASSETS_PATH))
    return assets


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
