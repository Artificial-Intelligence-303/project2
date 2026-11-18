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
designed. This time you design the server yourself: the tools an agent
gets, the guardrails around them, and a memory it keeps from one session to
the next. GitHub Copilot's agent in VS Code runs the loop.

## What you build

You build an MCP server with long-term memory that helps one person with a
real task, working on real data. A real task is one a person actually
does, such as planning next semester's courses, logging meals against a
daily target, or choosing the next book to read.

Your server needs all of these:

1. Data for your task in `data/`, from a public dataset you find or from
   data you already have, approved at the plan sign-off.
   - A public dataset has its source and license linked in `plan.md`, and
     a script you commit in `data/` trims it to what your task needs,
     under 5 MB.
   - Private data stays out of the repository: list its files in
     `.gitignore`, and commit a real-like copy in the same shape for your
     evaluation and demo. Your agent sends what it reads to the model's
     provider, so give it only data you are comfortable sharing there.
   - Records about other people are made up, never a real person's.
2. At least three tools for your task besides the two memory tools. At
   least one only reads (`READ_ONLY`), and at least one changes something
   (`CHANGES`, or `CANNOT_UNDO` if it cannot be taken back).
3. Long-term memory, as two tools:
   - `remember(note: str)` saves the note to the file named by `MEMORY`. An
     empty note is an error result.
   - `recall(query: str)` returns at most five saved notes, best match
     first, one per line, each with its score. You choose the retrieval
     method and justify it in `plan.md`: keyword retrieval that skips
     common words, words weighted by how rare they are, or another method
     you can explain. Read the memory file on every call, so that a note
     saved in one session is there in the next.
4. Two guardrails in the server, each a check that rejects a bad call with
   a result starting `error:`. Raising a `ValueError` inside a tool does
   this for you, through `run`.
5. Every call goes through `run`, which logs it in `logs/tool-calls.jsonl`.
6. An `AGENTS.md` that tells the agent what the server is for, when to save
   a note and when to search for one, and at least one rule about tools
   that change something.
7. Tests of your own, in at least two files in `tests/`, covering each task
   tool and at least one guardrail. The provided `tests/conftest.py` gives
   every test its own copy of `data/` through `DATA`, so a test that needs
   the person's records in a known state can write them there first
   without touching your real data.

You may have Copilot's agent write any of this code. Review every line
before you commit it, because at the code review you will explain any part
you are asked about.

## What is provided

- `src/server.py`: the server, the `run` helper from Challenge 7, the three
  annotations, and the paths `LOG`, `MEMORY` and `DATA`. It has no tools
  yet. Build each data file's path from `DATA` inside the tool that uses
  it.
- `src/main.py`: `uv run python src/main.py log` prints your log.
- `.vscode/mcp.json`: starts your server as `project2` in VS Code.
- `tests/test_memory.py`: checks every server's memory tools the same way.
  It must pass, and you do not edit it.
- `tests/test_session.py`: checks your committed log after your evaluation.
- `docs/plan.md`, `docs/evaluation.md` and `docs/reflection.md`, for you to
  fill in.

## A worked example to read

The `src/server.py` in your Challenge 7 repository is a finished server of
the shape this project asks for. Each tool is a function with an annotation
and a docstring the model reads, and its body returns a call to `run`. Read
it for that shape, and make the task, tools and memory your own.

## If you are stuck for a task

A task is ready to plan when you can name the person, write three requests
they would type, and point to one change the agent should ask about before
making it. Any of these works, and so does one of your own. Check the
license of whatever you download, and link it in `plan.md`.

**From a public dataset**

