# CodeScribe

Your own AI chatbot, coding agent, and VS Code extension.

## Components

- `backend/` — FastAPI server with LLM + tool-calling
- `cli/` — Terminal coding agent
- `web/` — Browser chatbot UI
- `vscode-ext/` — VS Code extension

## Quick Start

1. Copy `.env.example` to `.env` and set `OPENAI_API_KEY`.
2. Start the backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   python main.py
   ```
3. Open `web/index.html` in a browser.
4. Run the CLI:
   ```bash
   cd cli
   python kodex.py
   ```
5. For the VS Code extension:
   ```bash
   cd vscode-ext
   npm install
   npm run compile
   ```
   Then press F5 in VS Code.

## API

`POST /chat`

```json
{
  "messages": [{"role": "user", "content": "fix the bug in auth.py"}],
  "mode": "agent",
  "workspace": ".",
  "model": "gpt-4o-mini"
}
```

Modes:

- `chat` — general conversation
- `agent` — can read/write files and run shell commands