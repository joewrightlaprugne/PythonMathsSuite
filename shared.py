from math import floor, log, ceil
from Differentiator import *
import math, cmath, ast, operator, re

def roundSF(x, sf=2): # Round to n significant figures
    if type(x) is complex:
        return c_roundSF(x)
    if abs(x) < 0.000001:
        return 0
    try:
        return round(x, sf - int(floor(log(abs(x))))-1)
    except ValueError:
        return 0

def c_roundSF(x, sigfigs=2): # Round both components of a complex number
    return complex(roundSF(x.real, sigfigs), roundSF(x.imag, sigfigs))

def cleanInput(x):
  x = x.replace("ln", "log")

  trigSquared = "(sin|cos|tan)\^2(.*)"
  ts = re.compile(trigSquared)
  tsf = ts.finditer(x)

  for match_ in tsf:
    x = x.replace(match_.group(0), "(" + match_.group(0).replace("^2", "") + ")^2")

  return x

def derivativeAtPoint(f, u, complexFlag=0): # Estimates the derivative at the point u for a complex function f(z)
    x = u + 0.0001
    y2 = evaluateWrapper(f, x, complexFlag)
    x = u - 0.0001
    y1 = evaluateWrapper(f, x, complexFlag)
    return (y2 - y1)/0.0002
        
def solveC(equation, seed):
    side = equation.split("=")
    if len(side) != 2:
        return None
    eq = "(" + side[0] + ") - (" + side[1] + ")"
    x1 = seed
    x0 = seed-2
    c = 0
    while abs(x1-x0) > 0.000001:
        x0 = x1
        x = x0
        try:
            fx0 = evaluateWrapper(eq, x, 1)
            dfx0 = derivativeAtPoint(eq, x0, 1)
        except ZeroDivisionError:
            return None
        except OverflowError:
            return None
        except ValueError:
            return None
        if dfx0 == 0:
            x1 += 0.1
            continue
        if c > 15:
            return None
        x1 = x0 - fx0/dfx0
        c += 1
    x = x1
    yc = evaluateWrapper(side[0], x, 1)
    return x1

def minDistBetweenRoots(f, a, b):
    x = a
    try:
        e = evaluateWrapper(f, x)
    except ZeroDivisionError:
        e = 1000
    except ValueError:
        e = "ERROR"
    while e == "ERROR" or isinstance(e, complex):
        x += 0.01
        if x > b:
            return [-2, -2]
        try:
            e = evaluateWrapper(f, x)
        except ValueError:
            e = "ERROR"
    a = x
    c = 0
    lastroot = 0
    d = []
    for i in range(1, ceil(100*(b-a)) + 1):
        j = a + i/100
        x = j
        try:
            e2 = evaluateWrapper(f, x)
        except ZeroDivisionError:
            e2 = 1000
        except ValueError:
            e2 = "ERROR"
        if isinstance(e2, complex):
            e2 = "ERROR"
        try:
            if e2/e < 0:
                c += 1
                d.append(abs(j - lastroot))
                lastroot = j
        except ZeroDivisionError:
            c += 1
            d.append(abs(j - lastroot))
            lastroot = j
        except TypeError:
            e2 = 1
            e = 1
            continue
        e = e2
    if len(d) == 1:
        return [d[0], c]
    if len(d) == 0:
        return [-1, c]
    return [min(d[1:]), c]


def solveR(equation, seed):
    side = equation.split("=")
    if len(side) != 2:
        return None
    eq = "(" + side[0] + ") - (" + side[1] + ")"
    x1 = seed
    x0 = seed-1
    c = 0
    while abs(x1-x0) > 0.000001:
        x0 = x1
        x = x0
        try:
            fx0 = evaluateWrapper(eq, x)
            dfx0 = derivativeAtPoint(eq, x0)
        except ZeroDivisionError:
            return None
        except OverflowError:
            return None
        except ValueError:
            return None
        if dfx0 == 0 or c > 15:
            return None
        x1 = x0 - fx0/dfx0
        c += 1
    x = x1
    yc = evaluateWrapper(side[0], x)
    return (x1, yc)

