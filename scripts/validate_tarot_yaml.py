from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from tarot.schema import load_all_tarot
from tarot.minorarcana_definitions import PIP_DEFS

def main():
    try:
        cards = load_all_tarot(
            "data/tarot/major_arcana.yaml",
            "data/tarot/minor_arcana.yaml",
        )
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    majors = [c for c in cards if c["id"] <= 21]
    minors = [c for c in cards if c["id"] >= 22]

    expected_majors = 22
    expected_minors = 4 * len(PIP_DEFS)  # 4 suits × 10 pips = 40

    if len(majors) != expected_majors:
        print(f"WARNING: expected {expected_majors} majors, found {len(majors)}")
    if len(minors) != expected_minors:
        print(f"WARNING: expected {expected_minors} minors, found {len(minors)}")

    print(f"OK: loaded {len(cards)} cards (majors={len(majors)}, minors={len(minors)})")

if __name__ == "__main__":
    main()
