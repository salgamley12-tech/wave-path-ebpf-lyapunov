from model.state.observation_state import state_from_measurements
from model.state.state_update import update_state_from_observation
from model.wave.state_wave import wave_config_from_state
from model.wave.damped_wave import run
from model.wave.lyapunov_bridge import wave_rows_to_lyapunov
from model.risk.lyapunov_risk import assess_lyapunov_risk
from policy.risk_policy import decide_from_risk
from controller.policy_controller import control_from_policy


def test_state_to_controller_trace():
    state0 = state_from_measurements(
        bytes_rate=1.0,
        syscall_rate=1.0,
        connection_rate=0.98,
        anomaly_score=0.1,
    )

    state1 = update_state_from_observation(
        state0,
        connection_rate=0.90,
    )

    wave = run(wave_config_from_state(state1))
    lyapunov = wave_rows_to_lyapunov(wave)

    risk = assess_lyapunov_risk(
        lyapunov[-1].V,
        lyapunov[-1].dVdt,
    )

    policy = decide_from_risk(risk.risk_level)
    controller = control_from_policy(policy.action)

    assert state1.connection_rate == 0.90
    assert lyapunov[-1].V >= 0
    assert risk.stable is True
    assert risk.risk_level == "LOW"
    assert policy.action == "MONITOR"
    assert controller.mode == "OBSERVE"
