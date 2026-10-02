from dataclasses import dataclass

@dataclass(frozen=True)
class State:
    bytes_rate: float
    syscall_rate: float
    connection_rate: float
    anomaly_score: float = 0.0

def normalize(x: State, baseline: State, eps=1e-12) -> State:
    return State(
        x.bytes_rate / max(abs(baseline.bytes_rate), eps),
        x.syscall_rate / max(abs(baseline.syscall_rate), eps),
        x.connection_rate / max(abs(baseline.connection_rate), eps),
        x.anomaly_score,
    )

def distance(a: State, b: State) -> float:
    vals=((a.bytes_rate-b.bytes_rate),(a.syscall_rate-b.syscall_rate),(a.connection_rate-b.connection_rate),(a.anomaly_score-b.anomaly_score))
    return sum(v*v for v in vals) ** 0.5
