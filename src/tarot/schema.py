from typing import List
from tarot_llm.common.io import load_yaml
from tarot_llm.common.types import CardMeaning

def load_tarot_yaml(path: str) -> List[CardMeaning]:
    data = load_yaml(path)  # expects list[dict]
    cards = []
    for row in data:
        cards.append(CardMeaning(
            name=row["name"],
            upright=row["upright"],
            reversed=row.get("reversed"),
            element=row.get("element"),
            suit=row.get("suit"),
            keywords=row.get("keywords", []),
            meta=row.get("meta", {}),
        ))
    return cards
