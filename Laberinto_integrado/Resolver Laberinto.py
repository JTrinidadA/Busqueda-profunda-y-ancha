import pygame
from tkinter import Tk, filedialog
import os
import Anchura
import manual
import Profundidad

# Dimensiones del laberinto (ancho y alto)
ANCHO = 600
ALTO = 600

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)  # Color azul
ROJO = (255, 0, 0)  # Color rojo
AMARILLO = (255, 255, 0)  # Color amarillo
VERDE = (0, 255, 0)

laberinto = None
# Coordenadas iniciales y finales para BFS
inicio = (0, 0)
fin = (0, 0)


# Inicializar Pygame
pygame.init()

# Inicializar pantalla
WINDOW_SIZE = (1000, 750)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Resolver laberinto")


# Definir colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Definir fuentes
font = pygame.font.Font(None, 36)

# Definir rectángulos para los botones
depth_button_rect = pygame.Rect(250, 300, 200, 50)
breadth_button_rect = pygame.Rect(250, 400, 200, 50)
manual_button_rect = pygame.Rect(250, 500, 200, 50)
button_color = GRAY

# Tkinter inicialización (para el diálogo de archivos)
root = Tk()
root.withdraw()  # Ocultar la ventana principal de Tkinter

# Estado inicial
state = 0
selected_file = ""

upload_button_rect = pygame.Rect(250, 300, 200, 50)
next_button_rect = pygame.Rect(250, 400, 200, 50)
button_color = GRAY

def state0():
    global state, selected_file
    screen.fill(BLACK)

    # Renderizar texto
    text1 = font.render("Ingrese el archivo del laberinto", True, (0, 0, 255))  # Color azul
    text2 = font.render("y el método que desea utilizar para resolverlo", True, (0, 0, 255))  # Color azul
    text1_rect = text1.get_rect(center=(WINDOW_SIZE[0] // 2, 50))
    screen.blit(text1, text1_rect)

    # Renderizar texto
    text = font.render("Estado 0: Subir archivo desde /laberintos", True, WHITE)
    screen.blit(text, (250, 250))

    # Dibujar botón de subir archivo
    pygame.draw.rect(screen, button_color, upload_button_rect)
    upload_button_text = font.render("Subir Archivo", True, BLACK)
    text_rect = upload_button_text.get_rect(center=upload_button_rect.center)
    screen.blit(upload_button_text, text_rect)


def state1():
    global state
    screen.fill(BLACK)
    # Dibujar botón de subir archivo con dimensiones 0,0,0,0 en la posición (0,0)
    pygame.draw.rect(screen, BLACK, pygame.Rect(0, 0, 0, 0))  # Hacer el rectángulo invisible
    continue_button_rect = pygame.Rect(0, 0, 0, 0)

    # Hacer el texto invisible
    dummy_text = font.render("", True, BLACK)
    screen.blit(dummy_text, (0, 0))  # Renderizar el texto en una posición fuera de la pantalla
    # Dibujar botón de subir archivo con dimensiones 0,0,0,0 en la posición (0,0)
    pygame.draw.rect(screen, button_color, pygame.Rect(0, 0, 0, 0))

    # Renderizar texto
    text1 = font.render("Ingrese el metodo por el cual va a resolver el laberinto", True, (0, 0, 255))  # Color azul
    text1_rect = text1.get_rect(center=(WINDOW_SIZE[0] // 2, 50))
    screen.blit(text1, text1_rect)

    # Dibujar botones
    pygame.draw.rect(screen, button_color, depth_button_rect)
    depth_button_text = font.render("Profundidad", True, BLACK)
    text_rect = depth_button_text.get_rect(center=(depth_button_rect.x + depth_button_rect.width / 2, depth_button_rect.y + depth_button_rect.height / 2))
    screen.blit(depth_button_text, text_rect)

    pygame.draw.rect(screen, button_color, breadth_button_rect)
    breadth_button_text = font.render("Anchura", True, BLACK)
    text_rect = breadth_button_text.get_rect(center=(breadth_button_rect.x + breadth_button_rect.width / 2, breadth_button_rect.y + breadth_button_rect.height / 2))
    screen.blit(breadth_button_text, text_rect)

    pygame.draw.rect(screen, button_color, manual_button_rect)
    manual_button_text = font.render("Manual", True, BLACK)
    text_rect = manual_button_text.get_rect(center=(manual_button_rect.x + manual_button_rect.width / 2, manual_button_rect.y + manual_button_rect.height / 2))
    screen.blit(manual_button_text, text_rect)


def state3():
    print("hola")

def handle_events():
    global state, selected_file
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if upload_button_rect.collidepoint(event.pos):
                open_file_dialog()
                state = 1  # Cambiar al siguiente estado después de subir el archivo
                # Imprimir el contenido del archivo en la consola
                if selected_file:
                    with open(selected_file, 'r') as file:
                        print("Contenido del archivo:")
                        print(file.read())
            elif depth_button_rect.collidepoint(event.pos) and state == 1:
                state = 2  # Cambiar al siguiente estado después de presionar el botón "Profundidad"
                depth_function()
            elif breadth_button_rect.collidepoint(event.pos) and state == 1:
                state = 2  # Cambiar al siguiente estado después de presionar el botón "Anchura"
                breadth_function(laberinto)
            elif manual_button_rect.collidepoint(event.pos) and state == 1:
                state = 2  # Cambiar al siguiente estado después de presionar el botón "Manual"
                manual_function(laberinto)

def cargar_laberinto_desde_archivo(nombre_archivo):
    laberinto = []
    with open(nombre_archivo, 'r') as file:
        for line in file:
            row = [int(cell) for cell in line.split()]
            laberinto.append(row)
    return laberinto

def open_file_dialog():
    global selected_file, laberinto
    # Abrir el diálogo de archivos en la carpeta "/laberintos"
    selected_file = filedialog.askopenfilename(initialdir=os.path.join(os.getcwd(), "laberintos"))
    print(f"Seleccionaste el archivo: {selected_file}")
    laberinto = cargar_laberinto_desde_archivo(selected_file)

def depth_function():
    #Profundidad.py
    print("profundidad")
def breadth_function(laberinto):
    Anchura.main(laberinto)
def manual_function(laberinto):
    manual.main(laberinto)

# Bucle principal
clock = pygame.time.Clock()
running = True

while running:
    handle_events()

    # Limpiar la pantalla
    screen.fill(BLACK)

    # Actualizar el estado de acuerdo con el valor de 'state'
    if state == 0:
        state0()
    elif state == 1:
        state1()
        # Limpiar elementos del estado 0
        upload_button_rect = pygame.Rect(0, 0, 0, 0)
    elif state == 3:
        state3()

    # Cambiar al siguiente estado después de procesar eventos
    pygame.display.flip()

    # Controlar la velocidad de fotogramas
    clock.tick(30)
