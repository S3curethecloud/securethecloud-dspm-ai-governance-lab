# DSPM Synthetic Evidence Summary

Generated at: `2026-06-30T03:22:57+00:00`

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

## Access Exposure Overview

- Total permissions: **8**
- Exposure level counts: `{'critical': 2, 'medium': 2, 'high': 3, 'low': 1}`
- Decision counts: `{'deny': 2, 'access_review': 2, 'approval_required': 3, 'monitor': 1}`
- External exposures: **1**
- Broad group exposures: **4**
- AI access exposures: **6**

## AI Interaction Observability Overview

- Total observed sessions: **5**
- Sensitive retrieval sessions: **4**
- External destination sessions: **1**
- Write or export sessions: **2**
- Observability level counts: `{'medium': 1, 'critical': 2, 'high': 1, 'low': 1}`
- Decision counts: `{'redact': 1, 'deny': 2, 'approval_required': 1, 'monitor': 1}`

## Unified Executive Risk Overview

- Total risk subjects: **17**
- Subject type counts: `{'asset': 9, 'ai_session': 5, 'ai_event': 3}`
- Priority counts: `{'critical': 8, 'high': 2, 'medium': 6, 'low': 1}`
- Decision counts: `{'deny': 8, 'approval_required': 2, 'control_required': 5, 'monitor': 2}`
- Top priority subjects: `[{'subject_id': 'hr-payroll-001', 'subject_type': 'asset', 'composite_score': 100, 'priority_level': 'critical', 'decision': 'deny'}, {'subject_id': 'legal-mna-002', 'subject_type': 'asset', 'composite_score': 100, 'priority_level': 'critical', 'decision': 'deny'}, {'subject_id': 'customer-records-003', 'subject_type': 'asset', 'composite_score': 100, 'priority_level': 'critical', 'decision': 'deny'}, {'subject_id': 'secrets-runbook-005', 'subject_type': 'asset', 'composite_score': 100, 'priority_level': 'critical', 'decision': 'deny'}, {'subject_id': 'ai-session-002', 'subject_type': 'ai_session', 'composite_score': 100, 'priority_level': 'critical', 'decision': 'deny'}]`

## Evidence Package Overview

- Artifact count: **12**
- Audit chain events: **12**
- Validation status: **passed**

## Executive Dashboard Overview

- Total KPIs: **8**
- KPI severity counts: `{'critical': 5, 'warning': 1, 'healthy': 2}`
- Top risk subject: `{'subject_id': 'hr-payroll-001', 'subject_type': 'asset', 'composite_score': 100, 'priority_level': 'critical', 'decision': 'deny', 'signal_count': 5, 'signal_types': ['access_exposure', 'ai_observability', 'classification', 'posture'], 'executive_reasons': ['sensitivity label is highly_confidential', 'sensitive data types detected: financial, payroll, pii', 'asset is broadly shared', 'AI access is allowed for this asset', 'DLP policy coverage is missing'], 'recommended_controls': ['Run access review and remove broad group access', 'Require AI access policy review before retrieval or summarization', 'Create or update DLP policy for detected sensitivity types', 'Map asset to Insider Risk review workflow', 'Review inferred sensitivity classification and map to label, DLP, or approval workflow']}`

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
