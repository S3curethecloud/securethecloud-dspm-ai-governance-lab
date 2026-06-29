# DSPM Synthetic Evidence Summary

Generated at: `2026-06-29T18:54:55+00:00`

## Posture Overview

- Posture score: **21.25**
- Average risk score: **78.75**
- Total assets: **5**
- Total AI interactions: **3**

## Classification Overview

- Total classified documents: **9**
- Label counts: `{'highly_confidential': 3, 'confidential': 2, 'regulated': 3, 'public': 1}`
- Type counts: `{'payroll': 1, 'pii': 3, 'financial': 2, 'legal': 1, 'customer_record': 2, 'credential': 2, 'phi': 1, 'pci': 1}`
- Decision counts: `{'approval_required': 8, 'monitor': 1}`

## Risk Counts

- critical: 4
- high: 1
- low: 1
- medium: 2

## Top Risks

### hr-payroll-001

- Score: 100
- Risk level: critical
- Decision: deny
- Reasons:
  - sensitivity label is highly_confidential
  - sensitive data types detected: financial, payroll, pii
  - asset is broadly shared
  - AI access is allowed for this asset
  - DLP policy coverage is missing
  - Insider Risk policy coverage is missing
- Recommendations:
  - Run access review and remove broad group access
  - Require AI access policy review before retrieval or summarization
  - Create or update DLP policy for detected sensitivity types
  - Map asset to Insider Risk review workflow

### legal-mna-002

- Score: 100
- Risk level: critical
- Decision: deny
- Reasons:
  - sensitivity label is confidential
  - sensitive data types detected: financial, legal
  - external sharing is enabled
  - Insider Risk policy coverage is missing
- Recommendations:
  - Block external sharing for sensitive assets or require approval
  - Map asset to Insider Risk review workflow

### customer-records-003

- Score: 100
- Risk level: critical
- Decision: deny
- Reasons:
  - sensitivity label is regulated
  - sensitive data types detected: customer_record, pii
  - AI access is allowed for this asset
  - DLP policy coverage is missing
- Recommendations:
  - Require AI access policy review before retrieval or summarization
  - Create or update DLP policy for detected sensitivity types

### secrets-runbook-005

- Score: 100
- Risk level: critical
- Decision: deny
- Reasons:
  - sensitivity label is highly_confidential
  - sensitive data types detected: credential
  - asset is broadly shared
  - AI access is allowed for this asset
  - DLP policy coverage is missing
  - Insider Risk policy coverage is missing
- Recommendations:
  - Run access review and remove broad group access
  - Require AI access policy review before retrieval or summarization
  - Create or update DLP policy for detected sensitivity types
  - Map asset to Insider Risk review workflow

### ai-event-002

- Score: 85
- Risk level: high
- Decision: approval_required
- Reasons:
  - AI interaction observed
  - prompt or response path includes sensitive data
  - AI interaction targets a non-internal destination
  - retrieved high-risk asset legal-mna-002
- Recommendations:
  - Inspect prompt, retrieved content, and response handling
  - Apply DLP control for risky destination

## Boundary

This evidence is synthetic, advisory-only, and not derived from a live Microsoft tenant or production data source.
