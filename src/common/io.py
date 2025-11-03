import json, pathlib, yaml
from typing import Iterable, Dict, Any

def load_yaml(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def dump_jsonl(records: Iterable[Dict[str, Any]], out_path: str):
    p = pathlib.Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
