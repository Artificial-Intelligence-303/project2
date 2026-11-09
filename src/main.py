"""Print the server's log as a transcript.

Usage:
    uv run python src/main.py log
"""

import json
import sys

from server import LOG


def show_log() -> None:
    """Print each logged call as two lines: the call and its result."""
    if not LOG.exists():
        print("No calls yet: the server has not received any.")
        return
    for line in LOG.read_text().splitlines():
        entry = json.loads(line)
        arguments = json.dumps(entry["arguments"])
        result = str(entry["result"]).replace("\n", "\n" + " " * 30)
        print(f"{entry['time']}  [call]   {entry['tool']} {arguments}")
        print(f"{' ' * 19}  [result] {result}")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "log":
        show_log()
    else:
        print(__doc__)
