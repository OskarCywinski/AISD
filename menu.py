import sys
from main import Graph, GraphAdjTable, GraphMatrix, GraphEdgeList

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
    # Tutaj wpisz, co ma robić funkcja
    print(f"Generating graph with {nodes} nodes and {saturation}% saturation.")

def generate_edge_list(nodes, saturation):
    # Tutaj wpisz, co ma robić funkcja
    print(f"Generating graph with {nodes} nodes and {saturation}% saturation.")

def generate_adj_table(nodes, saturation):
    # Tutaj wpisz, co ma robić funkcja
    print(f"Generating graph with {nodes} nodes and {saturation}% saturation.")

def exit():
    sys.exit(0)


if len(sys.argv) < 2:
    print("Invalid argument. Usage: python3 menu.py [--generate|--user-provided]")
    sys.exit(1)

arg = sys.argv[1]

allowed_types = {"matrix", "edge list", "adjacency table"}

edge_list = []

if arg == "--generate":
    try:
        type_input = input("Type> ").strip().lower()
        if type_input not in allowed_types:
            print(f"Invalid type. Allowed types: {', '.join(allowed_types)}")
            sys.exit(1)

        nodes = int(input("nodes> "))
        saturation = int(input("saturation> "))

    except ValueError:
        print("Invalid input. Please enter integers.")
        sys.exit(1)

    generate(nodes, saturation)

elif arg == "--user-provided":
        sys.stdin = open('/dev/tty')

        type_input = input("Type> ").strip().lower()
        if type_input not in allowed_types:
            print(f"Invalid type. Allowed types: {', '.join(allowed_types)}")
            sys.exit(1)

        try:
            nodes = int(input("nodes> "))
        except ValueError:
            print("Invalid nodes number.")
            sys.exit(1)

        for i in range(1, nodes + 1):
            conn = input(f"{i}> ").replace(',', ' ').strip().split()
            try:
                conn_numbers = list(map(int, conn))
            except ValueError:
                print("Invalid connection list. Only numbers are allowed.")
                sys.exit(1)

            for c in conn_numbers:
                if not (1 <= c <= nodes):
                    print(f"Connection number {c} out of allowed range (1 to {nodes})")
                    sys.exit(1)
                if c == i:
                    print(f"Node {i} cannot connect to itself!")
                    sys.exit(1)
                edge_list.append((i, c))
        print(edge_list)



else:
    print("Invalid argument. Usage: python3 menu.py [--generate|--user-provided]")
    sys.exit(1)

while True:
    print("\nNode Count>")
    print(" Nodes>")
    action = input("Action> ").strip().lower()
    
    match action:
        case "help" | "print" | "find" | "dfs" | "bfs" | "kahn" | "tarjan" | "export" | "exit":
            globals()[action]()
        case _:
            print("Invalid command. Type 'help' for a list of available commands.")
