"""Evidence package and audit-chain utilities for Phase 6.

The package model creates deterministic metadata for synthetic evidence artifacts
and links those records with hashes so reviewers can verify evidence consistency.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_payload(payload: Any) -> str:
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def payload_record_count(payload: Any) -> int | None:
    if isinstance(payload, list):
        return len(payload)
    if isinstance(payload, dict):
        if "results" in payload and isinstance(payload["results"], list):
            return len(payload["results"])
        if "summary" in payload and isinstance(payload["summary"], dict):
            return len(payload["summary"])
        return len(payload)
    return None


def payload_type(payload: Any) -> str:
    if isinstance(payload, list):
        return "list"
    if isinstance(payload, dict):
        return "object"
    return type(payload).__name__


def build_artifact_index(artifacts: dict[str, Any]) -> list[dict[str, Any]]:
    artifact_index = []
    for artifact_name in sorted(artifacts):
        payload = artifacts[artifact_name]
        canonical = canonical_json(payload)
        artifact_index.append(
            {
                "artifact_name": artifact_name,
                "content_type": "application/json" if artifact_name.endswith(".json") else "text/markdown",
                "payload_type": payload_type(payload),
                "record_count": payload_record_count(payload),
                "byte_size": len(canonical.encode("utf-8")),
                "sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
                "authority": "advisory_only",
            }
        )
    return artifact_index


def build_audit_chain(artifact_index: list[dict[str, Any]], generated_at: str) -> list[dict[str, Any]]:
    chain: list[dict[str, Any]] = []
    previous_hash = hashlib.sha256(f"GENESIS:{generated_at}".encode("utf-8")).hexdigest()

    for sequence, artifact in enumerate(artifact_index, start=1):
        event = {
            "sequence": sequence,
            "event_type": "artifact_registered",
            "artifact_name": artifact["artifact_name"],
            "artifact_sha256": artifact["sha256"],
            "previous_hash": previous_hash,
            "generated_at": generated_at,
            "authority": "advisory_only",
        }
        event_hash = sha256_payload(event)
        chain_entry = {**event, "event_hash": event_hash}
        chain.append(chain_entry)
        previous_hash = event_hash

    return chain


def build_validation_summary(
    artifact_index: list[dict[str, Any]],
    audit_chain: list[dict[str, Any]],
) -> dict[str, Any]:
    unique_hashes = {artifact["sha256"] for artifact in artifact_index}
    chain_complete = len(audit_chain) == len(artifact_index)
    chain_hashes_present = all(entry.get("event_hash") and entry.get("previous_hash") for entry in audit_chain)

    return {
        "artifact_count": len(artifact_index),
        "unique_artifact_hashes": len(unique_hashes),
        "audit_chain_events": len(audit_chain),
        "audit_chain_complete": chain_complete,
        "audit_chain_hashes_present": chain_hashes_present,
        "validation_status": "passed" if chain_complete and chain_hashes_present else "failed",
        "authority": "advisory_only",
    }


def build_evidence_package(artifacts: dict[str, Any], generated_at: str) -> dict[str, Any]:
    artifact_index = build_artifact_index(artifacts)
    audit_chain = build_audit_chain(artifact_index, generated_at)
    validation_summary = build_validation_summary(artifact_index, audit_chain)
    package_digest = sha256_payload(
        {
            "artifact_index": artifact_index,
            "audit_chain": audit_chain,
            "generated_at": generated_at,
        }
    )

    return {
        "package": {
            "lab": "securethecloud-dspm-ai-governance-lab",
            "generated_at": generated_at,
            "evidence_mode": "synthetic",
            "authority": "advisory_only",
            "package_digest": package_digest,
        },
        "artifact_index": artifact_index,
        "audit_chain": audit_chain,
        "validation_summary": validation_summary,
    }
