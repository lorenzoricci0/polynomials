import random
from itertools import zip_longest
import math
from fractions import Fraction

class Polynomial:
    def __init__(self, coefficients):
        self.coefficients = coefficients
        self.degree = len(coefficients) - 1
        self.trim()

    def trim(self):
        while len(self.coefficients) > 1 and self.coefficients[-1] == 0:
            self.coefficients.pop()

    def __add__(self, other):
        summed = [sum(t) for t in zip_longest(self.coefficients, other.coefficients, fillvalue=0)]
        return Polynomial(summed)

    def __sub__(self, other):
        subtracted = [a - b for a, b in zip_longest(self.coefficients, other.coefficients, fillvalue=0)]
        return Polynomial(subtracted)

    def __mul__(self, other):
        res = [0]*(len(self.coefficients) + len(other.coefficients) - 1)
        for i, c1 in enumerate(self.coefficients):
            for j, c2 in enumerate(other.coefficients):
                res[i+j] += c1*c2
        return Polynomial(res)
    
    def __eq__(self, other):
        self.trim()
        other.trim()
        return self.coefficients == other.coefficients
    
    def __str__(self):
        if all(c == 0 for c in self.coefficients):
            return "0"
        terms = []
        for power, coeff in enumerate(self.coefficients):
            if coeff == 0:
                continue
            if power == 0:
                term = f"{coeff}"
            elif power == 1:
                term = f"{'' if coeff==1 else '-' if coeff==-1 else coeff}x"
            else:
                term = f"{'' if coeff==1 else '-' if coeff==-1 else coeff}x^{power}"
            terms.append(term)
        return " + ".join(terms[::-1]).replace("+ -", "- ")

class Equation:
    def __init__(self, sides):
        self.left, self.right = sides

    def __str__(self):
        return f"{self.left} = {self.right}"

    def simplify(self):
        simplified_poly = self.left - self.right
        return Equation([simplified_poly, Polynomial([0])])

def random_polynomial(max_degree, coeff_range):
    degree = random.randint(0, max_degree)
    coefficients = [random.randint(-coeff_range, coeff_range) for _ in range(degree + 1)]
    if coefficients[-1] == 0:
        coefficients[-1] = random.choice([i for i in range(-coeff_range, coeff_range + 1) if i != 0])
    return Polynomial(coefficients)

def create_expression(max_degree, coeff_range, num_terms):
    expr_poly = random_polynomial(max_degree, coeff_range)
    expr_str = str(expr_poly)
    for _ in range(num_terms - 1):
        op = random.choice(['+', '-', '*'])
        next_poly = random_polynomial(max_degree, coeff_range)
        expr_str = f"({expr_str} {op} {next_poly})"
        if op == '+':
            expr_poly += next_poly
        elif op == '-':
            expr_poly -= next_poly
        elif op == '*':
            expr_poly *= next_poly
    return expr_str, expr_poly

def create_equation(max_degree, coeff_range, difficulty):
    p = random.randint(-5, 5)
    q = random.randint(1, 5) 
    x0 = Fraction(p, q)

    str_left, poly_left = create_expression(max_degree, coeff_range, difficulty)
    str_right, poly_right = create_expression(max_degree, coeff_range, difficulty)

    value_left_no_const = sum(c * (x0 ** i) for i, c in enumerate(poly_left.coefficients[1:], start=1))
    value_right_no_const = sum(c * (x0 ** i) for i, c in enumerate(poly_right.coefficients[1:], start=1)) + poly_right.coefficients[0]

    new_const = int(value_left_no_const + poly_left.coefficients[0] - value_right_no_const)
    poly_right.coefficients[0] = new_const

    eq_str = f"{str_left} = {str_right}"
    eq = Equation([poly_left, poly_right])

    return eq_str, eq, float(x0)

