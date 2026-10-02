from ai.risk import classify
from model.risk.lyapunov_risk import assess_lyapunov_risk


CASES = [
    ("NEGATIVE", -0.10, 0.10, 1.0),
    ("ZERO",      0.00, 0.10, 1.0),
    ("SMALL_POS", 0.02, 0.10, 1.0),
    ("LARGE_POS", 0.10, 0.10, 1.0),
    ("ANOMALY",   -0.10, 0.90, 1.0),
]


def main():
    results = []

    for name, dVdt, anomaly, V in CASES:
        old = classify(dVdt, anomaly).value
        new = assess_lyapunov_risk(V, dVdt).risk_level

        results.append({
            "case": name,
            "dVdt": dVdt,
            "anomaly_score": anomaly,
            "V": V,
            "old_risk": old,
            "new_risk": new,
            "match": old.upper() == new,
        })

    print("EXP-017 Decision Boundary Comparison")
    print()

    for r in results:
        print(
            f"{r['case']}: "
            f"old={r['old_risk']} "
            f"new={r['new_risk']} "
            f"match={r['match']}"
        )

    matches = sum(r["match"] for r in results)
    mismatches = len(results) - matches

    print()
    print(f"cases={len(results)}")
    print(f"matches={matches}")
    print(f"mismatches={mismatches}")

    if mismatches:
        print("EXP-017 STATUS: DIFFERENCE_DETECTED")
    else:
        print("EXP-017 STATUS: COMPATIBLE")


if __name__ == "__main__":
    main()
