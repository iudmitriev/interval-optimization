import re

import sympy as sym
import numpy

import interval as interval_lib
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

    custom_modules = [{'sin': intervals_sin, 'cos': intervals_cos, 'exp': intervals_exp, 'log': intervals_log}, 'numpy']
    f = sym.utilities.lambdify([var], diff, modules=custom_modules)
    interval_second_diff = sym.utilities.lambdify([var], second_diff, modules=custom_modules)

    result = SimpleNewtonInterval(f, interval_second_diff, interval, e)
    result.append(interval_lib.valueToInterval(interval[0]))
    result.append(interval_lib.valueToInterval(interval[1]))
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
    """
    Принимает тест в формате
    expression = выражение; interval = [левый конец, правый конец]; e = число; expected = число
    И запускает GetCriticalPoints для этого теста, после чего проверяет, что expected попало в множество критических точек

    У vocal 3 возможных значения: None, True и False
    В режиме True функция печатает поданный ей на вход тест и результат вычисления
    В остальных режимах функция ничего не печатает
    """

    test_format = r"expression = ([^;]+); interval = \[([^;,]+), ([^;,]+)\]; e = ([^;]+); expected = ([^;]+)"
    m = re.match(test_format, test)
    expression = sym.parsing.sympy_parser.parse_expr(m.group(1))
    interval = Interval([float(m.group(2)), float(m.group(3))])
    e = float(m.group(4))
    expected = float(m.group(5))

    critical_points = GetCriticalPoints(expression, interval, e)
    if vocal:
        print(f"Expression = {expression}, interval = {interval}, e = {e}")
        print("Critical points are ", end='')
        print_as_points(critical_points)

        print(f"Intervals are {critical_points}")
        print(f"Expected {expected}")

    for point in critical_points.data:
        if abs(expected - point.mid()) < e:
            if vocal:
                print_green("Passed!")
                print()
            return True
    else:
        if vocal:
            print_red(f"Failed!")
            print()
        return False


def RunTests(file='tests.txt', vocal=None):
    """
    Открывает файл file и читает из него тесты в формате
    expression = выражение; interval = [левый конец, правый конец]; e = число; expected = число

    У vocal 3 возможных значения: None, True и False
    В режиме None функция ничего не печатает и выбрасывает AssertionError в случае провала тестов
    В режиме False функция печатает результат тестов
    В режиме True функция печатает каждый тест в отдельности и итоговый результат
    """
    with open(file, 'r') as f:
        tests = f.readlines()
        tests_finished = 0
        tests_not_passed = 0
        tests_fail_to_match = 0
        for line in tests:
            if line[0] == '#' or line[0] == '\n':
                continue

            try:
                if vocal:
                    print_yellow(f"Running test {tests_finished}")
                result = RunTest(line, vocal)
                if not result:
                    tests_not_passed += 1
            except (ValueError, TypeError, AttributeError) as e:
                tests_fail_to_match += 1
                if vocal:
                    print_red(f"Failed to match test {tests_finished}")
                    print_red("Exception:")
                    print(e)
                    print()
            tests_finished += 1


        tests_passed = tests_finished - tests_fail_to_match - tests_not_passed
        if vocal is None:
            if tests_passed != tests_finished:
                raise AssertionError(f"Tests not passed: failed to match {tests_fail_to_match}, failed {tests_not_passed}")
            else:
                return

        if tests_finished != 0:
            print_yellow(f"Run {tests_finished} tests")
            if tests_fail_to_match != 0:
                print_red(f"Failed to match {tests_fail_to_match} tests")

            print_green(f"Passed {tests_passed}")
            if tests_passed != tests_finished:
                print_red(f"Failed {tests_not_passed}")
            else:
                print_green(f"All tests passed")



if __name__ == '__main__':
    RunTests(vocal=True)

    print("Running all tests...")
    RunTests(file='all_tests.txt', vocal=False)
