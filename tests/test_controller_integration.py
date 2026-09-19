from controller.controller import Controller
from policy.policy import Action


def test_controller_exposes_integrated_policy_and_control():
    c = Controller()

    risk, action = c.process(
        t=0.0,
        state=(1, 2),
        V=3.0,
        dVdt=1.0,
        anomaly_score=0.1,
        authorized=True,
    )

    assert risk.value == "high"
    assert action == Action.DROP

    assert c.last_policy_decision.risk_level == "HIGH"
    assert c.last_policy_decision.action == "MITIGATE"

    assert c.last_control_command.action == "MITIGATE"
    assert c.last_control_command.mode == "SAFE_RESPONSE"


def test_controller_preserves_policy_intent_when_unauthorized():
    c = Controller()

    risk, action = c.process(
        t=1.0,
        state=(1, 2),
        V=3.0,
        dVdt=0.0,
        anomaly_score=0.9,
        authorized=False,
    )

    assert risk.value == "high"
    assert action == Action.OBSERVE_ONLY

    assert c.last_policy_decision.risk_level == "HIGH"
    assert c.last_policy_decision.action == "MITIGATE"

    assert c.last_control_command.action == "MITIGATE"
    assert c.last_control_command.mode == "SAFE_RESPONSE"
