import json, os
from datetime import datetime

HISTORY_FILE = "data/local/history.json"

class MemoryManager:
    def __init__(self):
        os.makedirs("data/local", exist_ok=True)
        self.history = self._load()

    def _load(self):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save(self):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def add(self, role: str, content: str):
        self.history.append({"role": role, "content": content, "timestamp": datetime.now().isoformat()})
        if len(self.history) > 100:
            self.history = self.history[-100:]
        self.save()

    def get_messages(self, last_n=10):
        recent = self.history[-last_n:]
        return [{"role": m["role"], "content": m["content"]} for m in recent]

    def clear(self):
        self.history = []
        self.save()
