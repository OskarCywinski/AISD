import argparse
import sys
import os
from graph import Graph, GraphAdjTable, GraphMatrix, GraphEdgeList, matrix_to_adj_table, matrix_to_edge_list, edge_list_to_matrix, edge_list_to_adj_table, adj_table_to_matrix, adj_table_to_edge_list, generate_random_acyclic_graph

def help():
    print("\nCommands:")
    print("  Help   > Show this message")
    print("  Print  > Print the graph")
    print("  Find   > Check if an edge exists")
    print("  DFS    > perform Depth First Search")
    print("  BFS    > perform Breadth First Search")
    print("  Kahn   > sort the graph using Kahn's algorithm")
    print("  Tarjan > sort the graph using Tarjan's algorithm")
    print("  Export > Export the graph to tickzpicture")
    print("  Exit   > Exits the program\n")

graph = Graph()

def generate_matrix(nodes, saturation):
    # Generowanie grafu
    global graph
    print(f"Generating graph with {nodes} nodes and {saturation}% saturation.")
    graph = generate_random_acyclic_graph(nodes, saturation/100)
    graph.display()

def generate_edge_list(nodes, saturation):
    # Generowanie grafu
    global graph
    print(f"Generating graph with {nodes} nodes and {saturation}% saturation.")
    graph = generate_random_acyclic_graph(nodes, saturation/100)
    graph = matrix_to_edge_list(graph)
    graph.display()

def generate_adjacency_table(nodes, saturation):
    # Generowanie grafu
    global graph
    print(f"Generating graph with {nodes} nodes and {saturation}% saturation.")
    graph = generate_random_acyclic_graph(nodes, saturation/100)
    graph = matrix_to_adj_table(graph)
    graph.display()

def exit():
    sys.exit(0)

def print_graph():
    global graph
    graph.display()
    
def find():
    global graph
    while True:
        try:
            in_node = int(input("from> "))
            if in_node < 0 or in_node >= len(graph.get_all_nodes()):
                print(f"Node {in_node} is out of range. Please enter a valid node number.")
                continue
            break
        except:
            print("Invalid input. Please enter an integer.")
    while True:
        try:
            out_node = int(input("to> "))
            if out_node < 0 or out_node >= len(graph.get_all_nodes()):
                print(f"Node {out_node} is out of range. Please enter a valid node number.")
                continue
            break
        except:
            print("Invalid input. Please enter an integer.")
    if graph.has_edge(int(in_node), int(out_node)):
        print(True, ":  edge (", in_node, ",", out_node, ") exists in the graph")
    else:
        print(False, ":  edge (", in_node, ",", out_node, ") does not exist in the graph")
        
def depth_first_search():
    global graph
    graph.DFS(0)
    
def breadth_first_search():
    global graph
    graph.BFS(0)
    
def kahn():
    global graph
    graph.Kahn()
    
def tarjan():
    global graph
    graph.Tarjan()

def export():
    global graph
    graph.export()

def parse_graph_input(connections, num_nodes):
    # Parsowanie danych wejściowych na połączenia
    valid_connections = []
    for node_from, node_to in connections:
        if 1 <= node_from <= num_nodes and 1 <= node_to <= num_nodes and node_from != node_to:
            valid_connections.append((node_from, node_to))
        else:
            print(f"Warning: Invalid connection {node_from}-{node_to}, skipping.")
    
    return valid_connections 

def user_provided_from_stdin():
    connections = []

    if os.isatty(sys.stdin.fileno()):
        # Interaktywny tryb
        print("Interaktywny tryb wprowadzania danych.")
        while True:
            try:
                nodes = int(input("nodes> "))
                break
            except:
                print("Invalid input. Please enter an integer.")
        for i in range(nodes):
            while True:
                raw = input(f"{i}> ").strip()
                if not raw:
                    break
                try:
                    conn_nodes = list(map(int, raw.replace(',', ' ').split()))
                    # Sprawdź poprawność
                    if all(0 <= n < nodes and n != i for n in conn_nodes):
                        for n in conn_nodes:
                            connections.append((i, n))
                        break  # poprawne dane
                    else:
                        print(f"Niedozwolone połączenia. Możesz łączyć tylko z node'ami od 0 do {nodes-1}, bez połączeń do siebie ({i}).")
                except ValueError:
                    print("Podaj tylko liczby oddzielone spacją lub przecinkiem.")
    else:
        # Heredoc – dane z stdin
        print("Tryb heredoc – wczytywanie danych z stdin.")
        lines = sys.stdin.read().strip().splitlines()
        nodes = len(lines)
        for i, line in enumerate(lines):
            raw = line.strip()
            try:
                conn_nodes = list(map(int, raw.split()))
                for n in conn_nodes:
                    if 0 <= n < nodes and n != i:
                        connections.append((i, n))
                    else:
                        print(f"Pominięto niedozwolone połączenie: {i} → {n}")
            except ValueError:
                print(f"Pominięto nieprawidłowe dane w linii {i}: {line}")
    print(connections)

    # Pytamy o typ grafu na końcu
    sys.stdin = open('/dev/tty')
    graph_type = input("Type> ").strip().lower().replace(" ", "_")
    return graph_type, nodes, connections

