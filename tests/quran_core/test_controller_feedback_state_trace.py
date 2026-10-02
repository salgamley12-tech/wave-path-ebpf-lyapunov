from model.state.observation_state import state_from_measurements
from model.feedback.controller_feedback import create_feedback
from model.feedback.state_feedback import apply_feedback


def test_controller_feedback_state_trace():
    state0 = state_from_measurements(
        bytes_rate=1.0,
        syscall_rate=1.0,
        connection_rate=0.90,
        anomaly_score=0.1,
    )

    feedback = create_feedback(
        action="MONITOR",
        mode="OBSERVE",
        state_updated=False,
    )

    state1 = apply_feedback(state0, feedback)

    assert feedback.previous_action == "MONITOR"
    assert feedback.observed_mode == "OBSERVE"
    assert feedback.state_updated is False
    assert state1 == state0
