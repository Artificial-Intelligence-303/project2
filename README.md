# Project 2: An Agent with Memory

|                     |                                            |
| :------------------ | :----------------------------------------- |
| `Tuesday 10 Nov`    | Released, in lab                           |
| `Thursday 12 Nov`   | Plan due, 11:59pm                          |
| `Tuesday 24 Nov`    | Demo, in lab                               |
| `Tuesday 1 Dec`     | Due 2:30pm, with code review               |
| Points              | 14                                         |
| Format              | Individual                                 |

In Challenge 7 you ran an agent against an inbox server that someone else
designed. In this project you design the server: the tools an agent gets,
the guardrails around them, and a memory it keeps from one session to the
next. GitHub Copilot's agent in VS Code runs the loop.

## What you build

**An MCP server for a task you choose, for one person, with long-term
memory.** Some tasks that fit: a study planner that tracks assignments and
due dates, a pantry that suggests what to cook, a club's event sign-ups, a
reading log that recommends what to read next, a lab's equipment checkout.
Invent the data and keep it in `data/`.

Your server needs all of these:

1. **Tools for your task**, at least three besides the two memory tools.
   At least one only reads (`READ_ONLY`) and at least one changes something
   (`CHANGES`, or `CANNOT_UNDO` if it cannot be taken back).
2. **Long-term memory**, as two tools:
   - `remember(note: str)` saves the note to the file named by `MEMORY`. An
     empty note is an error result.
   - `recall(query: str)` returns at most five saved notes, best match
     first, one per line, each with its score. You choose the retrieval
     method and justify it in `plan.md`: keyword retrieval that skips
     common words, words weighted by how rare they are, or another method
     you can explain. Read the memory file on every call, so a note saved in
     one session is there in the next.
3. **Two guardrails in the server**: checks that reject a bad call with a
   result starting `error:`. Raising a `ValueError` inside a tool does this
   for you, through `run`.
4. **Every call goes through `run`**, so it is logged in
   `logs/tool-calls.jsonl`.
5. **`AGENTS.md`** tells the agent what the server is for, when to save a
   note and when to search for one, and at least one rule about tools that
   change something.
6. **Your own tests**, in at least two files of your own in `tests/`, for
   each task tool and at least one guardrail.

You may have Copilot's agent write any of this code. Review every line
before you commit it, because at the code review you explain any part you
are asked about.

## What is provided

- `src/server.py`: the server, the `run` helper from Challenge 7, the three
  annotations, and the paths `LOG` and `MEMORY`. It offers no tools yet.
- `src/main.py`: `uv run python src/main.py log` prints your log.
- `.vscode/mcp.json`: starts your server as `project2` in VS Code.
- `tests/test_memory.py`: checks every server's memory tools the same way.
  It must pass, and you do not edit it.
- `tests/test_session.py`: checks your committed log after your evaluation.
- `docs/plan.md`, `docs/evaluation.md` and `docs/reflection.md` to fill in.

## Evaluation: run your agent

Run at least six tasks through Copilot's agent in the Agents window, and
record each one in `docs/evaluation.md`. Between them they cover:

1. A task that uses a tool that reads and a tool that changes something,
   where you approve the change.
2. A task where you decline a change.
3. A task where the agent remembers something, then **a new session** that
   needs it. The two sessions count as two tasks.
4. A task where a guardrail rejects a call. Record what the agent did next.
5. **A planted instruction**: put an instruction addressed to the agent in
   your data, such as an item description or a saved note, and record
   whether the agent followed it.

Commit `logs/tool-calls.jsonl` with your evaluation. To start a fresh log
for a clean run, delete the file before you begin.

## Layout, and the automated checks

Run the checks yourself with `uv run gatorgrade --config gatorgrade.yml`;
they also run on GitHub when you push. They confirm that the memory tools
behave, the tests pass, the log shows real sessions, the style follows the
Google Python style guide (`uv run ruff check src tests`), and the
documents are complete. The repository needs at least 15 commits by the due
date. The checks confirm the pieces are there; the demo, the code review and
the reflection judge the design.

## What is due, and when

- **Thursday 12 November: `docs/plan.md`, by 11:59pm.** The instructor
  reads it and posts the **Plan sign-off** issue to your repository: a
  checklist where anything left unticked is what to change before you build
  that part.
- **Tuesday 24 November, in lab: a demo.** Run two of your evaluation tasks
  live in the Agents window, one of them using memory from an earlier
  session, and walk your table through the log. The **Demo** issue is
  filled in for you afterwards. This is the project's presentation.
- **Tuesday 1 December, 2:30pm: the finished project**, with
  `docs/evaluation.md` and `docs/reflection.md` complete and a code review
  in lab, recorded in the **Code review** issue.

## Evaluation

This project is worth **14 points**.

| Component | Value |
| :-------- | ----: |
| Implementation | 6 |
| Evaluation of the agent | 2 |
| Demo | 2 |
| Written reflection | 2 |
| Oral component of the code review | 2 |

**The implementation** is graded on the six requirements above, checked in
the code and by running it. **The evaluation** is graded on whether the six
tasks cover every required kind and whether each outcome is backed by lines
from your log. **The reflection** revisits your goals, ties memory and the
planted instruction to your own runs, and says who this agent could harm.

## How this project was built

I chose the project's design, its milestones and the demo as its
presentation. Claude drafted the README, the starting server, the provided
tests, the issue forms and the automated checks, and built a reference
server to check that the tests pass on working code and fail on the
starting code. I reviewed the result before release.

## AI use on this project

Full policy: **[AI in this course](https://areweagentsyet.com/ai/)**. The
evaluation sessions with Copilot's agent are the assignment. Any other AI
use, including an agent writing your code, is allowed and disclosed in
`docs/reflection.md`.
