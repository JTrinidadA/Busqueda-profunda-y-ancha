import pygame
import sys
import time

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)  # Color azul
ROJO = (255, 0, 0)  # Color rojo
AMARILLO = (255, 255, 0)  # Color amarillo
VERDE = (0, 255, 0)
BOSQUE = (33, 117, 3)
ARENA = (251, 197, 23)
AGUA = (99, 255, 222)
PIEDRA = (132, 132, 132)
LAND = (225, 169, 48)
# Coordenadas de inicio y fin
inicio = (0, 0)
fin = (0, 0)


def agente(seleccion):
    celdas_disponibles = [1, 2, 3]  # Valor predeterminado

    if seleccion == 1:
        #nombre = "Human"
        celdas_disponibles = [1, 2, 3, 4, 5, 6]
        
    elif seleccion == 2:
        #nombre = "Monkey"
        celdas_disponibles = [1, 2, 3, 4, 5, 6]
        
    elif seleccion == 3:
        #nombre = "Octopus"
        celdas_disponibles = [1, 2, 3, 6]
        
    elif seleccion == 4:
        #nombre = "Sasquatch"
        celdas_disponibles = [1, 2, 3, 4, 7]
        
        
    return celdas_disponibles
    



def encontrar_inicio_fin(laberinto):
    global inicio, fin
    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            if laberinto[fila][columna] == 2:
                inicio = (columna, fila)
            elif laberinto[fila][columna] == 3:
                fin = (columna, fila)


