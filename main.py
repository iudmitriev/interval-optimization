from critical_points import *
from terminal_colors import *

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
    e = float(m.group(4))
    expected = float(m.group(5))

    critical_points = GetCriticalPoints(expression, interval, e, classify=True)
    if vocal:
        print(f"Expression = {expression}, interval = {interval}, e = {e}")
        print("Critical points are ")
        print_critical_points(critical_points)
        print(f"Expected {expected}")

    if draw:
        f = sym.utilities.lambdify(['x'], expression)
        DrawPoints(critical_points, f, interval)

    for point in critical_points:
        if abs(expected - point.x) < e:
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


def DrawPoints(critical_points, func, interval):
    x = np.linspace(interval[0], interval[1], 1000)
    y = [func(p) for p in x]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, y, label='function')

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

    ax.plot(min_points_x, [func(x) for x in min_points_x], 'o', label='minimum points')
    ax.plot(max_points_x, [func(x) for x in max_points_x], 'o', label='maximum points')
    ax.plot(unknown_points_x, [func(x) for x in unknown_points_x], 'o', label='unknown points')

    ax.legend()
    plt.show()


if __name__ == '__main__':
    RunTests(vocal=True, draw=True)

    if True:
        print("Running all tests...")
        RunTests(file='all_tests.txt', vocal=True, draw=False)
