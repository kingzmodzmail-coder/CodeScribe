import json
import os
from pathlib import Path

MEMORY_DIR = ".codex_memory"


def _memory_path(session_id: str) -> str:
    safe_session_id = Path(session_id).name
    if safe_session_id != session_id:
        raise ValueError("Invalid session id")
    return os.path.join(MEMORY_DIR, f"{safe_session_id}.json")


def load_memory(session_id: str) -> list:
    path = _memory_path(session_id)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []


def save_memory(session_id: str, messages: list):
    os.makedirs(MEMORY_DIR, exist_ok=True)
    with open(_memory_path(session_id), "w") as f:
        json.dump(messages, f)
