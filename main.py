"""
main.py
-------
The Student Analytics Toolkit menu.

This file imports from every other module in the project and wires
them together into one interactive program. It holds almost no logic
of its own - each menu option calls a function or method that already
lives in models.py, data_tools.py, analytics.py, or reporting.py.

Every place user input is converted to a number is wrapped in
try/except, so bad input never crashes the program (see the RED RULE).
"""

from models import Student, HonoursStudent
from data_tools import generate_data_file, load_students, export_report, log_event
from analytics import (
    passing_students,
    make_grader,
    class_average,
    highest_score,
    lowest_score,
    pass_rate,
    scores_via_iterator,
)
from reporting import environment_report, date_report, timed_analysis

# Holds the current in-memory list of Student / HonoursStudent objects,
# populated by menu option 2 and used by every option after it.
students_objects = []


def build_students(raw_records):
    """
    Turn cleaned (name, score) tuples into Student / HonoursStudent
    objects. Every 3rd student is made an HonoursStudent, purely to
    demonstrate the subclass alongside the base class in one run.
    """
    built = []
    for i, (name, score) in enumerate(raw_records, start=1):
        student_id = f"S{i}"
        if i % 3 == 0:
            built.append(HonoursStudent(name, student_id, score, "Independent Research Project"))
        else:
            built.append(Student(name, student_id, score))
    return built


def print_menu():
    print("\n===== STUDENT ANALYTICS TOOLKIT =====")
    print("1. Generate sample data file")
    print("2. Load & clean records from file")
    print("3. View all students")
    print("4. Analyse (averages, pass/fail, top student)")
    print("5. Filter students (generator)")
    print("6. Grade with a custom pass mark (closure)")
    print("7. Environment & date report")
    print("8. Export results to a file")
    print("9. Exit")


def prompt_int(prompt_text):
    """Keep asking until the user types something that parses as an int."""
    while True:
        raw = input(prompt_text)
        try:
            return int(raw)
        except ValueError:
            print("That's not a whole number - please try again.")


def require_loaded_students():
    """Guard used by several menu options that need data loaded first."""
    if not students_objects:
        print("No students loaded yet. Use option 2 to load & clean data first.")
        return False
    return True


def handle_generate():
    path = generate_data_file()
    print(f"Sample data written to {path}")


def handle_load():
    global students_objects
    raw_records = load_students()
    if not raw_records:
        print("No usable data found. Generate a data file first (option 1).")
        return
    students_objects = build_students(raw_records)
    print(f"Loaded and cleaned {len(students_objects)} student records.")
    print(f"(Class variable check: Student.total_students is now {Student.total_students})")


def handle_view():
    if not require_loaded_students():
        return
    for student in students_objects:
        print(student)


def handle_analyse():
    if not require_loaded_students():
        return
    pairs = [(s.name, s.score) for s in students_objects]

    (avg, top, low, rate), elapsed = timed_analysis(
        lambda: (
            class_average(pairs),
            highest_score(pairs),
            lowest_score(pairs),
            pass_rate(pairs),
        )
    )

    print(f"Class average : {avg:.2f}")
    print(f"Highest score : {top[0]} ({top[1]})")
    print(f"Lowest score  : {low[0]} ({low[1]})")
    print(f"Pass rate     : {rate:.1f}%")
    print(f"Scores (via iter/next): {scores_via_iterator(pairs)}")
    print(f"(Analysis completed in {elapsed:.6f} seconds)")


def handle_filter():
    if not require_loaded_students():
        return
    threshold = prompt_int("Show students scoring at or above: ")
    pairs = [(s.name, s.score) for s in students_objects]

    print(f"Students scoring {threshold}+:")
    found_any = False
    for name, score in passing_students(pairs, threshold):
        print(f"  {name}: {score}")
        found_any = True
    if not found_any:
        print("  (no students matched)")


def handle_grade():
    if not require_loaded_students():
        return
    pass_mark = prompt_int("Enter a custom pass mark: ")
    standard_grader = make_grader(pass_mark)
    strict_grader = make_grader(pass_mark + 10)

    print(f"Grading with pass mark {pass_mark} (and {pass_mark + 10} for comparison):")
    for student in students_objects:
        print(
            f"  {student.name}: {standard_grader(student.score)} (pass mark {pass_mark}) "
            f"/ {strict_grader(student.score)} (pass mark {pass_mark + 10})"
        )


def handle_report():
    print(environment_report())
    print()
    target = input("Enter a target date (YYYY-MM-DD) or press Enter to skip: ").strip()
    print(date_report(target if target else None))


def handle_export():
    if not require_loaded_students():
        return
    pairs = [(s.name, s.score) for s in students_objects]

    top_name, top_score = highest_score(pairs)
    low_name, low_score = lowest_score(pairs)

    lines = ["===== STUDENT ANALYTICS REPORT =====", ""]
    lines.extend(str(s) for s in students_objects)
    lines.append("")
    lines.append(f"Class average: {class_average(pairs):.2f}")
    lines.append(f"Highest score: {top_name} ({top_score})")
    lines.append(f"Lowest score : {low_name} ({low_score})")
    lines.append(f"Pass rate    : {pass_rate(pairs):.1f}%")

    report_text = "\n".join(lines)
    path = export_report(report_text)
    print(f"Report exported to {path}")


MENU_ACTIONS = {
    "1": handle_generate,
    "2": handle_load,
    "3": handle_view,
    "4": handle_analyse,
    "5": handle_filter,
    "6": handle_grade,
    "7": handle_report,
    "8": handle_export,
}


def main():
    print("Welcome to the Student Analytics Toolkit!")
    while True:
        print_menu()
        choice = input("Choose an option (1-9): ").strip()

        if choice == "9":
            print("Goodbye!")
            log_event("Program exited normally.")
            break

        action = MENU_ACTIONS.get(choice)
        if action is None:
            print("Invalid option. Please choose a number from 1 to 9.")
            continue

        try:
            action()
        except Exception as exc:  # last-resort safety net so the menu keeps running
            print(f"Something went wrong with that option: {exc}")


if __name__ == "__main__":
    main()
