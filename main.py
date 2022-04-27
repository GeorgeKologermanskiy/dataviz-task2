import argparse
import os
from random import shuffle
from graph import Graph
from drawer import Drawer
from graham_coffman import graham_coffman
from linprog_layers import linprog_layers


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, type=str, help='Input graphml file')
    parser.add_argument('-w', required=False, type=int, help='Max layer size')
    parser.add_argument('-o', '--output', required=True, type=str, help='Output .svg file')
    return parser.parse_args()


def add_dummies(layers: list, graph: Graph):
    new_graph = Graph(None)
    N = graph.get_size()
    # copy graph
    for u in range(N):
        assert u == new_graph.add_vertex(False, len(graph.get_incoming_edges(u)) == 0)
    # mark layer for every real vertex
    layer_num = [0] * N
    for (num, layer) in enumerate(layers):
        for v in layer:
            layer_num[v] = num
    # stupid add dummy for every edge
    for u in range(N):
        for v in graph.get_outcoming_edges(u):
            if layer_num[u] + 1 == layer_num[v]:
                new_graph.add_edge(u, v)
            else:
                start = u
                for layer in range(layer_num[u] + 1, layer_num[v]):
                    dummy = new_graph.add_vertex(True, False)
                    layers[layer].append(dummy)
                    new_graph.add_edge(start, dummy)
                    start = dummy
                new_graph.add_edge(start, v)
    return layers, new_graph


def main():
    args = parse_args()
    input_file = args.input
    output_file = args.output
    w = args.w

    if not os.path.isfile(input_file):
        print(input_file, 'is not a regular file')
        return

    # parse graph from file
    graph = Graph(input_file)

    # calculate coords
    layers = graham_coffman(graph, w) if w is not None else linprog_layers(graph)
    # add dummies
    layers, graph = add_dummies(layers, graph)
    # create drawer & add vertexes with coords
    drawer = Drawer()
    step = 20
    coords = {}
    for (layer_num, layer) in enumerate(layers):
        if layer_num > 0:
            def get_x_coord(par):
                return coords[par][0]
            def func(u):
                s = sum(map(get_x_coord, graph.get_incoming_edges(u)))
                return (s / len(graph.get_incoming_edges(u)), u)
            layer = list(map(lambda x: x[1], sorted([func(u) for u in layer])))

        for (num, u) in enumerate(layer):
            coords[u] = ((layer_num % 2) * (step / 2) + num * step, layer_num * step)
            drawer.add_vertex(u, coords[u], graph.get_meta(u))

    # add edges
    for u in range(graph.get_size()):
        for v in graph.get_outcoming_edges(u):
            drawer.add_edge(u, v)

    # save as svg file
    drawer.saveSvg(output_file)


if __name__ == '__main__':
    main()
