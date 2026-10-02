import csv
import hashlib
import subprocess
import sys

INPUT = "experiments/integrated/sensitivity_scenarios.csv"


def file_hash(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)

    return h.hexdigest()


def main():
    before = file_hash(INPUT)

    subprocess.run(
        [
            sys.executable,
            "experiments/integrated/"
            "sensitivity_scenarios.py",
        ],
        check=True,
    )

    after = file_hash(INPUT)

    result = {
        "experiment": "EXP-009",
        "description": (
            "Reproducibility validation of "
            "the synthetic sensitivity experiment"
        ),
        "hash_before": before,
        "hash_after": after,
        "identical_output": before == after,
    }

    print(result)


if __name__ == "__main__":
    main()
