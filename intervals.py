from interval import *
import math
from copy import copy, deepcopy


class Intervals:
    def __init__(self, intervals):
        self.data = deepcopy(intervals)
        self._normalize()

    def __repr__(self):
        result = ""
        first = True
        for interval in self.data:
            if not first:
                result += ' U '
            result += str(interval)
            first = False
        return result

    def width(self):
        result = 0
        for interval in self.data:
            result += interval.width()
        return result

    def IsIn(self, number):
        for interval in self.data:
            if interval[0] <= number <= interval[1]:
                return True
        return False

    def __add__(self, other):
        result = []
        for interval1 in self.data:
            for interval2 in valueToIntervals(other).data:
                result.append(interval1 + interval2)
        return Intervals(result)

    def __sub__(self, other):
        result = []
        for interval1 in self.data:
            for interval2 in valueToIntervals(other).data:
                result.append(interval1 - interval2)
        return Intervals(result)

    def __mul__(self, other):
        result = []
        for interval1 in self.data:
            for interval2 in valueToIntervals(other).data:
                result.append(interval1 * interval2)
        return Intervals(result)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, power):
        result = []
        for interval in self.data:
            result.append(interval ** power)
        return Intervals(result)

    def add_number(self, number):
        result = self.data.copy()
        for interval in result:
            interval[0] += number
            interval[1] += number
        return Intervals(result)

    def mul_number(self, number):
        result = self.data.copy()
        for interval in result:
            interval[0] *= number
            interval[1] *= number
            if number < 0:
                interval[0], interval[1] = interval[1], interval[0]

        if number < 0:
            result.reverse()
        return Intervals(result)


    def inversed(self):
        result = []
        for interval in self.data:
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

    def append(self, interval):
        self.data.append(Interval(interval.x.copy()))
        self._normalize()

    def union(self, intervals):
        for interval in intervals.data:
            self.data.append(Interval(interval.x.copy()))
        self._normalize()

    def intersect_with_one_interval(self, interval):
        result = []
        for old_interval in self.data:
            intersection = Intersection(old_interval, interval)
            if intersection:
                result.append(intersection)
        self.data = result
        self._normalize()

    def intersect(self, intervals):
        result = []
        for new_interval in intervals.data:
            for old_interval in self.data:
                intersection = Intersection(old_interval, new_interval)
                if intersection:
                    result.append(intersection)
        self.data = result
        self._normalize()


    def _normalize(self):
        self.data.sort(key=lambda x: x[0])

        normalized = []
        for interval in self.data:
            if normalized and normalized[-1][1] >= interval[0]:
                normalized[-1][1] = max(normalized[-1][1], interval[1])
            else:
                normalized.append(interval)
        self.data = normalized


def valueToIntervals(expr):
    if isinstance(expr, Intervals):
        etmp = expr
    elif isinstance(expr, Interval):
        etmp = Intervals([expr])
    else:
        etmp = Intervals([Interval([expr, expr])])
    return etmp


def printAsPoints(intervals):
    first = True
    for interval in intervals.data:
        if not first:
            print(', ', end='')
        first = False
        print(interval.mid(), end='')
    print()
