import collections
import enum

import sympy as sym
import numpy

import interval as interval_lib
from intervals import *

CUSTOM_MODULES = [{'sin': intervals_sin, 'cos': intervals_cos, 'exp': intervals_exp, 'ln': intervals_ln}, 'numpy']


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

    diff_func = sym.utilities.lambdify(var, diff, modules=CUSTOM_MODULES)
    second_diff_func = sym.utilities.lambdify(var, second_diff, modules=CUSTOM_MODULES)

    conversion, result = SimpleNewtonInterval(diff_func, second_diff_func, interval, e)
    if classify:
        result = DiffClassification(result, second_diff_func)

        left_end = value_to_intervals(interval[0])
        if diff_func(left_end) > 0:
            left_end_type = Extrema.Minimum
        elif diff_func(left_end) < 0:
            left_end_type = Extrema.Maximum
        else:
            left_end_type = Extrema.Unknown
        left_end_point = CriticalPoint(x=interval[0], interval=left_end[0], type=left_end_type)
        result.append(left_end_point)

        right_end = value_to_intervals(interval[1])
        if diff_func(right_end) > 0:
            right_end_type = Extrema.Maximum
        elif diff_func(right_end) < 0:
            right_end_type = Extrema.Minimum
        else:
            right_end_type = Extrema.Unknown
        right_end_point = CriticalPoint(x=interval[1], interval=right_end[0], type=right_end_type)
        result.append(right_end_point)
    else:
        result.append(Interval.valueToInterval(interval[0]))
        result.append(Interval.valueToInterval(interval[1]))
    return conversion, result


class Extrema(enum.Enum):
    Minimum = enum.auto()
    Maximum = enum.auto()
    Unknown = enum.auto()

    def __str__(self):
        return self.name


CriticalPoint = collections.namedtuple('CriticalPoint', ['x', 'interval', 'type'])


def DiffClassification(critical_points, second_diff):
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
