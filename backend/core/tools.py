import os
import subprocess
from pathlib import Path

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file from the workspace",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write or overwrite a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_shell",
            "description": "Run a shell command in the workspace",
            "parameters": {
                "type": "object",
                "properties": {"command": {"type": "string"}},
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_dir",
            "description": "List files in a directory",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
]


REPO_ROOT = Path(__file__).resolve().parents[2]


def _workspace_root(workspace: str) -> Path:
    requested = Path(workspace)
    candidate = requested.resolve() if requested.is_absolute() else (REPO_ROOT / requested).resolve()
    if not candidate.is_dir():
        raise ValueError("Workspace must be an existing directory")
    try:
        candidate.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise ValueError("Workspace must stay within the repository") from exc
    return candidate


def _resolve_workspace_path(workspace: str, path: str) -> Path:
    root = _workspace_root(workspace)
    candidate = (root / path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError("Path must stay within the workspace")
    return candidate


def execute_tool(name: str, args: dict, workspace: str = ".") -> str:
    try:
        if name == "read_file":
            with open(_resolve_workspace_path(workspace, args["path"]), "r") as f:
                return f.read()
        if name == "write_file":
            target = _resolve_workspace_path(workspace, args["path"])
            os.makedirs(target.parent, exist_ok=True)
            with open(target, "w") as f:
                f.write(args["content"])
            return f"Wrote {args['path']}"
        if name == "run_shell":
            result = subprocess.run(
                args["command"],
                shell=True,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=_workspace_root(workspace),
            )
            return (result.stdout + result.stderr)[:4000]
        if name == "list_dir":
            return "\n".join(os.listdir(_resolve_workspace_path(workspace, args["path"])))
        return "Unknown tool"
    except Exception as e:
        return f"Error: {e}"
