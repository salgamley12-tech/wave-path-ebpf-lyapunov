from model.state.observation_state import state_from_measurements
from model.state.state_update import update_state_from_observation
from model.wave.state_wave import wave_config_from_state
from model.wave.damped_wave import run
from model.wave.lyapunov_bridge import wave_rows_to_lyapunov


def test_state_update_propagates_to_wave_and_lyapunov():
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

    wave0 = run(wave_config_from_state(state0))
    wave1 = run(wave_config_from_state(state1))

    lyap0 = wave_rows_to_lyapunov(wave0)
    lyap1 = wave_rows_to_lyapunov(wave1)

    assert state1.connection_rate == 0.90
    assert state1.connection_rate != state0.connection_rate

    assert wave0[0][3] != wave1[0][3]

    assert lyap0[-1].dVdt <= 0
    assert lyap1[-1].dVdt <= 0

    assert lyap1[-1].V != lyap0[-1].V
