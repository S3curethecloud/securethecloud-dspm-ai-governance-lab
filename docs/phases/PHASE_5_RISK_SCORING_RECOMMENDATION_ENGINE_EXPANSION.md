# Phase 5 Risk Scoring and Recommendation Engine Expansion

## Status

In progress

## Objective

Add a unified executive risk aggregation layer that correlates posture scoring, sensitivity classification, access exposure, and AI interaction observability.

Phase 5 turns separate evidence streams into one prioritized risk and recommendation model.

## Added Capabilities

- Unified executive risk aggregator.
- Cross-signal correlation by asset, AI event, and AI session.
- Signal diversity and repeated high-signal escalation.
- Normalized executive decision model.
- Unified recommendation aggregation.
- `/risk/unified` API endpoint.
- Unified risk evidence generation.

## Boundary

All risk aggregation is synthetic and advisory-only. No production enforcement, live tenant mutation, autonomous approval, or real customer data processing is introduced in this phase.

## Expected Evidence

When `python scripts/generate_evidence.py` runs, Phase 5 should add or refresh:

- `evidence/generated/unified_risk_results.json`
- `evidence/generated/unified_risk_summary.json`
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
http://127.0.0.1:8015/risk/unified
```
