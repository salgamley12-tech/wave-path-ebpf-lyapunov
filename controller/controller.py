from dataclasses import dataclass

from ai.risk import classify
from policy.policy import guard, Policy
from policy.risk_policy import decide_from_risk, PolicyDecision
from controller.policy_controller import control_from_policy, ControlCommand
from wave_path.path import WavePath, PathPoint


@dataclass
class Controller:
    policy: Policy = Policy()
    path: WavePath = None
    last_policy_decision: PolicyDecision = None
    last_control_command: ControlCommand = None

    def __post_init__(self):
        if self.path is None:
            self.path = WavePath()

    def process(
        self,
        t,
        state,
        V,
        dVdt,
        anomaly_score,
        authorized=True,
    ):
        risk = classify(dVdt, anomaly_score)

        # Analytical policy decision
        self.last_policy_decision = decide_from_risk(risk.value)

        # Operational control command
        self.last_control_command = control_from_policy(
            self.last_policy_decision.action
        )

        # Enforcement / authorization guard
        action = guard(risk, authorized, self.policy)

        # Preserve the existing WavePath contract
        self.path.append(
            PathPoint(
                t,
                tuple(state),
                V,
                dVdt,
                risk.value,
                action.value,
            )
        )

        # Preserve the original Controller API
        return risk, action
