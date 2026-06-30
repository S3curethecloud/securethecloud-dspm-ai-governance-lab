# Unified Risk Recommendation Model

## Purpose

The unified risk recommendation model expands the DSPM AI Governance Lab from separate findings into one executive risk view.

It answers:

> Which data, access, and AI activity risks should leadership prioritize first?

## Input Signals

| Signal | Source |
|---|---|
| Asset posture | `evidence/generated/asset_risk_results.json` |
| AI interaction posture | `evidence/generated/ai_interaction_risk_results.json` |
| Sensitivity classification | `evidence/generated/classification_results.json` |
| Access exposure | `evidence/generated/access_exposure_results.json` |
| AI interaction observability | `evidence/generated/ai_observability_results.json` |

## Correlation Strategy

The model correlates risk by subject:

- Asset IDs receive posture, classification, access exposure, and linked AI observability signals.
- AI event IDs receive AI interaction posture signals.
- AI session IDs receive AI observability signals.

AI observability signals are also linked back to retrieved asset IDs so leaders can see when a data asset is risky because of both static posture and runtime AI usage.

## Composite Score

Composite score is calculated as:

```text
highest signal score
+ signal diversity bonus
+ multiple high-signal bonus
+ repeated control-signal bonus
```

The score is capped at 100.

## Executive Decisions

| Score | Priority | Decision |
|---:|---|---|
| 90-100 | critical | deny |
| 75-89 | high | approval_required |
| 50-74 | high or medium | control_required |
| 0-49 | low or medium | monitor |

## Evidence Outputs

Phase 5 evidence generation adds:

- `evidence/generated/unified_risk_results.json`
- `evidence/generated/unified_risk_summary.json`
- Updated `evidence/generated/recommendation_register.json`
- Updated `evidence/generated/evidence_manifest.json`
- Updated `evidence/generated/executive_summary.md`

## Boundary

This model is synthetic and advisory-only. It does not perform production enforcement, live tenant mutation, autonomous approval, or real customer data processing.
