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


def main():
    data = load_reference()

    print("REFERENCE LOAD OK")
    print("interface:", data.get("interface"))
    print("version:", data.get("version"))
    print("mappings:", len(data.get("mappings", [])))


if __name__ == "__main__":
    main()
