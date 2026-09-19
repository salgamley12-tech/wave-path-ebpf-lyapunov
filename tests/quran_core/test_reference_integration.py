import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

EXPORT = (
    ROOT
    / "wave-path-quran-reference"
    / "integration"
    / "adapter"
    / "reference_export.json"
)


def test_reference_export():
    assert EXPORT.exists(), f"Missing reference export: {EXPORT}"

    with EXPORT.open(encoding="utf-8") as f:
        data = json.load(f)

    assert data["interface"] == "wave-path-quran-reference"
    assert data["version"] == "1.0"
    assert isinstance(data["mappings"], list)
    assert len(data["mappings"]) >= 1

    mapping = data["mappings"][0]

    required = [
        "id",
        "reference",
        "concept",
        "rule",
        "hypothesis",
        "variable",
        "indicator",
        "measurement",
        "validation"
    ]

    for field in required:
        assert field in mapping, f"Missing field: {field}"
