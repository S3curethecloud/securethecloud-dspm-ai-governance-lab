# Phase 7 Executive Posture Dashboard

## Status

In progress

## Objective

Add an executive posture dashboard layer that converts generated evidence into leadership-facing KPIs, top-risk cards, decision breakdowns, and control recommendation feeds.

Phase 7 makes the lab easier to demonstrate to executives, customers, auditors, and hiring panels.

## Added Capabilities

- Executive dashboard model.
- KPI extraction from generated evidence summaries.
- Top-risk executive card generation.
- Control recommendation dashboard feed.
- Dashboard summary generation.
- `/dashboard/executive` API endpoint.
- Executive dashboard unit tests.
- Evidence generator updates for dashboard outputs.

## Expected Evidence

When `python scripts/generate_evidence.py` runs, Phase 7 should add or refresh:

- `evidence/generated/executive_dashboard.json`
- `evidence/generated/dashboard_summary.json`
- Updated `evidence/generated/evidence_manifest.json`
- Updated `evidence/generated/executive_summary.md`

## Validation Commands

```bash
python scripts/validate_repo.py
python -m pytest
python scripts/generate_evidence.py
```

## Demo Endpoint

```text
http://127.0.0.1:8015/dashboard/executive
```

## Boundary

All dashboard outputs remain synthetic and advisory-only. No live tenant, production data source, or production enforcement path is introduced in this phase.
