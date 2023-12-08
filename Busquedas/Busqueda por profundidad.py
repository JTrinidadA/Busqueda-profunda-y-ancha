import pygame
import sys
import time

# Dimensiones del laberinto (ancho y alto)
ANCHO = 600
ALTO = 600

# Colores
VERDE = (0, 255, 0)  # Color verd
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)  # Color azul
ROJO = (255, 0, 0)  # Color rojo
AMARILLO = (255, 255, 0)  # Color amarillo
rastro_puntos = set()
ejecutar_algoritmo = True

# Laberinto
laberinto = [
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,1,1,1,1,0,1,1,1,1,1,1,1,1,1],
    [0,1,0,1,0,0,1,0,1,0,0,0,0,0,0],
    [0,0,1,1,1,1,1,0,1,0,0,0,0,0,0],
    [0,0,0,1,0,1,0,0,1,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,0,1,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,0,1,0,0,0,0,0,0],
    [0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,0,1,1,1,1,1,1,0,0,0,0,0,0],
    [1,1,0,1,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,1,0,0,0,0,0,0,0]
]
def dibujar_boton():
    pygame.draw.rect(screen, VERDE, (500, 10, 90, 30))
    fuente = pygame.font.Font(None, 36)
    texto = fuente.render("Modo Libre", True, NEGRO)
    screen.blit(texto, (500 + 5, 10 + 5))
def dibujar_laberinto():
    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            if laberinto[fila][columna] == 0:
                pygame.draw.rect(screen, NEGRO, (columna * 40, fila * 40, 40, 40))
            else:
                pygame.draw.rect(screen, BLANCO, (columna * 40, fila * 40, 40, 40))

    # Dibujar la entrada (azul) en [14][3]
    pygame.draw.rect(screen, AZUL, (3 * 40, 14 * 40, 40, 40))

    # Dibujar la salida (rojo) en [14][1]
    pygame.draw.rect(screen, ROJO, (14 * 40, 1 * 40, 40, 40))

    # Dibujar el punto amarillo en la posición actual
    pygame.draw.rect(screen, AMARILLO, (posicion_x, posicion_y, 40, 40))
    pygame.display.flip()

def guardar_movimiento(x, y):
    with open("movimientos.txt", "a") as file:
        file.write(f"{x},{y}\n")

def cargar_movimientos():
    movimientos = set()
    try:
        with open("movimientos.txt", "r") as file:
            for line in file:
                # Manejar la excepción si la línea está vacía
                try:
                    x, y = map(int, line.strip().split(","))
                    movimientos.add((x, y))
                except ValueError:
                    pass  # Ignorar líneas no válidas

    except FileNotFoundError:
        pass  # Si el archivo no existe, simplemente continuamos sin movimientos previos
    return movimientos

# Coordenadas iniciales del punto amarillo (entrada)
posicion_x = 3 * 40
posicion_y = 14 * 40

# Rastro de los puntos anteriores donde había opciones disponibles
rastro_puntos = set()

# Función para retroceder al último punto de decisión
def teletransportar_ultimo_camino_abierto():
    global posicion_x, posicion_y

    # Encontrar el último punto de decisión con "Camino abierto"
    ultimo_punto_decision = None
    while rastro_puntos:
        punto = rastro_puntos.pop()
        if f"{punto[0]},{punto[1]}\n" in movimientos_previos:
            # Encontramos el último punto de decisión con "Camino abierto"
            ultimo_punto_decision = punto
            break

    if ultimo_punto_decision is not None:
        # Teletransportar al último punto de decisión
        posicion_x, posicion_y = ultimo_punto_decision

        # Eliminar la opción que tomó para llegar aquí
        movimientos_previos.discard(f"{posicion_x},{posicion_y}\n")

        return True
    else:
        return False

def retroceder_al_ultimo_punto_de_decision():
    global posicion_x, posicion_y

    # Encontrar el último punto de decisión con "Camino abierto"
    ultimo_punto_decision = None
    while rastro_puntos:
        punto = rastro_puntos.pop()
        if f"{punto[0]},{punto[1]}\n" in movimientos_previos:
            # Encontramos el último punto de decisión con "Camino abierto"
            ultimo_punto_decision = punto
            break

    if ultimo_punto_decision is not None:
        # Retroceder al último punto de decisión
        posicion_x, posicion_y = ultimo_punto_decision
        return True
    else:
        return False

pygame.init()
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Laberinto")

reloj = pygame.time.Clock()

