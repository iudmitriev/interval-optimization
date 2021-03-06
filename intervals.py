from interval import Interval
from decimal import Decimal

import math
from copy import deepcopy


class Intervals:
    def __init__(self, intervals):
        assert isinstance(intervals, list), "Can create intervals only from list of intervals"
        for interval in intervals:
            assert isinstance(interval, Interval), "Can create intervals only from list of intervals"
        self.data = deepcopy(intervals)
        self._normalize()

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __bool__(self):
        return bool(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def __repr__(self):
        result = ""
        first = True
        for interval in self:
            if not first:
                result += ' U '
            result += str(interval)
            first = False
        return result

    def __eq__(self, other):
        other = value_to_intervals(other)
        if len(self) != len(other):
            return False

        for i in range(0, len(self)):
            if self.data[i] != other.data[i]:
                return False
        return True

    def __gt__(self, other):
        other = value_to_intervals(other)
        for interval1 in self:
            for interval2 in other:
                if not (interval1 > interval2):
                    return False
        return True

    def __lt__(self, other):
        other = value_to_intervals(other)
        for interval1 in self:
            for interval2 in other:
                if not (interval1 < interval2):
                    return False
        return True

    def isAround(self, value):
        for interval in self:
            if interval.isAround(value):
                return True
        return False

    def sum_width(self):
        return sum(interval.width() for interval in self)

    def max_width(self):
        return max(interval.width() for interval in self)

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
        if isinstance(power, Intervals):
            if len(power) != 1:
                raise ValueError("Wrong power")
            power = power.data[0]

        result = []
        for interval in self:
            result.append(interval ** power)
        return value_to_intervals(result)

    def inversed(self):
        result = []
        for interval in self:
            value = Interval([Decimal('1'), Decimal('1')]) / interval

            if isinstance(value[0], Interval):
                result.append(value[0])
                result.append(value[1])
            else:
                result.append(value)
        return Intervals(result)

    def __truediv__(self, other):
        other = value_to_intervals(other)
        result = Intervals([])

        for interval in self:
            for other_interval in other:
                result.union(value_to_intervals(interval / other_interval))
        return result

    def __rtruediv__(self, other):
        other = value_to_intervals(other)
        return other.__truediv__(self)

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
                left_end = max(old_interval[0], new_interval[0])
                right_end = min(old_interval[1], new_interval[1])
                intersection_part = Interval([left_end, right_end])
                if left_end <= right_end:
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
    x = value_to_intervals(x)
    result = [Interval.sin(interval) for interval in x]
    return Intervals(result)


def intervals_cos(x):
    x = value_to_intervals(x)
    result = [Interval.cos(interval) for interval in x]
    return Intervals(result)


def intervals_exp(x):
    x = value_to_intervals(x)
    result = [Interval.exp(interval) for interval in x]
    return Intervals(result)


def intervals_ln(x):
    x = value_to_intervals(x)
    result = [Interval.sin(interval) for interval in x]
    return Intervals(result)


def value_to_intervals(expr):
    if isinstance(expr, Intervals):
        return expr
    elif isinstance(expr, Interval):
        return Intervals([expr])
    elif isinstance(expr, list):
        return Intervals(expr)
    else:
        return Intervals([Interval.valueToInterval(expr)])


def print_as_points(intervals):
    first = True
    for interval in intervals:
        if not first:
            print(', ', end='')
        first = False
        print(interval.mid(), end='')
    print()
