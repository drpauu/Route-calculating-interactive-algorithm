import os
import sys
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import heapq
import scipy as sp
from graphviz import Graph
from pyvis.network import Network
from collections import defaultdict

# PRE: El fitxer "filename" existeix i conté línies amb el format "puntA puntB pes".
#      La línia "END OF INPUT" marca la fi del fitxer.
# POST: S'ha creat un diccionari "adjacency_list" que representa la llista d'adjacència.
#       Cada clau correspon a un punt del graf, i els seus valors són tuples amb els punts adjacents i els seus pesos associats.
# Cost espai-temporal: O(E), on E és el nombre d'arestes (relacions d'adjacència) al graf.
def read_file(filename: str = "input1.txt") -> dict:
    """
    Llegeix un fitxer de text i crea una llista d'adjacència per a un graf no dirigit.

    :param filename: El nom del fitxer a llegir (per defecte: "input1.txt").
    :return: Un diccionari que representa la llista d'adjacència.
    """
    adjacency_list = defaultdict(list) # Diccionari amb llistes com a valors per a cada clau
    with open(filename, 'r') as f:
        # Invariant: El bucle "for line in f" recorre totes les línies del fitxer.
        for line in f:
            line = line.strip() # Elimina espais en blanc al principi i al final de la línia
            if line != 'END OF INPUT':
                # Invariant: El bucle "for pointA, pointB, weight in line.split()" divideix cada línia en tres parts.
                pointA, pointB, weight = line.split() # Divideix la línia en tres parts
                weight = int(weight) # Converteix el pes a un enter
                # Afegeix una tupla (pointB, weight) a la llista d'adjacència de pointA i viceversa
                adjacency_list[pointA].append((pointB, weight))
                adjacency_list[pointB].append((pointA, weight))
    return adjacency_list

def uniform_cost_search(lista_de_adyacencia: dict, origen: str, destino: str) -> list:
    # Inicializar cola de prioridad con el nodo inicial y un costo de 0
    pq = [(0, origen, [origen])]
    # Inicializar conjunto de nodos visitados
    visitados = set()

    while pq:
        # Eliminar nodo con menor costo de la cola de prioridad
        costo, nodo, camino = heapq.heappop(pq)

        if nodo == destino:
            # Si se alcanza el nodo destino, devolver el camino desde el nodo origen hasta el nodo destino
            return camino

        if nodo not in visitados:
            # Marcar nodo como visitado
            visitados.add(nodo)
            # Agregar vecinos a la cola de prioridad con sus costos correspondientes
            for vecino, peso in lista_de_adyacencia[nodo]:
                if vecino not in visitados:
                    # Calcular costo del vecino como la suma del costo del nodo actual y el peso de la arista entre el nodo actual y el vecino
                    costo_vecino = costo + peso
                    # Agregar vecino a la cola de prioridad con su costo y camino correspondientes
                    heapq.heappush(pq, (costo_vecino, vecino, camino + [vecino]))

    # Si no se alcanza el nodo destino, devolver un camino vacío
    return []


# PRE: La variable 'adjacency_list' es un diccionario que representa la lista de adyacencia del grafo.
#      La variable 'path' es una lista que contiene la ruta óptima en el grafo, si se proporciona.
# POST: Se ha generado y mostrado el grafo en un archivo HTML.
# Costo espacial-temporal: O(V + E), donde V es el número de vértices y E es el número de aristas en el grafo.
def plot_graph(adjacency_list: dict, path: list = []):
    """
    Genera y muestra un grafo visualmente utilizando la biblioteca pyvis.

    Args:
        adjacency_list (dict): Diccionario que representa la lista de adyacencia del grafo.
        path (list, optional): Ruta óptima a resaltar en el grafo. Por defecto, una lista vacía.

    Returns:
        None
    """
    # Crear un objeto Network para visualizar el grafo
    net = Network(notebook=True, height="750px", width="100%", cdn_resources='in_line') # Se configura para ser mostrado en un entorno de notebook, con una altura de 750px y un ancho del 100% de la ventana del navegador. Además se especifica que los recursos necesarios para visualizar el grafo se incrustarán directamente en el HTML generado.   

    # Agregar nodos al grafo
    for node in adjacency_list.keys():
        net.add_node(node, label=node, title=node) # Invariante: este bucle itera sobre cada nodo en el diccionario “adjacency_list” y agrega cada nodo al grafo “net”. El “label” y el “title” de cada nodo se establecen en el nombre del nodo.

    # Agregar aristas al grafo
    for node, connections in adjacency_list.items():
        for connection, weight in connections:
            net.add_edge(node, connection, label=str(weight), title=str(weight)) # Invariante: este bucle anidado itera sobre cada nodo en el diccionario “adjacency_list” y sus conexiones. Para cada conexión, agrega una arista al grafo “net”. El “label” y el “title” de cada arista se establecen en el peso de la conexión.

    # Resaltar los nodos y aristas en la ruta óptima, si se proporciona
    if path:
        for node in path:
            net.get_node(node)["color"] = "green" # Invariante: este bucle itera sobre cada nodo en la lista “path”, estableciendo el color de cada nodo en verde.
        for i in range(len(path) - 1):
            from_node = path[i]
            to_node = path[i + 1]
            for edge in net.edges:
                if edge["from"] == from_node and edge["to"] == to_node or edge["from"] == to_node and edge["to"] == from_node:
                    edge["color"] = "red" # Invariante: este bucle itera sobre cada par de nodos consecutivos en “path”, encontrando la arista correspondiente en el grafo y estableciendo su color en rojo
                    break

    # Generar y mostrar el grafo en un archivo HTML
    net.show("graph.html")

