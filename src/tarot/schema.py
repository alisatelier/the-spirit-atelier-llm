# src/tarot/schema.py
from __future__ import annotations
from pathlib import Path
import yaml
from typing import Dict, List

# Minor-only metadata (suits/pips objects):
# You named this file minorarcana_definitions.py — that's fine.
from .minorarcana_definitions import SUIT_DEFS, PIP_DEFS

Card = Dict[str, object]

def _enrich_minor_card(card: Card) -> None:
    """
    Attach rich suit/pip metadata to a MINOR arcana card in-place.
    Safe to call even if fields already present.
    """
    suit = card.get("suit")
    pip  = card.get("pip")

    # --- Suit enrichment ---
    if isinstance(suit, str) and suit in SUIT_DEFS:
        sdef = SUIT_DEFS[suit]
        # element can be present in YAML; definitions win if absent
        card.setdefault("element", sdef["element"])
        card.setdefault("suit_meaning", sdef["phrase"])
        card.setdefault("suit_keywords", sdef["keywords"])
        card.setdefault("rws_suit", sdef["rws_equivalent"])
        card.setdefault("suit_holistic", sdef.get("holistic"))  # you added this in your defs

    # --- Pip enrichment ---
    if isinstance(pip, str) and pip in PIP_DEFS:
        pdef = PIP_DEFS[pip]
        # provide both upright and reversed pip descriptors for downstream use
        card.setdefault("pip_upright_keyword", pdef["upright_keyword"])
        card.setdefault("pip_upright_phrase",  pdef["upright_phrase"])
        card.setdefault("pip_reversed_keyword", pdef["reversed_keyword"])
        card.setdefault("pip_reversed_phrase",  pdef["reversed_phrase"])


    ALLOWED_PIPS = set(PIP_DEFS.keys())  # e.g., {"One","Two",...,"Ten"}
    if pip and pip not in ALLOWED_PIPS:
        raise ValueError(f"Unknown pip '{pip}' on card id={card.get('id')}")

    # Ensure the semantic fields exist even if author prose isn't ready yet.
    card.setdefault("upright", "")
    card.setdefault("reversed", "")
    card.setdefault("keywords", [])

def _load_yaml(path: Path) -> List[Card]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or []
    if not isinstance(data, list):
        raise ValueError(f"{path} must be a YAML sequence (list) of cards.")
    return data

def load_major(path: str | Path) -> List[Card]:
    cards = _load_yaml(Path(path))
    # Majors already have element/upright/reversed in your YAML.
    # Nothing else to enrich by default.
    for c in cards:
        c.setdefault("keywords", [])
    return cards

def load_minor(path: str | Path) -> List[Card]:
    cards = _load_yaml(Path(path))
    for c in cards:
        _enrich_minor_card(c)
    return cards

def load_all_tarot(major_path: str | Path, minor_path: str | Path) -> List[Card]:
    """Return a single list of cards (majors + minors) with minor cards enriched."""
    major = load_major(major_path)
    minor = load_minor(minor_path)
    all_cards = major + minor

    # Basic safety checks: unique IDs and required titles
    ids = set()
    for c in all_cards:
        cid = c.get("id")
        if cid in ids:
            raise ValueError(f"Duplicate card id detected: {cid}")
        ids.add(cid)
        if not c.get("tsa_title") or not c.get("rws_title"):
            raise ValueError(f"Card {cid} is missing tsa_title or rws_title.")
    return all_cards
