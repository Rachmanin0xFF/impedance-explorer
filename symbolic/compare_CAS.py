
from impedancenet import *
import cProfile
import matplotlib.pyplot as plt
import symbolica
import sympy
from symbolica_helpers import *
from profiling_analyzer import *
import numpy as np
import sympy
from sympy import S

PROFILING = True
SYMBOLICA_COMPLEXITY_ANALYSIS = True

with open('symbolica_license.txt') as f:
    symbolica.set_license_key(f.read().strip())

print("Generating Networks...")
test_net_sympy = ImpedanceNetwork(S.One, S.Zero, sympy.Symbol("s"))
test_net_symbolica = ImpedanceNetwork(symbolica.N(1).to_rational_polynomial(),
                                      symbolica.N(0).to_rational_polynomial(),
                                      symbolica.S("s").to_rational_polynomial())
test_net_numerical = ImpedanceNetwork()

print("Reducing...")

if SYMBOLICA_COMPLEXITY_ANALYSIS:
    for i in [75, 80, 85, 90, 95]:
        N = i
        #test_net_symbolica.from_random(N)
        #cProfile.run('test_net_symbolica.collapse(nodes_to_preserve=[2, 5])', 'symbolicastats')
        #print(f"{N} {get_stat('symbolicastats')}")
        for k in range(0, 1):
            test_net_symbolica.from_random(N)
            cProfile.run('test_net_symbolica.collapse(nodes_to_preserve=[2, 5])', 'symbolicastats')
            print(f"{N} {get_stat('symbolicastats')}")

# Sympy struggles lol (I just wanna run this script fast)
test_net_sympy.from_random(4)
test_net_symbolica.from_random(50)
test_net_numerical.from_random(25)

if PROFILING:
    cProfile.run('test_net_sympy.collapse(nodes_to_preserve=[2, 5], simplification_method=sympy.simplify)', 'sympystats')
    cProfile.run('test_net_symbolica.collapse(nodes_to_preserve=[2, 5])', 'symbolicastats')
    cProfile.run('test_net_numerical.collapse(nodes_to_preserve=[2, 5])', 'numericalstats')
else:
    test_net_sympy.collapse(nodes_to_preserve=[2, 5], simplification_method=sympy.simplify)
    test_net_symbolica.collapse(nodes_to_preserve=[2, 5])
    test_net_numerical.collapse(nodes_to_preserve=[2, 5])


if PROFILING:
    print("Sympy Stats:")
    show_stats('sympystats')

    print("Symbolica Stats:")
    show_stats('symbolicastats')

    print("Numerical Stats:")
    show_stats('numericalstats')

print("Sympy Expression:")
print(list(test_net_sympy.G.edges(data=True))[0][2]['expression'])

print("Symbolica Expression:")
print(list(test_net_symbolica.G.edges(data=True))[0][2]['expression'])

print("Numerical Expression:")
print(list(test_net_numerical.G.edges(data=True))[0][2]['expression'])