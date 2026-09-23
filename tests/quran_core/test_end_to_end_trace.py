from quran_core.reference.adapter.load_reference import (
    load_reference,
    validate_reference,
)
from model.hypothesis.reference_hypothesis import from_reference_mapping
from model.observation.reference_observation import define_observation
from model.observation.reference_observation_runner import run_observation
from model.state.observation_state import state_from_measurements
from model.wave.state_wave import wave_config_from_state
from model.wave.damped_wave import run
from model.wave.lyapunov_bridge import wave_rows_to_lyapunov
from model.risk.lyapunov_risk import assess_lyapunov_risk
from policy.risk_policy import decide_from_risk
from controller.policy_controller import control_from_policy
from model.feedback.controller_feedback import create_feedback


def test_end_to_end_trace():
    reference = load_reference()
    validate_reference(reference)

    mapping = reference["mappings"][0]
    hypothesis = from_reference_mapping(mapping)

    definition = define_observation(
        hypothesis,
        mapping["measurement"]["method"],
    )

    signal = [
        (0.0, 1.0),
        (0.001, 0.99),
        (0.002, 0.98),
    ]

    observations = run_observation(definition, signal)

    state = state_from_measurements(
        bytes_rate=1.0,
        syscall_rate=1.0,
        connection_rate=observations[-1].value,
        anomaly_score=0.1,
    )

    wave_config = wave_config_from_state(state)
    wave_rows = run(wave_config)

    lyapunov = wave_rows_to_lyapunov(wave_rows)

    risk = assess_lyapunov_risk(
        lyapunov[-1].V,
        lyapunov[-1].dVdt,
    )

    policy = decide_from_risk(risk.risk_level)
    controller = control_from_policy(policy.action)
    feedback = create_feedback(
        controller.action,
        controller.mode,
        state_updated=False,
    )

    assert mapping["id"] == "QRF-001"
    assert len(observations) == 3
    assert len(wave_rows) == 2001
    assert lyapunov[-1].dVdt <= 0
    assert risk.stable is True
    assert risk.risk_level == "LOW"
    assert policy.action == "MONITOR"
    assert controller.mode == "OBSERVE"
    assert feedback.previous_action == "MONITOR"
    assert feedback.observed_mode == "OBSERVE"
    assert feedback.state_updated is False
