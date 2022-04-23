import collections
import enum

import sympy as sym
import numpy

import interval as interval_lib
from intervals import *
from sympy_decimal_evaluation import *

CUSTOM_MODULES = [{'sin': intervals_sin, 'cos': intervals_cos, 'exp': intervals_exp, 'log': intervals_log}, 'numpy']


def SimpleNewtonInterval(func, interval_diff, interval, e, debug=True):
    result = Intervals([interval])

    while result and result.max_width() > e:
        if debug:
            print(result)
        new_result = Intervals([])
        for result_interval in result:
            area = interval_diff(value_to_intervals(result_interval))
            area = value_to_intervals(area)

            part_to_intersect = value_to_intervals(-func(result_interval.mid())) / value_to_intervals(area)
            part_to_intersect = part_to_intersect + value_to_intervals(result_interval.mid())

            result_part = value_to_intervals(result_interval)
            result_part.intersect(part_to_intersect)

            new_result.union(result_part)

        if result == new_result:
            return False, result
        result = new_result

    return True, result


class Extrema(enum.Enum):
    Minimum = enum.auto()
    Maximum = enum.auto()
    Unknown = enum.auto()

    def __str__(self):
        return self.name


def GetCriticalPoints(func, interval, e, var=sym.Symbol('x'), classify=False):
    diff = sym.diff(func, var)
    second_diff = sym.diff(diff, var)

    f = lambda value: eval_expression(diff, {'x': value})
    second_diff_func = lambda value: eval_expression(second_diff, {'x': value})

    conversion, result = SimpleNewtonInterval(f, second_diff_func, interval, e)
    result.append(Interval.valueToInterval(interval[0]))
    result.append(Interval.valueToInterval(interval[1]))

    return conversion, result
