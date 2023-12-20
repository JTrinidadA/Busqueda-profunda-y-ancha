import pygame
import sys
import subprocess  # Para ejecutar programas externos


# Initialize Pygame
pygame.init()

# Set up the screen
WINDOW_SIZE = (1400, 750)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Practica 2")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GOLD = (255, 215, 0)  # Color dorado

# Define fonts
title_font = pygame.font.SysFont("Arial", 40)
option_font = pygame.font.SysFont("Arial", 30)

# Function to display text on the screen
def display_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    return text_rect

# Function to handle option events
def handle_option(option):
    if option == 1:
        # Ejecutar el programa correspondiente a la opción 1
        print("Ejecutando programa para Crear laberinto")
        # Puedes reemplazar el siguiente comando con el que necesites
        subprocess.run(["python", "Crear Laberinto.py"])
    elif option == 2:
        # Ejecutar el programa correspondiente a la opción 2
        print("Ejecutando programa para Resolver laberinto")
        # Puedes reemplazar el siguiente comando con el que necesites
        subprocess.run(["python", "Resolver Laberinto.py"])
    elif option == 3:
        # Ejecutar el programa correspondiente a la opción 3
        print("Ejecutando programa para Cargar laberinto")
        # Puedes reemplazar el siguiente comando con el que necesites
        subprocess.run(["python", "Cargar Laberinto.py"])
    elif option == 4:
        # Salir del programa
        pygame.quit()
        sys.exit()

# Main game loop
options = ["Crear laberinto", "Resolver laberinto", "Cargar laberinto", "Salir"]
option_rects = []

for i, option in enumerate(options, start=1):
    text_rect = display_text(option, option_font, WHITE, WINDOW_SIZE[0] // 2, 120 + i * 40)
    option_rects.append((text_rect, i, option))

selected_option = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Verificar si el mouse hizo clic en alguna opción
            for text_rect, option_num, option_text in option_rects:
                if text_rect.collidepoint(pygame.mouse.get_pos()):
                    selected_option = option_num
                    handle_option(selected_option)

    # Clear the screen
    screen.fill(BLACK)

    # Display title
    display_text("Los Nalgones", title_font, WHITE, WINDOW_SIZE[0] // 2, 50)

    # Check if the mouse is over an option and change its color
    for text_rect, option_num, option_text in option_rects:
        if text_rect.collidepoint(pygame.mouse.get_pos()):
            color = GOLD
        else:
            color = WHITE
        display_text(option_text, option_font, color, text_rect.centerx, text_rect.centery)

    # Update the display
    pygame.display.update()
