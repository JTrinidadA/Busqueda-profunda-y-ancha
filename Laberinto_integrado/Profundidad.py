import pygame
import sys
import subprocess  # Para ejecutar programas externos

# Dimensiones del laberinto (ancho y alto)
ANCHO = 600
ALTO = 600

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)  # Color azul
ROJO = (255, 0, 0)  # Color rojo
AMARILLO = (255, 255, 0)  # Color amarillo

# Laberinto
laberinto = []
entrada = None
salida = None

def cargar_laberinto(nombre_archivo):
    laberinto.clear()
    with open(nombre_archivo, 'r') as file:
        for fila, line in enumerate(file):
            valores = line.split()
            fila_laberinto = []
            for columna, valor in enumerate(valores):
                valor = int(valor)
                fila_laberinto.append(valor)
                if valor == 2:  # Entrada
                    entrada = (columna, fila)
                elif valor == 3:  # Salida
                    salida = (columna, fila)
            laberinto.append(fila_laberinto)
    return entrada, salida

entrada, salida = cargar_laberinto("laberinto.txt")

# Coordenadas iniciales del punto amarillo (entrada)
posicion_x, posicion_y = entrada[0] * 40, entrada[1] * 40

# Función para dibujar el laberinto
def dibujar_laberinto():
    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            if laberinto[fila][columna] == 0:
                pygame.draw.rect(screen, NEGRO, (columna * 40, fila * 40, 40, 40))
            else:
                pygame.draw.rect(screen, BLANCO, (columna * 40, fila * 40, 40, 40))

            if laberinto[fila][columna] == 2:
                pygame.draw.rect(screen, AZUL, (columna * 40, fila * 40, 40, 40))  # Entrada
            elif laberinto[fila][columna] == 3:
                pygame.draw.rect(screen, ROJO, (columna * 40, fila * 40, 40, 40))  # Salida

    # Dibujar el punto amarillo en la posición actual
    pygame.draw.rect(screen, AMARILLO, (posicion_x, posicion_y, 40, 40))
    pygame.display.flip()

pygame.init()
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Laberinto")

reloj = pygame.time.Clock()

# Función para obtener las opciones disponibles
def obtener_opciones_disponibles(posicion_x, posicion_y, movimientos_previos):
    opciones = []
    for dx, dy in [(0, -40), (0, 40), (-40, 0), (40, 0)]:
        nueva_x = posicion_x + dx
        nueva_y = posicion_y + dy

        if (
            0 <= nueva_x < ANCHO
            and 0 <= nueva_y < ALTO
            and laberinto[nueva_y // 40][nueva_x // 40] == 1
            and (nueva_x // 40, nueva_y // 40) not in movimientos_previos
        ):
            opciones.append((dx, dy))

    return opciones

movimientos_previos = []

def cargar_movimientos():
    movimientos = []
    try:
        with open("movimientos.txt", "r") as file:
            lineas = file.readlines()
            for i in range(0, len(lineas), 2):
                pos_actual = eval(lineas[i].split(":")[1].strip())
                opciones = eval(lineas[i+1].split(":")[1].strip())
                movimientos.append((pos_actual, opciones))
    except FileNotFoundError:
        pass
    return movimientos

def guardar_movimiento(x, y, opciones_disponibles, camino_abierto):
    with open("movimientos.txt", "a") as file:
        file.write(f"Posición actual: ({x // 40}, {y // 40})\n")
        file.write(f"Opciones disponibles: {opciones_disponibles}\n")
        file.write(f"Camino abierto: {camino_abierto}\n")

def main():
    entrada, salida = cargar_laberinto("laberinto.txt")

    # Coordenadas iniciales del punto amarillo (entrada)
    posicion_x, posicion_y = entrada[0] * 40, entrada[1] * 40

    pygame.init()
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Laberinto")
    reloj = pygame.time.Clock()

    movimientos_previos = cargar_movimientos()

    modo_libre = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    modo_libre = not modo_libre

        if modo_libre:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and posicion_y > 0:
                posicion_y -= 40
            elif keys[pygame.K_DOWN] and posicion_y < ALTO - 40:
                posicion_y += 40
            elif keys[pygame.K_LEFT] and posicion_x > 0:
                posicion_x -= 40
            elif keys[pygame.K_RIGHT] and posicion_x < ANCHO - 40:
                posicion_x += 40

            dibujar_laberinto()
            reloj.tick(10)
            continue

        opciones_disponibles = obtener_opciones_disponibles(posicion_x, posicion_y, movimientos_previos)

        if opciones_disponibles:
            for dx, dy in opciones_disponibles:
                nueva_x = posicion_x + dx
                nueva_y = posicion_y + dy

                if laberinto[nueva_y // 40][nueva_x // 40] != 0:
                    posicion_x = nueva_x
                    posicion_y = nueva_y
                    break

            guardar_movimiento(posicion_x, posicion_y, opciones_disponibles, True)
            movimientos_previos.append((posicion_x // 40, posicion_y // 40))
        else:
            print("¡Laberinto resuelto o sin solución!")
            subprocess.run(["python", "leer_movimientos.py"])
            pygame.quit()
            sys.exit()

        dibujar_laberinto()
        reloj.tick(1)

        if (posicion_x // 40, posicion_y // 40) == salida:
            print("¡Laberinto resuelto!")
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()