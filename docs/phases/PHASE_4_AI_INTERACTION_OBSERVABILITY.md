# Phase 4 AI Interaction Observability

## Status

In progress

## Objective

Add session-level AI interaction observability to the DSPM AI Governance Lab.

Phase 4 expands the lab from asset classification and access exposure into prompt, retrieval, tool-call, and response-destination tracing.

## Added Capabilities

- Synthetic AI session fixture model.
- Synthetic retrieval trace fixture model.
- Synthetic tool call fixture model.
- Deterministic AI interaction observability engine.
- AI observability unit tests.
- `/observability/ai-interactions` API endpoint.
- AI observability evidence generation.

## Boundary

All AI session, retrieval, and tool-call inputs are synthetic. No live LLM provider, Microsoft Graph, Entra ID, SharePoint, Purview, Copilot telemetry, GitHub production repository, customer tenant, or authorization system integration is introduced in this phase.

## Expected Evidence

When `python scripts/generate_evidence.py` runs, Phase 4 should add or refresh:

- `evidence/generated/ai_observability_results.json`
- `evidence/generated/ai_observability_summary.json`
- Updated `evidence/generated/evidence_manifest.json`
- Updated `evidence/generated/executive_summary.md`
- Updated `evidence/generated/recommendation_register.json`

## Validation Commands

```bash
python scripts/validate_repo.py
python -m pytest
python scripts/generate_evidence.py
```

## Demo Endpoint

```text
http://127.0.0.1:8015/observability/ai-interactions
```
