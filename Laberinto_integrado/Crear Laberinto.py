import pygame
import sys
import os
from datetime import datetime

# Inicializar Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
GOLD = (255, 215, 0)

# Definir fuentes
font = pygame.font.SysFont("Arial", 20)

# Set up the screen
WINDOW_SIZE = (1400, 750)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Crear Laberinto")

# Inicializar variables
rows_input = ""
cols_input = ""
rows_active = True
cols_active = False
continue_active = False
button_pressed = False
state = 0  # Nuevo estado

color_inactive = pygame.Color("lightskyblue3")
color_active = pygame.Color("dodgerblue2")
color_continue = pygame.Color("green")

color_rows = color_active
color_cols = color_inactive
color_continue_button = color_inactive

clock = pygame.time.Clock()

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_click(event)

        if event.type == pygame.KEYDOWN:
            handle_key_down(event)

def handle_mouse_click(event):
    global rows_active, cols_active, continue_active, color_rows, color_cols, color_continue_button
    global rows_input, cols_input, rows, cols, state, button_pressed
    global continue_button_rect, rows_input_rect, cols_input_rect

    if rows_input_rect.collidepoint(event.pos):
        rows_active = not rows_active
        cols_active = False
        continue_active = False
        color_rows = color_active if rows_active else color_inactive
        color_cols = color_inactive
        color_continue_button = color_inactive
    elif cols_input_rect.collidepoint(event.pos):
        cols_active = not cols_active
        rows_active = False
        continue_active = False
        color_cols = color_active if cols_active else color_inactive
        color_rows = color_inactive
        color_continue_button = color_inactive
    elif continue_button_rect.collidepoint(event.pos):
        if rows_input and cols_input:
            try:
                rows = int(rows_input)
                cols = int(cols_input)
                if rows > 0 and cols > 0:
                    print(f"Crear laberinto de {rows} filas y {cols} columnas")
                    button_pressed = True
                    state = 1  # Cambiamos al nuevo estado permanente

                    # Desactivar y resetear elementos de la interfaz
                    rows_active = False
                    cols_active = False
                    continue_active = False
                    color_rows = color_inactive
                    color_cols = color_inactive
                    color_continue_button = color_inactive
                    continue_button_rect = pygame.Rect(0, 0, 0, 0)
                    rows_input_rect = pygame.Rect(0, 0, 0, 0)
                    cols_input_rect = pygame.Rect(0, 0, 0, 0)
            except ValueError:
                pass
    else:
        rows_active = False
        cols_active = False
        continue_active = False
        color_rows = color_inactive
        color_cols = color_inactive
        color_continue_button = color_inactive

def handle_key_down(event):
    global rows_active, cols_active, rows_input, cols_input

    if rows_active:
        if event.key == pygame.K_RETURN:
            rows_active = False
            cols_active = True
        elif event.key == pygame.K_BACKSPACE:
            rows_input = rows_input[:-1]
        else:
            rows_input += event.unicode
    elif cols_active:
        if event.key == pygame.K_RETURN:
            cols_active = False
            continue_active = True
        elif event.key == pygame.K_BACKSPACE:
            cols_input = cols_input[:-1]
        else:
            cols_input += event.unicode

def draw_input_box(rect, color, text):
    pygame.draw.rect(screen, color, rect, 2)
    txt_surface = font.render(text, True, color)
    width = max(200, txt_surface.get_width() + 10)
    rect.w = width
    screen.blit(txt_surface, (rect.x + 5, rect.y + 5))

def state0():
    global state, rows_input, cols_input, rows_active, cols_active, continue_active, color_rows, color_cols, color_continue_button
    global rows_input_rect, cols_input_rect, continue_button_rect

    # Dibujar las cajas de entrada y el botón
    rows_input_rect = pygame.Rect(700, 100, 100, 32)
    cols_input_rect = pygame.Rect(700, 150, 100, 32)
    continue_button_rect = pygame.Rect(600, 650, 200, 50)

    # Dibujar los textos "Filas" y "Columnas"
    text_surface_rows = font.render("Filas:", True, WHITE)
    text_surface_cols = font.render("Columnas:", True, WHITE)

    text_rect_rows = text_surface_rows.get_rect(center=(rows_input_rect.x - 60, rows_input_rect.centery))
    text_rect_cols = text_surface_cols.get_rect(center=(cols_input_rect.x - 80, cols_input_rect.centery))

    screen.blit(text_surface_rows, text_rect_rows)
    screen.blit(text_surface_cols, text_rect_cols)
    draw_input_box(rows_input_rect, color_rows, rows_input)
    draw_input_box(cols_input_rect, color_cols, cols_input)
    pygame.draw.rect(screen, color_continue_button, continue_button_rect)
    txt_surface = font.render("Continuar", True, BLACK)
    text_rect = txt_surface.get_rect(center=continue_button_rect.center)
    screen.blit(txt_surface, text_rect)

