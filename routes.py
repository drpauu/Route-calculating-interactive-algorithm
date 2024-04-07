import os
import sys
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import heapq

def command_line_inputs():
    try:
        origin = input("Ingrese la ciudad de origen: ")
        destination = input("Ingrese la ciudad de destino: ")
        return origin, destination
    except ValueError:
        print('Error en la entrada. Por favor, ingrese correctamente los datos.')
        sys.exit(1)

def read_file(filename: str = "/home/user/Github/Routes-algorithm/inputs/espanya.txt") -> dict:
    adjacency_list = {}
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.strip() != 'END OF INPUT':
                line = line.strip().split()
                if len(line) == 0: continue
                
                pointA, pointB, weight = line
                if pointA not in adjacency_list:
                    adjacency_list[pointA] = [(pointB, int(weight))]
                else:
                    adjacency_list[pointA].append((pointB, int(weight)))
                
                if pointB not in adjacency_list:
                    adjacency_list[pointB] = [(pointA, int(weight))]
                else:
                    adjacency_list[pointB].append((pointA, int(weight)))
                
    return adjacency_list

def choose_next_city(current_city: str, adjacency_list: dict) -> str:
    print(f"Actualmente estás en: {current_city}")
    connections = adjacency_list[current_city]
    print("Puedes moverte a las siguientes ciudades:")
    for i, (neighbor, _) in enumerate(connections):
        print(f"{i + 1}. {neighbor}")
    choice = int(input("Elige el número de tu próxima ciudad: ")) - 1
    return connections[choice][0]

def plot_graph(adjacency_list: dict, path: list = [], random_seed: int = 0):
    np.random.seed(random_seed)
    G = nx.Graph()
    nodes = list(adjacency_list.keys())
    G.add_nodes_from(nodes)
    for node, connections in adjacency_list.items():
        for connection in connections:
            G.add_edge(node, connection[0], weight=connection[1], inverse_weight=1/connection[1])
    pos = nx.layout.spring_layout(G, k=0.1, iterations=50, scale=7, weight='inverse_weight')
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=50)
    edges = G.edges()
    path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
    path_edges = [(u, v) for (u, v) in path_edges if G.has_edge(u, v)]
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=3, edge_color='red')
    nx.draw_networkx_edges(G, pos, edgelist=set(edges) - set(path_edges), width=1, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=5, font_family='sans-serif')
    plt.title("Dades sintètiques - Graf de les ciutats d'Espanya")
    plt.axis('off')
    plt.show()

def interactive_route_planning(adjacency_list: dict, origin: str, destination: str):
    current_city = origin
    path = [origin]

    while current_city != destination:
        next_city = choose_next_city(current_city, adjacency_list)
        path.append(next_city)
        current_city = next_city
        plot_graph(adjacency_list, path)
    
    print("Has llegado a tu destino.")
    print("Ruta seguida:")
    for city in path:
        print(city, end=" -> ")
    print("Fin")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    origin, destination = command_line_inputs()
    adjacency_list = read_file("/home/user/Github/Routes-algorithm/inputs/espanya.txt")
    interactive_route_planning(adjacency_list, origin, destination)

if __name__ == '__main__':
    main()
