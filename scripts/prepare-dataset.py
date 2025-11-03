"""
Usage:
  python -m scripts.prepare_dataset \
    --tarot data/tarot/cards.yaml \
    --runes data/runes/runes.yaml \
    --out data/processed/train.jsonl
"""
import argparse
from pathlib import Path
from typing import Dict, Iterable

from tarot_llm.tarot.schema import load_tarot_yaml
from tarot_llm.runes.schema import load_runes_yaml
from tarot_llm.common.io import dump_jsonl

def tarot_to_pairs(cards) -> Iterable[Dict]:
    for c in cards:
        instr = f"Give a one-card tarot reading in my voice.\nCard: {c.name} (upright)."
        if c.reversed:
            # you can choose to emit a second sample for reversed meanings later
            pass
        out = f"{c.upright}"
        yield {"instruction": instr, "input": "", "output": out}

def runes_to_pairs(runes) -> Iterable[Dict]:
    for r in runes:
        instr = f"Give a single-rune reading in my voice.\nRune: {r.name} ({r.posture})."
        out = r.meaning
        yield {"instruction": instr, "input": "", "output": out}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tarot", type=str, help="tarot YAML file")
    ap.add_argument("--runes", type=str, help="runes YAML file")
    ap.add_argument("--out", type=str, required=True, help="output JSONL")
    args = ap.parse_args()

    records = []
    if args.tarot and Path(args.tarot).exists():
        records += list(tarot_to_pairs(load_tarot_yaml(args.tarot)))
    if args.runes and Path(args.runes).exists():
        records += list(runes_to_pairs(load_runes_yaml(args.runes)))

    if not records:
        raise SystemExit("No records produced. Check paths to YAML files.")
    dump_jsonl(records, args.out)
    print(f"Wrote {len(records)} samples → {args.out}")

if __name__ == "__main__":
    main()
