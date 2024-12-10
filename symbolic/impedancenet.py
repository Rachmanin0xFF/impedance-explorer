
import pyvis.network
import networkx as nx
import itertools
import random
import math

class ImpedanceNetwork:
    def __init__(self, one=1, zero=0, s=1):
        self.m_s = s
        self.m_1 = one
        self.m_0 = zero
    
    def from_adjlist(self, pairs):
        self.G = nx.Graph()
        self.fill_properties_default()
    
    def get_most_distant_nodes(self):
        apl = dict(nx.all_pairs_shortest_path_length(self.G))
        bpl = [tuple((v, s, k)) for s, d in apl.items() for k, v in d.items() if v == max(d.values())]
        bpl.sort(key=lambda tup: tup[0], reverse=True)
        length, start, end = bpl[0]
        return (start, end)

    def from_random(self, n=8, calc_dEs=True):
        #self.G = nx.barabasi_albert_graph(n=n, m=1, seed=1337)
        self.G = nx.watts_strogatz_graph(n, 4, 0.2, seed=1337+19 + n - 32)
        #self.G = nx.gnp_random_graph(n, 2.5/(n-1), seed=1338)

        self.G = list(self.G.subgraph(c).copy() for c in nx.connected_components(self.G))[0]
        self.fill_properties_default()
        if calc_dEs:
            self.calc_all_dE()

    def fill_properties_default(self):
        nx.set_edge_attributes(self.G, self.m_1, 'expression')
        nx.set_edge_attributes(self.G, 1, 'expressionlength')
        nx.set_node_attributes(self.G, 0, 'dE')
        i = 0
        for w in self.G.edges(data=True):
            w[2]['color'] = 'red'
            if i % 3 == 0:
                w[2]['expression'] = self.m_s
                w[2]['color'] = 'green'
            if i % 3 == 1:
                w[2]['expression'] = self.m_1 / (self.m_s)
                w[2]['color'] = 'blue'
            i += 1

    def display_pyvis(self, show_labels=False):
        net = pyvis.network.Network()

        H = self.G.copy()
        for e in H.edges(data=True):
            if show_labels:
                e[2]['label'] = str(e[2]['expression'])
            # Pyvis tries to serialize every single network attribute into JSON,
            # even if it's not being displayed *eye roll*, making this necessary
            del e[2]['expression']
        if show_labels:
            for n in H.nodes(data=True):
                n[1]['label'] = str(n[0])#[1]['dE']
        nx.set_node_attributes(H, 'ellipse', 'shape')

        net.from_nx(H)
        net.toggle_physics(False)
        net.show_buttons(filter_=['physics']) 
        net.show('graph.html', notebook=False)
    
    def calc_bettercost(self, node_id):
        pairs = itertools.combinations(self.G.adj[node_id], 2)

        connected_edges = self.G.adj[node_id]
        
        cost = 0
        for i in connected_edges:
            cost += connected_edges[i]['expressionlength']
        
        #nc = sum([(self.G.edges[e]['expressionlength'] if self.G.has_edge(e[0], e[1]) else 0) for e in pairs])
        #mc = sum([self.G.edges[e]['expressionlength'] for e in self.G.edges(node_id)])

        existing_edges = sum([(1 if self.G.has_edge(e[0], e[1]) else 0) for e in pairs])
        d = self.G.degree[node_id]
        dE = d*(d-3)//2 - existing_edges
        
        #dE += math.log(cost)*0.01
        #dE = cost*0.1
        dE = random.randint(0, 100)

        self.G.nodes[node_id]['dE'] = dE
        return dE

    def calc_dE(self, node_id):
        #pairs = itertools.combinations(self.G.adj[node_id], 2)
        #existing_edges = sum([(1 if self.G.has_edge(e[0], e[1]) else 0) for e in pairs])
        #d = self.G.degree[node_id]
        #dE = d*(d-3)//2 - existing_edges
        #self.G.nodes[node_id]['dE'] = dE
        return self.calc_bettercost(node_id)

    def calc_all_dE(self):
        for n in self.G.nodes:
            self.calc_dE(n)
    
    def collapse(self, nodes_to_preserve, simplification_method=(lambda x : x)):
        edge_log = []
        op_log = []
        while len(self.G.nodes) > len(nodes_to_preserve):
            (a, b) = self.remove_min_node(True, nodes_to_preserve, simplification_method)
            edge_log.append(a)
            op_log.append(b)
        return (edge_log, op_log)

    def remove_min_node(self, update_dE=False, nodes_to_preserve=[], simplification_method=(lambda x : x)):
        def srt(x):
            return x[1]['dE'] + (100000 if (x[0] in nodes_to_preserve) else 0)
        return self.remove_node(min(self.G.nodes(data=True), key=srt)[0], update_dE, simplification_method)

    def remove_node(self, node_id, update_dE=True, simplification_method=(lambda x : x)):
        connected_edges = self.G.adj[node_id]
        
        length_sum = 0

        # Find summed inverse impedances to target node (reusable quantity)
        # "m_0" and "m_1" can either be 0 and 1 or the symbolic forms of those numbers
        z_inv = self.m_0
        for i in connected_edges:
            z_inv += self.m_1 / connected_edges[i]['expression']
        
        ops = 0
        # Look through all pairs of neighboring nodes
        for comb in itertools.combinations(connected_edges, 2):
            expr1 = connected_edges[comb[0]]['expression']
            expr2 = connected_edges[comb[1]]['expression']

            # Compute the equivalent resistance through the targeted node
            prod = simplification_method(expr1 * expr2 * z_inv)
            ops += 1
            if self.G.has_edge(comb[0], comb[1]):
                # If there's already an edge where we want to put one, merge our new
                # edge with it using the impedances-in-parallel rule.
                self.G.edges[comb]['expression'] = simplification_method(self.m_1 / (self.m_1 / prod + self.m_1 / self.G.edges[comb]['expression']))
            else:
                self.G.add_edge(comb[0], comb[1], expression=prod, expressionlength=0)
        self.G.remove_node(node_id)
        
        # This actually ends up being good enough; I hardly see a difference in performance
        # Really, I think it should affect second-deg. neighbors as well, but whatever
        if update_dE:
            for n in connected_edges:
                self.calc_dE(n)

        return [len(self.G.edges), ops]

if __name__ == "__main__":
    print("This is a module for reducing transfer function networks with NetworkX!")
    print("This code can also work with symbolica or sympy (I advise the latter) for symbolic circuit analysis.")
    print("Here, let's reduce a small random network:")

    test_net = ImpedanceNetwork()
    test_net.from_random(4)
    print("Edges Before Collapse:")
    print(test_net.G.edges(data=True))
    test_net.collapse([0, 4])
    print("Edges After Collapse:")
    print(test_net.G.edges(data=True))
    exit()