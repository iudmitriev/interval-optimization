import collections
import enum

import sympy as sym
import numpy

import interval as interval_lib
from intervals import *

ACCURACY = 1e-9

def is_zero(value):
    if abs(value) < ACCURACY:
        return True
    return False


def SimpleNewtonInterval(func, interval_diff, interval, e):
    found_zeros = Intervals([])
    result = Intervals([interval])

    while result and result.max_width() > e:
        new_result = Intervals([])
        for result_interval in result:
            area = interval_diff(value_to_intervals(result_interval))
            area = value_to_intervals(area)

            if is_zero(func(result_interval.mid())) and area.is_in(0):
                x = result_interval.mid()
                found_zeros.append(Interval([x - e / 4, x + e / 4]))

                result_part = Intervals([])
                result_part.append(Interval([result_interval[0], x - e/4]))
                result_part.append(Interval([x + e/4, result_interval[1]]))
            else:
                part_to_intersect = value_to_intervals(area).inversed()
                part_to_intersect = part_to_intersect * value_to_intervals(-func(result_interval.mid()))
                part_to_intersect = part_to_intersect + value_to_intervals(result_interval.mid())

                result_part = Intervals([result_interval])
                result_part.intersect(part_to_intersect)

            new_result.union(result_part)
        result = new_result

    result.union(found_zeros)
    return result


class Extrema(enum.Enum):
    Minimum = enum.auto()
    Maximum = enum.auto()
    Unknown = enum.auto()

    def __str__(self):
        return self.name


CriticalPoint = collections.namedtuple('CriticalPoint', ['x', 'delta', 'type'])


def SecondDiffClassification(critical_points, second_diff):
    result = []
    for interval in critical_points:
        if second_diff(interval.mid()) > ACCURACY:
            point_type = Extrema.Minimum
        elif second_diff(interval.mid()) < ACCURACY:
            point_type = Extrema.Maximum
        else:
            point_type = Extrema.Unknown

        point = CriticalPoint(x=interval.mid(), delta=interval.width()/2, type=point_type)
        result.append(point)
    return result


def print_critical_points(critical_points):
    for point in critical_points:
        print(f"Point {point.x} ± {point.delta}, type = {point.type}")


def GetCriticalPoints(func, interval, e, var=sym.Symbol('x'), classify=False):
    diff = sym.diff(func, var)
    second_diff = sym.diff(diff, var)

    custom_modules = [{'sin': intervals_sin, 'cos': intervals_cos, 'exp': intervals_exp, 'log': intervals_log}, 'numpy']
    f = sym.utilities.lambdify([var], diff, modules=custom_modules)
    second_diff_func = sym.utilities.lambdify([var], second_diff, modules=custom_modules)

    result = SimpleNewtonInterval(f, second_diff_func, interval, e)
    result.append(interval_lib.valueToInterval(interval[0]))
    result.append(interval_lib.valueToInterval(interval[1]))

    if classify:
        result = SecondDiffClassification(result, second_diff_func)
    return result


def GetGlobalMinimum(func, interval, e, var=sym.Symbol('x')):
    extremums = GetCriticalPoints(func, interval, e)
    f = sym.utilities.lambdify([var], func)

    global_minimum_point = interval[0]
    for interval in extremums:
        if f(global_minimum_point) > f(interval.mid()):
            global_minimum_point = interval.mid()
    return global_minimum_point
