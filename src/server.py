"""TODO: say in one sentence what this MCP server does, and for whom.

VS Code starts this server from `.vscode/mcp.json`, and Copilot's agent
calls its tools. Every call goes through `run`, which adds it to
`logs/tool-calls.jsonl`; `uv run python src/main.py log` prints that file.

The server, `run`, the three kinds of annotation and the paths `LOG`,
`MEMORY` and `DATA` are provided. Every tool is yours to write, `remember`
and `recall` included. Keep `LOG`, `MEMORY` and `DATA` as module-level
names, and build each data file's path from `DATA` inside the tool that
uses it, because the provided tests point all three at a scratch folder.
"""

import datetime
import json
from collections.abc import Callable
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

ROOT = Path(__file__).parent.parent
LOG = ROOT / "logs" / "tool-calls.jsonl"
DATA = ROOT / "data"
MEMORY = DATA / "memory.json"

server = MCPServer(
    "project2",
    instructions="TODO: one sentence on what this server is for.",
)

READ_ONLY = ToolAnnotations(read_only_hint=True)
CHANGES = ToolAnnotations(read_only_hint=False, destructive_hint=False)
CANNOT_UNDO = ToolAnnotations(read_only_hint=False, destructive_hint=True)


def run(
    tool: str, arguments: dict[str, object], work: Callable[[], str]
) -> str:
    """Run one tool call, log it, and return its result as text.

    A ValueError comes back as a result starting "error:", so the model
    can read what went wrong and try again.
    """
    try:
        result = work()
    except ValueError as problem:
        result = f"error: {problem}"
    entry = {
        "time": datetime.datetime.now().isoformat(timespec="seconds"),
        "tool": tool,
        "arguments": arguments,
        "result": result,
    }
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as log:
        log.write(json.dumps(entry) + "\n")
    return result


# Your tools go here. Each one is a function decorated with
# @server.tool(annotations=...), whose docstring is the description the
# model reads, and whose body returns run("name", {arguments}, lambda: ...).


if __name__ == "__main__":
    server.run()
