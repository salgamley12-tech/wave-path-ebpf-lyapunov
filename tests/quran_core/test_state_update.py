from model.state.observation_state import state_from_measurements
from model.state.state_update import update_state_from_observation


def test_state_update_from_observation():
    state0 = state_from_measurements(
        bytes_rate=1.0,
        syscall_rate=1.0,
        connection_rate=0.98,
        anomaly_score=0.1,
    )

    state1 = update_state_from_observation(
        state0,
        connection_rate=0.90,
    )

    assert state1.bytes_rate == state0.bytes_rate
    assert state1.syscall_rate == state0.syscall_rate
    assert state1.anomaly_score == state0.anomaly_score
    assert state1.connection_rate == 0.90
    assert state1.connection_rate != state0.connection_rate
