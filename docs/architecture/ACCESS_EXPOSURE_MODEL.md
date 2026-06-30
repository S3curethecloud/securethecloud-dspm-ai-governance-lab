# Access Exposure Model

## Purpose

The access exposure analyzer expands the DSPM AI Governance Lab from content classification into permission-aware data posture analysis.

It answers:

> Who can access sensitive data, and is that access appropriate before AI systems retrieve or summarize it?

## Inputs

| Input | Location |
|---|---|
| Synthetic identities | `data/access/identities.json` |
| Synthetic groups | `data/access/groups.json` |
| Synthetic permissions | `data/access/permissions.json` |
| Synthetic assets | `data/assets/sample_assets.json`, `data/assets/phase2_additional_assets.json` |

## Exposure Signals

The analyzer evaluates:

- Sensitive or regulated assets.
- Broad access groups.
- External or guest principals.
- Privileged or write-capable permissions.
- Inherited permissions.
- AI tool access to sensitive assets.
- Privileged identities.
- High-risk principals.

## Decisions

| Decision | Meaning |
|---|---|
| monitor | Low-risk permission state |
| access_review | Human access review recommended |
| approval_required | Approval required before continued access or AI retrieval |
| deny | Access should be removed or blocked in a real governance workflow |

## Evidence Outputs

Phase 3 evidence generation adds:

- `evidence/generated/access_exposure_results.json`
- `evidence/generated/access_exposure_summary.json`
- Updated `evidence/generated/recommendation_register.json`
- Updated `evidence/generated/evidence_manifest.json`
- Updated `evidence/generated/executive_summary.md`

## Boundary

This model is synthetic and advisory-only. It does not connect to Microsoft Graph, Entra ID, SharePoint, Purview, GitHub production repositories, customer tenants, or live authorization systems.
