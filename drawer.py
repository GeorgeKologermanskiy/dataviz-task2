import drawSvg as draw

class Drawer:

    def __init__(self):
        self.nodes_coords = {}
        self.edges = []

    def add_vertex(self, num: int, coords: tuple, meta):
        self.nodes_coords[num] = (coords, meta)

    def add_edge(self, num1: int, num2: int):
        self.edges.append((num1, num2))
    
    def saveSvg(self, output_file: str):
        # prepare arrows
        #arrow = draw.Marker(-0.1, -0.5, 0.9, 0.5, scale=4, orient='auto')
        #arrow.append(draw.Lines(-0.1, -0.5, -0.1, 0.5, 0.9, 0, fill='red', close=True))
        # calculate sizes
        x_limit = int(max(map(lambda x: x[0][0], self.nodes_coords.values())) + 40)
        y_limit = int(max(map(lambda x: x[0][1], self.nodes_coords.values())) + 40)
        d = draw.Drawing(x_limit, y_limit)
        # draw edges
        for edge in self.edges:
            a, b = edge
            a_coords = self.nodes_coords[a][0]
            b_coords = self.nodes_coords[b][0]
            l = draw.Line(
                a_coords[0] + 20, y_limit - (a_coords[1] + 20),
                b_coords[0] + 20, y_limit - (b_coords[1] + 20),
                fill='none',
                stroke='green')
                #marker_end=arrow)
            d.append(l)
        # draw vertexes
        r = 3
        for ((x, y), (is_dummy, is_root)) in self.nodes_coords.values():
            if is_dummy:
                continue
            circle = draw.Circle(x + 20, y_limit - (y + 20), r, fill='red' if is_root else 'blue')
            d.append(circle)
        # save to file
        d.saveSvg(output_file)