"""
data_tools.py
-------------
Handles everything to do with files: generating messy sample data,
cleaning it on load, exporting reports, and logging activity.

PE2 Module 2 & 4 concepts demonstrated:
- random module usage to generate sample data
- Deliberately messy strings (mixed case, stray spaces, odd formatting)
- The Module 2 string-cleaning pipeline: strip -> split -> title -> lower -> int
- File I/O with 'with' blocks (always closes files safely)
- 'w' mode (overwrite) vs 'a' mode (append) used for two different purposes
"""

import os
import random
from datetime import datetime

DATA_DIR = "data"
STUDENTS_FILE = os.path.join(DATA_DIR, "students.txt")
REPORT_FILE = os.path.join(DATA_DIR, "report.txt")
LOG_FILE = os.path.join(DATA_DIR, "activity.log")

# Deliberately messy name pool: mixed case and inconsistent spacing.
# This simulates "real world" dirty data that has to be cleaned on load.
_SAMPLE_NAMES = ["Lisa Rue",
    " John MATHEo",
    "  Michaella Peters",
    " Lebogang Maano  ",
    "Andile WALKER ",
    " Prudence Chia",
    " Kyle Noah ",
    " Masego Lekula ",
    " TINKy Bell  ",
    "  Neo Senametso ",
    " Anele Sander ",
    "  ADAE Moruti ",
]


def generate_data_file(num_records=10):
    """
    Create at least 8 messy student records and write them to
    data/students.txt, one 'name,score' per line.

    Uses random for scores and to pick/duplicate messy names, and
    opens the file with 'w' inside a with block (overwrite mode -
    every call replaces the previous sample file).
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    num_records = max(num_records, 8)  # never generate fewer than 8

    records = []
    for _ in range(num_records):
        name = random.choice(_SAMPLE_NAMES)
        score = random.randint(30, 100)
        # Add an extra stray space before the comma sometimes, to make
        # the cleaning step in load_students() actually necessary.
        separator = " ," if random.random() < 0.5 else ","
        records.append(f"{name}{separator}{score}")

    with open(STUDENTS_FILE, "w") as f:
        for line in records:
            f.write(line + "\n")

    log_event(f"Generated {num_records} sample student records to {STUDENTS_FILE}.")
    return STUDENTS_FILE


def load_students():
    """
    Read data/students.txt and return a clean list of (name, score) tuples.

    This is the Module 2 cleaning pipeline: strip whitespace, split on
    the comma, title-case the name, lower-case it first to normalise
    mixed CAPS, and convert the score to an int. Malformed lines are
    skipped rather than crashing the program.
    """
    if not os.path.exists(STUDENTS_FILE):
        return []

    cleaned = []
    with open(STUDENTS_FILE, "r") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            try:
                name_part, score_part = line.split(",")
                # lower() first normalises mixed CAPS, then title() gives
                # a consistent "Firstname Lastname" style capitalisation.
                # split()/join() also collapses any stray double-spaces
                # left over from the messy source data.
                name = " ".join(name_part.strip().lower().split()).title()
                score = int(score_part.strip())
                cleaned.append((name, score))
            except ValueError:
                # Skip any line that doesn't cleanly split into two parts
                # or whose score isn't a valid integer.
                continue

    log_event(f"Loaded and cleaned {len(cleaned)} student records from {STUDENTS_FILE}.")
    return cleaned


def export_report(text):
    """Write the given text to data/report.txt, overwriting any previous report."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(REPORT_FILE, "w") as f:
        f.write(text)
    log_event(f"Exported report to {REPORT_FILE}.")
    return REPORT_FILE


def log_event(message):
    """
    Append a timestamped line to data/activity.log.

    Uses 'a' (append) mode deliberately - unlike students.txt or
    report.txt, the log should never be overwritten; every call adds
    a new line to the history.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
