from graph import Graph

def graham_coffman(graph: Graph, w: int):
    # graph size
    N = graph.get_size()
    # top sort
    pi = top_sort(graph)
    # map with layers
    marked = [-1] * N
    layers = [[]]
    for _ in range(N):
        v = None
        for u in range(N):
            if marked[u] >= 0:
                continue
            if -1 in [marked[to] for to in graph.get_outcoming_edges(u)]:
                continue
            if v is None or pi[u] > pi[v]:
                v = u
        if len(layers[-1]) >= w or len(layers) in [marked[to] for to in graph.get_outcoming_edges(v)]:
            layers.append([])
        layers[-1].append(v)
        marked[v] = len(layers)
    layers.reverse()
    return layers

def top_sort(graph: Graph):
    N = graph.get_size()
    pi = [0] * N
    for i in range(1, N + 1):
        v = None # (-1, set())
        for u in range(N):
            if pi[u] > 0:
                continue
            ok = True
            for par in graph.get_incoming_edges(u):
                if pi[par] == 0:
                    ok = False
            if not ok:
                continue
            u_set = set([pi[par] for par in graph.get_incoming_edges(u)])
            if v is None or compare_sets(u_set, v[1]) < 0:
                v = (u, u_set)
        if v is None:
            break
        pi[v[0]] = i
    return pi

def compare_sets(A, B):
    for a, b in zip(reversed(sorted(A)), reversed(sorted(B))):
        if a < b:
            return -1
        if b < a:
            return 1
    if len(A) < len(B):
        return -1
    if len(B) < len(A):
        return 1
    return 0
