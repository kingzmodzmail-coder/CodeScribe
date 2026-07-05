import json
import os

import openai

from .tools import TOOL_DEFINITIONS, execute_tool

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def chat(messages, system, workspace=".", use_tools=True, model="gpt-4o-mini", max_iterations=20):
    full_messages = [{"role": "system", "content": system}] + messages

    for _ in range(max_iterations):
        response = client.chat.completions.create(
            model=model,
            messages=full_messages,
            tools=TOOL_DEFINITIONS if use_tools else None,
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            return msg.content

        full_messages.append(msg.model_dump())
        for call in msg.tool_calls:
            os.chdir(workspace)
            result = execute_tool(call.function.name, json.loads(call.function.arguments))
            full_messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result,
                }
            )

    return "Reached maximum tool-call iterations."
