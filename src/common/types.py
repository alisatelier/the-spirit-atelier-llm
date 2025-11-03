from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class CardMeaning:
    name: str
    upright: str
    reversed: Optional[str] = None
    element: Optional[str] = None
    suit: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    meta: Dict[str, str] = field(default_factory=dict)

@dataclass
class RuneMeaning:
    name: str
    posture: str  # "upright"|"reversed"|"merkstave"|etc.
    meaning: str
    keywords: List[str] = field(default_factory=list)
    meta: Dict[str, str] = field(default_factory=dict)
