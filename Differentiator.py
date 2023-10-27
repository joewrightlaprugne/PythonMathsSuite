import re
global simplify, undosubs

def undosubs(output, sub):
    c = 0
    for currentSub in sub:
        output = output.replace(chr(c+65), currentSub)
        c += 1
    return output

def applyBrackets(x):
    lastBracket = ""
    for i in range(0, len(x)):
        if x[i] == "(":
            lastBracket = "("
            continue
        if x[i] in ["+", "-", "/"] and lastBracket == "":
            return "(" + x + ")"
    lastBracket = ""
    for i in range(len(x)-1, -1, -1):
        if x[i] == ")":
            lastBracket = ")"
            continue
        if x[i] in ["+", "-", "/"] and lastBracket == "":
            return "(" + x + ")"
    return x

def simplify(output, sub=[]):
    output = undosubs(output, sub)
    output = output.replace("(0)", "0")
    output = output.replace("--", "")

    for i in re.compile("(\+|\-)0([A-Z]|[a-z]|\*|\+|\-|\/|\^|\)|\(|$)").finditer(output):
        G = i.group()
        output = output.replace(G, G[2:])
    
    return output

def D(f, sub=[], rec=0):

    if f.count("(") != f.count(")") or type(f) is not str:
        print(f, "is an invalid function")
        return

    f = f.strip()
    indent = "  "
    f0 = f

    #########################################################################
    # Input processing section: modifies the input so that it can be processed by the rest of the algorithm
    #########################################################################

    def groupSize(x):
        return len(x.group())

    for i in sorted(re.compile("(((ar)?c?(sin|cos|tan)h?)|e(h|x)p|sqrt|ln)\(.*\)\^(\-?\d+(\.\d+)?|(\((x|\+|\-|\/|[A-Z]|\d|\^|\*|\s|[a-z]|\(x\))+\)))").finditer(f), key=groupSize, reverse=True): # func(x)^2 => (func(x))^2 (SLOP)
        G = i.group()
        if G.count("(") != G.count(")"):
            break
        L = 0
        c = 0
        for char in G:
            if char == "(":
                L += 1
            if char == ")":
                L -= 1
            if char == "^" and L == 0:
                f = f.replace(G, "(" + G[:c] + ")" + G[c:])
            c += 1

##    for i in sorted(re.compile("e\^([a-z]|[A-Z]|\^|\*|\(|\))*").finditer(f), key=GroupSize, reverse=True): # e^f(x) => exp(f(x))
##        G = i.group()
##        if G[1] != "(" and G.count("(") == G.count(")"):
##            print(G)
    