def state1():
    global state, rows, cols, grid_state

    pygame.display.flip()
    screen.fill(BLACK)

    box_size = 30
    padding = 5
    start_x = 50
    start_y = 50

    # Inicializar la matriz que representa el estado de cada cuadrícula
    grid_state = [[False for _ in range(cols)] for _ in range(rows)]

    for row in range(rows):
        for col in range(cols):
            x = start_x + col * (box_size + padding)
            y = start_y + row * (box_size + padding)

            # Dibujar cuadrícula
            pygame.draw.rect(screen, WHITE, (x, y, box_size, box_size), 0 if grid_state[row][col] else 2)

    save_button_rect = pygame.Rect(600, 650, 200, 50)
    pygame.draw.rect(screen, WHITE, save_button_rect)
    txt_surface_save = font.render("Crear Laberinto", True, BLACK)
    text_rect_save = txt_surface_save.get_rect(center=save_button_rect.center)
    screen.blit(txt_surface_save, text_rect_save)

    pygame.display.flip()

    handling_events = True  # Variable de control para manejar eventos

    while handling_events:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo del ratón
                    mouseX, mouseY = event.pos

                    for row in range(rows):
                        for col in range(cols):
                            x = start_x + col * (box_size + padding)
                            y = start_y + row * (box_size + padding)

                            if x < mouseX < x + box_size and y < mouseY < y + box_size:
                                grid_state[row][col] = not grid_state[row][col]

                    screen.fill(BLACK)
                    for row in range(rows):
                        for col in range(cols):
                            x = start_x + col * (box_size + padding)
                            y = start_y + row * (box_size + padding)
                            pygame.draw.rect(screen, WHITE, (x, y, box_size, box_size), 0 if grid_state[row][col] else 2)

                    pygame.draw.rect(screen, WHITE, save_button_rect)
                    txt_surface_save = font.render("Crear Laberinto", True, BLACK)
                    text_rect_save = txt_surface_save.get_rect(center=save_button_rect.center)
                    screen.blit(txt_surface_save, text_rect_save)

                    pygame.display.flip()

                    if save_button_rect.collidepoint(event.pos):
                        print("Guardar")
                        for row in range(rows):
                            row_str = ""
                            for col in range(cols):
                                # Imprimir 1 si la casilla es blanca, 0 si es negra
                                row_str += "1" if grid_state[row][col] else "0"
                                if col < cols - 1:
                                    row_str += " "
                            print(row_str)
                        state = 2  # Cambiar al estado 2
                        print("Estado 2")
                        handling_events = False  # Salir del bucle de manejo de eventos

                        continue_button_rect = pygame.Rect(600, 650, 200, 50)
                        pygame.draw.rect(screen, WHITE, continue_button_rect)
                        txt_surface_continue = font.render("Agregar Inicio", True, BLACK)
                        text_rect_continue = txt_surface_continue.get_rect(center=continue_button_rect.center)
                        screen.blit(txt_surface_continue, text_rect_continue)

                        pygame.display.flip()