# Coordenadas iniciales del punto amarillo (entrada)
posicion_x = 3 * 40
posicion_y = 14 * 40

# Motor de prioridades
prioridades = [(0, -40), (0, 40), (-40, 0), (40, 0)]

# Función para obtener las opciones disponibles
def obtener_opciones_disponibles(posicion_x, posicion_y):
    opciones = []
    for dx, dy in prioridades:
        nueva_x = posicion_x + dx
        nueva_y = posicion_y + dy

        if (
            0 <= nueva_x < ANCHO
            and 0 <= nueva_y < ALTO
            and laberinto[nueva_y // 40][nueva_x // 40] == 1
            and (nueva_x, nueva_y) not in movimientos_previos
        ):
            opciones.append((dx, dy))

    return opciones

# Cargar movimientos previos
movimientos_previos = cargar_movimientos()

# Resto del código...

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                ejecutar_algoritmo = not ejecutar_algoritmo

                if ejecutar_algoritmo:
                    # Cargar movimientos previos al activar el algoritmo
                    movimientos_previos = cargar_movimientos()
            elif event.key == pygame.K_ESCAPE:
                ejecutar_algoritmo = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 500 <= x <= 590 and 10 <= y <= 40:
                ejecutar_algoritmo = not ejecutar_algoritmo
                if ejecutar_algoritmo:
                    # Cargar movimientos previos al activar el algoritmo
                    movimientos_previos = cargar_movimientos()
                    # Cargar movimientos previos al activar el algoritmo
                    movimientos_previos = cargar_movimientos()
        elif ejecutar_algoritmo and event.type == pygame.KEYDOWN:
            # Permitir al usuario salir del algoritmo presionando una tecla
            if event.key == pygame.K_ESCAPE:
                ejecutar_algoritmo = False

    # Permite al usuario mover el punto amarillo con las flechas del teclado
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and posicion_x - 40 >= 0 and laberinto[posicion_y // 40][posicion_x // 40 - 1] == 1:
        posicion_x -= 40
    elif keys[pygame.K_RIGHT] and posicion_x + 40 < ANCHO and laberinto[posicion_y // 40][posicion_x // 40 + 1] == 1:
        posicion_x += 40
    elif keys[pygame.K_UP] and posicion_y - 40 >= 0 and laberinto[posicion_y // 40 - 1][posicion_x // 40] == 1:
        posicion_y -= 40
    elif keys[pygame.K_DOWN] and posicion_y + 40 < ALTO and laberinto[posicion_y // 40 + 1][posicion_x // 40] == 1:
        posicion_y += 40

    if ejecutar_algoritmo:
        # Cargar movimientos previos al principio del bucle
        movimientos_previos = cargar_movimientos()

        opciones_disponibles = obtener_opciones_disponibles(posicion_x, posicion_y)

        with open("movimientos.txt", "a") as file:
            if opciones_disponibles:
                file.write(f"Opciones disponibles: {opciones_disponibles}\n")
                if len(opciones_disponibles) > 1:
                    file.write("Camino abierto\n")
                    rastro_puntos.add((posicion_x, posicion_y))  # Guardar el punto actual como punto de decisión
                else:
                    file.write("Camino cerrado\n")

        # Intentar mover en la dirección prioritaria, omitiendo las posiciones anteriores
        if opciones_disponibles:
            for dx, dy in opciones_disponibles:
                nueva_x = posicion_x + dx
                nueva_y = posicion_y + dy

                if (nueva_x, nueva_y) not in movimientos_previos:
                    guardar_movimiento(nueva_x, nueva_y)
                    posicion_x = nueva_x
                    posicion_y = nueva_y
                    break
            else:
                # Si no se puede avanzar, retroceder al último punto de decisión no visitado
                if rastro_puntos:
                    ultimo_punto_decision = next(iter(rastro_puntos))
                    rastro_puntos.remove(ultimo_punto_decision)
                    posicion_x, posicion_y = ultimo_punto_decision
                else:
                    # No hay más puntos de decisión, el laberinto está resuelto o no tiene solución
                    print("¡Laberinto resuelto o sin solución!")
                    pygame.quit()
                    sys.exit()

    dibujar_laberinto()
    dibujar_boton()
    pygame.display.flip()

    reloj.tick(1)

    if not ejecutar_algoritmo:
        # Verificar si el cuadro amarillo llega al cuadro rojo
        if (posicion_x // 40, posicion_y // 40) == (14, 1):
            print("¡Laberinto resuelto!")
            pygame.quit()
            sys.exit()