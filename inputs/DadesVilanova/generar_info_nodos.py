import json
import requests
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor, as_completed

def cargar_datos(archivo):
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("El archivo no se encontró.")
    except json.JSONDecodeError:
        print("Error al decodificar el archivo JSON.")
    return None

def obtener_direccion(lat, lon, access_token, session, cache):
    if (lat, lon) in cache:
        return cache[(lat, lon)]
    
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{lon},{lat}.json"
    params = {'access_token': access_token}

    try:
        response = session.get(url, params=params)
        response.raise_for_status()
        datos = response.json()
        if datos['features']:
            direccion = datos['features'][0]['place_name']
            cache[(lat, lon)] = direccion
            return direccion
        else:
            return "No se encontró ninguna dirección para las coordenadas dadas."
    except requests.RequestException as e:
        if isinstance(e, requests.HTTPError) and e.response.status_code == 429:
            print("Error 429: Demasiadas solicitudes. El programa se pausará durante 1 minuto.")
            time.sleep(60)  # Pausa durante 1 minuto
            return obtener_direccion(lat, lon, access_token, session, cache)  # Reintentar la solicitud
        else:
            return f"Error en la solicitud: {e}"
            
def procesar_nodo(element, access_token, session, cache):
    nodo_id = element['id']
    lat = element['lat']
    lon = element['lon']
    direccion = obtener_direccion(lat, lon, access_token, session, cache)
    return f"[{nodo_id}], [{lon},{lat}], [{direccion}], [disponible]"

def guardar_info_nodos(info_nodos, archivo):
    with open(archivo, 'w', encoding='utf-8') as file:
        for info in info_nodos:
            file.write(info + '\n')

def main():
    archivo_json = 'Vilanova.json'
    archivo_salida = 'info_nodos.txt'
    access_token = 'pk.eyJ1IjoiYWpidiIsImEiOiJjbHdmNTRscnoxbGgxMmlwYThqZDJmNmo2In0.Fxyr0FGk196DaN6v7Z71Zg'
    
    data = cargar_datos(archivo_json)
    if not data:
        return

    cache = {}

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)

    info_nodos = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(procesar_nodo, element, access_token, session, cache) for element in data['elements'] if element['type'] == 'node']
        for future in as_completed(futures):
            info_nodos.append(future.result())

    guardar_info_nodos(info_nodos, archivo_salida)

if __name__ == "__main__":
    main()

