import symbolica
with open('symbolica_license.txt') as f:
    symbolica.set_license_key(f.read().strip())

def factored(polynomial):
    str = ''
    for a in polynomial.factor():
        str += f"({a[0]})"
        if a[1] > 1:
            str += f"^{a[1]}"
    return a

def factored_string(x):
    if isinstance(x, symbolica.Polynomial):
        t = ''
        for a in x.factor():
            if len(str(a[0])) > 1:
                t += f"({a[0]})"
            else:
                t += str(a[0])
            if a[1] > 1:
                t += f"^{a[1]}"
        return t
    elif isinstance(x, symbolica.RationalPolynomial):
        t = f'({factored_string(x.numerator())})/({factored_string(x.denominator())})'
        return t
    return str(x)