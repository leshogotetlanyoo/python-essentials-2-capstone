"""
reporting.py
------------
Environment and date/time reporting.

PE2 Module 1 & 4 concepts demonstrated:
- platform and os for environment info
- datetime and calendar for date-based facts
- time for timing how long an analysis takes
"""

import calendar
import datetime
import os
import platform
import time

from data_tools import STUDENTS_FILE


def environment_report():
    """
    Return a multi-line string describing the runtime environment:
    OS, Python version, current working directory, and whether the
    student data file exists (and its size if so).
    """
    lines = [
        f"Operating System : {platform.system()} {platform.release()}",
        f"Python Version   : {platform.python_version()}",
        f"Working Directory: {os.getcwd()}",
    ]

    if os.path.exists(STUDENTS_FILE):
        size_bytes = os.path.getsize(STUDENTS_FILE)
        lines.append(f"{STUDENTS_FILE}      : exists ({size_bytes} bytes)")
    else:
        lines.append(f"{STUDENTS_FILE}      : does not exist yet (use option 1 to generate it)")

    return "\n".join(lines)


def date_report(target_date=None):
    """
    Return a multi-line string with today's date, a timestamp, days
    until an optional target_date (format 'YYYY-MM-DD'), and a couple
    of current-month facts (leap year, days in month).
    """
    now = datetime.datetime.now()
    lines = [
        f"Today's Date : {now.strftime('%A, %d %B %Y')}",
        f"Timestamp    : {now.strftime('%Y-%m-%d %H:%M:%S')}",
    ]

    if target_date:
        try:
            target = datetime.datetime.strptime(target_date, "%Y-%m-%d")
            days_remaining = (target.date() - now.date()).days
            lines.append(f"Days until {target_date}: {days_remaining}")
        except ValueError:
            lines.append(f"Could not parse '{target_date}' - expected format YYYY-MM-DD.")

    year, month = now.year, now.month
    lines.append(f"Leap year ({year})       : {calendar.isleap(year)}")
    lines.append(f"Days in {calendar.month_name[month]} {year}  : {calendar.monthrange(year, month)[1]}")

    return "\n".join(lines)


def timed_analysis(func, *args, **kwargs):
    """
    Run func(*args, **kwargs), timing how long it takes with the
    time module. Returns a tuple of (result, elapsed_seconds).
    """
    start = time.time()
    result = func(*args, **kwargs)
    elapsed = time.time() - start
    return result, elapsed
