# filename: verify_pygame_installation.py
try:
    import pygame
    print("Pygame is installed correctly!")
except ImportError:
    print("Pygame is not installed.")