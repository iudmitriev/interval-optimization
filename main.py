import re

import sympy as sym

from interval import *
from intervals import *
from terminal_colors import *


def SimpleNewtonInterval(func, interval_diff, interval, e):
    result = Intervals([interval])

    while result.width() > e:
        new_result = Intervals([])
        for result_interval in result.data:
            area = interval_diff(Intervals([result_interval]))

            part_to_intersect = value_to_intervals(area).inversed()
            part_to_intersect = part_to_intersect * value_to_intervals(-func(result_interval.mid()))
            part_to_intersect = part_to_intersect + value_to_intervals(result_interval.mid())

            result_part = Intervals([result_interval])
            result_part.intersect(part_to_intersect)

            new_result.union(result_part)
        result = new_result
    return result


def GetCriticalPoints(func, interval, e, var=sym.Symbol('x')):
    diff = sym.diff(func, var)
    second_diff = sym.diff(diff, var)

    f = sym.utilities.lambdify([var], diff)
    interval_second_diff = sym.utilities.lambdify([var], second_diff)

    result = SimpleNewtonInterval(f, interval_second_diff, interval, e)
    result.append(valueToInterval(interval[0]))
    result.append(valueToInterval(interval[1]))
    return result


def GetGlobalMinimum(func, interval, e, var=sym.Symbol('x')):
    extremums = GetCriticalPoints(func, interval, e)
    f = sym.utilities.lambdify([var], func)

    global_minimum_point = interval[0]
    for interval in extremums.data:
        if f(global_minimum_point) > f(interval.mid()):
            global_minimum_point = interval.mid()
    return global_minimum_point


def RunTest(test, vocal=None):
    '''

    :param test:
    :param vocal:
    :return:
    '''

    test_format = r"expression = ([^;]+); interval = \[([^;,]+), ([^;,]+)\]; e = ([^;]+); expected = ([^;]+)"
    m = re.match(test_format, test)
    expression = sym.parsing.sympy_parser.parse_expr(m.group(1))
    interval = Interval([float(m.group(2)), float(m.group(3))])
    e = float(m.group(4))
    expected = float(m.group(5))

    critical_points = GetCriticalPoints(expression, interval, e)
    if vocal is not None:
        print(f"Expression = {expression}, interval = {interval}, e = {e}")
        print("Critical points are ", end='')
        print_as_points(critical_points)

        if vocal:
            print(f"Intervals are {critical_points}")
        print(f"Expected {expected}")

    if critical_points.is_in(expected):
        if vocal is not None:
            print_green("Passed!")
            print()
        return True
    else:
        if vocal is not None:
            print_red(f"Failed!")
            print()
        return False


def RunTests(file='tests.txt', vocal=None):
    with open(file, 'r') as f:
        tests = f.readlines()
        tests_finished = 0
        tests_not_passed = 0
        tests_fail_to_match = 0
        for line in tests:
            if line[0] == '#' or line[0] == '\n':
                continue

            try:
                if vocal is not None:
                    print_yellow(f"Running test {tests_finished}")
                result = RunTest(line, vocal)
                if not result:
                    tests_not_passed += 1
            except (ValueError, TypeError, AttributeError):
                tests_fail_to_match += 1
                if vocal is not None:
                    print_red(f"Failed to match test {tests_finished}")
                raise
            tests_finished += 1

        print_yellow(f"Run {tests_finished} tests")
        if tests_fail_to_match != 0:
            print_red(f"Failed to match {tests_fail_to_match} tests")

        tests_passed = tests_finished - tests_fail_to_match - tests_not_passed
        print_green(f"Passed {tests_passed}")
        if tests_passed != tests_finished:
            print_red(f"Failed {tests_not_passed}")
        else:
            print_green(f"All tests passed")



if __name__ == '__main__':
    RunTests(vocal=True)
