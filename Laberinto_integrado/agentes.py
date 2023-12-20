import pygame
import sys
import time

def agente (seleccion): 
    if seleccion == 1:
        nombre = "humano"
        celdas_disponibles = {1, 2, 3, 4, 5, 6}
        costos = [
            1 : 1
            2 : 1
            3 : 1
            4 : 4
            5 : 3
            6 : 2
        ]