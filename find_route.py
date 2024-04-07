# Importación de módulos necesarios para el manejo de archivos, graficación, manejo de grafos, y cálculos numéricos
import os
import sys
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import heapq
import scipy as sp
from graphviz import Graph
from pyvis.network import Network

def read_file(filename: str = "input1.txt") -> dict:
    '''
    Lee un archivo de texto que describe un grafo y lo convierte en un diccionario de adyacencia.
    
    Cada línea del archivo debe contener dos nodos y el peso de la conexión entre ellos.
    El archivo puede terminar con una línea "END OF INPUT" para indicar el fin de las entradas.
    
    Parámetros:
    - filename: Ruta al archivo de entrada.
    
    Retorna:
    - Un diccionario donde cada clave es un nodo y su valor es una lista de tuplas, cada tupla contiene un nodo adyacente y el peso de la arista.
    '''
    
    adjacency_list = {}  # Inicialización del diccionario de adyacencia
    
    with open(filename, 'r') as f:  # Apertura del archivo en modo lectura
        lines = f.readlines()  # Lectura de todas las líneas del archivo
        for line in lines:  # Iteración sobre cada línea
            if line.strip() != 'END OF INPUT':  # Verificación de la línea especial de fin de entrada
                line = line.strip().split()  # División de la línea en partes
                if len(line) == 0: continue  # Ignora líneas vacías
                
                pointA, pointB, weight = line  # Desempaquetado de los elementos de la línea
                
                # Actualización del diccionario de adyacencia para ambos nodos, asegurando que la conexión sea bidireccional
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
    '''
    Implementa el algoritmo de búsqueda de costo uniforme (UCS) para encontrar la ruta más corta entre dos nodos.
    
    Utiliza una cola de prioridad para explorar los nodos en orden de su costo de ruta acumulado desde el origen,
    asegurando que la primera ruta completa encontrada al nodo destino es la más corta.
    
    Parámetros:
    - adjacency_list: El diccionario de adyacencia del grafo.
    - origin: El nodo de origen.
    - destination: El nodo de destino.
    
    Retorna:
    - Una lista de nodos representando la ruta óptima desde el origen hasta el destino, o una lista vacía si no se encuentra tal ruta.
    '''
    pq = [(0, origin, [origin])]  # Inicialización de la cola de prioridad con el nodo de origen
    visited = set()  # Conjunto para llevar registro de los nodos visitados

    while pq:
        cost, node, path = heapq.heappop(pq)  # Extracción del nodo con menor costo acumulado

        if node == destination:
            return path  # Retorno de la ruta si se alcanza el destino

        if node not in visited:
            visited.add(node)  # Marcación del nodo como visitado
            for neighbor, weight in adjacency_list[node]:  # Exploración de vecinos
                if neighbor not in visited:
                    neighbor_cost = cost + weight  # Cálculo del nuevo costo acumulado
                    heapq.heappush(pq, (neighbor_cost, neighbor, path + [neighbor]))  # Añadir vecino a la cola de prioridad

    return []  # Retorno de una lista vacía si no se encuentra una ruta al destino

def plot_graph(adjacency_list: dict, path: list = []):
    '''
    Genera y muestra una visualización de un grafo y, opcionalmente, una ruta específica dentro de ese grafo.
    
    Utiliza la biblioteca pyvis para crear un grafo interactivo visualizado en un archivo HTML.
    
    Parámetros:
    - adjacency_list: El diccionario de adyacencia que representa el grafo.
    - path: Una lista opcional de nodos que representa una ruta para resaltar en el grafo.
    '''
    net = Network(notebook=True, height="750px", width="100%", cdn_resources='in_line')
    
    # Añadir nodos y aristas al grafo interactivo
    for node in adjacency_list.keys():
        net.add_node(node, label=node, title=node)
    for node, connections in adjacency_list.items():
        for connection, weight in connections:
            net.add_edge(node, connection, label=str(weight), title=str(weight))

    # Resaltar la ruta específica, si se proporciona
    if path:
        for i in range(len(path) - 1):
            # Resaltar nodos y aristas de la ruta en rojo
            from_node, to_node = path[i], path[i + 1]
            net.get_node(from_node)["color"] = "green"
            net.get_edge(from_node, to_node)["color"] = "red"

    net.show("graph.html")  # Mostrar el grafo en un archivo HTML

# Las funciones `show_next_and_possible_moves` y `user_decide_next_move` facilitan la interacción con el usuario,
# permitiendo explorar el grafo y decidir movimientos siguiendo o desviándose de una ruta óptima precalculada.

def main():
    '''
    Función principal que coordina la ejecución del programa.
    
    Solicita al usuario ingresar los nodos de origen y destino, lee el archivo de definición del grafo,
    calcula y muestra la ruta óptima, y permite al usuario navegar por el grafo interactuando con él.
    '''
    # Limpieza de la consola para una mejor visualización
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Solicitud de entrada del usuario
    origin = input("Escribe la ciudad origen: ")
    destination = input("Escribe la ciudad destino: ")
    
    # Lectura del grafo desde un archivo y cálculo de la ruta óptima
    filename = "inputs/espanya.txt"
    adjacency_list = read_file(filename)
    optimal_path = uniform_cost_search(adjacency_list, origin, destination)
    
    # Visualización de la ruta óptima y navegación interactiva
    if optimal_path:
        print(f"La ruta óptima teórica desde {origin} hasta {destination} es: {' -> '.join(optimal_path)}")
        plot_graph(adjacency_list, path=optimal_path)
        user_decide_next_move(adjacency_list, origin, destination, optimal_path)
    else:
        print("No se encontró una ruta óptima.")
        
if __name__ == '__main__':
    main()
