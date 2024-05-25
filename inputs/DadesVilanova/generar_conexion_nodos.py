import json
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def cargar_datos(archivo):
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("El archivo no se encontró.")
    except json.JSONDecodeError:
        print("Error al decodificar el archivo JSON.")
    return None

def obtener_distancia_tiempo(coordenadas_origen, coordenadas_destino, access_token, session):
    url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{coordenadas_origen};{coordenadas_destino}?access_token={access_token}"
    response = session.get(url)
    if response.status_code == 200:
        data = response.json()
        distancia = data['routes'][0]['distance']
        tiempo = data['routes'][0]['duration']
        return distancia, tiempo
    elif response.status_code == 429:
        print("Error 429: Demasiadas solicitudes. El programa se pausará durante 1 minuto.")
        time.sleep(60)  # Pausa durante 1 minuto
        return obtener_distancia_tiempo(coordenadas_origen, coordenadas_destino, access_token, session)  # Reintentar la solicitud
    else:
        print("Error al obtener la distancia y tiempo:", response.text)
        return None, None

def procesar_conexion(nodo1, nodo2, nodos_coordenadas, access_token, session):
    if nodo1 in nodos_coordenadas and nodo2 in nodos_coordenadas:
        lon1, lat1 = nodos_coordenadas[nodo1]
        lon2, lat2 = nodos_coordenadas[nodo2]
        distancia, tiempo = obtener_distancia_tiempo(f"{lon1},{lat1}", f"{lon2},{lat2}", access_token, session)
        if distancia is not None and tiempo is not None:
            return f"{nodo1}, {nodo2}, {distancia}, {tiempo}"
    return None

def guardar_conexiones(conexiones, archivo_salida):
    with open(archivo_salida, 'w', encoding='utf-8') as file:
        for conexion in conexiones:
            file.write(conexion + '\n')

def main():
    archivo_json = 'Vilanova.json'
    archivo_salida = 'conexion_nodos.txt'
    access_token = 'pk.eyJ1IjoiYWpidiIsImEiOiJjbHdmNTRscnoxbGgxMmlwYThqZDJmNmo2In0.Fxyr0FGk196DaN6v7Z71Zg'

    data = cargar_datos(archivo_json)
    if not data:
        return

    nodos_coordenadas = {}
    conexiones = []

    for element in data['elements']:
        if element['type'] == 'node':
            nodo_id = element['id']
            lat = element['lat']
            lon = element['lon']
            nodos_coordenadas[nodo_id] = (lon, lat)

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for element in data['elements']:
            if element['type'] == 'way':
                nodes = element['nodes']
                oneway = element['tags'].get('oneway', 'no')
                for i in range(len(nodes) - 1):
                    nodo1 = nodes[i]
                    nodo2 = nodes[i+1]
                    if oneway == 'yes':
                        futures.append(executor.submit(procesar_conexion, nodo1, nodo2, nodos_coordenadas, access_token, session))
                    else:
                        futures.append(executor.submit(procesar_conexion, nodo1, nodo2, nodos_coordenadas, access_token, session))
                        futures.append(executor.submit(procesar_conexion, nodo2, nodo1, nodos_coordenadas, access_token, session))
        for future in as_completed(futures):
            conexion = future.result()
            if conexion:
                conexiones.append(conexion)

    guardar_conexiones(conexiones, archivo_salida)

if __name__ == "__main__":
    main()
