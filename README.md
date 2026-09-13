# Student Analytics Toolkit

A terminal-based Student Analytics Toolkit that generates sample student
data, cleans it, models it with classes, analyses it, and produces
report and log files — a single menu-driven program that combines
everything from Python Essentials 2 (Modules 1–4) into one project.

## 1. What it does

Run the program and you get a menu that walks through a full data
pipeline: generate messy sample data -> clean it on load -> turn it
into `Student`/`HonoursStudent` objects -> analyse it (averages, pass
rates, filtering) -> report on it (environment, dates) -> export the
results to a file. Every stage is backed by real code, not a stub.

## 2. About this submission

- **Name:** _[TETLANYO O LESHOGO]_
- **Cohort:** 2026 DS Jan Cohort

## 3. Features

- Generates realistic, deliberately messy sample data (mixed case,
  stray spaces) so there's something worth cleaning
- Cleans and parses that data with a string-processing pipeline
- Models students as objects, including an `HonoursStudent` subclass
  with its own grading rule
- Filters students lazily with a generator (`passing_students`)
- Grades students with a closure (`make_grader`) that remembers a
  custom pass mark
- Reports class statistics: average, highest/lowest score, pass rate
- Reports on the runtime environment (OS, Python version) and dates
  (today's date, days until a target date, days in the month)
- Exports a full report to `data/report.txt` and logs every action
  with a timestamp to `data/activity.log`
- Handles bad input everywhere without ever crashing

## 4. How to run

```bash
git clone https://github.com/<your-username>/python-essentials-2-capstone.git
cd python-essentials-2-capstone
pip install -r requirements.txt   # optional — no third-party packages needed
python main.py
```

Then just follow the on-screen menu. Start with option 1 (generate
data), then 2 (load & clean it) — most other options need a loaded
dataset first and will tell you so if you skip ahead.

## 5. Project structure

```
python-essentials-2-capstone/
├── main.py           # The menu loop — imports and wires everything else together
├── models.py          # Student and HonoursStudent classes (the data model)
├── data_tools.py      # Generating, cleaning, exporting, and logging file data
├── analytics.py       # Generator, closure, iterator, and statistics functions
├── reporting.py       # Environment report and date/calendar report
├── requirements.txt   # Dependency list (empty — stdlib only)
├── CONCEPTS.md         # Written explanation of the PE2 concepts used
├── .gitignore          # Keeps generated data files and __pycache__ out of git
└── data/               # Created/filled at runtime (students.txt, report.txt, activity.log)
```

## 6. Concepts demonstrated

| PE2 Concept | Where it lives |
|---|---|
| Classes, `__init__`, instance & class variables | `models.py` — `Student.school_name`, `Student.total_students` |
| Inheritance, `super()`, method overriding | `models.py` — `HonoursStudent` overrides `get_grade()` |
| `__str__` dunder method | `models.py` — both classes print a clean one-line summary |
| File I/O with `with`, `'w'` vs `'a'` mode | `data_tools.py` — `generate_data_file`/`export_report` use `'w'`, `log_event` uses `'a'` |
| String cleaning pipeline (`strip`/`split`/`title`/`lower`/`int`) | `data_tools.py` — `load_students()` |
| Generators (`yield`) | `analytics.py` — `passing_students()` |
| Closures | `analytics.py` — `make_grader()` |
| Iterators (`iter()`/`next()`) | `analytics.py` — `scores_via_iterator()` |
| Standard library: `random`, `statistics` | `data_tools.py`, `analytics.py` |
| Standard library: `platform`, `os` | `reporting.py` — `environment_report()` |
| Standard library: `datetime`, `calendar`, `time` | `reporting.py` — `date_report()`, `timed_analysis()` |
| Modular design, multi-file imports | `main.py` imports from every other file |
| `try`/`except` around all numeric input | `main.py` — `prompt_int()` and the main loop |

## 7. Sample output

Menu, as seen on launch:

```
===== STUDENT ANALYTICS TOOLKIT =====
1. Generate sample data file
2. Load & clean records from file
3. View all students
4. Analyse (averages, pass/fail, top student)
5. Filter students (generator)
6. Grade with a custom pass mark (closure)
7. Environment & date report
8. Export results to a file
9. Exit
Choose an option (1-9):
```

Example output after generating, loading, and viewing students:

```
S1: Peter Pan | Score: 88 | Grade: Distinction
S2: Wendy Darling | Score: 44 | Grade: Fail
S3: Peter Pan | Score: 73 | Grade: Pass | Research Topic: Independent Research Project
S4: Neo Anderson | Score: 61 | Grade: Pass
S5: Trinity Moss | Score: 50 | Grade: Pass
S6: Lisa Smith | Score: 68 | Grade: Pass | Research Topic: Independent Research Project
S7: Tinker Bell | Score: 94 | Grade: Distinction
S8: Wendy Darling | Score: 65 | Grade: Pass
S9: Wendy Darling | Score: 70 | Grade: Pass | Research Topic: Independent Research Project
S10: Captain Hook | Score: 49 | Grade: Fail
```

Example analysis output (option 4):

```
Class average : 66.20
Highest score : Tinker Bell (94)
Lowest score  : Wendy Darling (44)
Pass rate     : 80.0%
Scores (via iter/next): [88, 44, 73, 61, 50, 68, 94, 65, 70, 49]
(Analysis completed in 0.000088 seconds)
```

Example `data/report.txt` (option 8):

```
===== STUDENT ANALYTICS REPORT =====

S1: Peter Pan | Score: 88 | Grade: Distinction
S2: Wendy Darling | Score: 44 | Grade: Fail
S3: Peter Pan | Score: 73 | Grade: Pass | Research Topic: Independent Research Project
S4: Neo Anderson | Score: 61 | Grade: Pass
S5: Trinity Moss | Score: 50 | Grade: Pass
S6: Lisa Smith | Score: 68 | Grade: Pass | Research Topic: Independent Research Project
S7: Tinker Bell | Score: 94 | Grade: Distinction
S8: Wendy Darling | Score: 65 | Grade: Pass
S9: Wendy Darling | Score: 70 | Grade: Pass | Research Topic: Independent Research Project
S10: Captain Hook | Score: 49 | Grade: Fail

Class average: 66.20
Highest score: Tinker Bell (94)
Lowest score : Wendy Darling (44)
Pass rate    : 80.0%
```

Example `data/activity.log`:

```
[2026-09-12 10:15:38] Generated 10 sample student records to data/students.txt.
[2026-09-12 10:15:38] Loaded and cleaned 10 student records from data/students.txt.
[2026-09-12 10:15:38] Exported report to data/report.txt.
[2026-09-12 10:15:38] Program exited normally.
```
