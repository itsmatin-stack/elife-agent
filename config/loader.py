import json, os

def load_config():
    path = os.path.join(os.path.dirname(__file__), "settings.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
