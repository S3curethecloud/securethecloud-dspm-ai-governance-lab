# Architecture Baseline

## Baseline Pattern

```text
Synthetic Data Estate
  -> Discovery / Inventory
  -> Classification
  -> Access Exposure Analysis
  -> AI Interaction Observation
  -> Risk Scoring
  -> Recommendation Generation
  -> Evidence Store
  -> Executive Dashboard
```

## Primary Components

| Component | Responsibility |
|---|---|
| Data asset inventory | Synthetic representation of files, repositories, blobs, and collaboration data |
| AI interaction events | Synthetic Copilot-style and agent-style data access events |
| Scoring engine | Deterministic risk score and decision recommendation |
| Policy rules | Human-readable advisory rules for DSPM posture recommendations |
| API shell | Local FastAPI interface for assets, events, risks, and summary posture |
| Evidence store | Future generated outputs for audit-ready evidence packages |
| Dashboard | Future executive posture and readiness surface |

## Current Runtime

- Python
- FastAPI
- Pydantic
- Pytest
- JSON fixtures
- YAML policy rules

## Integration Direction

The Microsoft Copilot Governance Lab remains the Copilot adoption and governance-control-plane companion.

This DSPM lab becomes the data posture layer that can feed Copilot readiness, oversharing detection, sensitivity label gaps, DLP recommendations, and evidence posture into the broader governance platform.
