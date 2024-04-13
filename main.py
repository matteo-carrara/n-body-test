import pygame

class Body:
  def __init__(self, radius, x, y) -> None:
    self.radius = radius

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
    pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)

  def anim(self):
    b = self
    b.x += 0
    b.y += 0

    if b.x + b.radius > screen_width or b.x - b.radius < 0:
        b.x -= 2  

    if b.y + b.radius > screen_height or b.y - b.radius < 0:
        b.y -= 1

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()

b = Body(10, 10000, 100000)

running = True
i = 0
while running:
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  screen.fill(BLACK)

  b.draw()
  b.anim()


  pygame.display.flip()

  clock.tick(60)
  i+=1
  print(i)  

pygame.quit()
