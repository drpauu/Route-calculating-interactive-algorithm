import os
import sys
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import heapq
        
def read_file(filename: str = "input1.txt") -> dict:
    
    '''
    Takes a file as input. 
    Each line denotes two nodes and their connection weight.
    
    Return a dictionary of nodes and their connections and weights.
    '''
    
    adjacency_list = {}
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.strip() != 'END OF INPUT':
                line = line.strip().split()
                if len(line) == 0: continue
                
                pointA, pointB, weight = line
                
                # Update the dictionary bidirectionally
                if pointA not in adjacency_list:
                    adjacency_list[pointA] = [(pointB, int(weight))]
                else:
                    adjacency_list[pointA].append((pointB, int(weight)))
                
                if pointB not in adjacency_list:
                    adjacency_list[pointB] = [(pointA, int(weight))]
                else:
                    adjacency_list[pointB].append((pointA, int(weight)))
                
    return adjacency_list

def uniform_cost_search(adjacency_list: dict, origin: str, destination: str) -> list:
    # Initialize priority queue with the starting node and a cost of 0
    pq = [(0, origin, [origin])]
    # Initialize visited set
    visited = set()

    while pq:
        # Remove node with smallest cost from priority queue
        cost, node, path = heapq.heappop(pq)

        if node == destination:
            # If the destination node is reached, return the path from the origin node to the destination node
            return path

        if node not in visited:
            # Mark node as visited
            visited.add(node)
            # Add neighbors to priority queue with their corresponding costs
            for neighbor, weight in adjacency_list[node]:
                if neighbor not in visited:
                    # Compute cost of neighbor as the sum of the cost of the current node and the weight of the edge between the current node and the neighbor
                    neighbor_cost = cost + weight
                    # Add neighbor to priority queue with its corresponding cost and path
                    heapq.heappush(pq, (neighbor_cost, neighbor, path + [neighbor]))

    # If the destination node is not reached, return an empty path
    return []

def plot_graph(adjacency_list: dict, path: list = [], random_seed: int = 0):
    '''
    Takes an adjacency list as input.
    Draws a graph of nodes and their connections.
    '''
    
    np.random.seed(random_seed)
    
    # Create a new graph object
    G = nx.Graph()
    
    # Add nodes to the graph
    nodes = list(adjacency_list.keys())
    G.add_nodes_from(nodes)
    
    # Add edges to the graph
    for node, connections in adjacency_list.items():
        for connection in connections:
            G.add_edge(node, connection[0], weight=connection[1], inverse_weight=1/connection[1])
    
    # Get the positions of the nodes in the graph
    pos = nx.layout.spring_layout(G, k=0.1, iterations=50, scale=7, weight='inverse_weight')
    
    # Draw the nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=50)
    
    # Draw the edges
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    
    # Draw edges in path in red
    path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
    path_edges = [(u, v) for (u, v) in path_edges if G.has_edge(u, v)]
    
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=3, edge_color='red')
    nx.draw_networkx_edges(G, pos, edgelist=set(edges) - set(path_edges), width=1, edge_color='gray')
    
    # Draw the labels
    nx.draw_networkx_labels(G, pos, font_size=5, font_family='sans-serif')
    
    # Add a title and display the graph
    plt.title("Dades sintètiques - Graf de les ciutats d'Espanya")
    plt.axis('off')
    plt.show()

    
def output_path(adjacency_list: dict, path: list):
    # Compute the cost of the path
    distance = 0
    for i, node in enumerate(path):
        
        if i == len(path) - 1:
            break
        
        connections = adjacency_list[node]
        for connection in connections:
            name = connection[0]
            if name == path[i+1]:
                distance += connection[1]
                break
        
    if len(path) == 0:
        print("distance: infinity")
        print("route:")
        print("none")
        return
        
    print(f"distance: {distance} km")
    print("route:")
    
    if len(path) == 1:
        print(f"{path[0]} to {path[0]}, 0 km")
        return
    
    for i, node in enumerate(path):
        if i == len(path) - 1:
            break
        
        connections = adjacency_list[node]
        dist = 0
        for connection in connections:
            name = connection[0]
            if name == path[i+1]:
                dist = connection[1]
                break
        
        print(f"{node} to {path[i+1]}, {dist} km")


