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

TIMESTEP = 0.01


def calculate_collision_velocities(
    mass1, mass2, velocity1x, velocity1y, velocity2x, velocity2y
):
    """
    This function calculates the final velocities of two bodies after a 2D elastic collision.

    Args:
        mass1 (float): Mass of the first body.
        mass2 (float): Mass of the second body.
        velocity1x (float): Initial x-component of velocity of the first body.
        velocity1y (float): Initial y-component of velocity of the first body.
        velocity2x (float): Initial x-component of velocity of the second body.
        velocity2y (float): Initial y-component of velocity of the second body.

    Returns:
        tuple: A tuple containing the final velocities (v1fx, v1fy, v2fx, v2fy) for body 1 and body 2 in x and y directions.
    """

    # Conservation of momentum (x and y components)
    v1fx = (mass1 * velocity1x + mass2 * velocity2x) / (mass1 + mass2)
    v1fy = (mass1 * velocity1y + mass2 * velocity2y) / (mass1 + mass2)
    v2fx = (mass2 * velocity2x + mass1 * velocity1x) / (mass1 + mass2)
    v2fy = (mass2 * velocity2y + mass1 * velocity1y) / (mass1 + mass2)

    return v1fx, v1fy, v2fx, v2fy


def point_dist(x1, y1, x2, y2):
    # Calculate the squared difference in x and y coordinates
    delta_x = (x2 - x1) ** 2
    delta_y = (y2 - y1) ** 2

    # Apply the Pythagorean theorem and return the distance
    distance = math.sqrt(delta_x + delta_y)
    return distance


def gravitational_acceleration(
    body1_mass, body2_mass, body1_pos, body2_pos, gravitational_constant
):
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
    force_magnitude = (
        gravitational_constant
        * body1_mass
        * body2_mass
        / np.linalg.norm(distance_vector) ** 2
    )

    # Calculate acceleration due to gravity (Newton's second law)
    acceleration = (
        force_magnitude / body1_mass * distance_vector / np.linalg.norm(distance_vector)
    )

    return acceleration


class Body:
    coll_distance = {}  # first the index, then the distance
    skip = False
    mass = 0
    vx = 60
    vy = 60
    border = False
    border_cnt = 0

    def __init__(self, radius, x, y, color=WHITE) -> None:
        self.radius = radius
        self.rad = radius
        self.color = color

        if x < radius:
            x = radius

        if y < radius:
            y = radius

        if x > screen_width:
            x = screen_width

        if y > screen_height:
            y = screen_height

        self.x = x
        self.y = y

    def look_result(self, times):
        self.border_cnt = times

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        text = (
            "m "
            + f"{self.mass:.0e}"
            + " vx"
            + f"{self.vx:.1f}"
            + " vy"
            + f"{self.vy:.1f}"
        )

        # text_surface = font.render(text, True, RED)
        # screen.blit(text_surface, (self.x, self.y))

        if self.border_cnt > 0:
            self.border_cnt -= 1
            print("x,y", self.x, self.y)
            # input()

    def skip_update(self):
        self.skip = True

    def step_back(self):
        self.x = self.old_x
        self.y = self.old_y

    def update_pos(self):
        if self.skip == True:
            self.skip = False
            return

        b = self

        if len(self.coll_distance.keys()) > 0:
            # print("WARNING THIS OBJECT COLLIDED")
            pass

        self.old_x = self.x
        self.old_y = self.y

        b.x += b.vx * TIMESTEP
        b.y += b.vy * TIMESTEP

        if b.x > screen_width - b.rad:
            print("X COLLISION", b.x)
            b.x = (screen_width - b.rad) - (b.x - (screen_width - b.rad))
            b.vx = -b.vx

            # input()
            self.look_result(3)
        if b.x < b.rad:
            print("X COLLISION", b.x)
            b.x = b.rad + abs(b.x - b.rad)
            b.vx = -b.vx

            # input()
            self.look_result(3)
        if b.y > screen_height - b.rad:
            print("Y COLLISION", b.y)
            b.y = (screen_height - b.rad) - (b.y - (screen_height - b.rad))
            b.vy = -b.vy

            # input()
            self.look_result(3)
        if b.y < b.rad:
            print("Y COLLISION", b.y)
            b.y = b.rad + (b.rad - b.y)
            b.vy = -b.vy

            # input()
            self.look_result(3)

    def look_newpos(self):
        if self.border:
            # input()
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
    distance = ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

    # Check for non-overlap conditions
    return distance > r1 + r2  # Circles are too far apart


def create_bodies(num):
    min_radius = 30
    max_radius = 120
    minmass = int(1e15)
    maxmass = int(1e16)
    ret = []

    for i in range(num):
        print("Generating object", i)

        found = False
        c = random.randrange(64, 256)
        color = (
            c,
            c,
            c,
        )

        while not found:
            print("Generating...")

            rad = random.randrange(min_radius, max_radius + 1)
            test_x = random.randrange(rad, screen_width + 1)
            test_y = random.randrange(rad, screen_height + 1)

            found = True
            i = 0
            print("Checking collisions")
            for other in ret:
                print("Check against #", i)
                good = do_not_overlap(
                    (other.x, other.y), (test_x, test_y), other.rad, rad
                )
                i += 1

                if not good:
                    found = False
                    print("\n\n!!!!!!!!!!!!!!!!! Overlap detected\n\n")
                    break
                else:
                    print("Is good")

        print("Found, appending result")
        print("Obj", rad, test_x, test_y)
        ret.append(Body(rad, test_x, test_y, color))
        ret[-1].mass = minmass + ((maxmass - minmass) * rad / max_radius)

        print("Drawing screen")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        for b in ret:
            b.draw()

        pygame.display.flip()

    print("Leaving generation...")
    # input()
    return ret


