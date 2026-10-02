from ai.risk import classify
from policy.policy import guard, Action
from policy.risk_policy import decide_from_risk
from controller.policy_controller import control_from_policy


def test_high_risk_policy_and_guard_are_both_visible():
    risk = classify(
        dVdt=1.0,
        anomaly_score=0.1,
    )

    decision = decide_from_risk(risk.value)
    command = control_from_policy(decision.action)
    action = guard(risk, authorized=True)

    assert risk.value == "high"

    assert decision.action == "MITIGATE"
    assert command.mode == "SAFE_RESPONSE"

    assert action == Action.DROP


def test_unauthorized_high_risk_preserves_safe_control_intent():
    risk = classify(
        dVdt=0.0,
        anomaly_score=0.9,
    )

    decision = decide_from_risk(risk.value)
    command = control_from_policy(decision.action)
    action = guard(risk, authorized=False)

    assert risk.value == "high"

    assert decision.action == "MITIGATE"
    assert command.mode == "SAFE_RESPONSE"

    assert action == Action.OBSERVE_ONLY
