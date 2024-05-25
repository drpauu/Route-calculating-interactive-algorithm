import json
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

def load_routes_from_file(filename='fictitious_routes.json'):
    with open(filename, 'r') as file:
        routes = json.load(file)
    return routes

def display_routes_table(routes):
    df = pd.DataFrame(routes)
    print(df)
    return df

def visualize_routes(routes):
    G = nx.Graph()
    
    for route in routes:
        origin = route['origin']
        destination = route['destination']
        distance = route['distance']
        time = route['time']
        
        G.add_edge(origin, destination, distance=distance, time=time)
    
    pos = nx.spring_layout(G)
    edge_labels = {(u, v): f"{d['distance']} km, {d['time']} min" for u, v, d in G.edges(data=True)}
    
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    
    plt.title("Visualització de Rutes Fictícies")
    plt.show()

def main():
    routes = load_routes_from_file()
    
    # Mostrar les rutes en format tabular
    display_routes_table(routes)
    
    # Visualitzar les rutes en un graf
    visualize_routes(routes)

if __name__ == "__main__":
    main()
