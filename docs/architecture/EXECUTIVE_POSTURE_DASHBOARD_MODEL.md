# Executive Posture Dashboard Model

## Purpose

The executive posture dashboard model turns generated DSPM, AI governance, unified risk, and evidence package outputs into leadership-facing KPIs and top-risk cards.

It answers:

> What should an executive or governance leader look at first?

## Inputs

| Input | Source |
|---|---|
| Posture summary | `evidence/generated/posture_summary.json` |
| Classification summary | `evidence/generated/classification_summary.json` |
| Access exposure summary | `evidence/generated/access_exposure_summary.json` |
| AI observability summary | `evidence/generated/ai_observability_summary.json` |
| Unified risk summary and results | `evidence/generated/unified_risk_summary.json`, `evidence/generated/unified_risk_results.json` |
| Evidence validation summary | `evidence/generated/evidence_validation_summary.json` |

## Dashboard Outputs

Phase 7 adds:

- `evidence/generated/executive_dashboard.json`
- `evidence/generated/dashboard_summary.json`

## Dashboard Sections

The dashboard contains:

- Executive KPI strip.
- KPI severity counts.
- Top risk cards.
- Decision breakdown.
- Priority breakdown.
- Evidence health.
- Control recommendation feed.

## KPI Categories

The dashboard model includes KPIs for:

- DSPM posture score.
- Critical risk subjects.
- Deny decisions.
- Approval-required decisions.
- Sensitive AI retrieval sessions.
- AI access exposures.
- Classified documents.
- Evidence validation status.

## API Endpoint

```text
GET /dashboard/executive
```

## Boundary

This model is synthetic and advisory-only. It does not perform production enforcement, live tenant mutation, autonomous approval, or real customer data processing.
