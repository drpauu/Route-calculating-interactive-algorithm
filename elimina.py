def remove_duplicates_and_write_back(file_path):
    unique_edges = set()

    # Leer el archivo y almacenar aristas únicas
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line == "END OF INPUT" or not line:
                continue  # Ignorar líneas vacías o la línea de fin
            
            parts = line.split()
            if len(parts) < 3:
                print(f"Ignorando línea mal formada: {line}")
                continue  # Ignorar líneas que no tienen el formato correcto
            
            # Ordenar las ciudades alfabéticamente y formar una tupla con las ciudades y la distancia
            city1, city2, distance = sorted(parts[:-1]) + [parts[-1]]
            unique_edges.add((city1, city2, distance))
    
    # Sobrescribir el archivo con las aristas únicas
    with open(file_path, 'w') as file:
        for edge in sorted(unique_edges):
            file.write(f"{edge[0]} {edge[1]} {edge[2]}\n")
        # Es opcional añadir "END OF INPUT" al final del archivo, dependiendo de si tu aplicación lo necesita

file_path = '/home/user/GitHub/Routes-algorithm/inputs/espanya.txt'  # Asegúrate de que la ruta del archivo sea la correcta

# Llamar a la función para eliminar duplicados y modificar el archivo
remove_duplicates_and_write_back(file_path)

print("Las aristas repetidas han sido eliminadas del archivo.")
