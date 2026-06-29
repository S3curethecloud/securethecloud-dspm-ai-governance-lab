# DSPM Risk Model

## Scoring Objective

The risk model is deterministic, transparent, and interview-friendly. It is not a machine learning model. It is a control reasoning model for sensitive data posture.

## Asset Risk Inputs

| Input | Risk Signal |
|---|---|
| Sensitivity label | Higher classification increases base risk |
| Sensitivity type | PII, PHI, PCI, payroll, legal, credentials, and customer records increase risk |
| Broad access | all_employees, everyone, company_all, and domain_users increase exposure |
| External sharing | External exposure increases risk sharply |
| AI access | AI retrieval or summarization raises governance risk |
| Missing DLP | Missing control coverage increases risk |
| Missing Insider Risk | Missing review workflow increases risk for high-risk data |

## AI Interaction Risk Inputs

| Input | Risk Signal |
|---|---|
| Sensitive data in prompt/retrieval path | Indicates AI/data exposure |
| External destination | Indicates potential exfiltration path |
| High-risk retrieved asset | Indicates inherited data posture risk |

## Decision Thresholds

| Score | Level | Decision Bias |
|---:|---|---|
| 0-39 | low | allow |
| 40-64 | medium | redact |
| 65-89 | high | approval_required |
| 90-100 | critical | deny or approval_required depending on exposure path |

## Design Rationale

The scoring model is intentionally explainable. Every score must map back to specific posture reasons and recommendations.