def calc_forces(b):
    for i in range(len(b)):
        print("\n\nUsing elem", i)
        print("Mass", b[i].mass, "Center", b[i].x, b[i].y)

        for k in range(len(b)):
            if k == i:
                continue

            print("Against", k)
            print("Mass", b[k].mass, "Center", b[k].x, b[k].y)

            d = point_dist(b[i].x, b[i].y, b[k].x, b[k].y)
            print("Distance", d)

            acc = gravitational_acceleration(
                b[i].mass,
                b[k].mass,
                np.array([b[i].x, b[i].y]),
                np.array([b[k].x, b[k].y]),
                G,
            )
            print("Acceleration of body", i, acc)

            b[i].vx += acc[0] * TIMESTEP
            b[i].vy += acc[1] * TIMESTEP

            print("New velocity", b[i].vx, b[i].vy)

    print("updating positions for timestep")
    for elem in b:
        elem.update_pos()


def separate_circles(c1x, c1y, r1, c2x, c2y, r2):
  """
  This function calculates the new centers of two partially overlapping circles,
  such that they barely touch after separation (maximizing their overlap).

  Args:
      c1x: x-coordinate of the center of circle 1
      c1y: y-coordinate of the center of circle 1
      r1: radius of circle 1
      c2x: x-coordinate of the center of circle 2
      c2y: y-coordinate of the center of circle 2
      r2: radius of circle 2

  Returns:
      A tuple of two tuples, each containing the new (x, y) center coordinates 
      for the corresponding circle. 
  """
  # Calculate the distance between the centers
  distance = math.sqrt((c1x - c2x)**2 + (c1y - c2y)**2)

  # Minimum distance between the circles for them to touch
  min_distance = r1 + r2

  # No overlap if distance is greater than or equal to minimum distance
  if distance >= min_distance:
    return c1x, c1y, c2x, c2y

  # Overlap exists

  # Calculate the direction vector between the centers
  direction_x = c2x - c1x
  direction_y = c2y - c1y

  # Normalize the direction vector
  norm = math.sqrt(direction_x**2 + direction_y**2)
  unit_direction_x = direction_x / norm
  unit_direction_y = direction_y / norm

  # Move each circle center by half of the difference between actual distance 
  # and minimum distance in the direction vector
  new_c1x = c1x + unit_direction_x * (distance - min_distance) / 2
  new_c1y = c1y + unit_direction_y * (distance - min_distance) / 2
  new_c2x = c2x - unit_direction_x * (distance - min_distance) / 2
  new_c2y = c2y - unit_direction_y * (distance - min_distance) / 2

  return new_c1x, new_c1y, new_c2x, new_c2y

def univ_collision(b, ind_fixed):
    found = 0

    still_broken = []

    for i in range(len(b)):
        for k in range(len(b)):
            if k == i:
                continue

            if not do_not_overlap(
                (b[i].x, b[i].y), (b[k].x, b[k].y), b[i].rad, b[k].rad
            ):
                print("Collided")
                
                print("Centering objects")
                print("Before", b[i].x, b[i].y, b[k].x, b[k].y)
                b[i].x, b[i].y, b[k].x, b[k].y = separate_circles(b[i].x, b[i].y, b[i].rad, b[k].x, b[k].y, b[k].rad)
                print("After", b[i].x, b[i].y, b[k].x, b[k].y)
                #input()
                
                if sorted([i, k]) in ind_fixed:
                    print("Already fixed")
                    print("Old distance", b[i].coll_distance[k])
                    nd = point_dist(b[i].x, b[i].y, b[k].x, b[k].y)
                    print("New distance", nd)

                    if nd < b[i].coll_distance[k]:
                        print("The object got closer, reverting")
                        # b[i].step_back()
                        # b[k].step_back()
                    else:
                        print("The objects are moving away")

                    # input()
                    still_broken.append(sorted([i, k]))
                else:
                    found += 1
                    r = calculate_collision_velocities(
                        b[i].mass, b[k].mass, b[i].vx, b[i].vy, b[k].vx, b[k].vy
                    )
                    b[i].vx = r[0]
                    b[i].vy = r[1]
                    b[k].vx = r[2]
                    b[k].vy = r[3]
                    ind_fixed.append(sorted([i, k]))
                    print("New velocities", r)
                    tmp_dist = point_dist(b[i].x, b[i].y, b[k].x, b[k].y)
                    b[i].coll_distance[k] = tmp_dist
                    b[k].coll_distance[i] = tmp_dist
                    


    to_delete = []
    try:
        for i in range(len(ind_fixed)):
            if not (ind_fixed[i] in still_broken):
                to_delete.append(i)
    except:
        print(ind_fixed)
        exit(1)

    tmplist = [a for b, a in enumerate(ind_fixed) if b not in to_delete]

    if found > 0:
        print("Found collisions:", found)
        # input()

    return tmplist


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)


b = create_bodies(5)


running = True
i = 0
tmp = []
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    for elem in b:
        elem.draw()
        # elem.anim()

    pygame.display.flip()

    clock.tick(60)
    print("Calculating forces...")
    calc_forces(b)
    tmp = univ_collision(b, tmp)
    # input()

pygame.quit()
