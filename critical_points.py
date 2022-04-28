import collections
import enum

import sympy as sym
import numpy

import interval as interval_lib
from intervals import *
from sympy_decimal_evaluation import *

CUSTOM_MODULES = [{'sin': intervals_sin, 'cos': intervals_cos, 'exp': intervals_exp, 'log': intervals_log}, 'numpy']


def SimpleNewtonInterval(func, interval_diff, interval, e, _debug=False):
    result = Intervals([interval])

    while result and result.max_width() > e:
        if _debug:
            print(result)
        new_result = Intervals([])
        for result_interval in result:
            area = interval_diff(value_to_intervals(result_interval))
            area = value_to_intervals(area)

            part_to_intersect = -func(value_to_intervals(result_interval.mid()))
            part_to_intersect = value_to_intervals(part_to_intersect) / area
            part_to_intersect = part_to_intersect + value_to_intervals(result_interval.mid())

            result_part = value_to_intervals(result_interval)
            result_part.intersect(part_to_intersect)

            new_result.union(result_part)

        if result == new_result:
            return False, result
        result = new_result

    return True, result


def GetCriticalPoints(func, interval, e, var=sym.Symbol('x'), classify=False):
    diff = sym.diff(func, var)
    second_diff = sym.diff(diff, var)

    f = sym.utilities.lambdify(var, diff, modules=CUSTOM_MODULES)
    # f = lambda value: eval_expression(diff, {'x': value})
    second_diff_func = sym.utilities.lambdify(var, second_diff, modules=CUSTOM_MODULES)
    # second_diff_func = lambda value: eval_expression(second_diff, {'x': value})

    conversion, result = SimpleNewtonInterval(f, second_diff_func, interval, e)
    result.append(Interval.valueToInterval(interval[0]))
    result.append(Interval.valueToInterval(interval[1]))
    if classify:
        result = SecondDiffClassification(result, second_diff_func)
    return conversion, result


class Extrema(enum.Enum):
    Minimum = enum.auto()
    Maximum = enum.auto()
    Unknown = enum.auto()

    def __str__(self):
        return self.name


CriticalPoint = collections.namedtuple('CriticalPoint', ['x', 'interval', 'type'])


def SecondDiffClassification(critical_points, second_diff):
    result = []
    for interval in critical_points:
        value_in_point = second_diff(value_to_intervals(interval))
        if value_in_point > 0:
            point_type = Extrema.Minimum
        elif value_in_point < 0:
            point_type = Extrema.Maximum
        else:
            point_type = Extrema.Unknown

        point = CriticalPoint(x=interval.mid(), interval=interval, type=point_type)
        result.append(point)
    return result


def print_critical_points(critical_points):
    for point in critical_points:
        print(f"Point {point.x}, interval = [{point.interval[0]}, {point.interval[1]}], type = {point.type}")
