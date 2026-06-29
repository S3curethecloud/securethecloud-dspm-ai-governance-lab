"""Typed models for the synthetic DSPM AI governance lab."""

from typing import Any, Literal

from pydantic import BaseModel, Field

RiskLevel = Literal["low", "medium", "high", "critical"]
Decision = Literal["allow", "redact", "approval_required", "deny"]


class DataAsset(BaseModel):
    asset_id: str
    name: str
    location: str
    owner: str
    business_domain: str
    sensitivity_label: str
    sensitivity_types: list[str] = Field(default_factory=list)
    shared_with: list[str] = Field(default_factory=list)
    external_sharing: bool = False
    dlp_policy_present: bool = False
    insider_risk_policy_present: bool = False
    ai_access_allowed: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class AIInteraction(BaseModel):
    event_id: str
    timestamp: str
    user: str
    department: str
    ai_app: str
    prompt_category: str
    retrieved_assets: list[str] = Field(default_factory=list)
    sensitive_data_detected: bool = False
    destination: str = "internal"
    action: str = "summarize"


class RiskResult(BaseModel):
    subject_id: str
    score: int
    risk_level: RiskLevel
    decision: Decision
    reasons: list[str]
    recommendations: list[str]
