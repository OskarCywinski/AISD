#   Graph Class
import math
class Graph:
    def add_edge(self, u, v):
        raise NotImplementedError

    def has_edge(self, u, v):
        raise NotImplementedError

    def display(self):
        raise NotImplementedError
    
    def get_neighbors(self, u):
        raise NotImplementedError
    
    def calculate_in_degrees(self):
        raise NotImplementedError
    
    def add_edges(self, l):
        for u, v in l:
            self.add_edge(u, v)
    

    def export(self):
        print("Eksportuję graf do TikZ:\n")

        # Użyjemy self.n jeśli jest, w przeciwnym razie spróbujemy get_all_nodes()
        if hasattr(self, 'n'):
            nodes = list(range(self.n))
        else:
            nodes = list(self.get_all_nodes())

        tikz = ["\\begin{tikzpicture}[->,>=stealth,shorten >=1pt,auto,node distance=2cm, thick, main node/.style={circle,draw}]"]

        # Umieszczamy wierzchołki na okręgu
        angle_step = 360 / len(nodes)
        for i in nodes:
            angle = i * angle_step
            x = round(5 * math.cos(math.radians(angle)), 2)
            y = round(5 * math.sin(math.radians(angle)), 2)
            tikz.append(f"\\node[main node] ({i}) at ({x},{y}) {{{i}}};")

        # Dodajemy krawędzie
        for i in nodes:
            for j in nodes:
                if self.has_edge(i, j):
                    tikz.append(f"\\path[->] ({i}) edge ({j});")

        tikz.append("\\end{tikzpicture}")

        print("\n".join(tikz))
    
    def BFS(self, start):
        visited = set()
        queue = [start]
        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.add(node)
                print(node, end=' ')
                for neighbor in self.get_neighbors(node):
                    if neighbor not in visited:
                        queue.append(neighbor)
        print()
        
    def DFS(self, start):
        visited = set()
        stack = [start]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                print(node, end=' ')
                for neighbor in self.get_neighbors(node):
                    if neighbor not in visited:
                        stack.append(neighbor)
        print()
        
    def Kahn(self):
        # Step 1: Calculate in-degrees of all nodes
        in_degree = self.calculate_in_degrees()

        # Step 2: Collect all nodes with in-degree 0
        queue = [node for node in in_degree if in_degree[node] == 0]
        topological_order = []

        # Step 3: Process nodes with in-degree 0
        while queue:
            node = queue.pop(0)
            topological_order.append(node)

            for neighbor in self.get_neighbors(node):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Step 4: Check for cycles
        if len(topological_order) != len(in_degree):
            print("Graph has a cycle. Topological sorting is not possible.")
        else:
            print("Topological Order:", topological_order)
            
    def Tarjan(self):
        # Step 1: Initialize variables
        nodes = set()  # Collect all nodes in the graph
        for u in self.get_all_nodes():
            nodes.add(u)
            for v in self.get_neighbors(u):
                nodes.add(v)

        unmarked = nodes  # Nodes that are unmarked
        temporary = set()  # Nodes with a temporary mark
        permanent = set()  # Nodes with a permanent mark
        topological_order = []  # Result list
        cycle_found = [False]  # Use a list to allow modification in nested scope

        def visit(node):
            if node in permanent:
                return  # Node is already permanently marked
            if node in temporary:
                print("Graph has a cycle. Topological sorting is not possible.")
                cycle_found[0] = True
                return  # Cycle detected

            # Mark the node temporarily
            temporary.add(node)

            # Visit all neighbors
            for neighbor in self.get_neighbors(node):
                if not cycle_found[0]:
                    visit(neighbor)

            # Mark the node permanently and add to the result
            temporary.remove(node)
            permanent.add(node)
            topological_order.append(node)

        # Step 2: Visit all nodes
        while unmarked and not cycle_found[0]:
            node = unmarked.pop()
            visit(node)

        # Step 3: Print the result only if no cycle was found
        if not cycle_found[0]:
            print("Topological Order:", topological_order[::-1])  # Reverse the order
        
    
#   Matrix Subclass

class GraphMatrix(Graph):
    def __init__(self, num_nodes):
        self.n = num_nodes
        self.matrix = [[0] * self.n for _ in range(self.n)]

    def add_edge(self, u, v):
        self.matrix[u][v] = 1

    def has_edge(self, u, v):
        return self.matrix[u][v] == 1

    def display(self):
        for row in self.matrix:
            print(row)
            
    def get_neighbors(self, u):
        neighbors = []
        for v in range(self.n):
            if self.has_edge(u, v):
                neighbors.append(v)
        return neighbors
    
    def calculate_in_degrees(self):
        in_degree = {node: 0 for node in range(self.n)}
        for u in range(self.n):
            for v in range(self.n):
                if self.matrix[u][v] == 1:
                    in_degree[v] += 1
        return in_degree
    
    def get_all_nodes(self):
        return range(self.n)
        

#   Edge List Subclass

class GraphEdgeList(Graph):
    def __init__(self):
        self.edges = []

    def add_edge(self, u, v):
        self.edges.append((u, v))

    def has_edge(self, u, v):
        return (u, v) in self.edges

    def display(self):
        for u, v in self.edges:
            print(f"{u} -> {v}")
            
    def get_neighbors(self, u):
        neighbors = []
        for edge in self.edges:
            if edge[0] == u:
                neighbors.append(edge[1])
        return neighbors
    
    def calculate_in_degrees(self):
        nodes = {u for u, v in self.edges}.union({v for u, v in self.edges})
        in_degree = {node: 0 for node in nodes}
        for u, v in self.edges:
            in_degree[v] += 1
        return in_degree
    
    def get_all_nodes(self):
        nodes = set()
        for u, v in self.edges:
            nodes.add(u)
            nodes.add(v)
        return nodes

