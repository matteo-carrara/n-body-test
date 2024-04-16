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

screen_width = 800
screen_height = 600

TIMESTEP = 0.0064
BODIES_GEN = 3

TRAIL_LENGHT = 1600

GRAVITY_ENABLED = False
UNIV_BORDERS = True

ZOOM_ENABLED = False
COLOR_PALETTE = "scientific"

MIN_MASS = 9e15
MAX_MASS = 9e16

b = []
control_queue = queue.Queue()
tk_terminate = threading.Event()
shared_tk_window = queue.Queue()

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.Font(None, 32)
pygame_terminate = False