def getAllSolsIntervalR(equation, a, b):
    side = equation.split("=")
    if len(side) != 2 or b <= a:
        return None

    asympP = detectAsymp("(" + side[0] + ") - (" + side[1] + ")", a, b)
    asympN = detectAsymp("(" + side[1] + ") - (" + side[0] + ")", a, b)
    if asympP is not None:
        b = asympP
    if asympN is not None:
        a = asympN
    if b-a < 0.01:
        return []
    
    mindist = minDistBetweenRoots("(" + side[0] + ") - (" + side[1] + ")", a, b)
    if mindist[1] == 0:
        return []
    if mindist[1] == 1:
        t = solveR(equation, mindist[0])
        if t is None:
            return []
        else:
            return [t]
    intSize = mindist[0]/2
    maxRoots = mindist[1]
    ints = (b - a)/intSize
    solutions = set()
    roundedSolutions = set()
    c = 0
    for i in range(0, ceil(ints)):
        if c == maxRoots:
            break
        result = solveR(equation, a + i*intSize)
        if result is None:
            continue
        if not (a < result[0] < b):
            continue
        r = roundSF(result[0], 6)
        L = len(roundedSolutions)
        roundedSolutions.add(r)
        if len(roundedSolutions) > L:
            c += 1
            if isinstance(result[0], complex) and isinstance(result[1], complex):
                if result[0].imag == 0 and result[1].imag == 0:
                    solutions.add((result[0].real, result[1].real))
                else:
                    continue
            solutions.add(result)
    if len(solutions) == 0:
        return []
    return solutions

def getAllSolsIntervalC(eq, a, b, ai, bi, s=30): # Find all complex solutions to an equation with real part between x1 and x2, and imaginary part between y1 and y2

    LHS = eq.split("=")[0].strip()
    RHS = eq.split("=")[1].strip()
    intR = round((b-a)/s)
    intC = round((bi-ai)/s)
  
    solutions = set()
    roundedSolutions = set()
    for i in range(0, s):
        for j in range(0, s):
            result = solveC(eq, complex(a + intR*i, ai + intR*j))
            if result is None:
                continue
            if not (a < result.real < b) or not (ai < result.imag < bi):
                continue
            r = c_roundSF(result, 5)
            L = len(roundedSolutions)
            roundedSolutions.add(r)
            if len(roundedSolutions) > L:
                solutions.add(result)
    if len(roundedSolutions) == 0:
        return []
    return roundedSolutions

def getIntersBetweenAllEq(equations, a, b):
    sols = set()
    for i in range(0, len(equations)):
        t = getAllSolsIntervalR(equations[i].func.strip("y = ") + " = 0", a, b)
        sols = sols.union(t)
        x = 0
        try:
            sols.add((0, evaluateWrapper(equations[i].func.strip("y = "), x)))
        except ZeroDivisionError:
            pass
        except ValueError:
            pass
        for j in range(i+1, len(equations)):
            t = getAllSolsIntervalR(equations[i].func.strip("y = ") + " = " + equations[j].func.strip("y = "), a, b)
            sols = sols.union(t)
    return sols

def getIntersSingleEq(equation, equations, a, b):
    sols = set()
    t = getAllSolsIntervalR(equation.func.strip("y = ") + " = 0", a, b)
    sols = sols.union(t)
    x = 0
    try:
        sols.add((0, evaluateWrapper(equation.func.strip("y = "), x)))
    except ZeroDivisionError:
        pass
    except ValueError:
        pass
    for i in equations:
        t = getAllSolsIntervalR(equation.func.strip("y = ") + " = " + i.func.strip("y = "), a, b)
        sols = sols.union(t)
    return sols
    
##############