def dibujar_laberinto(screen, laberinto, ancho_celda, alto_celda, laberinto_copia):
    screen.fill(BLANCO)  # Llenar la pantalla con el color blanco

    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            if laberinto[fila][columna] == 1:
                pygame.draw.rect(screen, LAND, (columna * ancho_celda, fila * alto_celda, ancho_celda, alto_celda))
            if laberinto[fila][columna] == 0:
                pygame.draw.rect(screen, NEGRO, (columna * ancho_celda, fila * alto_celda, ancho_celda, alto_celda))
            elif laberinto[fila][columna] == 4:
                pygame.draw.rect(screen, BOSQUE, (columna * ancho_celda, fila * alto_celda, ancho_celda, alto_celda))
            elif laberinto[fila][columna] == 5:
                pygame.draw.rect(screen, ARENA, (columna * ancho_celda, fila * alto_celda, ancho_celda, alto_celda))
            elif laberinto[fila][columna] == 6:
                pygame.draw.rect(screen, AGUA, (columna * ancho_celda, fila * alto_celda, ancho_celda, alto_celda))
            elif laberinto[fila][columna] == 7:
                pygame.draw.rect(screen, PIEDRA, (columna * ancho_celda, fila * alto_celda, ancho_celda, alto_celda))
            elif laberinto[fila][columna] == "v":
                pygame.draw.circle(screen, VERDE, (columna * ancho_celda + ancho_celda // 2, fila * alto_celda + alto_celda // 2), min(ancho_celda, alto_celda) // 2)
          
        ''' elif laberinto_copia[fila][columna] > 1:
                # Marcar con 'o' en casillas con más de un camino
                pygame.draw.circle(screen, NEGRO, (columna * ancho_celda + ancho_celda // 2, fila * alto_celda + alto_celda // 2), min(ancho_celda, alto_celda) // 4)
                pygame.draw.circle(screen, BLANCO, (columna * ancho_celda + ancho_celda // 2, fila * alto_celda + alto_celda // 2), min(ancho_celda, alto_celda) // 2)
'''
    pygame.draw.rect(screen, AZUL, (inicio[0] * ancho_celda, inicio[1] * alto_celda, ancho_celda, alto_celda))

    # Dibujar la salida (rojo) en la posición de fin
    pygame.draw.rect(screen, ROJO, (fin[0] * ancho_celda, fin[1] * alto_celda, ancho_celda, alto_celda))

    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            if laberinto_copia[fila][columna] == 0:
                pygame.draw.rect(screen, NEGRO, (columna * ancho_celda, fila * alto_celda, ancho_celda, alto_celda))

    pygame.draw.rect(screen, AMARILLO, (posicion_x, posicion_y, ancho_celda, alto_celda))

    pygame.display.flip()


def marcar_celdas_vecinas(laberinto_copia, fila, columna):
    # Incrementar el valor de la celda actual
    laberinto_copia[fila][columna] += 1

    # Marcar las celdas vecinas en todas las direcciones, con un alcance de dos celdas
    for i in range(-2, 3):
        for j in range(-2, 3):
            if 0 <= fila + i < len(laberinto_copia) and 0 <= columna + j < len(laberinto_copia[0]):
                laberinto_copia[fila + i][columna + j] += 1



def marcar_laberinto_completo(laberinto_copia):
    # Marcar_todo el laberinto copia con 1
    for fila in range(len(laberinto_copia)):
        for columna in range(len(laberinto_copia[0])):
            laberinto_copia[fila][columna] = 1

def marcar_celda_con_v(laberinto, fila, columna):
    laberinto[fila][columna] = 'v'

def main(laberinto):

    pygame.init()
    global screen, posicion_x, posicion_y, inicio, fin

    print("Humano    1")
    print("Mono      2")
    print("Pulpo     3")
    print("Sasquatch 4")
    celdas = agente(input("seleccione un agente: "))
    # Establecer tamaño fijo para las celdas
    ancho_celda, alto_celda = 40, 40

    encontrar_inicio_fin(laberinto)

    # Coordenadas iniciales del punto amarillo (entrada)
    posicion_x = inicio[0] * ancho_celda
    posicion_y = inicio[1] * alto_celda

    # Dimensiones del laberinto (ancho y alto)
    ANCHO = ancho_celda * len(laberinto[0])
    ALTO = alto_celda * len(laberinto)

    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Laberinto")

    laberinto_copia = [[0] * len(laberinto[0]) for _ in range(len(laberinto))]

    reloj = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if posicion_x - ancho_celda >= 0 and laberinto[posicion_y // alto_celda][
                        posicion_x // ancho_celda - 1] in celdas:
                        # Actualizar laberinto_copia después del movimiento a la izquierda
                        marcar_celdas_vecinas(laberinto_copia, posicion_y // alto_celda, posicion_x // ancho_celda)
                        posicion_x -= ancho_celda
                elif event.key == pygame.K_RIGHT:
                    if posicion_x + ancho_celda < ANCHO and laberinto[posicion_y // alto_celda][
                        posicion_x // ancho_celda + 1] in celdas:
                        # Actualizar laberinto_copia después del movimiento a la derecha
                        marcar_celdas_vecinas(laberinto_copia, posicion_y // alto_celda, posicion_x // ancho_celda)
                        posicion_x += ancho_celda
                elif event.key == pygame.K_UP:
                    if posicion_y - alto_celda >= 0 and laberinto[posicion_y // alto_celda - 1][
                        posicion_x // ancho_celda] in celdas:
                        # Actualizar laberinto_copia después del movimiento hacia arriba
                        marcar_celdas_vecinas(laberinto_copia, posicion_y // alto_celda - 1, posicion_x // ancho_celda)
                        posicion_y -= alto_celda
                elif event.key == pygame.K_DOWN:
                    if posicion_y + alto_celda < ALTO and laberinto[posicion_y // alto_celda + 1][
                        posicion_x // ancho_celda] in celdas:
                        # Actualizar laberinto_copia después del movimiento hacia abajo
                        marcar_celdas_vecinas(laberinto_copia, posicion_y // alto_celda + 1, posicion_x // ancho_celda)
                        posicion_y += alto_celda

        dibujar_laberinto(screen, laberinto, ancho_celda, alto_celda, laberinto_copia)

         # Marcar la celda con 'v' cada vez que el cuadro amarillo se mueva
        fila_actual = posicion_y // alto_celda
        columna_actual = posicion_x // ancho_celda
        marcar_celda_con_v(laberinto, fila_actual, columna_actual)

        pygame.display.flip()
        reloj.tick(60)

        # Verificar si el cuadro amarillo llega al cuadro rojo
        if (posicion_x // ancho_celda, posicion_y // alto_celda) == fin:
            print("¡Laberinto resuelto!")
            # Marcar_todo el laberinto copia con 1
            marcar_laberinto_completo(laberinto_copia)
            dibujar_laberinto(screen, laberinto, ancho_celda, alto_celda, laberinto_copia)
            pygame.display.flip()
            time.sleep(1)  # Retraso de un segundo
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    nombre_archivo_laberinto = "laberinto.txt"
    with open(nombre_archivo_laberinto, 'r') as file:
        laberinto = [list(map(int, line.strip())) for line in file]
    main(laberinto)

