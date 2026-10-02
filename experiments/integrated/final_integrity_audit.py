import csv
import json
import math
import os

FILES = [
    "experiments/integrated/results.csv",
    "experiments/integrated/results_full.csv",
    "experiments/integrated/sensitivity_scenarios.csv",
    "experiments/integrated/sensitivity_scenarios.json",
    "experiments/integrated/sensitivity_analysis.json",
    "experiments/integrated/EXP_008_validation.json",
    "experiments/integrated/EXP_010_final_report.json",
]


def check_files():
    return {
        path: os.path.exists(path)
        for path in FILES
    }


def check_results_full():
    path = "experiments/integrated/results_full.csv"

    with open(
        path,
        newline="",
        encoding="utf-8",
    ) as f:
        rows = list(csv.DictReader(f))

    required = {
        "t",
        "bytes_rate",
        "connection_rate",
        "anomaly_score",
        "V",
        "dVdt",
        "risk",
        "action",
        "authorized",
    }

    fields_ok = required.issubset(rows[0].keys())

    finite_ok = True

    for row in rows:
        for field in [
            "t",
            "bytes_rate",
            "connection_rate",
            "anomaly_score",
            "V",
            "dVdt",
        ]:
            if not math.isfinite(float(row[field])):
                finite_ok = False

    return {
        "samples_200": len(rows) == 200,
        "required_fields": fields_ok,
        "finite_values": finite_ok,
    }


def check_sensitivity():
    path = (
        "experiments/integrated/"
        "sensitivity_scenarios.json"
    )

    with open(
        path,
        encoding="utf-8",
    ) as f:
        data = json.load(f)

    summary = data["summary"]

    low_v = summary["low"]["max_V"]
    medium_v = summary["medium"]["max_V"]
    high_v = summary["high"]["max_V"]

    low_d = summary["low"]["max_dVdt"]
    medium_d = summary["medium"]["max_dVdt"]
    high_d = summary["high"]["max_dVdt"]

    return {
        "low_samples": summary["low"]["samples"] == 200,
        "medium_samples": summary["medium"]["samples"] == 200,
        "high_samples": summary["high"]["samples"] == 200,
        "V_order": high_v > medium_v > low_v,
        "dVdt_order": high_d > medium_d > low_d,
    }


def main():
    file_checks = check_files()
    results_checks = check_results_full()
    sensitivity_checks = check_sensitivity()

    all_checks = {}

    all_checks.update(
        {
            "files": all(file_checks.values()),
            "results_full": all(results_checks.values()),
            "sensitivity": all(sensitivity_checks.values()),
        }
    )

    validation_passed = all(all_checks.values())

    result = {
        "experiment": "EXP-011",
        "description": (
            "Final integrity audit of the "
            "integrated experimental artifacts"
        ),
        "file_checks": file_checks,
        "results_checks": results_checks,
        "sensitivity_checks": sensitivity_checks,
        "validation_passed": validation_passed,
    }

    output = (
        "experiments/integrated/"
        "EXP_011_integrity_audit.json"
    )

    with open(
        output,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            result,
            f,
            indent=2,
        )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
