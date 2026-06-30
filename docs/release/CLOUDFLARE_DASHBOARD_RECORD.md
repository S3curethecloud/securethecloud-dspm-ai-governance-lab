# Cloudflare Dashboard Release Record

## Dashboard URL

```text
https://securethecloud-dspm-ai-governance-lab.pages.dev/
```

## Purpose

This Cloudflare Pages dashboard provides a public portfolio/demo view of the SecureTheCloud DSPM AI Governance Lab.

The dashboard presents:

- DSPM posture score.
- Critical risk subjects.
- Deny and approval-required decisions.
- Sensitive AI retrieval sessions.
- AI access exposures.
- Evidence validation health.
- Top risk cards.
- Recommendation register.
- AI Governance Companion export summary.
- Evidence manifest artifacts.

## Deployment Source

```text
S3curethecloud/securethecloud-dspm-ai-governance-lab
```

## Pages Configuration

```text
Framework preset: None
Production branch: main
Build output directory: frontend
Dashboard data bundle: frontend/data
```

## Evidence Loading Model

The dashboard loads static bundled evidence from:

```text
frontend/data/executive_dashboard.json
frontend/data/evidence_manifest.json
frontend/data/ai_governance_companion_export_summary.json
```

## Verified Behavior

The hosted dashboard displayed:

```text
advisory_only evidence loaded
```

This confirms that bundled static evidence was loaded successfully by the browser.

## Boundary

The hosted dashboard is synthetic and advisory-only. It does not connect to a live Microsoft tenant, production data source, production authorization system, or real customer dataset.
