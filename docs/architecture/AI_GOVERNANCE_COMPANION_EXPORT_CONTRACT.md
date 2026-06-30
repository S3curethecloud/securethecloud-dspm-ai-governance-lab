# AI Governance Companion Export Contract

## Purpose

The AI Governance Companion Export Contract provides an optional one-way evidence summary from the DSPM AI Governance Lab to a future or separate AI governance companion lab.

It answers:

> What should another governance lab know about DSPM posture, AI observability, executive risk, evidence health, and top-risk subjects without merging repositories?

## Export Type

```text
one_way_summary
```

## Contract Rules

The export contract is intentionally constrained:

- No repository merge required.
- No codebase dependency required.
- No live tenant required.
- No production enforcement.
- No autonomous approval.
- No real customer data.

## Export Outputs

Phase 8 adds:

- `evidence/generated/ai_governance_companion_export.json`
- `evidence/generated/ai_governance_companion_export_summary.json`

## Export Contents

The export includes:

- Contract metadata.
- Source lab identity.
- Target context.
- Evidence mode.
- Executive KPI summary.
- Top risk subject.
- Unified risk counts.
- AI observability counts.
- Evidence validation status.
- Recommended use guidance.
- Boundary markers.

## API Endpoint

```text
GET /exports/ai-governance-companion
```

## Boundary

This model is synthetic and advisory-only. It does not perform production enforcement, live tenant mutation, autonomous approval, repository merging, runtime coupling, or real customer data processing.
