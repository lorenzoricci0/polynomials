import random

class Polynomial:
    def __init__(self, coefficients):
        self.coefficients = coefficients[:]
        self.trim()

    def trim(self):
        while len(self.coefficients) > 1 and self.coefficients[-1] == 0:
            self.coefficients.pop()
        self.degree = len(self.coefficients) - 1

    def __add__(self, other):
        if isinstance(other, Polynomial):
            max_len = max(len(self.coefficients), len(other.coefficients))
            new_coeffs = [0] * max_len
            for i in range(max_len):
                c1 = self.coefficients[i] if i < len(self.coefficients) else 0
                c2 = other.coefficients[i] if i < len(other.coefficients) else 0
                new_coeffs[i] = c1 + c2
            return Polynomial(new_coeffs)
        elif isinstance(other, (int, float)):
            new_coeffs = self.coefficients[:]
            new_coeffs[0] += other
            return Polynomial(new_coeffs)
        return NotImplemented

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, Polynomial):
            max_len = max(len(self.coefficients), len(other.coefficients))
            new_coeffs = [0] * max_len
            for i in range(max_len):
                c1 = self.coefficients[i] if i < len(self.coefficients) else 0
                c2 = other.coefficients[i] if i < len(other.coefficients) else 0
                new_coeffs[i] = c1 - c2
            return Polynomial(new_coeffs)
        elif isinstance(other, (int, float)):
            new_coeffs = self.coefficients[:]
            new_coeffs[0] -= other
            return Polynomial(new_coeffs)
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            new_coeffs = [-c for c in self.coefficients]
            new_coeffs[0] += other
            return Polynomial(new_coeffs)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Polynomial):
            new_degree = self.degree + other.degree
            new_coeffs = [0] * (new_degree + 1)
            for i, c1 in enumerate(self.coefficients):
                for j, c2 in enumerate(other.coefficients):
                    new_coeffs[i + j] += c1 * c2
            return Polynomial(new_coeffs)
        elif isinstance(other, (int, float)):
            return Polynomial([c * other for c in self.coefficients])
        return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Polynomial([c / other for c in self.coefficients])
        elif isinstance(other, Polynomial):
            dividend = self.coefficients[:]
            divisor = other.coefficients[:]
            if other.degree < 0 or all(c == 0 for c in divisor):
                raise ZeroDivisionError("division by zero polynomial")

            quotient = [0] * (max(0, self.degree - other.degree) + 1)
            while len(dividend) - 1 >= other.degree:
                power = len(dividend) - 1 - other.degree
                coeff = dividend[-1] / divisor[-1]
                quotient[power] = coeff
                for i in range(other.degree + 1):
                    dividend[power + i] -= coeff * divisor[i]
                while len(dividend) > 1 and dividend[-1] == 0:
                    dividend.pop()
            return Polynomial(quotient), Polynomial(dividend)
        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            return Polynomial([other]) / self
        return NotImplemented

    def __pow__(self, exponent):
        if exponent < 0:
            raise ValueError("Negative exponent not supported for polynomials")
        result = Polynomial([1])
        base = self
        while exponent > 0:
            if exponent % 2 == 1:
                result *= base
            base *= base
            exponent //= 2
        return result

    def __neg__(self):
        return Polynomial([-c for c in self.coefficients])

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            return self.coefficients == other.coefficients
        elif isinstance(other, (int, float)):
            return self.degree == 0 and self.coefficients[0] == other
        return False

    def __str__(self):
        terms = []
        for power in range(self.degree, -1, -1):
            coeff = self.coefficients[power]
            if coeff == 0:
                continue
            if power == 0:
                term = f"{coeff}"
            elif power == 1:
                term = f"{'' if abs(coeff) == 1 else coeff}x"
                if coeff == -1:
                    term = "-x"
            else:
                term = f"{'' if abs(coeff) == 1 else coeff}x^{power}"
                if coeff == -1:
                    term = f"-x^{power}"
            terms.append(term)
        if not terms:
            return "0"
        result = terms[0]
        for term in terms[1:]:
            if term.startswith("-"):
                result += " - " + term[1:]
            else:
                result += " + " + term
        return result

    def __repr__(self):
        return str(self)


def random_polynomial(degree, coeff_range):
    coefficients = [random.randint(-coeff_range, coeff_range) for _ in range(degree + 1)]
    return Polynomial(coefficients)