def user_provided_from_file(file_path):
    # Wczytuje dane z pliku
    print(f"Wczytywanie danych z pliku: {file_path}")
    try:
        with open(file_path, 'r') as f:
            graph_type = f.readline().strip().lower()  # Typ grafu w pierwszej linii
            nodes = int(f.readline().strip())  # Liczba węzłów w drugiej linii
            input_data = f.read()
        connections = parse_graph_input(input_data, nodes)
        return graph_type, nodes, connections
    except FileNotFoundError:
        print(f"Błąd: Plik {file_path} nie istnieje.")
        sys.exit(1)

# Argumenty
parser = argparse.ArgumentParser()
parser.add_argument('--user-provided', action='store_true')
parser.add_argument('--generate', action='store_true')
parser.add_argument('--file', type=str, help='Path to the input file')
args = parser.parse_args()

selected_args = sum([args.user_provided, args.generate])

# Sprawdzenie poprawności argumentów
if selected_args == 0:
    print("Błąd: Musisz podać jeden z argumentów: --user-provided lub --generate")
    sys.exit(1)
elif selected_args > 1:
    print("Błąd: Nie możesz podać obu argumentów jednocześnie. Wybierz tylko jeden z: --user-provided lub --generate")
    sys.exit(1)

# Jeśli użytkownik podał dane
if args.user_provided:
    if args.file:
        # Jeśli podano plik
        graph_type, nodes, connections = user_provided_from_file(args.file)
    else:
        # Jeśli dane są przez heredoc
        graph_type, nodes, connections = user_provided_from_stdin()

    # Tworzymy graf na podstawie podanych danych
    if graph_type == "matrix":
        graph = GraphMatrix(nodes)
    elif graph_type == "edge_list":
        graph = GraphEdgeList(nodes)
    elif graph_type == "adjacency_table":
        graph = GraphAdjTable(nodes)
    else:
        print(f"Unknown graph type: {graph_type}")
        sys.exit(1)

    # Dodajemy połączenia
    for node_from, node_to in connections:
        graph.add_edge(node_from, node_to)
    
    graph.display()

elif args.generate:
    # Generowanie danych
    print("Dane zostaną wygenerowane automatycznie.")
    allowed_types = {"matrix", "edge_list", "adjacency_table"}
    while True:
        type_input = input("Type> ").strip().lower().replace(" ", "_")
        if type_input in allowed_types:
            break
        print(f"Invalid type. Allowed types: {', '.join(allowed_types)}")
    
    while True:
        try:
            nodes = int(input("nodes> "))
            break
        except:
            print("Invalid input. Please enter an integer.")
    while True:
        try:
            saturation = int(input("saturation> "))
            if saturation < 0 or saturation > 100:
                print("Saturation must be between 0 and 100.")
                continue
            break
        except:
            print("Invalid input. Please enter an integer.")
    match type_input:
        case "matrix" | "edge_list" | "adjacency_table":
            globals()[f"generate_{type_input}"](nodes, saturation)
        case _:
            print(f"Unknown type: {type_input}")

else:
    print("Musisz podać jeden z argumentów: --user-provided lub --generate")

# Wykonywanie komend po wybraniu
while True:
    print("\nNode Count>", len(graph.get_all_nodes()))
    action = input("Action> ").strip().lower()
    
    match action:
        case "help" | "print" | "find" | "depth-first search" | "breadth-first search" | "kahn" | "tarjan" | "export" | "exit":
            globals()[action.replace(" ", "_").replace("-","_")]() if action != "print" else print_graph()
        case _:
            print("Invalid command. Type 'help' for a list of available commands.")
