"""Deterministic 1D damped oscillator/wave-path reference model.

The model is deliberately ordinary mathematics. It is not claimed to be
extracted from Quran 41:53. It supplies a reproducible physical-style signal
for testing the architecture.
"""
from dataclasses import dataclass
import csv, math

@dataclass
class Config:
    seconds: float = 2.0
    dt: float = 0.001
    omega: float = 2.0 * math.pi
    damping: float = 0.35
    u0: float = 1.0
    v0: float = 0.0

def step(u, v, cfg):
    # semi-implicit Euler for u' = v, v' = -omega^2 u - 2*damping*v
    a = -(cfg.omega ** 2) * u - 2.0 * cfg.damping * v
    v1 = v + cfg.dt * a
    u1 = u + cfg.dt * v1
    return u1, v1

def energy(u, v, omega):
    return 0.5 * (v*v + (omega*u)*(omega*u))

def run(cfg=Config(), output=None):
    rows=[]
    u, v = cfg.u0, cfg.v0
    n = int(cfg.seconds / cfg.dt) + 1
    prev_v = v
    for k in range(n):
        t = k * cfg.dt
        V = energy(u, v, cfg.omega)
        if k == 0:
            dV = 0.0
        else:
            dV = (V - rows[-1][3]) / cfg.dt
        rows.append((t, u, v, V, dV))
        u, v = step(u, v, cfg)
    if output:
        with open(output, 'w', newline='') as f:
            w=csv.writer(f)
            w.writerow(['t','u','v','V','dVdt'])
            w.writerows(rows)
    return rows
