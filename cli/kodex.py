import os

import requests

API = os.getenv("CODEX_API_URL", "http://localhost:8000/chat")
WORKSPACE = os.getenv("CODEX_WORKSPACE", os.getcwd())


def main():
    print("CodeScribe coding agent. Type 'exit' to quit.")
    print(f"Workspace: {WORKSPACE}")
    print(f"API: {API}")

    messages = []

    while True:
        try:
            user = input("\n> ")
        except (EOFError, KeyboardInterrupt):
            break
        if user.lower() in ("exit", "quit"):
            break

        messages.append({"role": "user", "content": user})
        try:
            res = requests.post(
                API,
                json={
                    "messages": messages,
                    "mode": "agent",
                    "workspace": WORKSPACE,
                },
            )
            reply = res.json()["reply"]
        except Exception as e:
            reply = f"Error talking to API: {e}"
        messages.append({"role": "assistant", "content": reply})
        print(f"\n{reply}")


if __name__ == "__main__":
    main()
