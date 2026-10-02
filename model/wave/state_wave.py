from dataclasses import dataclass

from model.state.state import State
from model.wave.damped_wave import Config


@dataclass(frozen=True)
class StateWaveInput:
    u0: float
    v0: float


def state_to_wave_input(state: State) -> StateWaveInput:
    return StateWaveInput(
        u0=float(state.anomaly_score),
        v0=float(state.connection_rate),
    )


def wave_config_from_state(
    state: State,
    base_config: Config | None = None,
) -> Config:
    cfg = base_config or Config()
    wave_input = state_to_wave_input(state)

    return Config(
        seconds=cfg.seconds,
        dt=cfg.dt,
        omega=cfg.omega,
        damping=cfg.damping,
        u0=wave_input.u0,
        v0=wave_input.v0,
    )