def state2():
    global state, rows, cols, grid_state, original_grid

    box_size = 30
    padding = 5
    start_x = 50
    start_y = 50

    entry_selected = None  # Inicializar la variable entry_selected
    prev_entry_selected = None  # Rastrear el cuadro previamente seleccionado

    # Dibujar el arreglo guardado en el estado 1
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * (box_size + padding)
            y = start_y + row * (box_size + padding)

            # Dibujar cuadrícula
            pygame.draw.rect(screen, WHITE, (x, y, box_size, box_size), 0 if grid_state[row][col] else 2)

    handling_events = True  # Variable de control para manejar eventos

    while handling_events:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo del ratón
                    mouseX, mouseY = event.pos

                    for row in range(rows):
                        for col in range(cols):
                            x = start_x + col * (box_size + padding)
                            y = start_y + row * (box_size + padding)

                            if x < mouseX < x + box_size and y < mouseY < y + box_size:
                                if grid_state[row][col] and entry_selected is None:
                                    entry_selected = (row, col)
                                    grid_state[row][col] = False  # Limpiar la casilla anterior
                                elif not grid_state[row][col] and entry_selected is not None:
                                    prev_entry_selected = entry_selected
                                    row_selected, col_selected = entry_selected
                                    grid_state[row_selected][col_selected] = False  # Limpiar la casilla anterior
                                    entry_selected = (row, col)

                    # Restaurar el color del cuadro previamente seleccionado
                    if prev_entry_selected is not None:
                        row_selected, col_selected = prev_entry_selected
                        x = start_x + col_selected * (box_size + padding)
                        y = start_y + row_selected * (box_size + padding)
                        pygame.draw.rect(screen, WHITE, (x, y, box_size, box_size), 0 if grid_state[row_selected][col_selected] else 2)

                    screen.fill(BLACK)
                    for row in range(rows):
                        for col in range(cols):
                            x = start_x + col * (box_size + padding)
                            y = start_y + row * (box_size + padding)
                            if entry_selected is not None and (row, col) == entry_selected:
                                pygame.draw.rect(screen, BLUE, (x, y, box_size, box_size))
                            else:
                                pygame.draw.rect(screen, WHITE, (x, y, box_size, box_size), 0 if grid_state[row][col] else 2)

                    continue_button_rect = pygame.Rect(600, 650, 200, 50)
                    pygame.draw.rect(screen, WHITE, continue_button_rect)
                    txt_surface_continue = font.render("Agregar Inicio", True, BLACK)
                    text_rect_continue = txt_surface_continue.get_rect(center=continue_button_rect.center)
                    screen.blit(txt_surface_continue, text_rect_continue)

                    pygame.display.flip()

                    if continue_button_rect.collidepoint(event.pos) and entry_selected is not None:
                        handling_events = False  # Salir del bucle de manejo de eventos

    # Antes de pasar al estado 3, guardar el arreglo en el original de la cuadrícula
    original_grid = [[2 if cell == 2 else 1 if cell == 1 else 0 for cell in row] for row in grid_state]

    # Marcar la casilla de inicio con el valor 2
    if entry_selected is not None:
        row_selected, col_selected = entry_selected
        original_grid[row_selected][col_selected] = 2

    state = 3  # Cambiar al estado 3 después de completar la interacción

    # Imprimir la matriz en la consola con el formato adecuado
    print("Matriz resultante:")
    for row in range(rows):
        row_str = ""
        for col in range(cols):
            row_str += str(original_grid[row][col])
            if col < cols - 1:
                row_str += " "
        print(row_str)
    continue_button_rect = pygame.Rect(600, 650, 200, 50)
    pygame.draw.rect(screen, WHITE, continue_button_rect)
    txt_surface_continue = font.render("Agregar Final", True, BLACK)
    text_rect_continue = txt_surface_continue.get_rect(center=continue_button_rect.center)
    screen.blit(txt_surface_continue, text_rect_continue)

    pygame.display.flip()

    print("Estado 3")


