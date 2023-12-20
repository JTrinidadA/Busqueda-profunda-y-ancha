import networkx as nx
import matplotlib.pyplot as plt
import re

def traducir_opciones(coordenada, opciones):
    traducidas = []
    for dx, dy in opciones:
        nueva_x = coordenada[0] + dx
        nueva_y = coordenada[1] + dy
        traducidas.append((nueva_x, nueva_y))
    return traducidas

def leer_movimientos(nombre_archivo):
    movimientos = []
    with open(nombre_archivo, "r") as file:
        lineas = file.readlines()
        for i in range(0, len(lineas), 3):
            match = re.search(r"\((\d+), (\d+)\)", lineas[i])
            if match:
                coordenada = tuple(map(int, match.groups()))
            else:
                continue

            camino_abierto = "True" in lineas[i + 2]

            opciones_disponibles = []
            opciones_match = re.search(r"\[((-?\d+), (-?\d+))(, (-?\d+), (-?\d+))*\]", lineas[i + 1])
            if opciones_match:
                opciones = opciones_match.groups()[1:]
                opciones = list(map(int, filter(None, opciones)))
                opciones_disponibles = [(opciones[i], opciones[i + 1]) for i in range(0, len(opciones), 2)]
                opciones_disponibles = traducir_opciones(coordenada, opciones_disponibles)

            movimientos.append((coordenada, opciones_disponibles, camino_abierto))

    return movimientos

