import re

from critical_points import *
from terminal_colors import *

from decimal import Decimal

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def RunTest(test, vocal=None, draw=False):
    """
    Принимает тест в формате
    expression = выражение; interval = [левый конец, правый конец]; e = число; expected = число
    И запускает GetCriticalPoints для этого теста, после чего проверяет,
    что expected попало в множество критических точек

    У vocal 3 возможных значения: None, True и False
    В режиме True функция печатает поданный ей на вход тест и результат вычисления
    В остальных режимах функция ничего не печатает
    """

    test_format = r"expression = ([^;]+); interval = \[([^;,]+), ([^;,]+)\]; e = ([^;]+); expected = ([^;]+)"
    m = re.match(test_format, test)
    expression = sym.parsing.sympy_parser.parse_expr(m.group(1))
    interval = Interval([float(m.group(2)), float(m.group(3))])
    e = Decimal(m.group(4))
    expected = Decimal(m.group(5))

    conversion, critical_points = GetCriticalPoints(expression, interval, e / 10, classify=False)
    if vocal:
        print(f"Expression = {expression}, interval = {interval}, e = {e}")
        print(f"Expected {expected}")
        if not conversion:
            print_red("No real result")

    if draw:
        DrawPoints(critical_points, expression, interval)

    for interval in critical_points:
        if vocal:
            print(f'interval [{interval[0]}, {interval[1]}]')
        if interval.isAround(expected) or abs(interval.mid() - expected) < e:
            if vocal:
                print_green("Passed!")
                print()
            return True
    else:
        if vocal:
            print_red(f"Failed!")
            print()
        return False


def RunTests(file='tests.txt', vocal=None, draw=False):
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
                result = RunTest(line, vocal, draw)
                if not result:
                    tests_not_passed += 1
            except (ValueError, TypeError, AttributeError) as e:
                tests_fail_to_match += 1
                if vocal:
                    print_red(f"Failed to match test {tests_finished}")
                    print_red("Exception:")
                    print(e)
                    print()

                if vocal is None:
                    raise
            tests_finished += 1


        tests_passed = tests_finished - tests_fail_to_match - tests_not_passed
        if vocal is None:
            if tests_passed != tests_finished:
                raise AssertionError(f"Tests not passed: failed to match {tests_fail_to_match}, "
                                     f"failed {tests_not_passed}")
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


def DrawPoints(critical_points, expression, interval):
    func = sym.utilities.lambdify(['x'], expression)
    x = np.linspace(interval[0], interval[1], 1000)
    y = list(map(func, x))

    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(x, y, color='b', label=str(expression))

    min_points_x = []
    max_points_x = []
    unknown_points_x = []
    for p in critical_points:
        if p.type == Extrema.Minimum:
            min_points_x.append(p.x)
        elif p.type == Extrema.Maximum:
            max_points_x.append(p.x)
        else:
            unknown_points_x.append(p.x)

    ax.scatter(min_points_x, list(map(func, min_points_x)), color='r', label='minimum points')
    ax.scatter(max_points_x, list(map(func, max_points_x)), color='g', label='maximum points')
    ax.scatter(unknown_points_x, list(map(func, unknown_points_x)), color='y', label='unknown points')

    ax.legend()
    plt.show()


if __name__ == '__main__':
    if True:
        RunTests(vocal=True, draw=False)

    if False:
        print("Running all tests...")
        RunTests(file='all_tests.txt', vocal=None, draw=False)
