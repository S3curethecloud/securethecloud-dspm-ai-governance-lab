from backend.app.classifier import classify_document, classify_documents, summarize_classification_results


PATTERNS = [
    {
        "pattern_id": "PAT-PII-SSN-001",
        "name": "Synthetic SSN token",
        "sensitivity_type": "pii",
        "inferred_label": "regulated",
        "regex": "SYNTHETIC-SSN-[0-9]{3}-[0-9]{2}-[0-9]{4}",
        "risk_points": 35,
        "confidence": 0.95,
    },
    {
        "pattern_id": "PAT-CREDENTIAL-001",
        "name": "Synthetic API key token",
        "sensitivity_type": "credential",
        "inferred_label": "highly_confidential",
        "regex": "SYNTHETIC-API-KEY-[A-Z0-9]{8,32}",
        "risk_points": 40,
        "confidence": 0.98,
    },
]


def test_classifier_detects_regulated_pii():
    result = classify_document(
        {
            "asset_id": "synthetic-pii-001",
            "content": "Synthetic row contains SYNTHETIC-SSN-123-45-6789 for test classification.",
        },
        PATTERNS,
    )

    assert result["asset_id"] == "synthetic-pii-001"
    assert result["inferred_label"] == "regulated"
    assert "pii" in result["detected_types"]
    assert result["decision"] == "approval_required"


def test_classifier_detects_credential_like_content():
    result = classify_document(
        {
            "asset_id": "synthetic-secret-001",
            "content": "Runbook contains SYNTHETIC-API-KEY-ABCDEFGH12345678 for lab testing.",
        },
        PATTERNS,
    )

    assert result["inferred_label"] == "highly_confidential"
    assert "credential" in result["detected_types"]
    assert result["decision"] == "approval_required"


def test_classification_summary_counts_labels_and_types():
    results = classify_documents(
        [
            {
                "asset_id": "synthetic-pii-001",
                "content": "Synthetic row contains SYNTHETIC-SSN-123-45-6789.",
            },
            {
                "asset_id": "public-001",
                "content": "Public onboarding content with no sensitive marker.",
            },
        ],
        PATTERNS,
    )

    summary = summarize_classification_results(results)

    assert summary["total_documents"] == 2
    assert summary["label_counts"]["regulated"] == 1
    assert summary["label_counts"]["public"] == 1
    assert summary["type_counts"]["pii"] == 1
