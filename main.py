class Polynomial:
    def __init__(self, coefficients):
        self.coefficients = coefficients
        self.degree = len(coefficients) - 1

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
        if exponent == 0:
            return Polynomial([1])
        result = Polynomial(self.coefficients)
        for _ in range(exponent - 1):
            result *= self
        return result

    def __str__(self):
        return self.string()

    def string(self):
        terms = []
        for power in range(self.degree, -1, -1):
            coeff = self.coefficients[power]
            if coeff == 0:
                continue
            if power == 0:
                term = f"{coeff}"
            elif power == 1:
                if coeff == 1:
                    term = "x"
                elif coeff == -1:
                    term = "-x"
                else:
                    term = f"{coeff}x"
            else:
                if coeff == 1:
                    term = f"x^{power}"
                elif coeff == -1:
                    term = f"-x^{power}"
                else:
                    term = f"{coeff}x^{power}"
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


p = Polynomial([1, 0, -2])
q = Polynomial([0, 1])     
print(p)
print(q)

print(p + q)  
print(p * q) 
print(p ** 2)
