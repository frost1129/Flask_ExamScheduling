class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node] = set()

    def add_edge(self, node1, node2):
        if node1 in self.nodes and node2 in self.nodes:
            self.nodes[node1].add(node2)
            self.nodes[node2].add(node1)

    def remove_node(self, node):
        if node in self.nodes:
            for neighbor in self.nodes[node]:
                self.nodes[neighbor].remove(node)
            del self.nodes[node]

    def remove_edge(self, node1, node2):
        if node1 in self.nodes and node2 in self.nodes:
            self.nodes[node1].remove(node2)
            self.nodes[node2].remove(node1)

    def get_nodes(self):
        return list(self.nodes)

    def get_edges(self):
        edges = set()
        for node in self.nodes:
            for neighbor in self.nodes[node]:
                edge = (node, neighbor)
                edges.add(tuple(sorted(edge)))
        return edges


def welsh_powell(graph):
    # Sắp xếp các đỉnh theo độ bậc giảm dần
    sorted_nodes = sorted(graph.nodes.keys(), key=lambda x: len(graph.nodes[x]), reverse=True)

    # Đánh dấu tất cả các đỉnh chưa được tô màu
    colored = {}
    for node in graph.nodes:
        colored[node] = None

    # Bắt đầu tô màu
    color = 0
    # Tô màu cho đỉnh đầu tiên (có bậc lớn nhất)
    colored[sorted_nodes[0]] = color

    # Lặp qua các đỉnh còn lại và tô màu
    for node in sorted_nodes[1:]:
        # Tìm màu của các đỉnh kề với đỉnh hiện tại
        neighbor_colors = {colored[neighbor] for neighbor in graph.nodes[node] if neighbor in colored}

        # Tìm màu chưa được sử dụng để tô cho đỉnh hiện tại
        for color in range(len(sorted_nodes)):
            if color not in neighbor_colors:
                colored[node] = color
                break
        print(neighbor_colors)
    return colored
