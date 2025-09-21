class Polynomial:
    def __init__(self, coefficients):
        self.coefficients = coefficients
        self.degree = len(coefficients) - 1
        self.trim()
    def __add__(self, other):
        max_len = max(len(self.coefficients), len(other.coefficients))
        new_coeffs = [0] * max_len
        for i in range(max_len):
            c1 = self.coefficients[i] if i < len(self.coefficients) else 0
            c2 = other.coefficients[i] if i < len(other.coefficients) else 0
            new_coeffs[i] = c1 + c2
        return Polynomial(new_coeffs)
    def __mul__(self, other):
        new_degree = self.degree + other.degree
        new_coeffs = [0] * (new_degree + 1)
        for i, c1 in enumerate(self.coefficients):
            for j, c2 in enumerate(other.coefficients):
                new_coeffs[i + j] += c1 * c2
        return Polynomial(new_coeffs)
    def __pow__(self, exponent):
        result = Polynomial([1])
        base = self
        while exponent > 0:
            if exponent % 2 == 1:
                result *= base
            base *= base
            exponent //= 2
        return result
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
    def trim(self):
        while len(self.coefficients) > 1 and self.coefficients[-1] == 0:
            self.coefficients.pop()
        self.degree = len(self.coefficients) - 1


