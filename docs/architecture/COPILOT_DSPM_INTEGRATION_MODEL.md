# Copilot Governance and DSPM Integration Model

## Decision

The SecureTheCloud Microsoft Copilot Governance Lab is relevant to this DSPM AI Governance Lab and should be treated as a companion repository, not copied wholesale into this repository.

## Why It Is Relevant

The Microsoft Copilot Governance Lab focuses on secure Copilot adoption, control-plane structure, evidence generation, workspace architecture, and claims-safe governance workflows.

This DSPM lab focuses on the data posture layer that informs whether Copilot-style assistants and agents should be allowed to retrieve, summarize, or reason over sensitive data.

Together, they form a stronger architecture:

```text
Microsoft Copilot Governance Lab
  -> AI adoption governance
  -> control catalog
  -> readiness workflow
  -> evidence workspaces
  -> secure adoption checklist

DSPM AI Governance Lab
  -> sensitive data inventory
  -> oversharing analysis
  -> AI/data interaction scoring
  -> DLP and Insider Risk recommendations
  -> posture evidence
```

## Integration Boundary

The repos should remain separate because they serve different layers:

| Repository | Primary Layer | Role |
|---|---|---|
| Microsoft Copilot Governance Lab | Copilot adoption governance | Assesses Copilot readiness and governance controls |
| DSPM AI Governance Lab | Data posture governance | Assesses sensitive data exposure and AI data access risk |

## Recommended Local Workspace

Clone both repos side-by-side:

```bash
mkdir -p ~/securethecloud-labs
cd ~/securethecloud-labs

gh repo clone S3curethecloud/securethecloud-dspm-ai-governance-lab
gh repo clone S3curethecloud/SecureTheCloud-Microsoft-Copilot-Governance-Lab
```

Recommended local layout:

```text
securethecloud-labs/
├── securethecloud-dspm-ai-governance-lab/
└── SecureTheCloud-Microsoft-Copilot-Governance-Lab/
```

## Future Cross-Repo Contract

A future phase may add an export/import contract like this:

```json
{
  "source": "securethecloud-dspm-ai-governance-lab",
  "target": "SecureTheCloud-Microsoft-Copilot-Governance-Lab",
  "artifact_type": "dspm_posture_evidence",
  "fields": [
    "posture_score",
    "risk_counts",
    "top_risks",
    "dlp_recommendations",
    "insider_risk_recommendations",
    "ai_sensitive_data_events"
  ],
  "authority": "advisory_only"
}
```

## Future Phase Candidate

**Phase 8: Copilot Governance Companion Export**

Goal:

- Export DSPM posture summary into a static evidence artifact.
- Allow the Copilot Governance Lab to reference the DSPM evidence as a readiness input.
- Preserve separate repository boundaries.
- Avoid live tenant integration unless separately authorized.
