
# Hey, me. It's a rational expression and polynomial class with some operator overrides
# Intended for symbolic use; you can put whatever you want in Rational.N/D, though

import math

class Polynomial:
    def __init__(self, coefficients):
        self.c = coefficients
    
    def __add__(self, other):
        if isinstance(other, Polynomial):
            if len(other.c) > len(self.c):
                coeffs = other.c.copy()
                for i in range(len(self.c)):
                    coeffs[i + len(other.c) - len(self.c)] += self.c[i]
            else:
                coeffs = self.c.copy()
                for i in range(len(other.c)):
                    coeffs[i + len(self.c) - len(other.c)] += other.c[i]
            return Polynomial(coeffs)
        else:
            raise TypeError("Can only add another Polynomial object")
    
    def remove_thismanyx(self, n):
        self.c = self.c[:-n]

    def count_zeroes(self):
        if len(self.c) <= 1: return 0
        i = 0
        for x in self.c[::-1]:
            if x == 0:
                i += 1
            else:
                return i
        return len(self.c)
    
    def div_all(self, n):
        self.c = [x // n for x in self.c]
        print(self.c)
    
    def __mul__(self, other):
        if isinstance(other, Polynomial):
            result_coeffs = [0] * (len(self.c) + len(other.c) - 1)
            for i, a in enumerate(self.c):
                for j, b in enumerate(other.c):
                    result_coeffs[i + j] += a * b
            return Polynomial(result_coeffs)
        else:
            raise TypeError("Can only multiply by another Polynomial object")
    
    def __str__(self):
        terms = []
        for i, coeff in enumerate(self.c[::-1]):
            if coeff == 0:
                continue
            if i == 0:
                term = str(coeff)
            elif i == 1:
                term = f"{coeff}x"
            else:
                term = f"{coeff}x^{i}"
            terms.append(term)
        return " + ".join(terms[::-1])

class RationalExpr:
    def __init__(self, numerator, denominator):
        self.N = numerator
        self.D = denominator
        assert(self.D != 0)
    
    def __add__(self, other):
        if isinstance(other, RationalExpr):
            return RationalExpr(self.N*other.D + other.N*self.D, self.D*other.D)
        else:
            return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, RationalExpr):
            return RationalExpr(self.N * other.N, self.D * other.D)
        else:
            return RationalExpr(self.N * other, self.D)

    def __truediv__(self, other):
        if isinstance(other, RationalExpr):
            return RationalExpr(self.N*other.D, self.D*other.N)
    
    def __iadd__(self, other):
        self.N = self.N*other.D + other.N*self.D
        self.D = self.D*other.D
        return self
    
    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'({self.N})/({self.D})'
    
    def simplify(self):
        # TODO: factoring!
        print(f"simplifying{str(self)}")
        trailing = min(self.N.count_zeroes(), self.D.count_zeroes())
        if trailing > 0:
            self.N.remove_thismanyx(trailing)
            self.D.remove_thismanyx(trailing)

        gcd = math.gcd(*(self.N.c + self.D.c))
        if gcd > 1:
            print('dividing by ' + str(gcd))
            self.N.div_all(gcd)
            self.D.div_all(gcd)
        
        print(f"found{str(self)}")
        return self

class RationalConstants:
    Rational1 = RationalExpr(Polynomial([1]), Polynomial([1]))
    Rational0 = RationalExpr(Polynomial([0]), Polynomial([1]))
    RationalS = RationalExpr(Polynomial([1, 0]), Polynomial([1]))

if __name__ == "__main__":
    print("This is a small module to add, multiply, and divide simple rational expressions.")
    print("I haven't implemented actual simplification (factoring + cancelling) yet. TODO!")