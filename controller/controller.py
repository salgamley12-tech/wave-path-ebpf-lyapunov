from dataclasses import dataclass
from ai.risk import classify
from policy.policy import guard, Policy, Action
from wave_path.path import WavePath, PathPoint

@dataclass
class Controller:
    policy: Policy = Policy()
    path: WavePath = None
    def __post_init__(self):
        if self.path is None: self.path = WavePath()
    def process(self, t, state, V, dVdt, anomaly_score, authorized=True):
        risk=classify(dVdt, anomaly_score)
        action=guard(risk, authorized, self.policy)
        self.path.append(PathPoint(t, tuple(state), V, dVdt, risk.value, action.value))
        return risk, action
