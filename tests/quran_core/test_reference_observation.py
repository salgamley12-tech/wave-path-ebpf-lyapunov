from model.hypothesis.reference_hypothesis import ReferenceHypothesis
from model.observation.reference_observation import (
    ObservationDefinition,
    define_observation,
)


def test_hypothesis_to_observation_definition():
    hypothesis = ReferenceHypothesis(
        reference_id="QRF-001",
        concept="Human responsibility and stewardship",
        rule="Actions should be evaluated in relation to responsibility and consequences.",
        hypothesis="Explicit representation can improve decision traceability.",
        variables=[
            "responsibility_level",
            "system_state",
            "decision_consequence",
        ],
        indicators=[
            "responsibility_score",
            "state_deviation",
            "decision_traceability",
        ],
    )

    definition = define_observation(
        hypothesis,
        "Defined project metrics from observed system data",
    )

    assert isinstance(definition, ObservationDefinition)
    assert definition.reference_id == "QRF-001"
    assert definition.variables == hypothesis.variables
    assert definition.indicators == hypothesis.indicators
    assert definition.measurement_method
