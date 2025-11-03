# src/tarot/meaning.py
from __future__ import annotations
from typing import Dict, List, Literal, Optional

Orientation = Literal["upright", "reversed"]
Card = Dict[str, object]

def _is_minor(card: Card) -> bool:
    # minors in your deck have pip+suit fields; majors don't
    return "pip" in card and "suit" in card

def compose_minor_meaning(card: Card, orientation: Orientation = "upright") -> str:
    """
    Compose a readable minor-arcana meaning using your pip & suit definitions.
    Uses auto text if `upright`/`reversed` prose is empty in YAML.
    """
    suit = str(card.get("suit", ""))
    pip = str(card.get("pip", ""))

    # phrases/keywords injected by your schema enrichment:
    pip_kw_u = card.get("pip_upright_keyword")
    pip_ph_u = card.get("pip_upright_phrase")
    pip_kw_r = card.get("pip_reversed_keyword")
    pip_ph_r = card.get("pip_reversed_phrase")

    suit_phrase = card.get("suit_meaning")  # from your SUIT_DEFS["phrase"]
    suit_keywords = card.get("suit_keywords") or []
    suit_kw_str = ", ".join(suit_keywords) if suit_keywords else ""

    # user-authored prose from YAML (may be empty strings)
    authored_u = (card.get("upright") or "").strip()
    authored_r = (card.get("reversed") or "").strip()

    if orientation == "upright":
        if authored_u:
            return str(authored_u)
        # fallback auto-meaning
        pieces = []
        if pip_kw_u:
            pieces.append(f"{pip_kw_u} in the realm of {suit}.")
        if pip_ph_u:
            pieces.append(str(pip_ph_u))
        if suit_phrase:
            pieces.append(str(suit_phrase))
        if suit_kw_str:
            pieces.append(f"Keywords: {suit_kw_str}.")
        return " ".join(pieces) or "Meaning forthcoming."
    else:
        if authored_r:
            return str(authored_r)
        # fallback auto-meaning (reversed)
        pieces = []
        if pip_kw_r:
            pieces.append(f"{pip_kw_r} in the realm of {suit}.")
        if pip_ph_r:
            pieces.append(str(pip_ph_r))
        if suit_phrase:
            pieces.append(str(suit_phrase))
        if suit_kw_str:
            pieces.append(f"Keywords: {suit_kw_str}.")
        return " ".join(pieces) or "Meaning forthcoming."

def compose_major_meaning(card: Card, orientation: Orientation = "upright") -> str:
    """
    Majors already have authored text in your YAML.
    If one side is missing (rare), return a gentle placeholder.
    """
    text = (card.get(orientation) or "").strip()
    return text or ("Meaning forthcoming." if orientation == "upright" else "Shadow meaning forthcoming.")

def get_card_meaning(card: Card, orientation: Orientation = "upright") -> str:
    return compose_minor_meaning(card, orientation) if _is_minor(card) else compose_major_meaning(card, orientation)

def find_card(cards: List[Card], *, id: Optional[int] = None, tsa_title: Optional[str] = None) -> Card:
    if id is not None:
        for c in cards:
            if c.get("id") == id:
                return c
        raise KeyError(f"No card with id={id}")
    if tsa_title:
        target = tsa_title.strip().lower()
        for c in cards:
            if str(c.get("tsa_title", "")).strip().lower() == target:
                return c
        raise KeyError(f"No card with tsa_title='{tsa_title}'")
    raise ValueError("Provide id or tsa_title.")
