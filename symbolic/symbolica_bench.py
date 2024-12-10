from symbolica_helpers import *
import random
import time
import cProfile
n0 = symbolica.N(0).to_rational_polynomial()
n1 = symbolica.N(1).to_rational_polynomial()
s = symbolica.S("s").to_rational_polynomial()

def powa(s, n):
    if n == 1:
        return s
    elif n == 0:
        return n1
    elif n > 1:
        return powa(s, n-1)*s
    print("AAAAA")
    exit()

def make_big_expr(N, numlen):
    term = n0
    for i in range(1, N):
        term = term + symbolica.N(random.randint(0, numlen)).to_rational_polynomial()*powa(s, i)
    return term



i = 100
w = 10**100

A = make_big_expr(i, w)
B = make_big_expr(i, w)

C = make_big_expr(i, w)
D = make_big_expr(i, w)

E = make_big_expr(i, w)
F = make_big_expr(i, w)

F1 = A/B
F2 = C/D
F3 = E/F

t_ns0 = time.time_ns()

def symgo():
    U = F1 + n1/(F1*F2 + F3)
def do_fu():
    for i in range(0, 1000):
        symgo()
cProfile.run('do_fu()')
print(i, time.time_ns() - t_ns0)
#print(U)