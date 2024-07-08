# Boolean Expression and Arithmetic Expression Parser

This project implements a parser for boolean and arithmetic expressions. It is designed to evaluate expressions and solve a set of equations and inequalities using the Z3 theorem prover.

## Project Structure

- **bool.py**: Contains classes and functions to parse and evaluate boolean expressions.
- **pcomb.py**: Implements a set of combinator parsers used to build more complex parsers for arithmetic and boolean expressions.
- **se.py**: Contains classes and functions to parse and evaluate arithmetic expressions.
- **start.py**: Demonstrates the usage of the parsers and evaluators. It includes functions to print, evaluate, and solve expressions.

## Features

- **Parsing Arithmetic Expressions**: Handles addition, multiplication, and parenthesized expressions.
- **Parsing Boolean Expressions**: Supports logical operations such as AND, OR, and comparison operations like equals and less than.
- **Evaluation**: Evaluate expressions given an environment (a mapping of variables to values).
- **Solving**: Solve sets of equations and inequalities using the Z3 theorem prover.

## How to Use

### Parsing and Printing Expressions

You can parse and print boolean and arithmetic expressions using the `printExpr` function in `start.py`.

```python
>>> printExpr("x = y")
(x = y)
>>> printExpr("x + 2 * y")
(x + (2 * y))
>>> printExpr("x < 2 and y < 1")
((x < 2) and (y < 1))
>>> printExpr("(x + 2*y < 15 + x * x) or z = 5")
(((x + (2 * y)) < (15 + (x * x))) or (z = 5))
```

### Evaluating Expressions

You can evaluate expressions given an environment using the `evalExpr` function in `start.py`.

```python
env = {'x': 1, 'y': 2, 'z': 3}
>>> evalExpr("x = y", env)
False
>>> evalExpr("x + 2 * y", env)
5
>>> evalExpr("x < 2 and y < 1", env)
False
>>> evalExpr("(x + 2*y < 15 + x * x) or z = 5", env)
True
```

### Solving Equations and Inequalities

The `solve` function in `start.py` can be used to solve sets of equations and inequalities.

```python
>>> sol = solve(["x + y + z = 10", "x < y", "x < 3", "0 < x"])
>>> sol
{'z = 5', 'y = 3', 'x = 2'}
>>> sol = solve(["x + y + z = 10", "x < y", "x < 3", "5 < x"])
No solution!
>>> sol = solve(["x + y + z = 10", "x < y or x = y", "x < 3", "5 < x or 0 < x"])
>>> sol
{'x = 1', 'y = 2', 'z = 7'}
```

## Requirements

- Python 3.x
- Z3 Theorem Prover (`pip install z3-solver`)

## Running Tests

You can run the tests to ensure everything is working correctly.

```sh
python -m doctest -v bool.py
python -m doctest -v se.py
python -m doctest -v pcomb.py
python -m doctest -v start.py
```

