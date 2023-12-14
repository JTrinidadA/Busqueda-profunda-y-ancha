import pygame
from tkinter import Tk, filedialog
import os
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
WINDOW_SIZE = (1000, 750)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Crear Laberinto")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Font settings
font = pygame.font.Font(None, 36)

# Input box settings
input_rect = pygame.Rect(250, 300, 400, 40)
input_color_inactive = pygame.Color('lightskyblue3')
input_color_active = pygame.Color('dodgerblue2')
input_color = input_color_inactive
input_text = ''
input_active = False

# Button settings
browse_button_rect = pygame.Rect(250, 400, 200, 50)
upload_button_rect = pygame.Rect(500, 400, 200, 50)
button_color = GRAY

# Tkinter initialization (for file dialog)
root = Tk()
root.withdraw()  # Hide the main window

# Variables for the message
message_text = ''
message_timer = 0

# Main loop
running = True
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                input_active = not input_active
            else:
                input_active = False
            input_color = input_color_active if input_active else input_color_inactive

            # Open file dialog when the "Browse" button is clicked
            if browse_button_rect.collidepoint(event.pos):
                file_path = filedialog.askopenfilename(initialdir=os.path.join(os.getcwd(), "laberintos"))
                if file_path:
                    input_text = file_path

            # Upload file when the "Upload" button is clicked
            elif upload_button_rect.collidepoint(event.pos) and input_text:
                # Save the maze file to the "laberintos" folder
                maze_filename = os.path.join("laberintos", os.path.basename(input_text))
                with open(maze_filename, 'wb') as dest:
                    with open(input_text, 'rb') as src:
                        dest.write(src.read())
                input_text = ''  # Reset input_text after upload

                # Show success message for 3 seconds
                message_text = 'Archivo gaurdado exitosamente!'
                message_timer = current_time + 3000  # 3000 milliseconds (3 seconds)

    # Update display
    screen.fill(BLACK)

    # Render text
    text = font.render("Ingresar Laberinto", True, WHITE)
    screen.blit(text, (250, 250))

    # Draw input box
    pygame.draw.rect(screen, input_color, input_rect, 2)
    txt_surface = font.render(input_text, True, WHITE)
    width = max(200, txt_surface.get_width() + 10)
    input_rect.w = width
    screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 5))
    pygame.draw.rect(screen, WHITE, input_rect, 2)

    # Draw browse button
    pygame.draw.rect(screen, button_color, browse_button_rect)
    browse_button_text = font.render("Seleccionar", True, BLACK)
    screen.blit(browse_button_text, (browse_button_rect.x + 50, browse_button_rect.y + 15))

    # Draw upload button
    pygame.draw.rect(screen, button_color, upload_button_rect)
    upload_button_text = font.render("Subir", True, BLACK)
    screen.blit(upload_button_text, (upload_button_rect.x + 50, upload_button_rect.y + 15))

    # Draw success message if applicable
    if current_time < message_timer:
        message_surface = font.render(message_text, True, WHITE)
        screen.blit(message_surface, (250, 500))

    pygame.display.flip()

    # Quit Pygame after 3 seconds of showing the success message
    if current_time > message_timer and message_timer != 0:  # Add condition to prevent premature exit
        running = False

# Quit Pygame
pygame.quit()
sys.exit()
