"""Optional AI Governance Companion evidence export contract for Phase 8.

This module builds a standalone, one-way export payload that another governance
lab can review without merging repositories or creating a code dependency.
"""

from __future__ import annotations

from typing import Any


EXPORT_CONTRACT_VERSION = "1.0"


def build_export_contract(generated_at: str) -> dict[str, Any]:
    return {
        "contract_name": "securethecloud-dspm-ai-governance-companion-export",
        "contract_version": EXPORT_CONTRACT_VERSION,
        "generated_at": generated_at,
        "source_lab": "securethecloud-dspm-ai-governance-lab",
        "target_context": "optional-ai-governance-companion-evidence",
        "export_type": "one_way_summary",
        "evidence_mode": "synthetic",
        "authority": "advisory_only",
        "repo_merge_required": False,
        "codebase_dependency_required": False,
        "live_tenant_required": False,
    }


def build_companion_findings(
    executive_dashboard: dict[str, Any],
    unified_risk_summary: dict[str, Any],
    observability_summary: dict[str, Any],
    evidence_validation_summary: dict[str, Any],
) -> dict[str, Any]:
    dashboard_summary = executive_dashboard.get("summary", {})
    top_risk_subject = dashboard_summary.get("top_risk_subject") or {}

    return {
        "executive_kpis": {
            "total_kpis": dashboard_summary.get("total_kpis", 0),
            "kpi_severity_counts": dashboard_summary.get("kpi_severity_counts", {}),
        },
        "top_risk_subject": {
            "subject_id": top_risk_subject.get("subject_id"),
            "subject_type": top_risk_subject.get("subject_type"),
            "composite_score": top_risk_subject.get("composite_score"),
            "priority_level": top_risk_subject.get("priority_level"),
            "decision": top_risk_subject.get("decision"),
        },
        "unified_risk": {
            "total_subjects": unified_risk_summary.get("total_subjects", 0),
            "priority_counts": unified_risk_summary.get("priority_counts", {}),
            "decision_counts": unified_risk_summary.get("decision_counts", {}),
        },
        "ai_observability": {
            "total_sessions": observability_summary.get("total_sessions", 0),
            "sensitive_retrieval_sessions": observability_summary.get("sensitive_retrieval_sessions", 0),
            "external_destination_sessions": observability_summary.get("external_destination_sessions", 0),
            "write_or_export_sessions": observability_summary.get("write_or_export_sessions", 0),
        },
        "evidence_health": {
            "artifact_count": evidence_validation_summary.get("artifact_count", 0),
            "audit_chain_events": evidence_validation_summary.get("audit_chain_events", 0),
            "validation_status": evidence_validation_summary.get("validation_status", "unknown"),
        },
    }


def build_export_summary(export_payload: dict[str, Any]) -> dict[str, Any]:
    findings = export_payload["findings"]
    top_risk = findings.get("top_risk_subject", {})
    return {
        "contract_version": export_payload["export_contract"]["contract_version"],
        "export_type": export_payload["export_contract"]["export_type"],
        "authority": export_payload["export_contract"]["authority"],
        "repo_merge_required": export_payload["export_contract"]["repo_merge_required"],
        "codebase_dependency_required": export_payload["export_contract"]["codebase_dependency_required"],
        "top_risk_subject_id": top_risk.get("subject_id"),
        "top_risk_decision": top_risk.get("decision"),
        "total_risk_subjects": findings.get("unified_risk", {}).get("total_subjects", 0),
        "evidence_validation_status": findings.get("evidence_health", {}).get("validation_status", "unknown"),
    }


def build_companion_export(
    executive_dashboard: dict[str, Any],
    unified_risk_summary: dict[str, Any],
    observability_summary: dict[str, Any],
    evidence_validation_summary: dict[str, Any],
    generated_at: str,
) -> dict[str, Any]:
    payload = {
        "export_contract": build_export_contract(generated_at),
        "findings": build_companion_findings(
            executive_dashboard,
            unified_risk_summary,
            observability_summary,
            evidence_validation_summary,
        ),
        "recommended_use": [
            "Review DSPM risk posture in a companion AI governance evidence walkthrough",
            "Map top-risk subjects to AI governance controls and approval policy design",
            "Use as an optional evidence artifact without repository merge or runtime dependency",
        ],
        "boundary": {
            "synthetic_only": True,
            "advisory_only": True,
            "no_repo_merge": True,
            "no_codebase_dependency": True,
            "no_live_tenant": True,
            "no_production_enforcement": True,
        },
    }
    payload["summary"] = build_export_summary(payload)
    return payload
