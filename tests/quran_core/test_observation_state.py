from model.state.observation_state import state_from_measurements
from model.state.state import State


def test_measurements_to_state():
    state = state_from_measurements(
        bytes_rate=100.0,
        syscall_rate=20.0,
        connection_rate=5.0,
        anomaly_score=0.25,
    )

    assert isinstance(state, State)
    assert state.bytes_rate == 100.0
    assert state.syscall_rate == 20.0
    assert state.connection_rate == 5.0
    assert state.anomaly_score == 0.25
