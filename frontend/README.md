# Frontend Workspace

The frontend workspace now contains a static executive posture dashboard for the SecureTheCloud DSPM AI Governance Lab.

## Dashboard Views

The dashboard renders:

- DSPM posture score
- Critical risk subjects
- Deny and approval-required decisions
- Sensitive AI retrieval sessions
- AI access exposures
- Evidence validation health
- Top risk cards
- Recommendation register
- AI Governance Companion export summary
- Evidence manifest artifacts

## Source Data

The dashboard reads generated evidence from:

- `../evidence/generated/executive_dashboard.json`
- `../evidence/generated/evidence_manifest.json`
- `../evidence/generated/ai_governance_companion_export_summary.json`

## Local Preview

Run from the repository root:

```bash
python scripts/generate_evidence.py
python -m http.server 8080
```

Open:

```text
http://127.0.0.1:8080/frontend/
```

## Cloudflare Pages Preview Option

For a static Cloudflare Pages preview, deploy the repository with the output directory set to the repository root so `/frontend/` can read `/evidence/generated/` artifacts.

Suggested preview route:

```text
/frontend/
```

## Boundary

This dashboard is synthetic and advisory-only. It does not connect to a live Microsoft tenant, production data source, production authorization system, or real customer dataset.
