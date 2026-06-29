# Phase 2 Synthetic Data Estate and Classifier Expansion

## Status

In progress

## Objective

Expand the DSPM lab from pre-labeled posture scoring into deterministic sensitive-data classification.

Phase 2 adds synthetic content samples, classification patterns, classifier logic, classifier tests, API exposure, and generated classification evidence.

## Added Capabilities

- Synthetic sensitivity pattern catalog.
- Additional unlabeled synthetic assets.
- Synthetic document/content samples.
- Deterministic classifier engine.
- Classification summary generation.
- `/classification/patterns` API endpoint.
- `/classification/assets` API endpoint.
- Classification evidence generation.

## Boundary

All classification inputs are synthetic. No live Microsoft tenant, Purview, Graph, customer data, or production classifier integration is introduced in this phase.

## Expected Evidence

When `python scripts/generate_evidence.py` runs, Phase 2 should add or refresh:

- `evidence/generated/classification_results.json`
- `evidence/generated/classification_summary.json`
- Updated `evidence/generated/evidence_manifest.json`
- Updated `evidence/generated/executive_summary.md`
- Updated `evidence/generated/recommendation_register.json`

## Validation Commands

```bash
python scripts/validate_repo.py
python -m pytest
python scripts/generate_evidence.py
```

## Demo Endpoints

```text
http://127.0.0.1:8015/classification/patterns
http://127.0.0.1:8015/classification/assets
```