def state3():
    global state, rows, cols, grid_state, original_grid

    box_size = 30
    padding = 5
    start_x = 50
    start_y = 50

    entry_selected = None  # Inicializar la variable entry_selected
    prev_entry_selected = None  # Rastrear el cuadro previamente seleccionado

    # Dibujar el arreglo guardado en el estado 1
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * (box_size + padding)
            y = start_y + row * (box_size + padding)

            # Dibujar cuadrícula
            pygame.draw.rect(screen, WHITE, (x, y, box_size, box_size), 0 if grid_state[row][col] else 2)

    handling_events = True  # Variable de control para manejar eventos

    while handling_events:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo del ratón
                    mouseX, mouseY = event.pos

                    for row in range(rows):
                        for col in range(cols):
                            x = start_x + col * (box_size + padding)
                            y = start_y + row * (box_size + padding)

                            if x < mouseX < x + box_size and y < mouseY < y + box_size:
                                if grid_state[row][col] and entry_selected is None:
                                    entry_selected = (row, col)
                                    grid_state[row][col] = False  # Limpiar la casilla anterior
                                elif not grid_state[row][col] and entry_selected is not None:
                                    prev_entry_selected = entry_selected
                                    row_selected, col_selected = entry_selected
                                    grid_state[row_selected][col_selected] = False  # Limpiar la casilla anterior
                                    entry_selected = (row, col)

                    # Restaurar el color del cuadro previamente seleccionado
                    if prev_entry_selected is not None:
                        row_selected, col_selected = prev_entry_selected
                        x = start_x + col_selected * (box_size + padding)
                        y = start_y + row_selected * (box_size + padding)
                        pygame.draw.rect(screen, WHITE, (x, y, box_size, box_size), 0 if original_grid[row_selected][col_selected] == 0 else 1 if original_grid[row_selected][col_selected] == 1 else 2)


                    screen.fill(BLACK)
                    for row in range(rows):
                        for col in range(cols):
                            x = start_x + col * (box_size + padding)
                            y = start_y + row * (box_size + padding)
                            if entry_selected is not None and (row, col) == entry_selected:
                                pygame.draw.rect(screen, RED, (x, y, box_size, box_size))
                            elif original_grid[row][col] == 2:
                                pygame.draw.rect(screen, BLUE, (x, y, box_size, box_size))
                            elif original_grid[row][col] == 1:
                                pygame.draw.rect(screen, WHITE, (x, y, box_size, box_size))
                            elif original_grid[row][col] == 0:
                                pygame.draw.rect(screen, BLACK, (x, y, box_size, box_size))
                    continue_button_rect = pygame.Rect(600, 650, 200, 50)
                    pygame.draw.rect(screen, WHITE, continue_button_rect)
                    txt_surface_continue = font.render("Agregar Final", True, BLACK)
                    text_rect_continue = txt_surface_continue.get_rect(center=continue_button_rect.center)
                    screen.blit(txt_surface_continue, text_rect_continue)

                    pygame.display.flip()

                    if continue_button_rect.collidepoint(event.pos) and entry_selected is not None:
                        handling_events = False  # Salir del bucle de manejo de eventos


    # Marcar la casilla de inicio con el valor 3
    if entry_selected is not None:
        row_selected, col_selected = entry_selected
        original_grid[row_selected][col_selected] = 3

    state = 4  # Cambiar al estado 4 después de completar la interacción

    # Imprimir la matriz en la consola con el formato adecuado
    print("Matriz resultante:")
    for row in range(rows):
        row_str = ""
        for col in range(cols):
            row_str += str(original_grid[row][col])
            if col < cols - 1:
                row_str += " "
        print(row_str)

    print("Estado 4")

def state4():
    global state, original_grid

    # Dibujar el arreglo en la pantalla
    screen.fill(BLACK)
    for row in range(rows):
        for col in range(cols):
            x = 50 + col * 35
            y = 50 + row * 35
            if original_grid[row][col] == 3:
                pygame.draw.rect(screen, RED, (x, y, 30, 30))
            elif original_grid[row][col] == 2:
                pygame.draw.rect(screen, BLUE, (x, y, 30, 30))
            elif original_grid[row][col] == 1:
                pygame.draw.rect(screen, WHITE, (x, y, 30, 30))
            elif original_grid[row][col] == 0:
                pygame.draw.rect(screen, BLACK, (x, y, 30, 30))

    # Imprimir el mensaje en la pantalla
    txt_surface = font.render("Laberinto creado", True, WHITE)
    text_rect = txt_surface.get_rect(center=(400, 550))
    screen.blit(txt_surface, text_rect)

    # Crear el nombre del archivo con la hora actual
    now = datetime.now()
    timestamp = now.strftime("%H%M%S")
    filename = f"laberinto{timestamp}.txt"
    filepath = os.path.join("laberintos", filename)

    # Guardar el arreglo en el archivo
    with open(filepath, "w") as file:
        for row in original_grid:
            row_str = " ".join(map(str, row))
            file.write(row_str + "\n")

    # Cambiar al siguiente estado después de un tiempo
    pygame.display.flip()
    pygame.time.delay(3000)  # Esperar 3 segundos
    state = 0  # Cambiar al estado inicial
    pygame.quit()
    sys.exit()

# Bucle principal
while True:
    handle_events()

    # Limpiar la pantalla
    screen.fill(BLACK)

    if state == 0:  # Estado inicial
        state0()
    elif state == 1:  # Nuevo estado después de presionar el botón
        state1()
    elif state == 2:
        state2()
    elif state == 3:
        state3()
    elif state == 4:
        state4()

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de fotogramas
    clock.tick(30)
