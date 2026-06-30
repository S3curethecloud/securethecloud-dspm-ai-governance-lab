# AI Interaction Observability Model

## Purpose

The AI interaction observability model expands the DSPM AI Governance Lab from data posture and access exposure into session-level AI activity tracing.

It answers:

> What did the AI session request, what sensitive assets were retrieved, which tools were called, and where did the response go?

## Inputs

| Input | Location |
|---|---|
| AI session fixture model | `data/observability/ai_sessions.json` |
| Retrieval trace fixture model | `data/observability/retrieval_traces.json` |
| Tool call fixture model | `data/observability/tool_calls.json` |
| Synthetic assets | `data/assets/sample_assets.json`, `data/assets/phase2_additional_assets.json` |

## Observability Signals

The observability engine evaluates:

- Prompt risk signals.
- Retrieved sensitive assets.
- Multiple sensitive retrievals in one session.
- External or partner response destinations.
- Write, export, ticketing, or egress tool actions.
- Denied tool calls.
- Sensitive retrieval without approval.
- Service-agent or agentic workflow retrieval of sensitive data.

## Decisions

| Decision | Meaning |
|---|---|
| monitor | Low-risk AI session state |
| redact | Response should be redacted or minimized before release |
| approval_required | Human approval required before response release or tool execution |
| deny | Response or tool action should be blocked in a real governance workflow |

## Timeline Model

Each observed session produces a timeline containing:

- Session start event.
- Retrieval trace events.
- Tool call events.
- Response destination event.

This gives the lab an evidence path from prompt to retrieval to tool use to destination.

## Evidence Outputs

Phase 4 evidence generation adds:

- `evidence/generated/ai_observability_results.json`
- `evidence/generated/ai_observability_summary.json`
- Updated `evidence/generated/recommendation_register.json`
- Updated `evidence/generated/evidence_manifest.json`
- Updated `evidence/generated/executive_summary.md`

## Boundary

This model is synthetic and advisory-only. It does not connect to live LLM providers, Microsoft Graph, Entra ID, SharePoint, Purview, Copilot telemetry, GitHub production repositories, customer tenants, or live authorization systems.
