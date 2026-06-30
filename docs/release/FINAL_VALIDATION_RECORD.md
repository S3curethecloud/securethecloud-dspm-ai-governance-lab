# Final Validation Record

## Purpose

This record defines the final validation gate for the SecureTheCloud DSPM AI Governance Lab release.

## Required Local Validation Commands

Run from the repository root:

```bash
python scripts/validate_repo.py
python -m pytest
python scripts/generate_evidence.py
git status --short
```

## Expected Local Validation Results

```text
VALIDATION PASSED: DSPM lab contract is intact.
24 passed
Generated synthetic DSPM evidence in evidence/generated
```

`git status --short` should be clean before final release closure.

## Required CI Validation

The GitHub Actions workflow must pass on `main`:

```text
.github/workflows/ci.yml
```

CI validates:

- Repository contract.
- Unit tests.
- Evidence generation.
- Frontend dashboard data bundle presence.
- Generated evidence output presence.

## Required Dashboard Validation

The Cloudflare Pages dashboard must load successfully:

```text
https://securethecloud-dspm-ai-governance-lab.pages.dev/
```

Expected dashboard status badge:

```text
advisory_only evidence loaded
```

## Boundary Validation

The final release must preserve these boundaries:

- Synthetic-only evidence.
- Advisory-only decisions.
- No live Microsoft tenant connection.
- No production data source.
- No production enforcement.
- No autonomous approval.
- No real customer data.

## Final Gate Status

Pending until local validation, CI validation, and release closure evidence are confirmed.
