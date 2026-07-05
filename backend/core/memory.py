import json
import os

MEMORY_DIR = ".codex_memory"


def load_memory(session_id: str) -> list:
    path = os.path.join(MEMORY_DIR, f"{session_id}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []


def save_memory(session_id: str, messages: list):
    os.makedirs(MEMORY_DIR, exist_ok=True)
    with open(os.path.join(MEMORY_DIR, f"{session_id}.json"), "w") as f:
        json.dump(messages, f)
