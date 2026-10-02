from model.state.state import State


REQUIRED_FIELDS = (
    "bytes_rate",
    "syscall_rate",
    "connection_rate",
)


def state_from_measurements(
    bytes_rate: float,
    syscall_rate: float,
    connection_rate: float,
    anomaly_score: float = 0.0,
) -> State:
    return State(
        bytes_rate=float(bytes_rate),
        syscall_rate=float(syscall_rate),
        connection_rate=float(connection_rate),
        anomaly_score=float(anomaly_score),
    )
