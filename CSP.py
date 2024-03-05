def parse_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extract the number of colors
    colors_line = next(line for line in lines if line.startswith('colors ='))
    colors = int(colors_line.strip().split('=')[1].strip())

    # Extract the edges
    edges = []
    for line in lines:
        if not line.startswith('#') and ',' in line:
            edge = tuple(map(int, line.strip().split(',')))
            edges.append(edge)

    return colors, edges


class GraphColoringCSP:
    def __init__(self, colors, edges):
        self.vertices = set()
        self.edges = edges
        self.colors = colors
        self.domain = {}
        self.initialize_domains()
        self.adjacency_list = self.create_adjacency_list()

    # Initialize the domain of each vertex with all possible colors
    def initialize_domains(self):
        for edge in self.edges:
            self.vertices.add(edge[0])
            self.vertices.add(edge[1])
        for vertex in self.vertices:
            self.domain[vertex] = list(range(self.colors))

    def create_adjacency_list(self):
        adjacency_list = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            adjacency_list[edge[0]].add(edge[1])
            adjacency_list[edge[1]].add(edge[0])
        return adjacency_list

    # Apply the AC3 algorithm to achieve arc consistency before backtracking
    def ac3(self):
        queue = [(vertex, neighbor) for vertex in self.vertices for neighbor in self.adjacency_list[vertex]]
        while queue:
            vertex1, vertex2 = queue.pop(0)
            if self.revise(vertex1, vertex2):
                if not self.domain[vertex1]:
                    return False
                for neighbor in self.adjacency_list[vertex1] - {vertex2}:
                    queue.append((neighbor, vertex1))
        return True

    # Revise the domain of vertex1 considering its relation with vertex2
    def revise(self, vertex1, vertex2):
        revised = False
        for color in self.domain[vertex1]:
            if all(color == other_color for other_color in self.domain[vertex2]):
                self.domain[vertex1].remove(color)
                revised = True
        return revised

    # Minimum Remaining Values (MRV) heuristic
    def select_unassigned_vertex(self, assignment):
        unassigned_vertices = [v for v in self.vertices if v not in assignment]
        return min(unassigned_vertices, key=lambda vertex: (len(self.domain[vertex]), -len(self.adjacency_list[vertex])))

    def order_domain_values(self, vertex, assignment):
        return self.domain[vertex]

    def is_consistent(self, vertex, color, assignment):
        for neighbor in self.adjacency_list[vertex]:
            if neighbor in assignment and assignment[neighbor] == color:
                return False
        return True

    # Assign a color to a vertex and update the domain of its neighbors
    def assign(self, vertex, color, assignment):
        assignment[vertex] = color
        for neighbor in self.adjacency_list[vertex]:
            if color in self.domain[neighbor]:
                self.domain[neighbor].remove(color)

    # Backtrack to find a solution to the CSP
    def backtrack(self, assignment):
        if len(assignment) == len(self.vertices):
            return assignment

        vertex = self.select_unassigned_vertex(assignment)
        for color in self.order_domain_values(vertex, assignment):
            if self.is_consistent(vertex, color, assignment):
                assignment_copy = assignment.copy()
                assignment_copy[vertex] = color
                result = self.backtrack(assignment_copy)
                if result:
                    return result
        return None

    def solve(self):
        self.ac3()
        assignment = {}
        return self.backtrack(assignment)

#Load the graph——coloring test file
file_path = 'C:/Graduate/AI/project2/graph_coloring.txt'

colors, edges = parse_input_file(file_path)
solver = GraphColoringCSP(colors, edges)
solution = solver.solve()
print(solution)
