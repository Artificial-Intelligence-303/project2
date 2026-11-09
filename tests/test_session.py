"""Provided: checks on your real log, from your sessions with the agent.

These read `logs/tool-calls.jsonl` in your repository, so they fail until
you have run your evaluation tasks in VS Code and committed the log. Do not
edit this file.
"""

import json
from pathlib import Path

LOG = Path(__file__).parent.parent / "logs" / "tool-calls.jsonl"


def entries() -> list[dict]:
    """Return every logged call, or none if the log does not exist yet."""
    if not LOG.exists():
        return []
    return [json.loads(line) for line in LOG.read_text().splitlines()]


def succeeded(tool: str) -> bool:
    """Whether the log holds a call to this tool that was not an error."""
    return any(
        entry["tool"] == tool and not str(entry["result"]).startswith("error")
        for entry in entries()
    )


def test_the_log_holds_twenty_calls() -> None:
    """Your evaluation produced at least twenty tool calls."""
    assert len(entries()) >= 20


def test_the_agent_remembered_and_recalled() -> None:
    """The agent saved a note and searched its memory."""
    assert succeeded("remember") and succeeded("recall")


def test_a_guardrail_rejected_a_call() -> None:
    """At least one call came back as an error result."""
    assert any(str(entry["result"]).startswith("error") for entry in entries())


def test_the_agent_used_three_of_your_tools() -> None:
    """Calls to at least three tools besides remember and recall."""
    used = {entry["tool"] for entry in entries()} - {"remember", "recall"}
    assert len(used) >= 3
