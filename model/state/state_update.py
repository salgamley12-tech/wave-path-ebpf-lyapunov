from model.state.state import State


def update_state_from_observation(
    state: State,
    connection_rate: float,
) -> State:
    return State(
        bytes_rate=state.bytes_rate,
        syscall_rate=state.syscall_rate,
        connection_rate=float(connection_rate),
        anomaly_score=state.anomaly_score,
    )
