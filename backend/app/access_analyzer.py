"""Synthetic access exposure analyzer for Phase 3.

The analyzer evaluates who can access synthetic assets and whether that access
creates data exposure before AI retrieval or summarization.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

SENSITIVE_LABELS = {"confidential", "highly_confidential", "regulated"}
HIGH_RISK_TYPES = {"pii", "phi", "pci", "payroll", "legal", "credential", "customer_record", "financial"}
PRIVILEGED_ACCESS_LEVELS = {"owner", "admin", "edit", "write"}
PRIVILEGED_ROLES = {"owner", "admin", "editor", "contributor"}
BROAD_GROUP_IDS = {"group-all-employees", "group-domain-users", "everyone", "company_all", "domain_users"}


def index_by(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {item[key]: item for item in items}


def asset_is_sensitive(asset: dict[str, Any]) -> bool:
    label = asset.get("sensitivity_label", "public")
    sensitivity_types = set(asset.get("sensitivity_types", []))
    return label in SENSITIVE_LABELS or bool(sensitivity_types & HIGH_RISK_TYPES)


def resolve_principal(
    permission: dict[str, Any],
    identities_by_id: dict[str, dict[str, Any]],
    groups_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    principal_id = permission["principal_id"]
    principal_type = permission["principal_type"]

    if principal_type == "group":
        group = groups_by_id.get(principal_id, {})
        return {
            "principal_id": principal_id,
            "principal_type": "group",
            "display_name": group.get("display_name", principal_id),
            "is_broad": bool(group.get("is_broad", principal_id in BROAD_GROUP_IDS)),
            "external": bool(group.get("is_external", permission.get("external", False))),
            "privileged": bool(group.get("privileged", False)),
            "member_count": len(group.get("members", [])),
        }

    identity = identities_by_id.get(principal_id, {})
    return {
        "principal_id": principal_id,
        "principal_type": principal_type,
        "display_name": identity.get("display_name", principal_id),
        "is_broad": False,
        "external": bool(identity.get("external", permission.get("external", False))),
        "privileged": bool(identity.get("privileged", False)),
        "risk_tier": identity.get("risk_tier", "unknown"),
        "department": identity.get("department", "unknown"),
    }


def exposure_level(score: int) -> str:
    if score >= 90:
        return "critical"
    if score >= 65:
        return "high"
    if score >= 35:
        return "medium"
    return "low"


def exposure_decision(score: int) -> str:
    if score >= 90:
        return "deny"
    if score >= 65:
        return "approval_required"
    if score >= 35:
        return "access_review"
    return "monitor"


def analyze_permission(
    asset: dict[str, Any],
    permission: dict[str, Any],
    identities_by_id: dict[str, dict[str, Any]],
    groups_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    principal = resolve_principal(permission, identities_by_id, groups_by_id)
    score = 0
    reasons: list[str] = ["access permission observed"]
    recommendations: list[str] = []
    sensitive_asset = asset_is_sensitive(asset)

    if sensitive_asset:
        score += 20
        reasons.append("asset is sensitive or contains high-risk data types")

    if principal.get("is_broad"):
        score += 30
        reasons.append("principal is a broad access group")
        recommendations.append("Remove broad group access and replace with least-privilege group access")

    if principal.get("external") or permission.get("external"):
        score += 35
        reasons.append("access includes external or guest principal")
        recommendations.append("Require external sharing approval and expiration review")

    access_level = permission.get("access_level", "read")
    roles = set(permission.get("roles", []))
    if access_level in PRIVILEGED_ACCESS_LEVELS or roles & PRIVILEGED_ROLES:
        score += 25
        reasons.append("permission grants privileged or write-capable access")
        recommendations.append("Downgrade privileged access unless explicit owner approval exists")

    if permission.get("inherited"):
        score += 10
        reasons.append("permission is inherited and may be difficult to govern directly")
        recommendations.append("Review inheritance path and break inheritance for sensitive assets when needed")

    if permission.get("ai_tool_access_allowed") and sensitive_asset:
        score += 20
        reasons.append("AI tool access is allowed for a sensitive asset")
        recommendations.append("Require AI access approval before retrieval or summarization")

    if principal.get("is_broad") and permission.get("ai_tool_access_allowed") and sensitive_asset:
        score += 10
        reasons.append("broad access and AI access combine on a sensitive asset")
        recommendations.append("Block AI retrieval until broad access is remediated")

    if principal.get("privileged") and sensitive_asset:
        score += 15
        reasons.append("principal has privileged identity characteristics")
        recommendations.append("Require privileged access review for sensitive data access")

    if principal.get("risk_tier") == "high" and sensitive_asset:
        score += 10
        reasons.append("principal risk tier is high")
        recommendations.append("Require high-risk principal review before data access is retained")

    score = min(score, 100)

    return {
        "permission_id": permission["permission_id"],
        "asset_id": asset["asset_id"],
        "asset_name": asset.get("name", asset["asset_id"]),
        "principal": principal,
        "access_level": access_level,
        "roles": permission.get("roles", []),
        "source": permission.get("source", "unknown"),
        "inherited": bool(permission.get("inherited", False)),
        "ai_tool_access_allowed": bool(permission.get("ai_tool_access_allowed", False)),
        "score": score,
        "exposure_level": exposure_level(score),
        "decision": exposure_decision(score),
        "reasons": reasons,
        "recommendations": recommendations,
        "authority": "advisory_only",
    }


def analyze_access_exposure(
    assets: list[dict[str, Any]],
    permissions: list[dict[str, Any]],
    identities: list[dict[str, Any]],
    groups: list[dict[str, Any]],
) -> dict[str, Any]:
    assets_by_id = index_by(assets, "asset_id")
    identities_by_id = index_by(identities, "identity_id")
    groups_by_id = index_by(groups, "group_id")

    results = [
        analyze_permission(assets_by_id[permission["asset_id"]], permission, identities_by_id, groups_by_id)
        for permission in permissions
        if permission["asset_id"] in assets_by_id
    ]

    level_counts = Counter(result["exposure_level"] for result in results)
    decision_counts = Counter(result["decision"] for result in results)
    external_count = sum(1 for result in results if result["principal"].get("external"))
    broad_count = sum(1 for result in results if result["principal"].get("is_broad"))
    ai_access_count = sum(1 for result in results if result.get("ai_tool_access_allowed"))

    return {
        "summary": {
            "total_permissions": len(results),
            "level_counts": dict(level_counts),
            "decision_counts": dict(decision_counts),
            "external_exposures": external_count,
            "broad_group_exposures": broad_count,
            "ai_access_exposures": ai_access_count,
            "authority": "advisory_only",
        },
        "results": sorted(results, key=lambda result: result["score"], reverse=True),
    }
