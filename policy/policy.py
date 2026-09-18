from enum import Enum
from dataclasses import dataclass
from ai.risk import Risk

class Action(str, Enum):
    OBSERVE_ONLY='observe_only'
    PASS='pass'
    DROP='drop'

@dataclass(frozen=True)
class Policy:
    version: str='1.0'
    enforce_high_risk: bool=True
    fail_closed: bool=False

def guard(risk: Risk, authorized: bool, policy: Policy=Policy()) -> Action:
    if not authorized:
        return Action.OBSERVE_ONLY
    if risk is Risk.HIGH and policy.enforce_high_risk:
        return Action.DROP
    return Action.PASS