##    print("Input:", f)
##    print("Subs:", sub, rec+1)

    #########################################################################
    # The basic derivative section: handles c*F(x) where F(x) is a basic function like trig, exp, polynomial and c is a real number
    #########################################################################

    ################# TRIG FUNCTIONS + EXP + SQRT #################
    if re.compile("\-?(\d+(\.\d+)?\*)?(((ar)?c?(sin|cos|tan)h?)|e(h|x)p|sqrt)\(x\)$").match(f): # c*sin(x)
        dx = {
            "sin": "cos(x)",
            "cos": "sin(x)",
            "tan": "/((cos(x))^2)",
            "sinh": "cosh(x)",
            "cosh": "sinh(x)",
            "tanh": "/((cosh(x))^2)",
            "arcsin": "/(sqrt(1 - x^2))",
            "arccos": "/(sqrt(1 - x^2))",
            "arctan": "/(1 + x^2)",
            "arsinh": "/(sqrt(1 + x^2))",
            "arcosh": "/(sqrt(x^2 - 1))",
            "artanh": "/(1 - x^2)",
            "exp": "exp(x)",
            "sqrt": "/(2*sqrt(x))"
        }
        part = f.split("*")
        func = part[-1].split("(")[0]
        c = part[0]
        newfunc = dx[func]
        if len(part) != 1:
            if newfunc[0] == "/":
                r = str(c) + newfunc
            else:
                r = str(c) + "*" + newfunc
        else:
            if func not in ["sin", "cos", "sinh", "cosh", "exp"]:
                r = "1" + newfunc
                newfunc = "1" + newfunc
            else:
                r = newfunc
        if newfunc == "/(sqrt(1 - x^2))" or newfunc == "/(2*sqrt(x))" or newfunc == "sin(x)":
            if newfunc == "sin(x)":
                r = "-" + r
                newfunc = "-" + newfunc
            else:
                newfunc = "1" + newfunc
        r = simplify(r, sub)
        print(indent*rec, "Standard derivative: d/dx[ " + func + "(x) ] = " + newfunc)
        print(indent*rec, "d/dx[ " + f + " ] = " + r)
        return r
    
    ################# POLYNOMIALS #################
    if f == "x":
        return "1"
    if f == "-x":
        return "-1"
    if re.compile("\-?(\d+(\.\d+)?\*)?x$").match(f): # c*x
        print(indent*rec, "Standard derivative: d/dx[x] = 1")
        print(indent*rec, "d/dx[ " + f + " ] = " + f[:-2])
        return f[:-2]
    if re.compile("\-?x\*(\d+(\.\d+)?)").match(f): # x*c
        print(indent*rec, "Standard derivative: d/dx[x] = 1")
        print(indent*rec, "d/dx[ " + f + " ] = " + f[2:])
        return f[2:]
    if re.compile("\-?(\d+(\.\d+)?\\/)?x$").match(f): # c/x
        r = "-" + f[:-2] + "/(x^2)"
        print(indent*rec, "Power rule: d/dx[1/x] = d/dx[x^-1] = -x^-2 = -1/x^2")
        print(indent*rec, "d/dx[ " + f + " ] = " + r)
        return r
    if re.compile("\-?x\\/(\d+(\.\d+)?)").match(f): # x/c
        r = f.replace("x", "1")
        print(indent*rec, "Standard derivative: d/dx[x] = 1")
        print(indent*rec, "d/dx[ " + f + " ] = " + r)
        return r
    try: ## c (constant)
        float(f.strip("()").strip("-").strip("()"))
        print(indent*rec, "Standard derivative: d/dx[c] = 0")
        print(indent*rec, "d/dx[ " + f + " ] = 0")
        return "0"
    except ValueError:
        pass
    if re.compile("\-?(\d+(\.\d+)?\*)?x\^\-?\d+(\.?\d+|$)").match(f): # c*x^n
        try:
            c = float(f.split("*x^")[0])
        except ValueError:
            c = 1
        if f.split("x")[0] == "-":
            c = -1
        n = float(f.split("^")[1])
        newc = c*n
        if newc.is_integer():
            newc = int(newc)
            if newc == 1:
                newc = ""
        if n.is_integer():
            n = int(n)-1
            if n == 0:
                r = str(newc)
            if n == 1:
                r = str(newc) + "*x"
            if n > 1:
                r = str(newc) + "*x^" + str(n)
        else:
            r = str(newc) + "*x^" + str(n-1)
        print(indent*rec, "Power rule: d/dx[x^n] = n*x^(n-1)")
        print(indent*rec, "d/dx[ " + f + " ] = " + r)
        return r

    ################# EXPONENTIAL/LOGARITHMIC #################
    if re.compile("\-?(\d+(\.\d+)?\*)?\-?\d+(\.?\d+)?\^\(?x\)?").match(f): # c*n^x
        r = "ln(" + f.split("^")[0].split("*")[-1] + ")*" + f
        print(indent*rec, "Exponential rule: d/dx[n^x] = ln(n)*n^x")
        print(indent*rec, "d/dx[ " + f + " ] = " + r)
        return r
    if re.compile("\-?(\d+(\.\d+)?\*)?ln\(x\)$").match(f): # c*ln(x)
        if len(f[:-6]) == 0:
            c = 1
        else:
            c = f[:-6]
        r = str(c) + "/x"
        print(indent*rec, "Standard derivative: d/dx[ln(x)] = 1/x")
        print(indent*rec, "d/dx[ " + f + " ] = " + r)
        return str(c) + "/x"
    
    #########################################################################
    # The chain rule section: handles stuff like c*sin(A), c*A, c*A^n, etc.
    #########################################################################

    if re.compile("\-?(\d+(\.\d+)?\*)?(((ar)?c?(sin|cos|tan)h?)|e(h|x)p|sqrt)\([A-Z]\)$").match(f): # c*g(f(x)) => c*f'(x)*g'(f(x))
        part = f.split("*")
        func = part[-1].split("(")[0] + "("
        print(indent*rec, "Chain rule: d/dx[ f(g(x)) ] = g'(x)*f'(g(x))")
        part = f.split(func)[1][:-1]
        
        D0 = D(sub[ord(part)-65], sub, rec+1)
        D1 = D(f.replace(part, "x"), sub, rec+1).replace("exp", "ehp").replace("x", sub[ord(part)-65]).replace("ehp", "exp")
        if D0 == "1":
            print(indent*rec, "d/dx[ " + f + " ] = " + D1)
            return simplify(D1, sub)
        if D1 == "1":
            print(indent*rec, "d/dx[ " + f + " ] = " + D0)
            return simplify(D0, sub)
        D0 = applyBrackets(D0)
        D1 = applyBrackets(D1)
            
        r = D0 + "*" + D1
        print(indent*rec, "d/dx[ " + f + " ] = " + undosubs(r, sub))
        return simplify(r, sub)
    if re.compile("\-?(\d+(\.\d+)?\*)?ln\([A-Z]\)$").match(f): # c*ln(f)
        print(indent*rec, "Chain rule: d/dx[ f(g(x)) ] = g'(x)*f'(g(x))")
        part = f.split("ln(")[1][:-1]
        D0 = D(sub[ord(part)-65], sub, rec+1)
        D1 = D(f.replace(part, "x"), sub, rec+1).replace("exp", "ehp").replace("x", sub[ord(part)-65]).replace("ehp", "exp")

        D0 = applyBrackets(D0)
        D1 = applyBrackets(D1)
        r = D0 + "*" + D1
        if D0 == "1":
            r = D1
        if D1 == "1":
            r = D0
        if D0 == "0" or D1 == "0":
            r = "0"

        print(indent*rec, "d/dx[ " + f + " ] = " + r)
        return r
    if re.compile("^(\d+(\.\d+)?\*)?\(?[A-Z]\)?$").match(f): # c*(f), c*f
        part = f.split("*")
        for char in f:
            if char.isalpha():
                r = simplify(D(sub[ord(char)-65], sub, rec+1), sub)
                return r
    if re.compile("^\-?(\d+(\.\d+)?\*)?\(?[A-Z]\)?$").match(f): # (f)/c, f/c
        part = f.split("/")
        for char in f:
            if char.isalpha():
                r = simplify(D(sub[ord(char)-65], sub, rec+1) + "/" + part[1], sub)
                return r
    if re.compile("^\-?(\d+(\.\d+)?\/)?\(?[A-Z]\)?$").match(f): # c/(f), c/f
        for char in f:
            if char.isalpha():
                part = f.split("/")
                D0 = part[0]
                D1 = applyBrackets(D(sub[ord(char)-65], sub, rec+1))
                D2 = applyBrackets(part[1])
                r = "-" + D0 + "*" + D1 + "/" + D2 + "^2"

                if D0 == "0":
                    r = "0"
                if D0 == "1":
                    r = D1 + "/" + D2 + "^2"
                return r
    if re.compile("^\-?\(?(\d+(\.\d+)?\*)?[A-Z]\)?\^\d+(\.?\d+|$)").match(f): # c*(f)^n, c*f^n
        for char in f:
            if char.isalpha():
                part = f.split("^")
                D0 = str(part[1])
                D1 = applyBrackets(D(sub[ord(char)-65], sub, rec+1))
                D2 = part[0]
                D3 = str(int(part[1])-1)
                r = D0 + "*" + D1 + "*" + D2 + "^" + D3

                if D0 == "0":
                    r = "0"
                if D3 == "0":
                    r = D0 + "*" + D1
                if D3 == "1":
                    D0 + "*" + D1 + "*" + D2
                return r
    if re.compile("\-?(\d+(\.\d+)?\*)?\-?\d+(\.?\d+)?\^\(?[A-Z]\)?").match(f): # c*n^(f), c*n^f
        part = f.split("^")[1].strip("()")
        D0 = applyBrackets(D(sub[ord(part)-65], sub, rec+1))
        D1 = f.split("^")[0].split("*")[-1]
        r = D0 + "*ln(" + D1 + ")*" + f

        if D0 == "0":
            r = "0"
        if D0 == "1":
            r = "ln(" + D1 + ")*" + f
        
        c = 0
        for currentSub in sub:
            r = r.replace(chr(c+65), currentSub)
            c += 1
        r = simplify(r, sub)
        return r

    #########################################################################
    # Substituting section: does stuff like sin(cos(x^2) + 1) => sin(A)
    #########################################################################
    
    L = 0
    c = len(sub)
    thisSub = ""
    for char in f:
        if char == ")":
            L -= 1
            if not L and len(thisSub) > 1:
                f = f.replace(thisSub, chr(c+65))
                sub.append(thisSub)
                c += 1
                thisSub = ""
            if not L and len(thisSub) == 1:
                thisSub = ""
        if L > 0:
            thisSub += char
        if char == "(":
            L += 1

    #########################################################################
    # Product/quotient/exponent rule section: only applies to one-part functions (not a sum of other functions)
    #########################################################################
    
    if " + " not in f and " - " not in f:
        # The product rule section: handles f(x)*g(x)
        multpos = f.find("*")
        if multpos > -1:
            first = f[:multpos]
            last = f[multpos+1:]
            D0 = D(first, sub, rec+1)
            D1 = D(last, sub, rec+1)
            print(indent*rec, "Product rule: d/dx[f(x)*g(x)] = f'(x)*g(x) + f(x)*g'(x)")
            print(indent*rec, "d/dx[" + first + "*" + last + "] = d/dx[" + first + "]*" + last + " + d/dx[" + last + "]*" + first)

            D0 = applyBrackets(D0)
            D1 = applyBrackets(D1)
            r = first + "*" + D1 + " + " + last + "*" + D0
            if D0 == "1":
                r = first + "*" + D1 + " + " + last
            if D1 == "1":
                r = first + " + " + last + "*" + D0
            if D0 == "0":
                r = first + "*" + D1
            if D1 == "0":
                r = last + "*" + D0 

            return simplify(r, sub)

        # The quotient rule section: handles stuff like f(x)/g(x)

        divpos = f.find("/")
        if divpos > -1:
            first = f[:divpos]
            last = f[divpos+1:]
            print(indent*rec, "Quotient rule: d/dx[f(x)/g(x)] = [f'(x)*g(x) - f(x)*g'(x)]/g(x)^2")
            print(indent*rec, "d/dx[" + first + "/" + last + "] = [ d/dx[" + first + "]*" + last + " - d/dx[" + last + "]*" + first + " ]/" + last + "^2")
            D0 = D(first, sub, rec+1)
            D1 = D(last, sub, rec+1)

            D0 = applyBrackets(D0)
            D1 = applyBrackets(D1)
            r = "(" + D0 + "*" + last + " - " + D1 + "*" + first + ")/" + last + "^2"
            if D0 == "1":
                r = "(" + last + " - " + D1 + "*" + first + ")/" + last + "^2"
            if D1 == "1":
                r = "(" + D0 + "*" + last + " - " + first + ")/" + last + "^2"
            if D0 == "0":
                r = " -" + D1 + "*" + first + "/" + last + "^2"
            if D1 == "0":
                r = "(" + D0 + "*" + last + ")/" + last + "^2"
            
            return simplify(r, sub)

        # The "exponential rule" section: handles stuff like f(x)^g(x)

        exppos = f.find("^")
        if exppos > -1:
            first = f[:exppos]
            last = f[exppos+1:]
            print(indent*rec, "Rewrite", f, "as exp(" + last + "*ln(" + first + "))")
            try:
                int(first)
            except ValueError:
                try:
                    int(last)
                except:
                    if first == "e":
                        return D("exp(" + last + ")")
                    else:
                        return D("exp(" + last + "*ln(" + first + "))")
                    

    #########################################################################
    # The recursion section: turns p(z) + q(z) - r(z) into D(p(z)) + D(q(z)) - D(r(z))
    #########################################################################
    
    f = f.replace("- ", "+ -")
    parts = f.split("+")
    newf = ""
    for part in parts:
        newf += D(part, sub, rec+1) + " + "
    output = newf[:-3].replace(" + -", " - ")
    output = undosubs(output, sub)

    if f0 == f and len(parts) == 1:
        print(f, "is an invalid function")
        return

    output = simplify(output, sub)
    print(rec, "Output: ", output)
    return output