def dibujar_grafo(grafo):
    posiciones = {nodo: (nodo[0], -nodo[1]) for nodo in grafo.nodes()}
    etiquetas = {(nodo1, nodo2): f'{grafo[nodo1][nodo2]["weight"]:.2f}' for nodo1, nodo2 in grafo.edges()}

    nx.draw(grafo, pos=posiciones, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue')
    nx.draw_networkx_edge_labels(grafo, pos=posiciones, edge_labels=etiquetas)
    plt.show()

def crear_grafo(movimientos):
    grafo = nx.DiGraph()
    for i in range(len(movimientos) - 1):
        nodo_actual = movimientos[i][0]
        opciones = movimientos[i][1]

        for opcion in opciones:
            grafo.add_edge(nodo_actual, opcion)

        if not grafo.has_node(movimientos[i + 1][0]):
            if not opciones:
                print(f"Warning: No hay opciones disponibles para el nodo {nodo_actual}.")
                continue

            nodo_siguiente = min(opciones, key=lambda x: ((x[0] - movimientos[i + 1][0][0])**2 + (x[1] - movimientos[i + 1][0][1])**2)**0.5)
            grafo.add_edge(nodo_siguiente, movimientos[i + 1][0])

    return grafo

# Uso del método
movimientos = leer_movimientos("movimientos.txt")
grafo = crear_grafo(movimientos)
dibujar_grafo(grafo)


def crear_grafo(movimientos):
    grafo = nx.DiGraph()
    for i in range(len(movimientos) - 1):
        nodo_actual = movimientos[i][0]
        opciones_relativas = movimientos[i][1]

        # Traducir opciones a coordenadas absolutas
        opciones_absolutas = traducir_opciones(nodo_actual, opciones_relativas)

        for opcion in opciones_absolutas:
            grafo.add_edge(nodo_actual, opcion)

        if not grafo.has_node(movimientos[i + 1][0]):
            if not opciones_absolutas:
                print(f"Warning: No hay opciones disponibles para el nodo {nodo_actual}.")
                continue

            nodo_siguiente = min(opciones_absolutas, key=lambda x: ((x[0] - movimientos[i + 1][0][0])**2 + (x[1] - movimientos[i + 1][0][1])**2)**0.5)
            grafo.add_edge(nodo_siguiente, movimientos[i + 1][0])

    return grafo


# Uso del método
movimientos = leer_movimientos("movimientos.txt")
grafo = crear_grafo(movimientos)
dibujar_grafo(grafo)

def traducir_opciones(coordenada, opciones):
    traducidas = []
    for dx, dy in opciones:
        nueva_x = coordenada[0] + dx
        nueva_y = coordenada[1] + dy
        traducidas.append((nueva_x, nueva_y))
    return traducidas

def dibujar_arbol(movimientos):
    fig, ax = plt.subplots()
    ax.set_aspect('equal', 'box')
    ax.axis('off')

    # Dibujar las flechas según los movimientos
    for movimiento in movimientos:
        coordenada, opciones, _ = movimiento
        for opcion in opciones:
            arrow = FancyArrowPatch(
                (coordenada[0], coordenada[1]),
                (opcion[0], opcion[1]),
                mutation_scale=15,
                color='gray',
                arrowstyle='-|>',
                linestyle='dashed',
            )
            ax.add_patch(arrow)

    # Marcar las posiciones iniciales y finales
    for movimiento in movimientos:
        coordenada, _, _ = movimiento
        plt.scatter(coordenada[0], coordenada[1], color='green', s=50, zorder=5)
    plt.scatter(movimientos[-1][0][0], movimientos[-1][0][1], color='red', s=50, zorder=5)

    plt.show()

def leer_movimientos(nombre_archivo):
    movimientos = []
    with open(nombre_archivo, "r") as file:
        lineas = file.readlines()
        for i in range(0, len(lineas), 3):  # Avanzamos de tres en tres líneas
            # Buscamos la coordenada entre paréntesis
            match = re.search(r"\((\d+), (\d+)\)", lineas[i])
            if match:
                coordenada = tuple(map(int, match.groups()))
            else:
                continue  # O sal del bucle si no se encuentra una coincidencia

            # Ignoramos lo que está entre corchetes y obtenemos el valor de "Camino abierto"
            camino_abierto = "True" in lineas[i + 2]

            # Traducir opciones disponibles a las coordenadas a las que se movería
            opciones_disponibles = []
            opciones_match = re.search(r"\[((-?\d+), (-?\d+))(, (-?\d+), (-?\d+))*\]", lineas[i + 1])
            if opciones_match:
                opciones = opciones_match.groups()[1:]
                opciones = list(map(int, filter(None, opciones)))
                opciones_disponibles = [(opciones[i], opciones[i + 1]) for i in range(0, len(opciones), 2)]
                opciones_disponibles = traducir_opciones(coordenada, opciones_disponibles)

            movimientos.append((coordenada, opciones_disponibles, camino_abierto))

    return movimientos

# Uso del método
#movimientos = leer_movimientos("movimientos.txt")
#dibujar_arbol(movimientos)

def distancia_entre_puntos(punto1, punto2):
    return ((punto1[0] - punto2[0])**2 + (punto1[1] - punto2[1])**2)**0.5

def agregar_arista(graph, nodo1, nodo2):
    distancia = distancia_entre_puntos(nodo1, nodo2)
    graph.add_edge(nodo1, nodo2, weight=distancia)

def crear_grafo(movimientos):
    grafo = nx.DiGraph()
    nodos_por_coordenada = {}  # Diccionario para almacenar nodos por coordenada

    for coordenada, opciones_relativas, _ in movimientos:
        # Traducir opciones a coordenadas absolutas
        opciones_absolutas = traducir_opciones(coordenada, opciones_relativas)

        # Si el nodo actual no existe en el grafo, añadirlo
        if coordenada not in nodos_por_coordenada:
            grafo.add_node(coordenada)
            nodos_por_coordenada[coordenada] = grafo.nodes[coordenada]

        # Añadir conexiones al grafo
        for opcion in opciones_absolutas:
            # Si el nodo de la opción no existe en el grafo, añadirlo
            if opcion not in nodos_por_coordenada:
                grafo.add_node(opcion)
                nodos_por_coordenada[opcion] = grafo.nodes[opcion]

            # Añadir arista desde el nodo actual al nodo de la opción
            grafo.add_edge(coordenada, opcion)

    return grafo



def dibujar_grafo(grafo):
    posiciones = {nodo: (nodo[0], -nodo[1]) for nodo in grafo.nodes()}
    etiquetas = {(nodo1, nodo2): f'{grafo[nodo1][nodo2]["weight"]:.2f}' for nodo1, nodo2 in grafo.edges()}

    nx.draw(grafo, pos=posiciones, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue')
    nx.draw_networkx_edge_labels(grafo, pos=posiciones, edge_labels=etiquetas)
    plt.show()

# Uso del método
movimientos = leer_movimientos("movimientos.txt")
grafo = crear_grafo(movimientos)
dibujar_grafo(grafo)



import re
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

def traducir_opciones(coordenada, opciones):
    traducidas = []
    for dx, dy in opciones:
        nueva_x = coordenada[0] + dx
        nueva_y = coordenada[1] + dy
        traducidas.append((nueva_x, nueva_y))
    return traducidas

def dibujar_arbol(movimientos):
    fig, ax = plt.subplots()
    ax.set_aspect('equal', 'box')
    ax.axis('off')

    # Dibujar las flechas según los movimientos
    for movimiento in movimientos:
        coordenada, opciones, _ = movimiento
        for opcion in opciones:
            arrow = FancyArrowPatch(
                (coordenada[0], coordenada[1]),
                (opcion[0], opcion[1]),
                mutation_scale=15,
                color='gray',
                arrowstyle='-|>',
                linestyle='dashed',
            )
            ax.add_patch(arrow)

    # Marcar las posiciones iniciales y finales
    for movimiento in movimientos:
        coordenada, _, _ = movimiento
        plt.scatter(coordenada[0], coordenada[1], color='green', s=50, zorder=5)
    plt.scatter(movimientos[-1][0][0], movimientos[-1][0][1], color='red', s=50, zorder=5)

    plt.show()

def dibujar_arbol_terminal(movimientos):
    for movimiento in movimientos:
        coordenada, opciones, _ = movimiento
        print(f"Coordenada: {coordenada}, Opciones: {opciones}")

# Uso del método
movimientos = leer_movimientos("movimientos.txt")
dibujar_arbol_terminal(movimientos)


# Uso del método
movimientos = leer_movimientos("movimientos.txt")
dibujar_arbol(movimientos)

