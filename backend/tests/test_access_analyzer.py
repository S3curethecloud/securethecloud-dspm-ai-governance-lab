from backend.app.access_analyzer import analyze_access_exposure, analyze_permission


ASSET = {
    "asset_id": "hr-payroll-001",
    "name": "Executive Payroll Adjustments",
    "sensitivity_label": "highly_confidential",
    "sensitivity_types": ["pii", "payroll", "financial"],
}

IDENTITIES = [
    {
        "identity_id": "user-platform-admin-001",
        "display_name": "Synthetic Platform Admin",
        "risk_tier": "high",
        "privileged": True,
        "external": False,
    }
]

GROUPS = [
    {
        "group_id": "group-all-employees",
        "display_name": "All Employees",
        "is_broad": True,
        "is_external": False,
        "privileged": False,
        "members": ["user-platform-admin-001"],
    },
    {
        "group_id": "group-external-partners",
        "display_name": "External Partners",
        "is_broad": False,
        "is_external": True,
        "privileged": False,
        "members": [],
    },
]


def test_broad_group_ai_access_to_sensitive_asset_is_critical():
    permission = {
        "permission_id": "perm-test-001",
        "asset_id": "hr-payroll-001",
        "principal_id": "group-all-employees",
        "principal_type": "group",
        "access_level": "read",
        "roles": ["viewer"],
        "inherited": True,
        "external": False,
        "ai_tool_access_allowed": True,
        "source": "test",
    }

    result = analyze_permission(
        ASSET,
        permission,
        {identity["identity_id"]: identity for identity in IDENTITIES},
        {group["group_id"]: group for group in GROUPS},
    )

    assert result["exposure_level"] == "critical"
    assert result["decision"] == "deny"
    assert result["principal"]["is_broad"] is True


def test_external_write_access_requires_approval():
    permission = {
        "permission_id": "perm-test-002",
        "asset_id": "hr-payroll-001",
        "principal_id": "group-external-partners",
        "principal_type": "group",
        "access_level": "edit",
        "roles": ["editor"],
        "inherited": False,
        "external": True,
        "ai_tool_access_allowed": False,
        "source": "test",
    }

    result = analyze_permission(
        ASSET,
        permission,
        {identity["identity_id"]: identity for identity in IDENTITIES},
        {group["group_id"]: group for group in GROUPS},
    )

    assert result["exposure_level"] in {"high", "critical"}
    assert result["decision"] in {"approval_required", "deny"}
    assert result["principal"]["external"] is True


def test_access_exposure_summary_counts_broad_external_and_ai_access():
    permissions = [
        {
            "permission_id": "perm-test-001",
            "asset_id": "hr-payroll-001",
            "principal_id": "group-all-employees",
            "principal_type": "group",
            "access_level": "read",
            "roles": ["viewer"],
            "inherited": True,
            "external": False,
            "ai_tool_access_allowed": True,
            "source": "test",
        },
        {
            "permission_id": "perm-test-002",
            "asset_id": "hr-payroll-001",
            "principal_id": "group-external-partners",
            "principal_type": "group",
            "access_level": "edit",
            "roles": ["editor"],
            "inherited": False,
            "external": True,
            "ai_tool_access_allowed": False,
            "source": "test",
        },
    ]

    exposure = analyze_access_exposure([ASSET], permissions, IDENTITIES, GROUPS)

    assert exposure["summary"]["total_permissions"] == 2
    assert exposure["summary"]["broad_group_exposures"] == 1
    assert exposure["summary"]["external_exposures"] == 1
    assert exposure["summary"]["ai_access_exposures"] == 1
