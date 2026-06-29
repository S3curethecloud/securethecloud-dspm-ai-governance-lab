# Sensitivity Classification Model

## Purpose

The classifier expands the lab from pre-labeled posture scoring into content-driven synthetic classification.

It answers:

> What sensitive data types can be detected from synthetic document content before AI retrieval or summarization is allowed?

## Classification Inputs

| Input | Location |
|---|---|
| Pattern catalog | `data/classification_patterns/sensitivity_patterns.json` |
| Synthetic content samples | `data/content_samples/synthetic_documents.json` |
| Additional unlabeled assets | `data/assets/phase2_additional_assets.json` |

## Pattern Model

Each classifier pattern includes:

```json
{
  "pattern_id": "PAT-PII-SSN-001",
  "name": "Synthetic SSN token",
  "sensitivity_type": "pii",
  "inferred_label": "regulated",
  "regex": "SYNTHETIC-SSN-[0-9]{3}-[0-9]{2}-[0-9]{4}",
  "risk_points": 35,
  "confidence": 0.95
}
```

## Classification Output

Each classified document produces:

- asset ID
- classification score
- inferred sensitivity label
- detected sensitivity types
- matched pattern IDs
- confidence score
- decision
- advisory-only authority marker

## Decision Outcomes

| Decision | Meaning |
|---|---|
| monitor | No sensitive marker found or low sensitivity signal |
| label_required | Content should be reviewed for sensitivity label assignment |
| dlp_recommended | DLP policy mapping should be considered |
| approval_required | Human approval required before AI access or data movement |

## Boundary

This classifier uses synthetic patterns and synthetic documents only. It does not call Microsoft Purview, Microsoft Graph, Azure AI, external LLMs, or production scanning systems.
