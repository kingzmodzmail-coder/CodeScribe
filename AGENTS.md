# AGENTS.md

## Cursor Cloud specific instructions

CodeScribe is a small multi-part app. Standard setup/run commands live in `README.md`; only the non-obvious notes are captured here.

### Services

- `backend/` — FastAPI + OpenAI chat/agent server. Run with `cd backend && python3 main.py` (listens on `0.0.0.0:8000`, endpoint `POST /chat`). This is the only long-running service the other components depend on.
- `web/` — static chatbot page. `README.md` says to open `web/index.html` directly, but the page fetches `http://localhost:8000/chat`, so the backend must be running. Serving it over HTTP (e.g. `python3 -m http.server` from `web/`) avoids `file://` quirks.
- `cli/` — `python3 cli/kodex.py`; talks to the backend at `$CODEX_API_URL` (default `http://localhost:8000/chat`).
- `vscode-ext/` — TypeScript VS Code extension. `npm ci` then `npm run compile` (output in `out/`); it also calls `http://localhost:8000/chat`. Launching the extension host itself requires the VS Code GUI (F5), so it generally can't be exercised end-to-end headlessly — compiling is the practical check.

### Non-obvious notes

- The backend needs an LLM to do anything useful. `OPENAI_API_KEY` is **not** set in this environment, so `POST /chat` will 500 at the OpenAI call unless you provide one. The `openai` SDK also honors `OPENAI_BASE_URL`, so you can exercise the full pipeline (chat + agent tool-calling loop) without a real key by pointing `OPENAI_BASE_URL` at a local OpenAI-compatible mock and using any dummy `OPENAI_API_KEY`.
- Agent-mode tool calls (`read_file`/`write_file`/`run_shell`/`list_dir` in `backend/core/tools.py`) are sandboxed to the CodeScribe repo root (`REPO_ROOT = parents[2]` of `tools.py`); the request's `workspace` field does not widen this. Paths that escape the repo raise "Path must stay within the repository".
- `pip install` puts console scripts (`uvicorn`, etc.) in `~/.local/bin`, which is not on `PATH` by default; the app is started via `python3 main.py`, so this doesn't matter unless you invoke `uvicorn` directly.
- There is no automated test suite and no lint configuration in the repo.

### Sibling repo

The workspace also contains `DorkForge`, which is currently an empty AL (Dynamics 365 Business Central) scaffold — only a `.gitignore`, no source or setup.
