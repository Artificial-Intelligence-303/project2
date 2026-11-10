"""Point every test at its own log, memory and data, never at yours."""

import shutil
from pathlib import Path

import pytest

import server


@pytest.fixture(autouse=True)
def scratch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Give each test an empty log, an empty memory and a copy of data/."""
    data = tmp_path / "data"
    if server.DATA.is_dir():
        shutil.copytree(
            server.DATA, data, ignore=shutil.ignore_patterns("memory.json")
        )
    else:
        data.mkdir()
    monkeypatch.setattr(server, "DATA", data)
    monkeypatch.setattr(server, "LOG", tmp_path / "tool-calls.jsonl")
    monkeypatch.setattr(server, "MEMORY", tmp_path / "memory.json")
