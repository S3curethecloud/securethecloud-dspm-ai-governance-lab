"""Synthetic sensitive-data classifier for Phase 2.

The classifier is deterministic and pattern-based by design. It is meant to
represent DSPM classification logic without using real tenant data or external
services.
"""

from __future__ import annotations

import re
from collections import Counter
from typing import Any

LABEL_RANK = {
    "public": 0,
    "internal": 1,
    "confidential": 2,
    "highly_confidential": 3,
    "regulated": 4,
}

RANK_LABEL = {value: key for key, value in LABEL_RANK.items()}


def infer_label(matched_patterns: list[dict[str, Any]]) -> str:
    if not matched_patterns:
        return "public"
    highest_rank = max(LABEL_RANK.get(pattern.get("inferred_label", "internal"), 1) for pattern in matched_patterns)
    return RANK_LABEL[highest_rank]


def classification_decision(score: int, label: str, detected_types: list[str]) -> str:
    if "credential" in detected_types or label == "regulated" or score >= 80:
        return "approval_required"
    if score >= 50:
        return "dlp_recommended"
    if score >= 20:
        return "label_required"
    return "monitor"


def classify_document(document: dict[str, Any], patterns: list[dict[str, Any]]) -> dict[str, Any]:
    content = str(document.get("content", ""))
    matched_patterns: list[dict[str, Any]] = []

    for pattern in patterns:
        flags = 0 if pattern.get("case_sensitive") else re.IGNORECASE
        matches = re.findall(pattern["regex"], content, flags=flags)
        if not matches:
            continue
        matched_patterns.append(
            {
                "pattern_id": pattern["pattern_id"],
                "name": pattern["name"],
                "sensitivity_type": pattern["sensitivity_type"],
                "inferred_label": pattern["inferred_label"],
                "match_count": len(matches),
                "risk_points": int(pattern.get("risk_points", 0)),
                "confidence": float(pattern.get("confidence", 0.5)),
            }
        )

    detected_types = sorted({pattern["sensitivity_type"] for pattern in matched_patterns})
    inferred = infer_label(matched_patterns)
    score = min(sum(pattern["risk_points"] * pattern["match_count"] for pattern in matched_patterns), 100)
    average_confidence = 0.0
    if matched_patterns:
        average_confidence = round(
            sum(pattern["confidence"] for pattern in matched_patterns) / len(matched_patterns), 3
        )

    return {
        "asset_id": document["asset_id"],
        "classification_score": score,
        "inferred_label": inferred,
        "detected_types": detected_types,
        "matched_patterns": matched_patterns,
        "confidence": average_confidence,
        "decision": classification_decision(score, inferred, detected_types),
        "authority": "advisory_only",
    }


def classify_documents(documents: list[dict[str, Any]], patterns: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [classify_document(document, patterns) for document in documents]


def summarize_classification_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    label_counts = Counter(result["inferred_label"] for result in results)
    type_counts: Counter[str] = Counter()
    decision_counts = Counter(result["decision"] for result in results)

    for result in results:
        type_counts.update(result.get("detected_types", []))

    high_priority = [
        result
        for result in results
        if result["decision"] in {"approval_required", "dlp_recommended"}
    ]

    return {
        "total_documents": len(results),
        "label_counts": dict(label_counts),
        "type_counts": dict(type_counts),
        "decision_counts": dict(decision_counts),
        "high_priority_assets": sorted(
            high_priority,
            key=lambda item: item["classification_score"],
            reverse=True,
        ),
        "authority": "advisory_only",
    }
