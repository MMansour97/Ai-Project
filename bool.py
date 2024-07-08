from se import *
'''
<boolean_expression> ::= <disjunct> 'or' <boolean_expression> | <disjunct>
<disjunct>           ::= <conjunct> 'and' <disjunct> | <conjunct>
<conjunct>           ::= <arithmetic_expression> <cmp> <arithmetic_expression> | (<boolean_expression>)
<cmp>                ::= '=' | '<'
'''

class ParseBExpr(Parser):
    def __init__(self):
        self.parser = ParseOr() ^ ParseDisj()

class ParseDisj(Parser):
    def __init__(self):
        self.parser = ParseAnd() ^ ParseConj()

class ParseConj(Parser): 
    def __init__(self):
        self.parser = ParseArithmeticExpression() ^ ParseBParen()

class ParseArithmeticExpression(Parser): 
    def __init__(self):
        self.parser = ParseExpr() >> (lambda x : \
                        ParseCmp() >> (lambda y : \
                            ParseExpr() >> (lambda z : Return(Eq(x, z) if result(y) == "=" else LessThan(x, z)))))

class ParseCmp(Parser): 
    def __init__(self):
        self.parser = ParseSymbol("=") ^ ParseSymbol("<")


class ParseBVar(Parser):
    def __init__(self):
        self.parser = ParseIdentifier() >> (lambda name:
                      Return(BVar(name)))

class ParseBParen(Parser):
    def __init__(self):
        self.parser = ParseSymbol("(") >> (lambda _:
                      ParseBExpr()     >> (lambda e:
                      ParseSymbol(")") >> (lambda _:
                      Return(e))))

class ParseOr(Parser):
    def __init__(self):
        self.parser = ParseDisj() >> (lambda d:
                      ParseSymbol("or") >> (lambda _:
                      ParseBExpr() >> (lambda e:
                      Return(Or(d, e)))))

class ParseAnd(Parser):
    def __init__(self):
        self.parser = ParseConj() >> (lambda x:
                      ParseSymbol("and") >> (lambda _:
                      ParseDisj() >> (lambda y:
                      Return(And(x, y)))))


class BExpr:
    pass

class BVar(BExpr):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def ev(self, env):
        return env[self.name]

    def toZ3(self): 
        return Bool(self.name)

class Op2(BExpr):
    def __init__(self, left, right):
        self.left  = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.op} {self.right})"

    def ev(self, env):
        return self.fun(self.left.ev(env), self.right.ev(env))
    
class Or(Op2):
    op = "or"
    fun = lambda _, x, y: x or y

    def toZ3(self): # neu
        return z3.Or(self.left.toZ3(), self.right.toZ3())

class And(Op2):
    op = "and"
    fun = lambda _, x, y: x and y

    def toZ3(self): # neu
        return z3.And(self.left.toZ3(), self.right.toZ3())

class LessThan(Op2):
    op = "<"
    fun = lambda _ , x , y: x < y 

    def toZ3(self):
        return self.left.toZ3() < self.right.toZ3()
    
    
class Eq(Op2):
    op = "="
    fun = lambda _, x, y: x == y

    def toZ3(self):
        return self.left.toZ3() == self.right.toZ3()


