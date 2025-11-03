# scripts/try_meaning.py
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from tarot.schema import load_all_tarot
from tarot.meaning import get_card_meaning, find_card

def main():
    ap = argparse.ArgumentParser(description="Preview a tarot card meaning.")
    ap.add_argument("--id", type=int, help="Card id (e.g., 22)")
    ap.add_argument("--title", type=str, help='TSA title (e.g., "One of Sparks")')
    ap.add_argument("--orientation", choices=["upright", "reversed"], default="upright")
    ap.add_argument("--major", default="data/tarot/major_arcana.yaml")
    ap.add_argument("--minor", default="data/tarot/minor_arcana.yaml")
    args = ap.parse_args()

    cards = load_all_tarot(args.major, args.minor)
    card = find_card(cards, id=args.id, tsa_title=args.title)

    print(f"{card['tsa_title']} ({args.orientation})")
    print("-" * 60)
    print(get_card_meaning(card, args.orientation))

if __name__ == "__main__":
    main()
