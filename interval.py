import math
import sympy


class Interval:

    def __init__(self, x):
        self.x = x.copy()
        self.func = sympy.core.numbers.Number
        self.args = ()

    def __repr__(self):
        return "[" + str(self.x[0]) + ", " + str(self.x[1]) + "]"

    def mid(self):
        return 0.5 * (self.x[0] + self.x[1])

    def width(self):
        return self.x[1] - self.x[0]


    def scale(self, factor):
        m = 0.5 * (self.x[0] + self.x[1])
        r = 0.5 * (self.x[1] - self.x[0])
        self.x[0] = m - factor * r
        self.x[1] = m + factor * r


    def isIn(self, other):
        return (self.x[0] >= other.x[0]) and (self.x[1] <= other.x[1])


    def isNoIntersec(self, other):
        return (self.x[0] > other.x[1]) or (self.x[1] < other.x[0])


    def intersec(self, other):
        if self.x[0] > self.x[1]:
            raise ValueError(other.x[0], other.x[1], "results in wrong bounds:", self.x[0], self.x[1])
        return Interval([max(self.x[0], other.x[0]), min(self.x[1], other.x[1])])

    def __getitem__(self, item):
        return self.x[item]

    def __setitem__(self, key, value):
        self.x.__setitem__(key, value)

    def __neg__(self):
        ninterval = Interval(self.x)
        ninterval.x[0] = - self.x[1]
        ninterval.x[1] = - self.x[0]
        return ninterval

    def __add__(self, other):
        ointerval = valueToInterval(other)
        ninterval = Interval(self.x)
        ninterval.x[0] = self.x[0] + ointerval.x[0]
        ninterval.x[1] = self.x[1] + ointerval.x[1]
        return ninterval

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        ointerval = valueToInterval(other)
        ninterval = Interval(self.x)
        ninterval.x[0] = self.x[0] - ointerval.x[1]
        ninterval.x[1] = self.x[1] - ointerval.x[0]
        return ninterval


    def __rsub__(self, other):
        ointerval = valueToInterval(other)
        return ointerval.__sub__(self)


    def __pow__(self, other):
        ninterval = Interval(self.x)
        u = self.x[0] ** other
        v = self.x[1] ** other
        if other == 0:
            ninterval.x[0] = 1
            ninterval.x[1] = 1
        elif other % 2 == 0:
            ninterval.x[1] = max(u, v)
            if self.x[0] <= 0 and self.x[1] >= 0:
                ninterval.x[0] = 0
            else:
                ninterval.x[0] = min(u, v)
        else:
            ninterval.x[0] = u
            ninterval.x[1] = v
        return ninterval

    def __mul__(self, other):
        ointerval = valueToInterval(other)
        v = [self.x[0] * ointerval.x[0], self.x[0] * ointerval.x[1], self.x[1] * ointerval.x[0], self.x[1] * ointerval.x[1]]
        b = [min(v), max(v)]
        return Interval(b)


    def __truediv__(self, other):
        ointerval = valueToInterval(other)
        v = [self.x[0] / ointerval.x[0], self.x[0] / ointerval.x[1], self.x[1] / ointerval.x[0], self.x[1] / ointerval.x[1]]
        b = [min(v), max(v)]
        return Interval(b)

    def __floordiv__(self, other):
        ointerval = valueToInterval(other)
        if ointerval[0] != 0 and ointerval[1] != 0:
            v = [self.x[0] // ointerval.x[0], self.x[0] // ointerval.x[1], self.x[1] // ointerval.x[0],
                 self.x[1] // ointerval.x[1]]
            print(v)
            b = [min(v), max(v)]
        else:
            ointerval = Interval([0.001, 0.001])
            v = [self.x[0] // ointerval.x[0], self.x[0] // ointerval.x[1], self.x[1] // ointerval.x[0],
                 self.x[1] // ointerval.x[1]]
            print(v)
            b = [min(v), max(v)]
        return Interval(b)

    def __rmul__(self, other):
        return self.__mul__(other)


    def __rtruediv__(self, other):
        return self.__truediv__(other)


def valueToInterval(expr):
    if isinstance(expr, int):
        etmp = Interval([expr, expr])
    elif isinstance(expr, float):
        etmp = Interval([expr, expr])
    else:
        etmp = expr
    return etmp


def sin(x):
    if isinstance(x, int):
        return math.sin(x)
    elif isinstance(x, float):
        return math.sin(x)
    else:
        y = [math.sin(x[0]), math.sin(x[1])]
        pi2 = 2 * math.pi
        pi05 = math.pi / 2
        if math.ceil((x[0] - pi05)/pi2) <= math.floor((x[1] - pi05)/pi2):
            b = 1
        else:
            b = max(y)

        if math.ceil((x[0] + pi05)/pi2) <= math.floor((x[1] + pi05)/pi2):
            a = -1
        else:
            a = min(y)
        return Interval([a,b])


def cos(x):
    if isinstance(x, int):
        return math.cos(x)
    elif isinstance(x, float):
        return math.cos(x)
    else:
        y = [math.cos(x[0]), math.cos(x[1])]
        pi2 = 2 * math.pi
        if math.ceil(x[0]/pi2) <= math.floor(x[1]/pi2):
            b = 1
        else:
            b = max(y)
        if math.ceil((x[0] - math.pi)/pi2) <= math.floor((x[1] - math.pi)/pi2):
            a = -1
        else:
            a = min(y)
        return Interval([a,b])


def exp(x):
    return Interval([math.exp(x[0]), math.exp(x[1])])

def abs(x):
    if x[1] < 0:
        return Interval([-x[0], -x[1]])
    elif x[0] < 0 and x[1] > 0:
        if -x[0] > x[1]:
            return Interval([x[1], -x[0]])
        else:
            return Interval([-x[0], x[1]])
    else:
        return Interval([x[0], x[1]])


def log(x, base):
    if base > 1:
        return Interval([math.log(x[0], base), math.log(x[1], base)])
    else:
        return Interval([math.log(x[1], base), math.log(x[0], base)])


def Intersection(first_interval, second_interval):
    result = [max(first_interval[0], second_interval[0]), min(first_interval[1], second_interval[1])]
    if result[0] > result[1]:
        return []
    return Interval(result)

