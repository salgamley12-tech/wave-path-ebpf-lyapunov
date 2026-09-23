from dataclasses import dataclass


@dataclass(frozen=True)
class ControlCommand:
    action: str
    mode: str


def control_from_policy(action: str) -> ControlCommand:
    action = action.upper()

    modes = {
        "MONITOR": "OBSERVE",
        "INVESTIGATE": "ANALYZE",
        "MITIGATE": "SAFE_RESPONSE",
    }

    if action not in modes:
        raise ValueError(f"unknown policy action: {action}")

    return ControlCommand(
        action=action,
        mode=modes[action],
    )
