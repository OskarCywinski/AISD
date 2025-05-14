import argparse
import sys
from graph import Graph, GraphAdjTable, GraphMatrix, GraphEdgeList, matrix_to_adj_table, matrix_to_edge_list, edge_list_to_matrix, edge_list_to_adj_table, adj_table_to_matrix, adj_table_to_edge_list, generate_random_acyclic_graph_matrix

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

def generate_matrix(nodes, saturation):
    # Generowanie grafu
    print(f"Generating graph with {nodes} nodes and {saturation}% saturation.")
    Graph = generate_random_acyclic_graph_matrix(nodes, saturation/100)

def generate_edge_list(nodes, saturation):
    # Generowanie grafu
    print(f"Generating graph with {nodes} nodes and {saturation}% saturation.")
    Graph = generate_random_acyclic_graph_matrix(nodes, saturation/100)
    Graph = matrix_to_edge_list(Graph)

def generate_adj_table(nodes, saturation):
    # Generowanie grafu
    print(f"Generating graph with {nodes} nodes and {saturation}% saturation.")
    Graph = generate_random_acyclic_graph_matrix(nodes, saturation/100)
    Graph = matrix_to_adj_table(Graph)

def exit():
    sys.exit(0)

def Print():
    Graph.display()

def parse_graph_input(input_data):
    # Parsowanie danych wejściowych na połączenia
    connections = []
    lines = input_data.strip().splitlines()
    
    for i in range(len(lines)):
        node_from = i + 1  # Zaczynamy od 1
        node_to = int(lines[i])
        
        # Jeśli node_from jest różne od node_to, dodajemy połączenie
        if node_from != node_to:
            connections.append(f"{node_from}-{node_to}")
        else:
            print(f"Warning: Node {node_from} is trying to connect to itself, skipping.")
    
    return connections

def user_provided_from_stdin():
    # Obsługuje dane z heredoc
    print("Wczytywanie danych od użytkownika przez heredoc:")
    input_data = sys.stdin.read()
    connections = parse_graph_input(input_data)
    return connections

def user_provided_from_file(file_path):
    # Wczytuje dane z pliku
    print(f"Wczytywanie danych z pliku: {file_path}")
    try:
        with open(file_path, 'r') as f:
            input_data = f.read()
        connections = parse_graph_input(input_data)
        return connections
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
        connections = user_provided_from_file(args.file)
    else:
        # Jeśli dane są przez heredoc
        connections = user_provided_from_stdin()
    
    # Liczymy liczbę węzłów
    nodes = max([int(c.split('-')[0]) for c in connections] + [int(c.split('-')[1]) for c in connections])
    
    print(f"Wczytane dane: Połączenia: {connections}, Liczba węzłów: {nodes}")
    sys.stdin = open('/dev/tty')

elif args.generate:
    # Generowanie danych
    print("Dane zostaną wygenerowane automatycznie.")
    allowed_types = {"matrix", "edge_list", "adjacency_table"}
    while True:
        type_input = input("Type> ").strip().lower()
        if type_input in allowed_types:
            break
        print(f"Invalid type. Allowed types: {', '.join(allowed_types)}")
    
    nodes = int(input("nodes> "))
    saturation = int(input("saturation> "))
    match type_input:
        case "matrix" | "edge_list" | "adjacency_table":
            globals()[f"generate_{type_input}"](nodes, saturation)
        case _:
            print(f"Unknown type: {type_input}")

else:
    print("Musisz podać jeden z argumentów: --user-provided lub --generate")

# Wykonywanie komend po wybraniu
while True:
    print("\nNode Count>")
    print(" Nodes>")
    action = input("Action> ").strip().lower()
    
    match action:
        case "help" | "Print" | "find" | "dfs" | "bfs" | "kahn" | "tarjan" | "export" | "exit":
            globals()[action]()
        case _:
            print("Invalid command. Type 'help' for a list of available commands.")
