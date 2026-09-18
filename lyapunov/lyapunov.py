from dataclasses import dataclass

@dataclass(frozen=True)
class LyapunovResult:
    V: float
    dVdt: float

def oscillator_energy(u: float, v: float, omega: float) -> float:
    return 0.5 * (v*v + (omega*u)*(omega*u))

def finite_difference(prev_v: float, current_v: float, dt: float) -> float:
    if dt <= 0: raise ValueError('dt must be positive')
    return (current_v - prev_v)/dt