def evaluateWrapper(f, u, complexMode=0): # Evaluates f(x) at x=u
    if complexMode:
        try:
            return evaluate(f.replace("^", "**").replace("z", "(" + str(u) + ")"), 1)
        except OverflowError:
            return complex(10**10, 10**10)
    else:
        try:
            return evaluate(f.replace("^", "**").replace("x", "(" + str(u) + ")"), 0)
        except OverflowError:
            return 10**10

def evaluate(node, complexMode=0):

    op_map = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.UnaryOp: operator.neg,
    }

    if complexMode:
        func_map = {
            "log": cmath.log,
            "ln": cmath.log,
            "exp": cmath.exp,
            "sqrt": cmath.sqrt,
            "sin": cmath.sin,
            "cos": cmath.cos,
            "tan": cmath.tan,
            "arcsin": cmath.asin,
            "arccos": cmath.acos,
            "arctan": cmath.atan,
            "sinh": cmath.sinh,
            "cosh": cmath.cosh,
            "tanh": cmath.tanh,
            "arsinh": cmath.asinh,
            "arcosh": cmath.acosh,
            "artanh": cmath.atanh,
            "complex": complex
        }
    else:
        func_map = {
            "log": math.log,
            "ln": math.log,
            "exp": math.exp,
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "arcsin": math.asin,
            "arccos": math.acos,
            "arctan": math.atan,
            "sinh": math.sinh,
            "cosh": math.cosh,
            "tanh": math.tanh,
            "arsinh": math.asinh,
            "arcosh": math.acosh,
            "artanh": math.atanh
        }

    const_map = {
        "pi": math.pi,
        "e": math.e,
    }

    if isinstance(node, (list, tuple)):
        return [evaluate(sub_node, complexMode) for sub_node in node]

    elif isinstance(node, str):
        return evaluate(ast.parse(node), complexMode)

    elif isinstance(node, ast.Module):
        values = []
        for body in node.body:
            values.append(evaluate(body, complexMode))
        if len(values) == 1:
            values = values[0]
        return values

    elif isinstance(node, ast.Expr):
        return evaluate(node.value, complexMode)

    elif isinstance(node, ast.BinOp):
        left = evaluate(node.left, complexMode)
        op = node.op
        right = evaluate(node.right, complexMode)

        try:
            return op_map[type(op)](left, right)
        except KeyError:
            return None

    elif isinstance(node, ast.UnaryOp):
        right = evaluate(node.operand)
        return -1*evaluate(node.operand)

    elif isinstance(node, ast.Call):
        func_name = node.func.id
        args = [evaluate(arg, complexMode) for arg in node.args]

        try:
            return func_map[func_name](*args)
        except KeyError:
            return None

    elif isinstance(node, ast.Num):
        return node.n

    elif isinstance(node, ast.Name):
        try:
            return const_map[node.id]
        except KeyError:
            return None

    return None

def verify(expression, complexFlag=0):
    try:
        r = evaluateWrapper(expression, 1, complexFlag)
    except ZeroDivisionError:
        return True
    except ValueError:
        return True
    except SyntaxError:
        return False
    except TypeError:
        return False
    if r is None:
        return False
    if r == []:
        return False
    return True

def detectAsymp(f, a, b):
    r_old = None
    a_old = a
    while r_old is None and a <= b:
        try:
            r_old = evaluateWrapper(f, a)
        except ValueError:
            a += (b-a_old)/20
        except ZeroDivisionError:
            a += (b-a_old)/20
    if r_old is None:
        return None
    a = a_old
    flag = 0
    start = None
    for i in range(1, 20):
        if (not flag) and (abs(r_old) < 0.00001):
            flag = 1
            start = a + (i-1)*(b-a)/20
        try:
            r = evaluateWrapper(f, a + i*(b-a)/20)
        except ValueError:
            r = r_old
            continue
        except ZeroDivisionError:
            r = r_old
            continue
        if flag and abs(r) > abs(r_old):
            flag = 0
            start = None
        r_old = r
    return start
