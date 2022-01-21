from interval import Interval
from interval import sin, cos, exp, log

import math
from copy import deepcopy


class Intervals:
    def __init__(self, intervals):
        self.data = deepcopy(intervals)
        self._iteration_number = 0
        self._normalize()

    def __iter__(self):
        self._iteration_number = 0
        return self

    def __next__(self):
        if self._iteration_number < len(self.data):
            self._iteration_number += 1
            return self.data[self._iteration_number - 1]
        raise StopIteration

    def __repr__(self):
        result = ""
        first = True
        for interval in self:
            if not first:
                result += ' U '
            result += str(interval)
            first = False
        return result

    def width(self):
        result = 0
        for interval in self:
            result += interval.width()
        return result

    def is_in(self, number):
        for interval in self:
            if interval[0] <= number <= interval[1]:
                return True
        return False

    def __add__(self, other):
        result = []
        for interval1 in self:
            for interval2 in value_to_intervals(other):
                result.append(interval1 + interval2)
        return Intervals(result)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        result = []
        for interval1 in self:
            for interval2 in value_to_intervals(other):
                result.append(interval1 - interval2)
        return Intervals(result)

    def __rsub__(self, other):
        other_intervals = value_to_intervals(other)
        return other_intervals.__sub__(self)


    def __neg__(self):
        result = []
        for interval in self:
            result.append(-interval)
        return Intervals(result)

    def __mul__(self, other):
        result = []
        for interval1 in self:
            for interval2 in value_to_intervals(other):
                result.append(interval1 * interval2)
        return Intervals(result)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, power):
        result = []
        for interval in self:
            result.append(interval ** power)
        return Intervals(result)

    def inversed(self):
        result = []
        for interval in self:
            if interval[0] <= 0 <= interval[1]:
                if interval[0] != 0:
                    first = [-math.inf, 1 / interval[0]]
                    result.append(Interval(first))
                if interval[1] != 0:
                    second = [1 / interval[1], math.inf]
                    result.append(Interval(second))
            else:
                result.append(Interval([1 / interval[1], 1 / interval[0]]))
        return Intervals(result)

    def __truediv__(self, other):
        other = value_to_intervals(other)
        return self * other.inversed()

    def __rtruediv__(self, other):
        return other * self.inversed()

    def append(self, interval):
        self.data.append(Interval(interval.x.copy()))
        self._normalize()

    def union(self, intervals):
        intervals = value_to_intervals(intervals)
        for interval in intervals:
            self.data.append(Interval(interval.x.copy()))
        self._normalize()

    def intersect(self, intervals):
        intervals = value_to_intervals(intervals)
        result = []
        for new_interval in intervals:
            for old_interval in self:
                intersection_part = intersection(old_interval, new_interval)
                if intersection_part:
                    result.append(intersection_part)
        self.data = result
        self._normalize()


    def _normalize(self):
        self.data.sort(key=lambda x: x[0])

        normalized = []
        for interval in self:
            if normalized and normalized[-1][1] >= interval[0]:
                normalized[-1][1] = max(normalized[-1][1], interval[1])
            else:
                normalized.append(interval)
        self.data = normalized


def intervals_sin(x):
    if isinstance(x, (int, float, Interval)):
        return sin(x)
    elif isinstance(x, Intervals):

        result = []
        for interval in x:
            result.append(sin(interval))
        return Intervals(result)
    else:
        raise TypeError()


def intervals_cos(x):
    if isinstance(x, (int, float, Interval)):
        return cos(x)
    elif isinstance(x, Intervals):

        result = []
        for interval in x:
            result.append(cos(interval))
        return Intervals(result)
    else:
        raise TypeError()


def intervals_exp(x):
    if isinstance(x, (int, float, Interval)):
        return exp(x)
    elif isinstance(x, Intervals):

        result = []
        for interval in x:
            result.append(exp(interval))
        return Intervals(result)
    else:
        raise TypeError()


def intervals_log(x, base):
    if isinstance(x, (int, float, Interval)):
        return log(x, base)
    elif isinstance(x, Intervals):

        result = []
        for interval in x:
            result.append(log(interval, base))
        return Intervals(result)
    else:
        raise TypeError()


def value_to_intervals(expr):
    if isinstance(expr, Intervals):
        etmp = expr
    elif isinstance(expr, Interval):
        etmp = Intervals([expr])
    else:
        etmp = Intervals([Interval([expr, expr])])
    return etmp


def intersection(first_interval, second_interval):
    result = [max(first_interval[0], second_interval[0]), min(first_interval[1], second_interval[1])]
    if result[0] > result[1]:
        return []
    return Interval(result)



def print_as_points(intervals):
    first = True
    for interval in intervals:
        if not first:
            print(', ', end='')
        first = False
        print(interval.mid(), end='')
    print()
