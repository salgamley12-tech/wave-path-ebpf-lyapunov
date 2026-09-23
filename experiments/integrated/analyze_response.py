import csv
import json

INPUT = "experiments/integrated/results_full.csv"
OUTPUT = "experiments/integrated/response_analysis.json"


def first_time(rows, condition):
    for row in rows:
        if condition(row):
            return row["t"]
    return None


def main():
    with open(INPUT, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        raise RuntimeError("No data found")

    for r in rows:
        r["t"] = float(r["t"])
        r["V"] = float(r["V"])
        r["dVdt"] = float(r["dVdt"])
        r["anomaly_score"] = float(r["anomaly_score"])
        r["authorized"] = r["authorized"].lower() == "true"

    # بداية الاضطراب: أول حدث غير مصرح به
    disturbance_start = first_time(
        rows,
        lambda r: not r["authorized"]
    )

    # أول ارتفاع في المخاطر إلى HIGH
    first_high = first_time(
        rows,
        lambda r: r["risk"] == "high"
    )

    # أول إجراء DROP
    first_drop = first_time(
        rows,
        lambda r: r["action"] == "drop"
    )

    # أعلى dV/dt
    peak_rise = max(rows, key=lambda r: r["dVdt"])

    # أقل dV/dt
    peak_fall = min(rows, key=lambda r: r["dVdt"])

    # آخر حدث غير مصرح به
    unauthorized_rows = [
        r for r in rows
        if not r["authorized"]
    ]

    disturbance_end = (
        unauthorized_rows[-1]["t"]
        if unauthorized_rows
        else None
    )

    detection_delay = (
        first_high - disturbance_start
        if disturbance_start is not None
        and first_high is not None
        else None
    )

    response_delay = (
        first_drop - disturbance_start
        if disturbance_start is not None
        and first_drop is not None
        else None
    )

    high_to_drop_delay = (
        first_drop - first_high
        if first_high is not None
        and first_drop is not None
        else None
    )

    # نعتبر انتهاء الاضطراب عند آخر حدث غير مصرح به.
    # بعدها نبحث عن أول نقطة يبدأ فيها dV/dt بالانخفاض.
    recovery_start = None

    if disturbance_end is not None:
        for r in rows:
            if r["t"] > disturbance_end and r["dVdt"] < 0:
                recovery_start = r["t"]
                break

    recovery_delay = (
        recovery_start - disturbance_end
        if recovery_start is not None
        and disturbance_end is not None
        else None
    )

    result = {
        "experiment": "EXP-004",
        "samples": len(rows),

        "disturbance": {
            "start": disturbance_start,
            "end": disturbance_end,
            "duration": (
                disturbance_end - disturbance_start
                if disturbance_start is not None
                and disturbance_end is not None
                else None
            ),
        },

        "detection": {
            "first_high": first_high,
            "detection_delay": detection_delay,
        },

        "response": {
            "first_drop": first_drop,
            "response_delay": response_delay,
            "high_to_drop_delay": high_to_drop_delay,
        },

        "peak_dVdt": {
            "value": peak_rise["dVdt"],
            "t": peak_rise["t"],
            "V": peak_rise["V"],
            "risk": peak_rise["risk"],
            "action": peak_rise["action"],
        },

        "minimum_dVdt": {
            "value": peak_fall["dVdt"],
            "t": peak_fall["t"],
            "V": peak_fall["V"],
        },

        "recovery": {
            "recovery_start": recovery_start,
            "recovery_delay": recovery_delay,
        },
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))

    
if __name__ == "__main__":
    main()


