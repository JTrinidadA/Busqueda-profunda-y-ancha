import pygame
import sys

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)  # Color azul
ROJO = (255, 0, 0)  # Color rojo
AMARILLO = (255, 255, 0)  # Color amarillo

# Coordenadas de inicio y fin
inicio = (0, 0)
fin = (0, 0)


def obtener_dimensiones_laberinto(laberinto):
    ancho_celda = len(laberinto[0])*3
    alto_celda = len(laberinto)*3

    return ancho_celda, alto_celda
def encontrar_inicio_fin(laberinto):
    global inicio, fin
    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            if laberinto[fila][columna] == 2:
                inicio = (columna, fila)
            elif laberinto[fila][columna] == 3:
                fin = (columna, fila)

def dibujar_laberinto(screen, laberinto, ancho_celda, alto_celda):
    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            if laberinto[fila][columna] == 0:
                pygame.draw.rect(screen, NEGRO, (columna * ancho_celda, fila * alto_celda, ancho_celda, alto_celda))
            else:
                pygame.draw.rect(screen, BLANCO, (columna * ancho_celda, fila * alto_celda, ancho_celda, alto_celda))

    # Dibujar la entrada (azul) en la posición de inicio
    pygame.draw.rect(screen, AZUL, (inicio[0] * ancho_celda, inicio[1] * alto_celda, ancho_celda, alto_celda))

    # Dibujar la salida (rojo) en la posición de fin
    pygame.draw.rect(screen, ROJO, (fin[0] * ancho_celda, fin[1] * alto_celda, ancho_celda, alto_celda))

    # Dibujar el punto amarillo en la posición actual
    pygame.draw.rect(screen, AMARILLO, (posicion_x, posicion_y, ancho_celda, alto_celda))
    pygame.display.flip()


def main(laberinto):
    pygame.init()
    global screen, posicion_x, posicion_y, inicio, fin

    # Obtener dimensiones del laberinto y coordenadas de inicio y fin
    ancho_celda, alto_celda= obtener_dimensiones_laberinto(laberinto)
    encontrar_inicio_fin(laberinto)


    # Coordenadas iniciales del punto amarillo (entrada)
    posicion_x = inicio[0] * ancho_celda
    posicion_y = inicio[1] * alto_celda

    # Dimensiones del laberinto (ancho y alto)
    ANCHO = ancho_celda * len(laberinto[0])
    ALTO = alto_celda * len(laberinto)

    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Laberinto")

    reloj = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if posicion_x - ancho_celda >= 0 and laberinto[posicion_y // alto_celda][
                        posicion_x // ancho_celda - 1] in {1, 2, 3}:
                        posicion_x -= ancho_celda
                elif event.key == pygame.K_RIGHT:
                    if posicion_x + ancho_celda < ANCHO and laberinto[posicion_y // alto_celda][
                        posicion_x // ancho_celda + 1] in {1, 2, 3}:
                        posicion_x += ancho_celda
                elif event.key == pygame.K_UP:
                    if posicion_y - alto_celda >= 0 and laberinto[posicion_y // alto_celda - 1][
                        posicion_x // ancho_celda] in {1, 2, 3}:
                        posicion_y -= alto_celda
                elif event.key == pygame.K_DOWN:
                    if posicion_y + alto_celda < ALTO and laberinto[posicion_y // alto_celda + 1][
                        posicion_x // ancho_celda] in {1, 2, 3}:
                        posicion_y += alto_celda

        dibujar_laberinto(screen, laberinto, ancho_celda, alto_celda)
        reloj.tick(60)

        # Verificar si el cuadro amarillo llega al cuadro rojo
        if (posicion_x // ancho_celda, posicion_y // alto_celda) == fin:
            print("¡Laberinto resuelto!")
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    nombre_archivo_laberinto = "laberinto.txt"
    main(nombre_archivo_laberinto)