def user_decide_next_move(adjacency_list: dict, origin: str, destination: str, optimal_path):
    """
    Interactúa con el usuario para decidir el próximo destino en un recorrido, considerando o recalculando
    la ruta óptima según las elecciones del usuario.

    Parámetros:
    - adjacency_list: Diccionario que representa el grafo de ciudades conectadas.
    - origin: La ciudad de origen o punto de partida actual.
    - destination: La ciudad destino o punto final deseado.
    - optimal_path: Lista que representa la ruta óptima calculada desde el origen hasta el destino.

    La función continúa solicitando al usuario que elija su próximo movimiento hasta que se alcance el destino.
    Si el usuario elige el siguiente movimiento correcto según la ruta óptima, se avanza sin recalcular la ruta.
    De lo contrario, si elige un camino diferente, se recalcula y muestra una nueva ruta óptima desde la nueva posición actual hasta el destino.
    """
    current_origin = origin  # Ciudad actual de partida
    current_path_index = 0  # Índice de la ciudad actual en la ruta óptima

    while current_origin != destination: # Verificar si hay movimientos posibles desde la ubicación actual
        if current_origin in adjacency_list:
            possible_moves = adjacency_list[current_origin]
            print(f"\nTu siguiente movimiento debería ser: {optimal_path[current_path_index + 1]}")
            print(f"\nDesde {current_origin}, los movimientos posibles son:")
            for i, move in enumerate(possible_moves, start=1):
                next_destination, distance = move
                print(f"{i}. A {next_destination} con una distancia de {distance} km")

        	# Solicitar al usuario que elija su próximo destino
            choice = int(input("Elige tu próximo destino (número): ")) - 1
            if 0 <= choice < len(possible_moves):
                next_destination, _ = possible_moves[choice]
                print(f"\nHas elegido ir a {next_destination}.")

            	# Comprobar si la elección del usuario coincide con la ruta óptima
                if next_destination == optimal_path[current_path_index + 1]:
                    print("Has elegido el movimiento correcto según la ruta óptima.")
                    current_origin = next_destination
                    current_path_index += 1
                    if current_origin == destination:
                        print("Has llegado a tu destino final.")
                        return
                else:
                    # Recalcular y mostrar la nueva ruta óptima si el usuario elige un camino diferente
                    new_path = uniform_cost_search(adjacency_list, next_destination, destination)
                    if new_path:
                        print("Ruta recalculada hacia el destino final:", " -> ".join(new_path))
                        plot_graph(adjacency_list, path=new_path)
                        optimal_path = new_path
                        current_path_index = 0
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
    os.system('cls' if os.name == 'nt' else 'clear')  # Esborra la pantalla per a una millor visualització
    origin = str(input("Escribe la ciudad origen: "))  # Sol·licita a l'usuari la ciutat d'origen
    destination = str(input("Escribe la ciudad destino: "))  # Sol·licita a l'usuari la ciutat de destí

    filename = "inputs/espanya.txt"  # Defineix el nom del fitxer que conté les dades del graf
    adjacency_list = read_file(filename)  # Llegeix les dades del fitxer i crea la llista d'adjacència del graf

    print("Calculando la ruta óptima...")  # Indica que es calcula la ruta òptima
    optimal_path = uniform_cost_search(adjacency_list, origin, destination)  # Calcula la ruta òptima des de l'origen fins al destí
    if optimal_path:
        print(f"La ruta óptima teórica desde {origin} hasta {destination} es: {' -> '.join(optimal_path)}")
        # Imprimeix la ruta òptima teòrica des de l'origen fins al destí
        plot_graph(adjacency_list, path=optimal_path)  # Visualitza el graf amb la ruta òptima
    else:
        print("No se encontró una ruta óptima.")  # Indica que no s'ha trobat cap ruta òptima
        return

    user_decide_next_move(adjacency_list, origin, destination, optimal_path)  # Permet a l'usuari decidir els següents moviments

if __name__ == '__main__':
    main()  # Inicia l'execució del programa principal si s'executa com a script
