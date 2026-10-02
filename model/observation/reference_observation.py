from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ObservationDefinition:
    reference_id: str
    hypothesis: str
    variables: List[str]
    indicators: List[str]
    measurement_method: str


def define_observation(hypothesis, measurement_method: str):
    if not measurement_method.strip():
        raise ValueError("measurement_method is required")

    return ObservationDefinition(
        reference_id=hypothesis.reference_id,
        hypothesis=hypothesis.hypothesis,
        variables=list(hypothesis.variables),
        indicators=list(hypothesis.indicators),
        measurement_method=measurement_method,
    )
