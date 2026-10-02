import json
from pathlib import Path

from model.hypothesis.reference_hypothesis import (
    ReferenceHypothesis,
    from_reference_mapping,
)


ROOT = Path(__file__).resolve().parents[2]

EXPORT = (
    ROOT
    / "wave-path-quran-reference"
    / "integration"
    / "adapter"
    / "reference_export.json"
)


def test_reference_mapping_to_hypothesis():
    with EXPORT.open(encoding="utf-8") as f:
        data = json.load(f)

    mapping = data["mappings"][0]

    hypothesis = from_reference_mapping(mapping)

    assert isinstance(hypothesis, ReferenceHypothesis)
    assert hypothesis.reference_id == "QRF-001"
    assert hypothesis.concept
    assert hypothesis.rule
    assert hypothesis.hypothesis
    assert hypothesis.variables
    assert hypothesis.indicators
