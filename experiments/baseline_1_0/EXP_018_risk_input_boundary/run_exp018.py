from ai.risk import classify
from model.risk.lyapunov_risk import assess_lyapunov_risk

CASES = [
    ("LOW_ANOMALY", 1.0, -0.10, 0.10),
    ("HIGH_ANOMALY", 1.0, -0.10, 0.90),
    ("POSITIVE_DVDT_LOW_ANOMALY", 1.0, 0.02, 0.10),
    ("POSITIVE_DVDT_HIGH_ANOMALY", 1.0, 0.02, 0.90),
]

def main():
    print("EXP-018 Risk Input Boundary Comparison")
    print()

    for name, V, dVdt, anomaly_score in CASES:
        legacy = classify(dVdt, anomaly_score).value
        current = assess_lyapunov_risk(V, dVdt).risk_level

        print(
            f"{name}: "
            f"legacy={legacy} "
            f"current={current} "
            f"anomaly_score={anomaly_score}"
        )

    print()
    print("EXP-018 STATUS: COMPLETED")
    print("Boundary: anomaly_score is an input to the legacy classifier")
    print("but is not an independent input to the current Lyapunov risk assessment.")

if __name__ == "__main__":
    main()
