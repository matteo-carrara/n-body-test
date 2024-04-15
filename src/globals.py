import pygame
import random
import time
import numpy as np
import math
import queue
import tkinter as tk
import threading
import signal


# Define the gravitational constant
G = 6.6743e-11  # N * m^2 / kg^2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen_width = 1600
screen_height = 900

TIMESTEP = 0.0064
BODIES_GEN = 2
GRAVITY_ENABLED = True

b = []
control_queue = queue.Queue()
tk_terminate = threading.Event()

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.Font(None, 32)
pygame_terminate = False

