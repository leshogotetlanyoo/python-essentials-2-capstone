"""
models.py
---------
Defines the data model for the Student Analytics Toolkit.

PE2 Module 3 concepts demonstrated:
- A class with __init__, instance variables, and a class variable
- A class-level counter that increments on every instantiation
- Instance methods (get_grade, has_passed)
- The __str__ dunder method for clean, human-readable output
- Inheritance: HonoursStudent extends Student, calls super().__init__,
  and OVERRIDES get_grade() while still falling back to the parent
  implementation with super().get_grade()

This file only DEFINES objects. It does not print, read files, or
run any menu logic - that all happens elsewhere.
"""


class Student:
    """A single student record with a name, ID, and score."""

    # Class variable: shared by every Student instance
    school_name = "Melsoft Academy"

    # Class variable: counts how many Student objects have ever been made
    total_students = 0

    def __init__(self, name, student_id, score):
        self.name = name
        self.student_id = student_id
        self.score = score

        # Every time a Student (or subclass) is created, bump the counter
        Student.total_students += 1

    def get_grade(self):
        """Return a letter/word grade based on the score."""
        if self.score >= 80:
            return "Distinction"
        elif self.score >= 50:
            return "Pass"
        else:
            return "Fail"

    def has_passed(self):
        """Return True if the student's score is a passing score."""
        return self.score >= 50

    def __str__(self):
        return f"{self.student_id}: {self.name} | Score: {self.score} | Grade: {self.get_grade()}"


class HonoursStudent(Student):
    """
    A Student who is also doing an honours research project.

    Demonstrates inheritance: it reuses everything from Student via
    super().__init__, adds one new attribute (research_topic), and
    overrides get_grade() to apply a stricter distinction threshold -
    falling back to the parent's logic when that special case doesn't apply.
    """

    def __init__(self, name, student_id, score, research_topic):
        super().__init__(name, student_id, score)
        self.research_topic = research_topic

    def get_grade(self):
        # Honours students only need 75+ (not 80+) for a distinction,
        # and it gets a special label. Otherwise, fall back to the
        # normal Student grading rules via super().
        if self.score >= 75:
            return "Distinction (Honours)"
        return super().get_grade()

    def __str__(self):
        base = super().__str__()
        return f"{base} | Research Topic: {self.research_topic}"
