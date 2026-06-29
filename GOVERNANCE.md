# Governance Model

## Repository Classification

- **Platform type:** SecureTheCloud lab platform
- **Data mode:** Synthetic data only
- **Runtime mode:** Local/demo only
- **Production mode:** Not enabled
- **Enforcement mode:** Not enabled
- **Current phase:** Phase 0 / Phase 1 foundation

## Authority Boundary

This lab models DSPM-style risk discovery, posture scoring, recommendation logic, and evidence production. It does not perform production enforcement.

| Layer | Role | Authority |
|---|---|---|
| Synthetic data estate | Provides sample assets and events | No real data authority |
| Classifier | Identifies synthetic sensitivity patterns | Advisory only |
| Access analyzer | Flags oversharing and exposure | Advisory only |
| AI observer | Records synthetic AI/data interactions | Advisory only |
| Risk scoring engine | Produces repeatable risk score | Advisory only |
| Recommendation engine | Suggests DLP/IRM/access actions | Recommendation only |
| Human reviewer | Reviews and approves next action | Final governance authority |

## Blocked Scope

The following remain out of scope until a future explicit phase gate:

- Live Microsoft 365 tenant connection
- Live Microsoft Purview mutation
- Microsoft Graph write operations
- Production DLP or Insider Risk policy creation
- Real user behavior monitoring
- Real sensitive data processing
- Tenant-level permissions
- Automated approval or enforcement
- Compliance certification claims

## Required Evidence

Every phase closure must include:

- Scope completed
- Files changed
- Boundary validation
- Test or review evidence
- Known gaps
- Next authorized phase

## Claims-Safe Language

Use:

> DSPM-inspired lab, synthetic evidence, posture simulation, governance pattern, recommendation logic.

Avoid:

> Production-ready Purview replacement, certified compliance system, live enforcement platform, autonomous policy authority.
