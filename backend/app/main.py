"""Local API for the SecureTheCloud DSPM AI Governance Lab."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI

from backend.app.scoring import score_ai_interaction, score_asset, summarize_posture

ROOT = Path(__file__).resolve().parents[2]
ASSETS_PATH = ROOT / "data" / "assets" / "sample_assets.json"
EVENTS_PATH = ROOT / "data" / "events" / "ai_interactions.json"

app = FastAPI(
    title="SecureTheCloud DSPM AI Governance Lab",
    version="0.1.0",
    description="Synthetic DSPM posture scoring and AI data interaction governance API.",
)


def load_json(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


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
    return load_json(ASSETS_PATH)


@app.get("/ai-interactions")
def list_ai_interactions() -> list[dict]:
    return load_json(EVENTS_PATH)


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
