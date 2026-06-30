# Phase 3 Access Exposure Analyzer

## Status

In progress

## Objective

Add identity, group, and permission-aware access exposure analysis to the DSPM AI Governance Lab.

Phase 3 expands the lab from classification evidence into access posture evidence. It determines whether sensitive assets are exposed to broad groups, external principals, privileged identities, inherited permissions, or AI retrieval paths.

## Added Capabilities

- Synthetic identity fixture model.
- Synthetic group fixture model.
- Synthetic permissions fixture model.
- Deterministic access exposure analyzer.
- Access exposure unit tests.
- `/access/exposure` API endpoint.
- Access exposure evidence generation.

## Boundary

All identity, group, and permission inputs are synthetic. No live Microsoft Graph, Entra ID, SharePoint, Purview, GitHub production repository, customer tenant, or authorization system integration is introduced in this phase.

## Expected Evidence

When `python scripts/generate_evidence.py` runs, Phase 3 should add or refresh:

- `evidence/generated/access_exposure_results.json`
- `evidence/generated/access_exposure_summary.json`
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
http://127.0.0.1:8015/access/exposure
```
