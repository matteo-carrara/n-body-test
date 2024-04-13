import pygame
import random
import time
import numpy as np
import math

# Define the gravitational constant
G = 6.6743e-11  # N * m^2 / kg^2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
screen_width = 1280
screen_height = 900

TIMESTEP = 0.1


def point_dist(x1, y1, x2, y2):
  # Calculate the squared difference in x and y coordinates
  delta_x = (x2 - x1) ** 2
  delta_y = (y2 - y1) ** 2

  # Apply the Pythagorean theorem and return the distance
  distance = math.sqrt(delta_x + delta_y)
  return distance


def gravitational_acceleration(body1_mass, body2_mass, body1_pos, body2_pos, gravitational_constant):
  """
  Calculates the gravitational acceleration on two bodies due to their mutual attraction.

  Args:
      body1_mass (float): Mass of the first body.
      body2_mass (float): Mass of the second body.
      body1_pos (np.ndarray): (x, y) position of the first body.
      body2_pos (np.ndarray): (x, y) position of the second body.
      gravitational_constant (float): Gravitational constant (G).

  Returns:
      tuple: (ax, ay), the x and y components of acceleration for body1.
  """
  # Calculate distance vector between bodies
  distance_vector = body2_pos - body1_pos

  # Check for zero distance (avoid division by zero)
  if np.linalg.norm(distance_vector) < 1e-10:
    return np.zeros(2), np.zeros(2)

  # Calculate magnitude of gravitational force
  force_magnitude = gravitational_constant * body1_mass * body2_mass / np.linalg.norm(distance_vector)**2

  # Calculate acceleration due to gravity (Newton's second law)
  acceleration = force_magnitude / body1_mass * distance_vector / np.linalg.norm(distance_vector)

  return acceleration


class Body:
  mass = 0
  vx = 10
  vy = 10
  border = False
  border_cnt = 0

  def __init__(self, radius, x, y, color = WHITE) -> None:
    self.radius = radius
    self.rad = radius
    self.color = color

    if(x < radius):
      x = radius

    if(y < radius):
      y = radius

    if(x > screen_width):
      x = screen_width

    if (y > screen_height):
      y = screen_height

    self.x = x
    self.y = y
  
  def look_result(self, times):
     self.border_cnt = times

  def draw(self):
    pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    if(self.border_cnt > 0):
       self.border_cnt -= 1
       print("x,y", self.x, self.y)
       #input()

  def update_pos(self):
    b = self
    b.x += b.vx * TIMESTEP
    b.y += b.vy * TIMESTEP

    if(b.x > screen_width-b.rad):
       print("X COLLISION", b.x)
       b.x = (screen_width-b.rad) - (b.x - (screen_width-b.rad))
       b.vx = -b.vx
      
       #input()
       self.look_result(3)
    if (b.x < b.rad):
       print("X COLLISION", b.x)
       b.x = b.rad + abs(b.x - b.rad)
       b.vx = -b.vx
       
       #input()
       self.look_result(3)
    if(b.y > screen_height-b.rad):
       print("Y COLLISION", b.y)
       b.y = (screen_height - b.rad) - (b.y - (screen_height - b.rad))
       b.vy = -b.vy
       
       #input()
       self.look_result(3)
    if (b.y < b.rad):
       print("Y COLLISION", b.y)
       b.y = b.rad + (b.rad - b.y)
       b.vy = -b.vy
       
       #input()
       self.look_result(3)

  def look_newpos(self):
     if (self.border):
        #input()
        self.border = False

def do_not_overlap(p1, p2, r1, r2):
  """
  This function checks if two circles do not overlap.

  Args:
      p1: Center coordinates of the first circle as a tuple (x1, y1).
      p2: Center coordinates of the second circle as a tuple (x2, y2).
      r1: Radius of the first circle.
      r2: Radius of the second circle.

  Returns:
      True if the circles do not overlap, False otherwise.
  """
  # Calculate the distance between the centers
  distance = ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) ** 0.5

  # Check for non-overlap conditions
  return distance > r1 + r2  # Circles are too far apart



def create_bodies(num):
  min_radius = 20
  max_radius = 60
  minmass = int(1e13)
  maxmass = int(1e15)
  ret = []

  for i in range (num):
    print("Generating object", i)
    
    found = False
    color = (random.randrange(64, 256), random.randrange(64, 256), random.randrange(64, 256))
    
    while (not found):
        print("Generating...")

        rad = random.randrange(min_radius, max_radius+1)
        test_x = random.randrange(rad, screen_width+1)
        test_y = random.randrange(rad, screen_height+1)

        found = True
        i = 0
        print("Checking collisions")
        for other in ret:
            print("Check against #", i)
            good = do_not_overlap((other.x, other.y), (test_x, test_y), other.rad, rad)
            i += 1

            if (not good):
               found = False
               print("\n\n!!!!!!!!!!!!!!!!! Overlap detected\n\n")
               break
            else:
               print ("Is good")

    print("Found, appending result")
    print("Obj", rad, test_x, test_y)
    ret.append(Body(rad, test_x, test_y, color))
    ret[-1].mass = minmass + ((maxmass-minmass)* rad/max_radius)


    print("Drawing screen")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    screen.fill(BLACK)
    for b in ret:
        b.draw()
           
    pygame.display.flip()
    

    
  print("Leaving generation...")
  #input()  
  return ret


def calc_forces(b):
    for i in range(len(b)):
       print("\n\nUsing elem", i)
       print("Mass", b[i].mass, "Center", b[i].x, b[i].y)

       for k in range(len(b)):
          if (k == i):
             continue
          
          print("Against", k)
          print("Mass", b[k].mass, "Center", b[k].x, b[k].y)

          d = point_dist(b[i].x, b[i].y, b[k].x, b[k].y)
          print("Distance", d)

          acc = gravitational_acceleration(b[i].mass, b[k].mass, np.array([b[i].x, b[i].y]), np.array([b[k].x, b[k].y]), G)
          print("Acceleration of body", i, acc)

          b[i].vx += acc[0]*TIMESTEP
          b[i].vy += acc[1]*TIMESTEP

          print("New velocity",  b[i].vx, b[i].vy)

    print("updating positions for timestep")
    for elem in b:
        elem.update_pos()



pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()


b = create_bodies(5)


running = True
i = 0
while running:
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  screen.fill(BLACK)

  for elem in b:
     elem.draw()
     #elem.anim()


  pygame.display.flip()

  clock.tick(60)
  print("Calculating forces...")
  calc_forces(b)
  #input()

pygame.quit()
