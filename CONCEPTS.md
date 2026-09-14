# Concepts

## Which PE2 module does each file draw on, and how?

- **`models.py` — Module 3 (OOP).** Defines `Student` with `__init__`,
  instance attributes (`name`, `student_id`, `score`), a class
  variable (`school_name`), a class-level counter (`total_students`),
  and methods (`get_grade`, `has_passed`, `__str__`). `HonoursStudent`
  inherits from `Student`, calls `super().__init__()` to reuse the
  parent's setup, and overrides `get_grade()`.
- **`data_tools.py` — Modules 2 & 4 (strings & files).** `generate_data_file()`
  uses `random` to build messy records; `load_students()` runs them
  through the Module 2 cleaning pipeline (`strip` -> `split` -> `lower`
  -> `title` -> `int`); `export_report()` and `log_event()` do file
  writing, one in `'w'` mode and one in `'a'` mode.
- **`analytics.py` — Modules 1 & 4 (generators/closures/stdlib).**
  `passing_students()` is a generator (`yield`); `make_grader()` is a
  closure; `scores_via_iterator()` uses `iter()`/`next()` explicitly;
  the statistics functions use the `statistics` module.
- **`reporting.py` — Modules 1 & 4 (stdlib).** `environment_report()`
  uses `platform` and `os`; `date_report()` uses `datetime` and
  `calendar`; `timed_analysis()` uses `time`.
- **`main.py` — everything.** Imports from all four files above and
  wires each menu option to a function/method that already exists
  elsewhere, plus its own `try`/`except` input handling.

## Why is splitting the program across several files better than one big file?

Because each file has one job. If I need to fix how scores get
graded, I open `models.py` and I'm not scrolling past file-reading
code or menu text to find it. It also means the pieces can be tested
and reasoned about independently — I could test `analytics.py`'s
`make_grader()` on its own, with no file I/O or user input involved
at all. And because `main.py` only *imports and calls* the other
modules rather than repeating their logic, if a rule changes (say,
the pass mark for distinctions), it only needs to change in one
place. A single 300-line file would make all of that harder: more
scrolling, more risk of two copies of the same logic drifting apart,
and a much messier `git diff` every time I touched one small thing.

## Class vs object; generator vs normal function; closure; 'w' vs 'a'

**Class vs object.** `Student` in `models.py` is the *class* — a
blueprint that says every student has a name, ID, score, and a
`get_grade()` method. Each time `main.py` calls
`Student(name, student_id, score)` inside `build_students()`, that
creates one *object*: a specific student with its own values, like
`S3: Mary-Anne Peters | Score: 71 | Grade: Pass`. The class is the
recipe; the object is the actual meal.

**Generator vs normal function.** A normal function like
`class_average()` runs top to bottom and returns one value, then it's
done. `passing_students()` in `analytics.py` is a generator: it uses
`yield` instead of `return`, so calling it doesn't run the whole
function immediately — it hands back an object that produces one
`(name, score)` pair at a time, only when something asks for the next
one (like the `for` loop in `handle_filter()`). That matters for
memory: with a huge dataset, a generator never holds the whole
filtered list in memory at once.

**Closure.** `make_grader(pass_mark)` in `analytics.py` returns an
inner function, `grader`, which uses `pass_mark` even though
`make_grader()` has already finished running. In `handle_grade()` in
`main.py`, I call `make_grader(pass_mark)` and `make_grader(pass_mark + 10)`
to get two independent graders that each "remember" a different pass
mark — that's the closure keeping its own private copy of the
variable from the moment it was created.

**`'w'` vs `'a'` file modes.** `generate_data_file()` opens
`data/students.txt` with `'w'`, which means: erase whatever was there
before and start fresh — appropriate because every run should produce
one clean batch of sample data, not students piling up from every
previous run. `log_event()` opens `data/activity.log` with `'a'`,
which means: keep everything that was already there and add the new
line at the end — appropriate because the log is meant to be a
running history of everything the program has ever done, not just
the most recent action.

## What was the hardest part of combining four modules into one program, and how did you solve it?

Keeping `main.py` "thin." It would have been easy to write the
analysis or grading logic directly inside the menu loop, since that's
where the numbers are needed. Instead, every calculation lives in
`analytics.py` or `reporting.py`, and `main.py`'s handler functions
(like `handle_analyse()`) just call those functions and print the
results. The trick that made this manageable was building the
files bottom-up in the order suggested in the brief — `models.py`
first, then `data_tools.py`, then `analytics.py`, then `reporting.py`
— and testing each one on its own (e.g. calling `make_grader(50)(70)`
directly in a scratch script) *before* wiring it into the menu. By
the time `main.py` existed, every function it needed to call already
worked, so `main.py` really did end up being mostly a menu loop and
some `try`/`except` blocks, exactly as the brief asks for.
