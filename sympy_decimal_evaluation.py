import sympy
from decimal import Decimal
from interval import Interval
from intervals import value_to_intervals, intervals_sin, intervals_cos, intervals_exp, intervals_log


def eval_expression(expression, subs=None):
    if not expression.args:
        if isinstance(expression, sympy.Integer):
            value = int(sympy.N(expression))
            return value_to_intervals(value)
        elif isinstance(expression, (sympy.Float, sympy.Rational)):
            value = Decimal(float(sympy.N(expression)))
            return value_to_intervals(value)
        elif isinstance(expression, sympy.Symbol):
            if subs is None or str(expression) not in subs:
                raise ValueError(f"Unknown symbol without subs {expression}")
            value = subs[str(expression)]
            return value_to_intervals(value)
        else:
            raise NotImplementedError(f'Unknown simple type {type(expression)}')

    if isinstance(expression, sympy.Add):
        result = value_to_intervals(Decimal('0'))
        for leaf in expression.args:
            result += eval_expression(leaf, subs)
        return result

    if isinstance(expression, sympy.Mul):
        result = value_to_intervals(Decimal('1'))
        for leaf in expression.args:
            result *= eval_expression(leaf, subs)
        return result

    if isinstance(expression, sympy.Pow):
        value = eval_expression(expression.args[0], subs)
        base = eval_expression(expression.args[1], subs)
        return value ** base

    if isinstance(expression, sympy.sin):
        value = eval_expression(expression.args[0], subs)
        return intervals_sin(value)

    if isinstance(expression, sympy.cos):
        value = eval_expression(expression.args[0], subs)
        return intervals_cos(value)

    raise NotImplementedError(f'unknown complex type {type(expression)}')


if __name__ == '__main__':
    x = sympy.Symbol('x')

    I = Interval([Decimal(1), Decimal(2)])
    subs = {'x': I}

    expr = 2 * x
    y = eval_expression(expr, subs)
    print(y)

    print("Done!")