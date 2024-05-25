import random
import json
import keyboard  # Assegura't de tenir instal·lada la llibreria 'keyboard'

def generate_fictitious_route():
    origin = f'Node{random.randint(1, 100)}'
    destination = f'Node{random.randint(1, 100)}'
    distance = round(random.uniform(1, 100), 2)
    time = round(random.uniform(1, 120), 2)
    route = {
        'origin': origin,
        'destination': destination,
        'distance': distance,
        'time': time
    }
    return route

def save_routes_to_file(routes, filename='fictitious_routes.json'):
    with open(filename, 'w') as file:
        json.dump(routes, file, indent=4)

if __name__ == "__main__":
    routes = []
    print("Generant rutes fictícies... Prem qualsevol tecla per parar.")
    try:
        while True:
            route = generate_fictitious_route()
            routes.append(route)
            print(f"Afegida ruta: {route}")
            if keyboard.is_pressed('q'):  # L'usuari pot prémer la tecla 'q' per sortir del bucle
                print("S'ha pressionat la tecla per parar. Sortint...")
                break
    except KeyboardInterrupt:
        print("Interrupció de l'usuari. Sortint...")
    finally:
        save_routes_to_file(routes)
        print(f"Rutes guardades en 'fictitious_routes.json'")
