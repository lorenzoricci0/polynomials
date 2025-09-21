from random import randint, choice
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

class Polynomial:
    def __init__(self, coefficients):
        self.coefficients = coefficients
        self.degree = len(coefficients) - 1
        self.trim()

    @staticmethod
    def random_polynomial(degree, coeff_range):
        return Polynomial([randint(-coeff_range, coeff_range) for _ in range(degree + 1)])

    def trim(self):
        while len(self.coefficients) > 1 and self.coefficients[-1] == 0:
            self.coefficients.pop()
        self.degree = len(self.coefficients) - 1

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

# --- Nuova classe Expression flessibile ---
class Expression:
    def __init__(self, *elements, operation='add', exponent=2):
        """
        elements: polinomi o altre espressioni
        operation: 'add', 'mul', 'pow'
        exponent: solo per 'pow'
        """
        self.elements = elements
        self.operation = operation
        self.exponent = exponent

    def evaluate(self):
        if self.operation == 'add':
            result = self._eval_element(self.elements[0])
            for e in self.elements[1:]:
                result += self._eval_element(e)
            return result
        elif self.operation == 'mul':
            result = self._eval_element(self.elements[0])
            for e in self.elements[1:]:
                result *= self._eval_element(e)
            return result
        elif self.operation == 'pow':
            if len(self.elements) != 1:
                raise ValueError("Pow operation requires exactly one element")
            return self._eval_element(self.elements[0]) ** self.exponent
        else:
            raise ValueError("Unsupported operation")

    def _eval_element(self, e):
        if isinstance(e, Polynomial):
            return e
        elif isinstance(e, Expression):
            return e.evaluate()
        else:
            raise TypeError("Element must be Polynomial or Expression")

    def __str__(self):
        op_symbol = {'add': '+', 'mul': '*', 'pow': f'^{self.exponent}'}.get(self.operation, '?')
        if self.operation == 'pow':
            return f"({self.elements[0]}) {op_symbol}"
        else:
            return f" {op_symbol} ".join(f"({e})" for e in self.elements)

def random_expression(max_depth=2, max_polys=3, max_degree=2, coeff_range=5):
    """
    Genera un'espressione casuale.
    max_depth: profondità massima di nidificazione
    max_polys: massimo numero di polinomi o sotto-espressioni in un nodo
    max_degree: grado massimo dei polinomi casuali
    coeff_range: intervallo dei coefficienti casuali [-coeff_range, coeff_range]
    """
    if max_depth == 0:
        # Base: restituisci un polinomio casuale
        return Polynomial.random_polynomial(max_degree, coeff_range)
    
    num_elements = randint(1, max_polys)
    elements = [random_expression(max_depth-1, max_polys, max_degree, coeff_range) for _ in range(num_elements)]
    
    # Scegli un'operazione casuale
    operation = choice(['add', 'mul', 'pow'])
    
    if operation == 'pow':
        # Solo un elemento per potenza
        elem = choice(elements)
        exponent = randint(2, 3)  # esponenti piccoli per non esplodere
        return Expression(elem, operation='pow', exponent=exponent)
    else:
        return Expression(*elements, operation=operation)

pdf_file = "espressioni_random.pdf"
c = canvas.Canvas(pdf_file, pagesize=A4)
width, height = A4

y = height - 50  # margine superiore

for i in range(50):  # 50 espressioni per esempio
    expr = random_expression(max_depth=2, max_polys=3, max_degree=2, coeff_range=5)
    c.drawString(50, y, f"{i+1}. Expression:")
    y -= 15
    c.drawString(70, y, str(expr))
    y -= 30
    if y < 50:
        c.showPage()
        y = height - 50

c.save()
print(f"PDF generato: {pdf_file}")
