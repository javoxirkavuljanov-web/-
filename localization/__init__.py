import json
import os

_cache: dict[str, dict] = {}

def get_text(lang: str, key: str, **kwargs) -> str:
    if lang not in _cache:
        path = os.path.join(os.path.dirname(__file__), f"{lang}.json")
        if not os.path.exists(path):
            lang = "en"
            path = os.path.join(os.path.dirname(__file__), "en.json")
        with open(path, encoding="utf-8") as f:
            _cache[lang] = json.load(f)

    data = _cache[lang]
    keys = key.split(".")
    value = data
    for k in keys:
        value = value[k]

    if isinstance(value, str) and kwargs:
        return value.format(**kwargs)
    return value
