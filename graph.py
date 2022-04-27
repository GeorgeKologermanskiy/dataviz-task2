from pygraphml import GraphMLParser

class Graph:

    def __init__(self, input_file: str or None):
        if input_file is None:
            self.size = 0
            self.incoming_edges = []
            self.outcoming_edges = []
            self.vertex_meta = []
            return
        graph = GraphMLParser().parse(input_file)
        nodes_mapping = {}
        # parse vertexes
        for node in graph.nodes():
            id = node.id
            nodes_mapping[id] = len(nodes_mapping)
        self.size = len(nodes_mapping)
        self.incoming_edges = [[] for _ in range(self.size)]
        self.outcoming_edges = [[] for _ in range(self.size)]
        # parse edges
        for edge in graph.edges():
            num1 = nodes_mapping[edge.node1.id]
            num2 = nodes_mapping[edge.node2.id]
            self.outcoming_edges[num1].append(num2)
            self.incoming_edges[num2].append(num1)

    def add_vertex(self, is_dummy, is_root):
        num = self.size
        self.size += 1
        self.incoming_edges.append([])
        self.outcoming_edges.append([])
        self.vertex_meta.append((is_dummy, is_root))
        return num
    
    def add_edge(self, u, v):
        self.outcoming_edges[u].append(v)
        self.incoming_edges[v].append(u)

    def get_size(self):
        return self.size

    def get_meta(self, v):
        return self.vertex_meta[v]

    def get_outcoming_edges(self, v: int):
        return self.outcoming_edges[v]
    
    def get_incoming_edges(self, v: int):
        return self.incoming_edges[v]
