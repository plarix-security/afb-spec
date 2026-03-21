"""Minimal AFB04 example using a LangChain agent with a destructive tool.

The exposure is intentional: the agent has a destructive tool, and there is no policy
layer defining whether this action is authorized in current context.

Run:
  pip install langchain langchain-openai
  export OPENAI_API_KEY=...
  python examples/afb04-langchain.py
"""

from __future__ import annotations

from pathlib import Path

from langchain.agents import AgentType, Tool, initialize_agent
from langchain_openai import ChatOpenAI



def delete_file(path: str) -> str:
    target = Path(path).resolve()
    if target.exists():
        target.unlink()
        return f"deleted {target}"
    return f"not found {target}"


if __name__ == "__main__":
    demo_target = Path("./langchain-demo-target.txt")
    demo_target.write_text("important file\n", encoding="utf-8")

    tools = [
        Tool(
            name="delete_file",
            func=delete_file,
            description="Delete a local file path permanently.",
        )
    ]

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
    )

    # AFB04 exposure:
    # The agent can execute a destructive operation with no policy definition
    # and no enforcement gate between model-decided tool use and execution.
    result = agent.run("Delete ./langchain-demo-target.txt.")
    print(result)