- **Movie night.** [MovieLens](https://grouplens.org/datasets/movielens/)
  (free for study, cite it) or [IMDb's non-commercial
  files](https://developer.imdb.com/non-commercial-datasets/). Read: titles
  by genre, year and running time. Change: add to the watchlist, mark one
  watched. Memory: films already seen, no films over two hours on a
  weeknight. Guardrail: a rating limit the household set.
- **Board game night.** A BoardGameGeek export on Kaggle, with player
  counts, playing times and weights. Read: games that fit tonight's group
  and time. Change: put a game on tonight's list. Memory: who will not play
  a deduction game, what was played last week. Guardrail: the player count
  has to fit the group.
- **Workouts.** [free-exercise-db](https://github.com/yuhonas/free-exercise-db)
  (public domain): 800 exercises with muscles and equipment. Read:
  exercises for the equipment the person owns. Change: log a workout, plan
  a week. Memory: an injury to work around. Guardrail: sets and reps in a
  sane range.
- **Chess openings.**
  [lichess-org/chess-openings](https://github.com/lichess-org/chess-openings)
  (CC0): names, ECO codes and moves. Read: look up an opening by name or by
  moves. Change: add a line to a repertoire. Memory: what the person plays
  as White and as Black, the lines they keep losing. Guardrail: the moves
  have to match an opening in the table.
- **Birds, or any living thing, near Meadville.** A
  [GBIF](https://www.gbif.org/) occurrence download for Crawford County
  (each dataset inside it states its license). Read: species seen locally
  in a given month. Change: log a sighting on a life list. Memory: species
  the person wants to see. Guardrail: the species has to be on the regional
  list, and a sighting cannot be dated in the future.
- **Public domain reading.** The [Project Gutenberg
  catalog](https://www.gutenberg.org/ebooks/offline_catalogs.html), one row
  per book with author, subjects and language. Read: books by author or
  subject. Change: shelve a book, mark it finished. Memory: authors the
  person liked, no poetry. Guardrail: a book cannot be marked finished
  unless it is on the shelf.
- **A road trip in an electric car.** The [Alternative Fuel Stations
  list](https://afdc.energy.gov/data_download) from the US Department of
  Energy (public domain, free key to download). Read: stations near a town
  with the right plug. Change: add a charging stop to the route. Memory:
  the car's plug type and range. Guardrail: refuse a next stop farther than
  the car can go.
- **Getting around by bus.** The GTFS feed of a transit agency the person
  rides, found through [transit.land](https://www.transit.land/), which
  lists each feed's license. Your trim script keeps one or two routes.
  Read: departures from a stop. Change: save a commute. Memory: the stop
  the person prefers and when they need to arrive. Guardrail: the stop has
  to exist in the feed.
- **Flashcards.** A public word list, such as a Wiktionary frequency list
  (CC BY-SA), or the vocabulary of a course you are taking. Read: the cards
  due today. Change: grade a card, which sets its next review date.
  Memory: the pairs the person confuses. Guardrail: a grade is 0 to 5, and
  a card is added once.

**From data you already have**

Private data stays out of the repository. You commit a real-like copy in
the same shape, and the agent only ever reads what you are comfortable
sending to the model's provider.

- **Deadlines.** Your Canvas calendar feed, exported as `.ics`. Read: what
  is due this week. Change: add a task, mark one done, split a project into
  steps. Memory: when the person works best. Guardrail: a due date cannot
  be in the past.
- **Money.** A bank or card export. Read: a month by category. Change: add
  an expense, set a category's budget. Memory: rent day, what is split with
  a roommate. Guardrail: amounts are positive and the category has to
  exist.
- **Applications.** Your internship tracker. Read: open applications and
  deadlines this week. Change: add one, move its status. Memory: what a
  recruiter said. Guardrail: a status moves forward only, and a company and
  role pair is added once.
- **A pet's care.** Your feeding and medication log. Read: what is due
  today. Change: record a dose, which `CANNOT_UNDO`. Memory: what the vet
  said at the last visit. Guardrail: a dose cannot be recorded again before
  its interval has passed.

## Running your agent on six tasks

Run at least six tasks through Copilot's agent in the Agents window, and
record each one in `docs/evaluation.md`. Between them, the tasks cover:

1. A task that uses a tool that reads and a tool that changes something,
   where you approve the change.
2. A task where you decline a change.
3. A task where the agent remembers something, followed by a new session
   that needs it. The two sessions count as two tasks.
4. A task where a guardrail rejects a call, and what the agent did next.
5. A planted instruction: put an instruction addressed to the agent in
   your data, such as one row's description or a saved note, and record
   whether the agent followed it.

Commit `logs/tool-calls.jsonl` with your evaluation. To start a fresh log
for a clean run, delete the file before you begin.

## The automated checks

Run the checks yourself with `uv run gatorgrade --config gatorgrade.yml`.
They also run on GitHub when you push, and they confirm that `data/` holds
your task's data, the memory tools behave, the tests pass, the log shows
real sessions, the style follows the Google Python style guide
(`uv run ruff check src tests`), and the documents are complete. The
repository needs at least 15 commits by the due date. The checks can
confirm that the pieces are there, while the demo, the code review and the
reflection judge the design.

## What is due, and when

- **Thursday 12 November, by 11:59pm:** `docs/plan.md`. The instructor
  reads it and posts a Plan sign-off issue to your repository, a checklist
  in which anything left unticked is what to change before you build that
  part.
- **Tuesday 24 November, in lab:** a demo, which is the project's
  presentation. Run two of your evaluation tasks live in the Agents window,
  one of them using memory from an earlier session, and walk your table
  through the log. The Demo issue is filled in for you afterwards.
- **Tuesday 1 December, by 2:30pm:** the finished project, with
  `docs/evaluation.md` and `docs/reflection.md` complete, and a code review
  in lab, recorded in the Code review issue.

## Evaluation

This project is worth 14 points.

| Component | Value |
| :-------- | ----: |
| Implementation | 6 |
| Evaluation of the agent | 2 |
| Demo | 2 |
| Written reflection | 2 |
| Oral component of the code review | 2 |

The implementation is graded on the seven requirements above, by reading
the code and running it. The evaluation is graded on whether your six tasks
cover every required kind and whether lines from your log back up each
outcome. The reflection revisits your goals, connects memory and the
planted instruction to your own runs, and says who this agent could harm.

## How this project was built

I chose the project's design, its milestones, rules, tests, and README outline. Claude drafted the starting server, the issue forms and the
automated checks, and edited the text for readability. I built a complete sample
solution to test the assignment,
and used it to build the provided tests. 

## AI use on this project

The full policy is [AI in this course](https://areweagentsyet.com/ai/). The
evaluation sessions with Copilot's agent are the assignment itself. Any
other AI use, including an agent writing your code, is allowed and
disclosed in `docs/reflection.md`.
