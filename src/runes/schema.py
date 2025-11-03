from typing import List
from tarot_llm.common.io import load_yaml
from tarot_llm.common.types import RuneMeaning

def load_runes_yaml(path: str) -> List[RuneMeaning]:
    data = load_yaml(path)  # expects list[dict]
    runes = []
    for row in data:
        runes.append(RuneMeaning(
            name=row["name"],
            posture=row.get("posture", "upright"),
            meaning=row["meaning"],
            keywords=row.get("keywords", []),
            meta=row.get("meta", {}),
        ))
    return runes
