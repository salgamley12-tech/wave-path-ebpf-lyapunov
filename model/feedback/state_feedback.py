from model.state.state import State
from model.feedback.controller_feedback import Feedback


def apply_feedback(
    state: State,
    feedback: Feedback,
) -> State:
    if not feedback.state_updated:
        return state

    return State(
        bytes_rate=state.bytes_rate,
        syscall_rate=state.syscall_rate,
        connection_rate=state.connection_rate,
        anomaly_score=state.anomaly_score,
    )
