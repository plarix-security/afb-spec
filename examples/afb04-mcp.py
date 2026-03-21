"""Minimal AFB04 example for an MCP-style tool-calling agent.

This is runnable Python showing an MCP-like tool server and client-side agent loop.
The exposure is intentional: the agent executes a destructive tool call with no policy
layer defining or enforcing whether the action is allowed.

Run:
  python examples/afb04-mcp.py
"""

from __future__ import annotations

from pathlib import Path


class MinimalMCPToolServer:
    def list_tools(self) -> list[dict[str, str]]:
        return [
            {
                "name": "delete_file",
                "description": "Delete a local file path permanently.",
            }
        ]

    def call_tool(self, name: str, arguments: dict[str, str]) -> str:
        if name != "delete_file":
            raise ValueError(f"Unknown tool: {name}")

        path = Path(arguments["path"]).resolve()
        if path.exists():
            path.unlink()
            return f"deleted {path}"
        return f"not found {path}"


class MCPToolCallingAgent:
    def __init__(self, server: MinimalMCPToolServer) -> None:
        self.server = server

    def plan(self, user_prompt: str) -> dict[str, object]:
        # Minimal planner behavior for demonstration only.
        if "delete" in user_prompt.lower() and "file" in user_prompt.lower():
            return {
                "tool": "delete_file",
                "arguments": {"path": "./mcp-demo-target.txt"},
            }
        return {"tool": None, "arguments": {}}

    def run(self, user_prompt: str) -> str:
        tool_call = self.plan(user_prompt)

        # AFB04 exposure:
        # There is no policy definition (no allow/deny rules, no approvals,
        # no principal/resource checks) between planned action and execution.
        # The tool call crosses Agent -> Act directly and can be destructive.
        if tool_call["tool"]:
            return self.server.call_tool(tool_call["tool"], tool_call["arguments"])
        return "no-op"


if __name__ == "__main__":
    target = Path("./mcp-demo-target.txt")
    target.write_text("important file\n", encoding="utf-8")

    server = MinimalMCPToolServer()
    agent = MCPToolCallingAgent(server)

    result = agent.run("Please delete the file now.")
    print(result)
