# Scenario 001: Copilot Sensitive Data Oversharing

## Scenario

A company enables a Copilot-style assistant across HR, Finance, Legal, Engineering, and Customer Operations.

The security team needs to know whether sensitive data is overshared before AI assistants can retrieve and summarize enterprise content.

## Synthetic Findings

| Asset | Finding |
|---|---|
| Executive Payroll Adjustments | Highly confidential payroll data shared with all employees and available to AI |
| Confidential Acquisition Notes | Legal and financial data externally shared |
| Customer Support Export | Regulated customer records available to AI without DLP coverage |
| Legacy Integration Secret Notes | Credential-like content broadly accessible and available to AI |

## Expected Decisions

| Risk | Decision |
|---|---|
| Broad payroll exposure | approval_required or deny |
| External legal document exposure | deny |
| Customer record AI retrieval | approval_required |
| Credential-like content AI retrieval | deny |

## Evidence Required

- Asset ID
- Location
- Data owner
- Sensitivity label
- Sensitivity types
- Access scope
- AI access flag
- DLP coverage status
- Insider Risk coverage status
- Risk score
- Decision
- Recommendation list

## Interview Talking Point

This scenario demonstrates that Copilot and agent governance cannot start only at the application layer. It must include data readiness, oversharing discovery, sensitive data classification, DLP coverage, and evidence-backed approval workflows.
