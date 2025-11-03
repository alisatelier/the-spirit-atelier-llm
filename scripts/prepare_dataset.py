"""
Usage:
  python scripts/prepare_dataset.py \
    --tarot data/tarot/cards.yaml \
    --out data/processed/tarot_train.jsonl

  # (optional, if you add runes later)
  # --runes data/runes/runes.yaml
"""
import argparse
# scripts/prepare_dataset.py (top of file)
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from tarot.schema import load_all_tarot

cards = load_all_tarot(
    "data/tarot/major_arcana.yaml",
    "data/tarot/minor_arcana.yaml",
)

# from runes.schema import load_runes_yaml  # enable later if needed
from common.io import dump_jsonl


def tarot_to_pairs(cards) -> Iterable[Dict]:
    for c in cards:
        instr = f"Give a one-card tarot reading in my voice.\nCard: {c.name} (upright)."
        out = c.upright
        yield {"instruction": instr, "input": "", "output": out}

# def runes_to_pairs(runes) -> Iterable[Dict]:
#     for r in runes:
#         instr = f"Give a single-rune reading in my voice.\nRune: {r.name} ({r.posture})."
#         yield {"instruction": instr, "input": "", "output": r.meaning}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tarot", type=str, help="tarot YAML file")
    ap.add_argument("--runes", type=str, help="runes YAML file (optional)")
    ap.add_argument("--out", type=str, required=True, help="output JSONL")
    args = ap.parse_args()

    records = []

    if args.tarot and Path(args.tarot).exists():
        records += list(tarot_to_pairs(load_tarot_yaml(args.tarot)))

    # if args.runes and Path(args.runes).exists():
    #     from runes.schema import load_runes_yaml
    #     records += list(runes_to_pairs(load_runes_yaml(args.runes)))

    if not records:
        raise SystemExit("No records produced. Check --tarot/--runes paths.")
    dump_jsonl(records, args.out)
    print(f"Wrote {len(records)} samples → {args.out}")

if __name__ == "__main__":
    main()
