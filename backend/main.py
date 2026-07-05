from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List

from core.llm import chat

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]
    mode: str = "chat"
    workspace: str = "."
    model: str = "gpt-4o-mini"


SYSTEM_PROMPTS = {
    "chat": "You are CodeScribe, a helpful AI assistant.",
    "agent": """You are CodeScribe, a coding agent. You can read, write, and run code in the user's workspace.
Always think step by step. Prefer small edits. Run tests after changes.""",
}


@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    system = SYSTEM_PROMPTS.get(req.mode, SYSTEM_PROMPTS["chat"])
    reply = chat(
        messages=req.messages,
        system=system,
        workspace=req.workspace,
        use_tools=(req.mode == "agent"),
        model=req.model,
    )
    return {"reply": reply}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
