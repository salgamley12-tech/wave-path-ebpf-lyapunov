from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ReferenceHypothesis:
    reference_id: str
    concept: str
    rule: str
    hypothesis: str
    variables: List[str]
    indicators: List[str]


def from_reference_mapping(mapping: dict) -> ReferenceHypothesis:
    required = [
        "id",
        "concept",
        "rule",
        "hypothesis",
        "variable",
        "indicator",
    ]

    for field in required:
        if field not in mapping:
            raise ValueError(f"missing reference field: {field}")

    variables = [
        item["name"]
        for item in mapping["variable"]
        if "name" in item
    ]

    return ReferenceHypothesis(
        reference_id=mapping["id"],
        concept=mapping["concept"],
        rule=mapping["rule"],
        hypothesis=mapping["hypothesis"],
        variables=variables,
        indicators=list(mapping["indicator"]),
    )
