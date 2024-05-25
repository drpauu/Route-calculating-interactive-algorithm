import os
import json
import sqlite3
import heapq
from collections import defaultdict

def read_routes_from_json(filename: str) -> list:
    """
    Llegeix rutes des d'un fitxer JSON.

    :param filename: El nom del fitxer JSON.
    :return: Una llista de rutes.
    """
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            routes = json.load(file)
        return routes
    return []

def generate_adjacency_list(routes: list) -> dict:
    """
    Genera una llista d'adjacència a partir de les rutes donades.

    :param routes: Una llista de rutes.
    :return: Un diccionari que representa la llista d'adjacència.
    """
    adjacency_list = defaultdict(list)
    for route in routes:
        origin = route['origin']
        destination = route['destination']
        distance = route['distance']
        adjacency_list[origin].append((destination, distance))
        adjacency_list[destination].append((origin, distance))
    return adjacency_list

def uniform_cost_search(lista_de_adyacencia: dict, origen: str, destino: str) -> tuple:
    """
    Realiza una búsqueda de costo uniforme en un grafo representado por una lista de adyacencia.

    Args:
        lista_de_adyacencia (dict): Lista de adyacencia del grafo.
        origen (str): Nodo de inicio de la búsqueda.
        destino (str): Nodo de destino de la búsqueda.

    Returns:
        tuple: Una tupla que contiene la lista del camino óptimo desde el nodo de origen hasta el nodo de destino,
               y la distancia total de ese camino.
    """
    pq = [(0, 0, origen, [origen])]
    visitados = set()

    while pq:
        costo, distancia, nodo, camino = heapq.heappop(pq)
        if nodo == destino:
            return camino, distancia

        if nodo not in visitados:
            visitados.add(nodo)
            for vecino, peso in lista_de_adyacencia[nodo]:
                if vecino not in visitados:
                    costo_vecino = costo + peso
                    heapq.heappush(pq, (costo_vecino, distancia + peso, vecino, camino + [vecino]))

    return [], 0

def create_database(db_name='routes.db'):
    """
    Crea una base de datos SQLite para almacenar las rutas.

    :param db_name: El nombre del archivo de la base de datos.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            path TEXT NOT NULL,
            total_distance REAL NOT NULL
        )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_origin_destination ON routes (origin, destination)')
    conn.commit()
    conn.close()

def insert_route_to_db(route, db_name='routes.db'):
    """
    Inserta una ruta calculada en la base de datos.

    :param route: La ruta calculada.
    :param db_name: El nombre del archivo de la base de datos.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO routes (origin, destination, path, total_distance)
        VALUES (?, ?, ?, ?)
    ''', (route['origin'], route['destination'], json.dumps(route['path']), route['total_distance']))
    conn.commit()
    conn.close()

def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    input_filename = "fictitious_routes.json"
    db_name = "routes.db"

    routes = read_routes_from_json(input_filename)
    adjacency_list = generate_adjacency_list(routes)

    # Crear la base de datos y la tabla de rutas
    create_database(db_name)

    for route in routes:
        origin = route['origin']
        destination = route['destination']
        optimal_path, total_distance = uniform_cost_search(adjacency_list, origin, destination)
        if optimal_path:
            calculated_route = {
                'origin': origin,
                'destination': destination,
                'path': optimal_path,
                'total_distance': total_distance
            }
            # Insertar la ruta calculada en la base de datos
            insert_route_to_db(calculated_route, db_name)
            print(f"Ruta calculada des de {origin} fins a {destination}: {' -> '.join(optimal_path)}, Distància total: {total_distance} km")
        else:
            print(f"No s'ha trobat cap ruta òptima des de {origin} fins a {destination}.")

    print(f"Totes les rutes calculades s'han guardat en la base de dades '{db_name}'.")

if __name__ == '__main__':
    main()
