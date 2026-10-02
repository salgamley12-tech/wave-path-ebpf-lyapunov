from dataclasses import dataclass


@dataclass(frozen=True)
class Feedback:
    previous_action: str
    observed_mode: str
    state_updated: bool


def create_feedback(action: str, mode: str, state_updated: bool) -> Feedback:
    if not action.strip():
        raise ValueError("action is required")

    if not mode.strip():
        raise ValueError("mode is required")

    return Feedback(
        previous_action=action.upper(),
        observed_mode=mode.upper(),
        state_updated=bool(state_updated),
    )
