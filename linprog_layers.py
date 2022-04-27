from graph import Graph
from scipy.optimize import linprog

def linprog_layers(graph: Graph):
    N = graph.get_size()
    c = [len(graph.get_incoming_edges(v)) - len(graph.get_outcoming_edges(v)) for v in range(N)]
    A_ub = []
    for u in range(N):
        for v in graph.get_outcoming_edges(u):
            row = [0] * N
            row[u] = 1
            row[v] = -1
            A_ub.append(row)
    b_ub = [-1] * len(A_ub)
    # l = [0] * N
    # u = [N - 1] * N

    res = linprog(c, A_ub, b_ub, bounds=(0, N - 1), method="revised simplex")
    layers = []
    for (v, layer) in zip(range(N), list(map(int, res.x))):
        while len(layers) <= layer:
            layers.append([])
        layers[layer].append(v)
    return layers
