
from impedancenet import *
from symbolica_helpers import *
import time

test_net.display_pyvis(False)

for n in test_net.G.nodes(data=True):
    print(n)

for i in range(0, len(test_net.G.nodes)-2):
    if i in [32, 64, 87]:
        test_net.display_pyvis(False)
        time.sleep(1)
    test_net.remove_min_node(True)

test_net.display_pyvis(False)