from impedancenet import *
import matplotlib.pyplot as plt
import random
import numpy as np

N = 200
ca = 20
cb = 50

def batch():
    edge_logs = []

    test_net = ImpedanceNetwork()
    test_net.from_random(N)
    edge_log = []
    while len(test_net.G.nodes) > 2:
        edge_log.append(test_net.remove_min_node(False)[0])
    edge_logs.append(edge_log)

    test_net = ImpedanceNetwork()
    test_net.from_random(N)
    edge_log = []
    while len(test_net.G.nodes) > 2:
        test_net.calc_all_dE()
        edge_log.append(test_net.remove_min_node(True)[0])
    edge_logs.append(edge_log)

    test_net = ImpedanceNetwork()
    test_net.from_random(N)
    edge_log = []
    while len(test_net.G.nodes) > 2:
        choices = [x for x in list(test_net.G.nodes) if not x in [ca, cb]]
        edge_log.append(test_net.remove_node(random.choice(choices))[0])
    edge_logs.append(edge_log)

    return np.array(edge_logs, dtype=np.float64).T

avg = batch()
print(avg)
for i in range(0, 10):
    avg += batch()

avg *= 1.0 / 51.0
print(avg)

objs = plt.plot(avg)

np.savetxt("reduction_comparison.txt", avg, delimiter="\t")

plt.legend(objs, ('One-time dE calculation', 'Dynamic dE Updates', 'Random removal'))
plt.show()