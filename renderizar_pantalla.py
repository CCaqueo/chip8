import pygame
from constants import *

def inicializar_ventana():
    pygame.init()
    # Abrimos la ventana con el tamaño escalado
    ventana = pygame.display.set_mode((ANCHO_CHIP8 * ESCALA, ALTO_CHIP8 * ESCALA))
    pygame.display.set_caption("Mi Emulador CHIP-8")
    return ventana