def show_next_and_possible_moves(adjacency_list: dict, origin: str):
    """
    Muestra el siguiente movimiento recomendado y los movimientos posibles desde la ciudad de origen.
    
    :param adjacency_list: El diccionario de adyacencia que representa el grafo.
    :param origin: La ciudad de origen desde donde se calculan los movimientos.
    """
    if origin in adjacency_list:
        possible_moves = adjacency_list[origin]
        print(f"Desde {origin}, los movimientos posibles son:")
        for move in possible_moves:
            destination, distance = move
            print(f"  - A {destination} con una distancia de {distance} km")
    else:
        print(f"No se encontraron movimientos posibles desde {origin}.")


def user_decide_next_move(adjacency_list: dict, origin: str, destination: str, optimal_path):
    """
    Permite al usuario decidir el siguiente destino de los movimientos posibles. Si el usuario elige el movimiento
    correcto según la ruta óptima, no se recalcula la ruta. De lo contrario, se muestra la ruta recalculada hacia
    el destino final y el siguiente movimiento recomendado.
    
    :param adjacency_list: El diccionario de adyacencia que representa el grafo.
    :param origin: La ciudad de origen desde donde se calculan los movimientos.
    :param destination: El destino final deseado.
    :param optimal_path: La ruta óptima previamente calculada desde el origen hasta el destino.
    """
    current_origin = origin
    current_path_index = 0  # Índice del origen actual en la ruta óptima

    while current_origin != destination:
        if current_origin in adjacency_list:
            possible_moves = adjacency_list[current_origin]
            print(f"\nTu siguiente movimiento debería ser: {optimal_path[current_path_index + 1]}")
            print(f"\nDesde {current_origin}, los movimientos posibles son:")
            for i, move in enumerate(possible_moves, start=1):
                next_destination, distance = move
                print(f"{i}. A {next_destination} con una distancia de {distance} km")

            choice = int(input("Elige tu próximo destino (número): ")) - 1
            if 0 <= choice < len(possible_moves):
                next_destination, _ = possible_moves[choice]
                print(f"\nHas elegido ir a {next_destination}.")

                # Verificar si la elección coincide con el próximo paso en la ruta óptima
                if next_destination == optimal_path[current_path_index + 1]:
                    print("Has elegido el movimiento correcto según la ruta óptima.")
                    current_origin = next_destination
                    current_path_index += 1
                    if current_origin == destination:
                        print("Has llegado a tu destino final.")
                        return
                    continue
                
                # Recalcular la ruta si la elección no es el próximo paso en la ruta óptima
                new_path = uniform_cost_search(adjacency_list, next_destination, destination)
                if new_path:
                    print("Ruta recalculada hacia el destino final:", " -> ".join(new_path))
                    optimal_path = new_path  # Actualizar la ruta óptima con la nueva ruta
                    current_path_index = 0  # Resetear el índice de la ruta óptima
                else:
                    print("No se pudo encontrar una ruta desde tu ubicación actual hasta el destino final.")
                    return
                current_origin = next_destination
            else:
                print("Opción no válida, intenta de nuevo.")
        else:
            print(f"No se encontraron movimientos posibles desde {current_origin}.")
            return

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    origin = str(input("Escribe la ciudad origen: "))
    destination = str(input("Escribe la ciudad destino: "))
    
    filename = "inputs/espanya.txt"
    adjacency_list = read_file(filename)

    print("Calculando la ruta óptima...")
    optimal_path = uniform_cost_search(adjacency_list, origin, destination)
    if optimal_path:
        print(f"La ruta óptima teórica desde {origin} hasta {destination} es: {' -> '.join(optimal_path)}")
    else:
        print("No se encontró una ruta óptima.")
        return

    user_decide_next_move(adjacency_list, origin, destination, optimal_path)

if __name__ == '__main__':
    main()
