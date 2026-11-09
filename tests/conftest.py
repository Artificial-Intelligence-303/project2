"""Point every test at its own log and memory file, never at yours."""

from pathlib import Path

import pytest

import server


@pytest.fixture(autouse=True)
def scratch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Give each test an empty log and an empty memory."""
    monkeypatch.setattr(server, "LOG", tmp_path / "tool-calls.jsonl")
    monkeypatch.setattr(server, "MEMORY", tmp_path / "memory.json")
