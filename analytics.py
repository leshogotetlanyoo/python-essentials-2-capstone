"""
analytics.py
------------
The "clever bit": generators, closures, iterators, and statistics
for analysing student data.

PE2 Module 1 & 4 concepts demonstrated:
- A GENERATOR (passing_students) that uses yield, not a return list
- A CLOSURE (make_grader) that returns an inner function which
  remembers the pass_mark it was built with
- Explicit iterator use with iter()/next()
- statistics module usage for class-wide numbers
"""

import statistics


def passing_students(students, pass_mark=50):
    """
    Generator that yields (name, score) one at a time for every
    student whose score meets or beats pass_mark.

    Because this uses 'yield' instead of building and returning a
    list, values are produced lazily, one at a time, as the caller
    asks for them (e.g. in a for-loop).
    """
    for name, score in students:
        if score >= pass_mark:
            yield name, score


def make_grader(pass_mark):
    """
    Closure factory: returns a grader() function that "remembers"
    the pass_mark it was created with, even after make_grader() has
    finished running. Calling make_grader() twice with different
    pass marks produces two independent graders.
    """
    def grader(score):
        return "Pass" if score >= pass_mark else "Fail"

    return grader


def class_average(students):
    """Return the mean score across all students (0 if the list is empty)."""
    if not students:
        return 0.0
    scores = [score for _, score in students]
    return statistics.mean(scores)


def highest_score(students):
    """Return the (name, score) tuple for the top-scoring student."""
    if not students:
        return None
    return max(students, key=lambda pair: pair[1])


def lowest_score(students):
    """Return the (name, score) tuple for the lowest-scoring student."""
    if not students:
        return None
    return min(students, key=lambda pair: pair[1])


def pass_rate(students, pass_mark=50):
    """Return the percentage of students who passed, as a float."""
    if not students:
        return 0.0
    passed = sum(1 for _, score in students if score >= pass_mark)
    return (passed / len(students)) * 100


def scores_via_iterator(students):
    """
    Explicitly demonstrate iter()/next(): manually step through the
    list of scores one at a time using an iterator, rather than a
    for-loop, catching StopIteration when it runs out.
    """
    scores = [score for _, score in students]
    scores_iter = iter(scores)
    collected = []
    while True:
        try:
            collected.append(next(scores_iter))
        except StopIteration:
            break
    return collected
