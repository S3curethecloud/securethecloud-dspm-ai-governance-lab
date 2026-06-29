# Agent Operating Contract

This repository may use AI assistants for scaffolding, documentation, analysis, and code generation. All AI participation is bounded by the following contract.

## Allowed AI Actions

- Propose architecture, documentation, and implementation plans.
- Generate synthetic examples and synthetic test fixtures.
- Draft source-of-truth, governance, phase, and evidence documents.
- Suggest risk scoring, policy recommendation, and dashboard logic.
- Create code that remains reviewable, testable, and reversible.

## Blocked AI Actions

AI assistants must not:

- Approve their own work.
- Merge pull requests.
- Deploy infrastructure.
- Connect to real Microsoft 365, Purview, Graph, Azure, or customer tenants.
- Process real sensitive data.
- Mutate production DLP, Insider Risk, retention, access, or compliance policies.
- Override human review, policy review, or custodian approval.
- Represent lab outputs as production compliance certification.

## Agent Doctrine

```text
AI recommends. Humans approve.
Policy decides. Evidence proves.
The lab simulates posture logic; it does not enforce production controls.
```

## Required Review Posture

Every material change should preserve:

- Synthetic-data-only operation.
- No production tenant dependency.
- No hidden secrets.
- No autonomous authority.
- Clear source-of-truth updates.
- Evidence-first phase closure.
