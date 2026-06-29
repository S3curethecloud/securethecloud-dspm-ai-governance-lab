# Policy Recommendation Model

## Purpose

The recommendation model translates posture findings into advisory remediation actions.

It does not create, update, or enforce production policies.

## Recommendation Categories

| Category | Example Recommendation |
|---|---|
| DLP | Create or update DLP policy for detected sensitive data types |
| Insider Risk | Route high-risk exposure to human review workflow |
| Access Review | Remove broad groups from sensitive assets |
| Sensitivity Labeling | Apply confidential or regulated label to sensitive assets |
| AI Governance | Require approval before AI retrieval of high-risk assets |
| Redaction | Redact sensitive fields before AI summarization |
| External Sharing | Block or require approval for external destinations |

## Recommendation Record

```json
{
  "recommendation_id": "REC-DLP-001",
  "source_risk": "Sensitive payroll data is broadly shared",
  "policy_type": "DLP",
  "priority": "critical",
  "action": "Create DLP rule blocking payroll data from broad access and external destinations",
  "authority": "advisory_only"
}
```

## Claims Boundary

All recommendations are lab-generated simulation outputs. They should be reviewed by a human data owner, security architect, or governance board before production implementation.
