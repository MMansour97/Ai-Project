from bool import * 

class ParseGeneralExpr(ParseExpr , ParseBExpr): 
    def __init__(self):
        self.parser = ParseBExpr() ^ ParseExpr()

#-------------------

def printExpr(inp): 
    """
    >>> printExpr("x = y")
    (x = y)
    >>> printExpr("x + 2 * y")
    (x + (2 * y))
    >>> printExpr("x < 2 and y < 1")
    ((x < 2) and (y < 1))
    >>> printExpr("(x + 2*y < 15 + x * x) or z = 5")
    (((x + (2 * y)) < (15 + (x * x))) or (z = 5))
    >>> printExpr("x + 2*y < 15 + x * x or z = 5")
    (((x + (2 * y)) < (15 + (x * x))) or (z = 5))
    """
    x = result(ParseGeneralExpr().parse(str(inp)))
    print(x)
    
    
def evalExpr(inp, env): 
    """
    env = {'x':1 , 'y':2, 'z':3}
    evalExpr("x = y", env)
    False
    evalExpr("x + 2 * y" , env)
    5
    evalExpr("x < 2 and y < 1", env)
    False
    evalExpr("(x + 2*y < 15 + x * x) or z = 5", env)
    True
    evalExpr("x + 2*y < 15 + x * x or z = 5", env)
    True
    evalExpr("x * 2 + 3 < x * (2 + 3)", env)
    False
    evalExpr("y * 2 + 3 < y * (2 + 3)", env)
    True
    """
    x = result(ParseGeneralExpr().parse(str(inp))).ev(env)
    print(x)
# --------------------

def solve(exprs):
    """
    >>> sol = solve(["x + y +z = 10", "x < y", "x < 3", "0 < x"])
    >>> sol
    {'z = 5', 'y = 3', 'x = 2'}
    >>> sol = solve(["x + y +z = 10", "x < y", "x < 3", "5 < x"])
    No solution!
    >>> sol = solve(["x + y + z = 10", "x < y or x = y", "x < 3", "5 < x or 0 < x"])
    >>> sol
    {'x = 1', 'y = 2', 'z = 7'}
    """ 
    pge = ParseGeneralExpr()
    s = Solver()
    
    for expr in exprs:
        par = pge.parse(expr)
        res = result(par)
        r = res.toZ3()
        s.add(r)

    if (str(s.check()) == "unsat"):
        print("No solution!")
        return None
    
    ml = s.model()
    s = set()
    
    for i in ml:
        s.add(str(i) + " = " + str(ml[i]))
    return s 

sol = solve(["x + y +z = 10", "x < y", "x < 3", "0 < x"])
print(sol) # {'z = 5', 'x = 2', 'y = 3'}

print("---------------------------------------")

sol = solve(["x + y +z = 10", "x < y", "x < 3", "5 < x"]) #No solution!
print("---------------------------------------")

sol = solve(["x + y + z = 10", "x < y or x = y", "x < 3", "5 < x or 0 < x"])
print(sol) #{'x = 1', 'y = 2', 'z = 7'}
