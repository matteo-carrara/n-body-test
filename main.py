import pygame
import random
import time


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
screen_width = 800
screen_height = 600


class Body:
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
  
  def draw(self):
    pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

  def anim(self):
    b = self
    b.x += 0
    b.y += 0

    if b.x + b.radius > screen_width or b.x - b.radius < 0:
        b.x -= 2  

    if b.y + b.radius > screen_height or b.y - b.radius < 0:
        b.y -= 1


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





pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()


b = create_bodies(50)


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

pygame.quit()
