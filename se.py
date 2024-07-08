from pcomb import *

'''
<arithm_expression> ::= <term> '+' <arithm_expression> | <term>
<term>              ::= <factor> '*' <term> | <factor>
<factor>            ::= '(' <arithm_expression> ')' | <int> | <variable>
<int>               ::= INTEGER
<variable>          ::= IDENTIFIER
'''

class ParseExpr(Parser):
    def __init__(self):
        self.parser = ParsePlus() ^ ParseTerm()

class ParseTerm(Parser):
    def __init__(self):
        self.parser = ParseTimes() ^ ParseFactor()

class ParseFactor(Parser):
    def __init__(self):
        self.parser = ParseParen() ^  ParseCon() ^ ParseVar()

class ParseCon(Parser):
    def __init__(self):
        self.parser = ParseInt() >> (lambda n:
                      Return(Con(n)))

class ParseVar(Parser):
    def __init__(self):
        self.parser = ParseIdent() >> (lambda name:
                      Return(Var(name)))

class ParseParen(Parser):
    def __init__(self):
        self.parser = ParseSymbol('(') >> (lambda _:
                      ParseExpr()      >> (lambda e:
                      ParseSymbol(')') >> (lambda _:
                      Return(e))))

class ParsePlus(Parser):
    def __init__(self):
        self.parser = ParseTerm()      >> (lambda t:
                      ParseSymbol('+') >> (lambda _:
                      ParseExpr()      >> (lambda e:
                      Return(Plus(t, e)))))

class ParseTimes(Parser):
    def __init__(self):
        self.parser = ParseFactor()    >> (lambda x:
                      ParseSymbol('*') >> (lambda _:
                      ParseTerm()      >> (lambda y:
                      Return(Times(x, y)))))

        
class Expr:
    def toZ3(self): 
        return "Error not implemented"

    def __add__(self, other):
        return Plus(self, other)

    def __mul__(self, other):
        return Times(self, other)


class Con(Expr):
    def __init__(self, val):
        self.val = val

    def toZ3(self):
        return self.val
        
    def __str__(self):
        return str(self.val) # f"Con({self.val})"

    def ev(self, env):
        return self.val

    def simplify(self):
        return self

    def __eq__(self, other):
        if type(other).__name__ != "Con":
            return False
        return self.val == other.val
    
    def vars_(self):
        return []
    
class Var(Expr):
    def __init__(self, name):
        self.name = name
    
    def toZ3(self):
        return z3.Int(self.name)

    def __str__(self):
        return self.name # f"Var({self.name})"

    def ev(self, env):
        return env[self.name]

    def simplify(self):
        return self

    def __eq__(self, other):
        if type(other).__name__ != "Var":
            return False
        return self.name == other.name

    def vars_(self):
        return [self.name]
    
class BinOp(Expr):
    def __init__(self, left, right):
        self.left  = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.op} {self.right})" # f"{self.name}({self.left}, {self.right})" # +

    def ev(self, env):
        return self.fun(self.left.ev(env), self.right.ev(env))

    def __eq__(self, other):
        if not isinstance(other, BinOp):
            return False
        return self.name == other.name and self.left == other.left and self.right == other.right

    def vars_(self):
        return list(set(self.left.vars_() + self.right.vars_()))
    
    
class Plus(BinOp):
    name = "Plus"
    fun  = lambda _, x, y: x + y
    op   = '+'

    def simplify(self):
        simple_left  = self.left.simplify()
        simple_right = self.right.simplify()

        vl  = None
        vr = None
        if simple_left.vars_() == []:
            vl = simple_left.ev({})
        if simple_right.vars_() == []:
            vr = simple_right.ev({})

        if vl != None and vr != None:
            return Con(vl + vr)
        if vl == 0:
            return simple_right
        elif vr == 0:
            return simple_left
        else:
            return simple_left + simple_right

    def toZ3(self):
        return self.left.toZ3() + self.right.toZ3()
        
class Times(BinOp):
    name = "Times"
    fun  = lambda _, x, y: x * y
    op   = '*'

    def simplify(self):
        simple_left  = self.left.simplify()
        simple_right = self.right.simplify()
        vl  = None
        vr = None
        if simple_left.vars_() == []:
            vl = simple_left.ev({})
        if simple_right.vars_() == []:
            vr = simple_right.ev({})

        if vl != None and vr != None:
            return Con(vl * vr)
        if vl == 0 or vr == 0:
            return Con(0)
        elif vl == 1:
            return simple_right
        elif vr == 1:
            return simple_left
        else:
            return simple_left * simple_right

    def toZ3(self):
        return self.left.toZ3() * self.right.toZ3()