#   Adjacency Table Subclass

class GraphAdjTable(Graph):
    def __init__(self):
        self.adj = {}

    def add_edge(self, u, v):
        if u not in self.adj:
            self.adj[u] = []
        self.adj[u].append(v)

    def has_edge(self, u, v):
        return u in self.adj and v in self.adj[u]

    def display(self):
        for u in self.adj:
            print(f"{u}: {self.adj[u]}")
            
    def get_neighbors(self, u):
        return self.adj.get(u, [])
    
    def calculate_in_degrees(self):
        # Ensure all nodes are included, even those without outgoing edges
        in_degree = {node: 0 for node in self.get_all_nodes()}
        for u in self.adj:
            for v in self.adj[u]:
                in_degree[v] += 1
        return in_degree

    def get_all_nodes(self):
        # Include all nodes, even those without outgoing edges
        nodes = set(self.adj.keys())
        for neighbors in self.adj.values():
            nodes.update(neighbors)
        return nodes

def matrix_to_edge_list(matrix_graph):
    edge_list_graph = GraphEdgeList()
    for u in range(matrix_graph.n):
        for v in range(matrix_graph.n):
            if matrix_graph.matrix[u][v] == 1:
                edge_list_graph.add_edge(u, v)
    return edge_list_graph

def matrix_to_adj_table(matrix_graph):
    adj_table_graph = GraphAdjTable()
    for u in range(matrix_graph.n):
        for v in range(matrix_graph.n):
            if matrix_graph.matrix[u][v] == 1:
                adj_table_graph.add_edge(u, v)
    return adj_table_graph

def edge_list_to_matrix(edge_list_graph, num_nodes):
    matrix_graph = GraphMatrix(num_nodes)
    for u, v in edge_list_graph.edges:
        matrix_graph.add_edge(u, v)
    return matrix_graph

def edge_list_to_adj_table(edge_list_graph):
    adj_table_graph = GraphAdjTable()
    for u, v in edge_list_graph.edges:
        adj_table_graph.add_edge(u, v)
    return adj_table_graph

def adj_table_to_matrix(adj_table_graph):
    nodes = adj_table_graph.get_all_nodes()
    num_nodes = max(nodes) + 1  # Assuming nodes are 0-indexed
    matrix_graph = GraphMatrix(num_nodes)
    for u in adj_table_graph.adj:
        for v in adj_table_graph.adj[u]:
            matrix_graph.add_edge(u, v)
    return matrix_graph

def adj_table_to_edge_list(adj_table_graph):
    edge_list_graph = GraphEdgeList()
    for u in adj_table_graph.adj:
        for v in adj_table_graph.adj[u]:
            edge_list_graph.add_edge(u, v)
    return edge_list_graph

import random

def generate_random_acyclic_graph(num_nodes, saturation):
    """
    Generates a random DAG (Directed Acyclic Graph) as a GraphMatrix object with a specific saturation.

    :param num_nodes: Number of nodes in the graph
    :param saturation: Saturation level (0.0 to 1.0), representing the percentage of possible edges
    :return: GraphMatrix object representing the DAG
    """
    if not (0.0 <= saturation <= 1.0):
        raise ValueError("Saturation must be between 0.0 and 1.0")

    # For a DAG, only allow edges from lower to higher index (u < v)
    possible_edges = [(u, v) for u in range(num_nodes) for v in range(u + 1, num_nodes)]
    total_possible_edges = len(possible_edges)
    num_edges = int(total_possible_edges * saturation)

    # Randomly select edges to include
    selected_edges = random.sample(possible_edges, num_edges)

    # Build the GraphMatrix object
    graph = GraphMatrix(num_nodes)
    for u, v in selected_edges:
        graph.add_edge(u, v)

    return graph



# Example usage:
# num_nodes = 5
# saturation = 0.5
# dag_graph = generate_random_acyclic_graph(num_nodes, saturation)
# dag_graph.display()

# Example usage:
# num_nodes = 5
# saturation = 0.5
# dag_matrix = generate_random_acyclic_graph_matrix(num_nodes, saturation)
# for row in dag_matrix:
#     print(row)

# # Create a GraphMatrix
# matrix_graph = GraphMatrix(3)
# matrix_graph.add_edge(0, 1)
# matrix_graph.add_edge(1, 2)
# matrix_graph.add_edge(2, 0)

# # Test matrix_to_edge_list
# print("Matrix to Edge List:")
# edge_list_graph = matrix_to_edge_list(matrix_graph)
# edge_list_graph.display()

# # Test matrix_to_adj_table
# print("\nMatrix to Adjacency Table:")
# adj_table_graph = matrix_to_adj_table(matrix_graph)
# adj_table_graph.display()

# # Test edge_list_to_matrix
# print("\nEdge List to Matrix:")
# matrix_graph_from_edge_list = edge_list_to_matrix(edge_list_graph, 3)
# matrix_graph_from_edge_list.display()

# # Test edge_list_to_adj_table
# print("\nEdge List to Adjacency Table:")
# adj_table_graph_from_edge_list = edge_list_to_adj_table(edge_list_graph)
# adj_table_graph_from_edge_list.display()

# # Test adj_table_to_matrix
# print("\nAdjacency Table to Matrix:")
# matrix_graph_from_adj_table = adj_table_to_matrix(adj_table_graph)
# matrix_graph_from_adj_table.display()

# # Test adj_table_to_edge_list
# print("\nAdjacency Table to Edge List:")
# edge_list_graph_from_adj_table = adj_table_to_edge_list(adj_table_graph)
# edge_list_graph_from_adj_table.display()