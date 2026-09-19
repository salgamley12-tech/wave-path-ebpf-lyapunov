from dataclasses import dataclass


@dataclass(frozen=True)
class PolicyDecision:
    risk_level: str
    action: str


def decide_from_risk(risk_level: str) -> PolicyDecision:
    level = risk_level.upper()

    actions = {
        "LOW": "MONITOR",
        "MEDIUM": "INVESTIGATE",
        "HIGH": "MITIGATE",
    }

    if level not in actions:
        raise ValueError(f"unknown risk level: {risk_level}")

    return PolicyDecision(
        risk_level=level,
        action=actions[level],
    )
