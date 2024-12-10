from impedancenet import *
import matplotlib.pyplot as plt
from symbolica_helpers import *
import numpy as np
import cProfile
import time

with open('symbolica_license.txt') as f:
    symbolica.set_license_key(f.read().strip())

print("Generating Networks...")
test_net = ImpedanceNetwork(symbolica.N(1).to_rational_polynomial(),
                            symbolica.N(0).to_rational_polynomial(),
                            symbolica.S("s").to_rational_polynomial())


s = symbolica.S("s")
w = symbolica.S("w")
j = symbolica.S("j")
r = symbolica.S("r")

print("Reducing...")

test_net.from_random(32)
#test_net.display_pyvis(True)
cProfile.run('test_net.collapse([5, 26])')
#test_net.display_pyvis(True)
rexpr = list(test_net.G.edges(data=True))[0][2]['expression']
N = rexpr.numerator()
D = rexpr.denominator()
print(rexpr)

rexpr2 = rexpr.to_expression()
#rexpr2 = rexpr2.replace_all(s, w*j)

#for i in range(0, 50):
#    rexpr2 = rexpr2.replace_all(j**(i*4 + 1), j)
#    rexpr2 = rexpr2.replace_all(j**(i*4 + 2), -1)
#    rexpr2 = rexpr2.replace_all(j**(i*4 + 3), -j)
#    rexpr2 = rexpr2.replace_all(j**(i*4 + 4), 1)

#def conjugate(r):
#    return r.replace_all(j, -j)
#print(rexpr2)
#rexpr2 = rexpr2 * conjugate(rexpr2)
#print(rexpr2.expand())
#for i in range(0, 50):
#    rexpr2 = rexpr2.replace_all(j**(i*4 + 1), j)
#    rexpr2 = rexpr2.replace_all(j**(i*4 + 2), -1)
#    rexpr2 = rexpr2.replace_all(j**(i*4 + 3), -j)
#    rexpr2 = rexpr2.replace_all(j**(i*4 + 4), 1)
#print(rexpr2.expand())
#exit()
print(rexpr2.evaluate_complex({s : 2j}, {}))
xs = []
ys = []
yre = []
yim = []
yp = []
import cmath
for xc in np.arange(-3, 2, 0.01):
    x = 10**xc
    xp = 1j * 10**xc

    #rexpr_eval = rexpr2.replace_all(w, x)
    #rexpr_eval = rexpr_eval.replace_all(j, 0)
    y = rexpr2.evaluate_complex({s: xp}, {})
    
    if np.isfinite(y):
        xs.append(x)
        yre.append(y.real)
        yim.append(y.imag)
        ys.append(abs(y)**2)
        yp.append(cmath.phase(y))


xs = np.array(xs)
ys = np.array(ys)
yre = np.array(yre)
yim = np.array(yim)



#plt.plot(xs, yre)
#plt.plot(xs, yim)
plt.plot(xs, ys)
plt.yscale('log')
plt.xscale('log')
plt.show()

for x, re, im, sq, phase in zip(xs, yre, yim, ys, yp):
    print(x, re, im, sq, phase)

exit()

def to_np_poly(P):
    c = [0]*P.nterms()
    for x in P.coefficient_list(symbolica.S("s")):
        c[x[0][0]] = int(x[1].to_latex()[2:-2])
    return np.array(c[::-1], dtype=np.float64)

def get_roots(X):
    p = to_np_poly(X)
    roots = np.roots(p)
    err_roots = np.polyval(np.abs(p), np.abs(roots))*1e-16
    return roots, err_roots

zeros, err_zeros = get_roots(N)
poles, err_poles = get_roots(D)

def plot_poly(p):
    x = np.arange(-1, 1, 0.01)
    y = np.polyval(p, x)
    plt.plot(x, y)
    plt.show()

plot_poly(zeros)

time.sleep(1)
#test_net.display_pyvis(False)
exit()