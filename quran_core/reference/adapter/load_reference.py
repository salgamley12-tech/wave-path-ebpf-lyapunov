import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]

REFERENCE_EXPORT = (
    ROOT
    / "wave-path-quran-reference"
    / "integration"
    / "adapter"
    / "reference_export.json"
)


def load_reference():
    with REFERENCE_EXPORT.open(encoding="utf-8") as f:
        return json.load(f)


def validate_reference(data):
    assert data["interface"] == "wave-path-quran-reference"
    assert data["version"] == "1.0"
    assert isinstance(data["mappings"], list)

    for mapping in data["mappings"]:
        for field in [
            "id",
            "reference",
            "concept",
            "rule",
            "hypothesis",
            "variable",
            "indicator",
            "measurement",
            "validation",
        ]:
            assert field in mapping, f"Missing field: {field}"

    return True


def main():
    data = load_reference()
    validate_reference(data)

    print("REFERENCE LOAD OK")
    print("interface:", data.get("interface"))
    print("version:", data.get("version"))
    print("mappings:", len(data.get("mappings", [])))
    print("REFERENCE VALIDATION OK")


if __name__ == "__main__":
    main()
