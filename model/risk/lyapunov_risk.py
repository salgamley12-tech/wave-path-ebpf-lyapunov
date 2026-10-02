from dataclasses import dataclass


@dataclass(frozen=True)
class RiskResult:
    lyapunov_value: float
    dVdt: float
    stable: bool
    risk_level: str


def assess_lyapunov_risk(
    lyapunov_value: float,
    dVdt: float,
    tolerance: float = 0.0,
) -> RiskResult:
    V = float(lyapunov_value)
    dV = float(dVdt)

    if V < 0:
        raise ValueError("Lyapunov value must be non-negative")

    stable = dV <= tolerance

    if dV <= tolerance:
        risk_level = "LOW"
    elif dV <= abs(V) * 0.05:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    return RiskResult(
        lyapunov_value=V,
        dVdt=dV,
        stable=stable,
        risk_level=risk_level,
    )
