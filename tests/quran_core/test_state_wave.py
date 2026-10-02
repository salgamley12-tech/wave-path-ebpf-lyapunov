from model.state.observation_state import state_from_measurements
from model.wave.damped_wave import Config
from model.wave.state_wave import (
    StateWaveInput,
    state_to_wave_input,
    wave_config_from_state,
)


def test_state_to_wave_input():
    state = state_from_measurements(
        bytes_rate=100.0,
        syscall_rate=20.0,
        connection_rate=5.0,
        anomaly_score=0.25,
    )

    wave_input = state_to_wave_input(state)

    assert isinstance(wave_input, StateWaveInput)
    assert wave_input.u0 == 0.25
    assert wave_input.v0 == 5.0


def test_wave_config_from_state():
    state = state_from_measurements(
        bytes_rate=100.0,
        syscall_rate=20.0,
        connection_rate=5.0,
        anomaly_score=0.25,
    )

    cfg = wave_config_from_state(state)

    assert isinstance(cfg, Config)
    assert cfg.u0 == 0.25
    assert cfg.v0 == 5.0
