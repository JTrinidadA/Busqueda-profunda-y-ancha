import pygame
import sys
from collections import deque

# Dimensiones del laberinto (ancho y alto)
ANCHO = 600
ALTO = 600

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)  # Color azul
ROJO = (255, 0, 0)  # Color rojo
AMARILLO = (255, 255, 0)  # Color amarillo

laberinto = None
# Coordenadas iniciales y finales para BFS
inicio = (0, 0)
fin = (0, 0)

# Coordenadas iniciales del punto amarillo (entrada)
posicion_x, posicion_y = inicio[1] * 40, inicio[0] * 40

def cargar_laberinto_desde_archivo(nombre_archivo):
    laberinto = []
    with open(nombre_archivo, 'r') as file:
        for line in file:
            row = [int(cell) for cell in line.split()]
            laberinto.append(row)
    return laberinto

def encontrar_coordenadas(laberinto):
    for i, fila in enumerate(laberinto):
        for j, valor in enumerate(fila):
            if valor == 2:  # Inicio
                global inicio
                inicio = (i, j)
            elif valor == 3:  # Fin
                global fin
                fin = (i, j)

def dibujar_laberinto(screen):
    screen.fill(BLANCO)  # Llenar la pantalla con el color blanco

    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            if laberinto[fila][columna] == 0:
                pygame.draw.rect(screen, NEGRO, (columna * 40, fila * 40, 40, 40))
            else:
                pygame.draw.rect(screen, BLANCO, (columna * 40, fila * 40, 40, 40))

    # Dibujar la entrada (azul)
    pygame.draw.rect(screen, AZUL, (inicio[1] * 40, inicio[0] * 40, 40, 40))

    # Dibujar la salida (rojo)
    pygame.draw.rect(screen, ROJO, (fin[1] * 40, fin[0] * 40, 40, 40))

    # Dibujar el punto amarillo en la posición actual
    pygame.draw.rect(screen, AMARILLO, (posicion_x, posicion_y, 40, 40))

    pygame.display.flip()
def obtener_camino_corto(parent, inicio, fin):
    current = fin
    path = []
    while current != inicio:
        path.insert(0, current)
        current = parent[current]
    path.insert(0, inicio)
    return path

def bfs_laberinto(screen):
    global posicion_x, posicion_y
    visited = set()
    queue = deque([inicio])
    parent = {}

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = queue.popleft()
        if current == fin:
            # Imprimir y repetir el camino más corto
            path = obtener_camino(parent, inicio, fin)
            for paso in path:
                posicion_x, posicion_y = paso[1] * 40, paso[0] * 40
                dibujar_laberinto(screen)
                pygame.time.delay(500)  # Pausa para visualizar el movimiento

            # Imprimir el árbol después de haber encontrado la meta
            imprimir_arbol(parent, inicio, fin)

            # Imprimir el camino más corto en la terminal
            camino_corto = obtener_camino_corto(parent, inicio, fin)
            print("Camino más corto:", camino_corto)

            return True  # Llegó a la meta

        for neighbor in obtener_vecinos(current, laberinto):
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

                # Mover automáticamente el punto amarillo al mismo tiempo que se descubre el camino
                posicion_x, posicion_y = neighbor[1] * 40, neighbor[0] * 40
                dibujar_laberinto(screen)
                pygame.time.delay(500)  # Pausa para visualizar el movimiento

    # Imprimir el árbol y el camino más corto si no se alcanzó la meta
    imprimir_arbol(parent, inicio, fin)
    camino_corto = obtener_camino_corto(parent, inicio, fin)
    print("Camino más corto:", camino_corto)
    return False  # No llegó a la meta
def obtener_camino(parent, inicio, fin):
    current = fin
    path = []
    while current != inicio:
        path.insert(0, current)
        current = parent[current]
    path.insert(0, inicio)
    return path

def obtener_vecinos(posicion, laberinto):
    x, y = posicion
    vecinos = []

    # Verificar arriba, abajo, izquierda y derecha, excluyendo 0 (paredes)
    movimientos = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    for dx, dy in movimientos:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(laberinto) and 0 <= ny < len(laberinto[0]) and laberinto[nx][ny] != 0:
            vecinos.append((nx, ny))

    return vecinos


def imprimir_arbol(parent, inicio, fin):
    current = fin
    path = []
    while current != inicio:
        path.insert(0, current)
        current = parent[current]
    path.insert(0, inicio)

    print("\nÁrbol de pasos del algoritmo BFS:")
    for paso in path:
        print(f"Nodo: {paso}, Padre: {parent[paso]}")
    print("Fin del árbol de pasos del algoritmo BFS.")

# Resto del código...

def main():
    global laberinto, parent  # Agrega 'parent' aquí
    pygame.init()
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Laberinto")

    reloj = pygame.time.Clock()

    # Encuentra el camino utilizando BFS
    laberinto = cargar_laberinto_desde_archivo("laberinto.txt")
    encontrar_coordenadas(laberinto)
    llego_a_la_meta = bfs_laberinto(screen)

    # Bucle principal del juego
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Dibujar el laberinto y el punto amarillo en la nueva posición
        dibujar_laberinto(screen)

        pygame.time.delay(100)  # Pausa para controlar la velocidad del movimiento

        if llego_a_la_meta:
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
