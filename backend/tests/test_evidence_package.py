from backend.app.evidence_package import build_artifact_index, build_audit_chain, build_evidence_package


def test_artifact_index_is_deterministic_and_hashes_payloads():
    artifacts = {
        "b.json": {"value": 2},
        "a.json": [{"value": 1}],
    }

    first = build_artifact_index(artifacts)
    second = build_artifact_index(artifacts)

    assert first == second
    assert [artifact["artifact_name"] for artifact in first] == ["a.json", "b.json"]
    assert all(len(artifact["sha256"]) == 64 for artifact in first)


def test_audit_chain_links_each_artifact_hash():
    artifact_index = build_artifact_index({"a.json": {"value": 1}, "b.json": {"value": 2}})
    chain = build_audit_chain(artifact_index, "2026-06-30T00:00:00Z")

    assert len(chain) == 2
    assert chain[0]["event_hash"] == chain[1]["previous_hash"]
    assert chain[0]["artifact_sha256"] == artifact_index[0]["sha256"]
    assert chain[1]["artifact_sha256"] == artifact_index[1]["sha256"]


def test_evidence_package_validation_summary_passes():
    package = build_evidence_package(
        {
            "artifact_one.json": {"status": "ok"},
            "artifact_two.json": [{"id": "one"}, {"id": "two"}],
        },
        "2026-06-30T00:00:00Z",
    )

    assert package["package"]["evidence_mode"] == "synthetic"
    assert package["validation_summary"]["validation_status"] == "passed"
    assert package["validation_summary"]["artifact_count"] == 2
    assert len(package["package"]["package_digest"]) == 64
