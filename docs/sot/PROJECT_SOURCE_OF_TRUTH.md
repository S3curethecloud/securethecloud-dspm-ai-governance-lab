# Project Source of Truth

## Project Name

SecureTheCloud DSPM AI Governance Lab

## Purpose

Build an enterprise-grade, simulation-first Data Security Posture Management lab for GenAI, Microsoft Copilot-style assistants, agents, sensitive data exposure, and governance evidence.

The lab answers:

> Is the enterprise data estate ready for AI retrieval, summarization, and agentic workflows?

## Current State

The lab is in bootstrap/foundation state.

It currently provides:

- Repository doctrine and governance boundary.
- Synthetic data asset inventory.
- Synthetic AI interaction events.
- Deterministic risk scoring engine.
- Local FastAPI API shell.
- CI validation workflow.
- Repository validation script.
- Initial policy rule definitions.

## Non-Negotiable Boundary

This lab is synthetic-only until explicitly authorized by a later phase.

No real tenant connection, real customer data, live Purview mutation, Graph write operation, production enforcement, or autonomous approval is allowed.

## Strategic Positioning

This lab complements Microsoft Copilot governance by shifting the security lens from the app/runtime layer to the data posture layer.

It is designed to show:

- What sensitive data exists.
- Where it lives.
- Who can access it.
- Whether it is overshared.
- Whether AI apps or agents interact with it.
- Which controls should be recommended.
- Which evidence proves readiness or risk.

## Phase Authority

Current authorized work:

- Phase 0 bootstrap.
- Phase 1 architecture and risk model.
- Synthetic fixtures.
- Local scoring engine.
- Evidence contract planning.

Blocked until future phase:

- Live Microsoft 365 / Purview / Graph connector.
- Production access tokens.
- Tenant onboarding.
- Runtime enforcement.
- Automated DLP or Insider Risk policy creation.
