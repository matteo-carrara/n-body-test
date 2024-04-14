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

b = []

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

def calculate_kinetic_energy(masses, velocities):
  """
  This function calculates the kinetic energy of each flying mass in a 2D space.

  Args:
      masses (list): A list containing the mass of each flying object.
      velocities (list): A list containing the velocity vector (2D) for each object (e.g., [vx, vy]).

  Returns:
      list: A list containing the kinetic energy of each flying object.
  """

  if len(masses) != len(velocities):
    raise ValueError("Lengths of masses and velocities lists must be equal.")

  kinetic_energies = []
  for mass, velocity in zip(masses, velocities):
    # Calculate magnitude squared of velocity vector (2D)
    magnitude_squared = sum(v**2 for v in velocity)
    # Calculate kinetic energy for each mass
    kinetic_energy = 0.5 * mass * magnitude_squared
    kinetic_energies.append(kinetic_energy)

  return kinetic_energies

class Body:
    coll_distance = {}  # first the index, then the distance
    skip = False
    mass = 0
    vx = 0
    vy = 0
    border = False
    border_cnt = 0
    colliding = 0

    def accel(self, ax, ay):
        if (self.colliding == 0):
            self.vx += ax
            self.vy += ay
        else:
            #print("Colliding, skipping")
            pass

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
            "vx"
            + f"{self.vx:.1f}"
            + " vy"
            + f"{self.vy:.1f}"
        )

        text_surface = font.render(text, True, RED)
        screen.blit(text_surface, (self.x, self.y))

        if self.border_cnt > 0:
            self.border_cnt -= 1
            ##print("x,y", self.x, self.y)
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
            # ##print("WARNING THIS OBJECT COLLIDED")
            pass

        self.old_x = self.x
        self.old_y = self.y

        b.x += b.vx * TIMESTEP
        b.y += b.vy * TIMESTEP

        if b.x > screen_width - b.rad:
            ##print("X COLLISION", b.x)
            b.x = (screen_width - b.rad) - (b.x - (screen_width - b.rad))
            b.vx = -b.vx

            # input()
            self.look_result(3)
        if b.x < b.rad:
            ##print("X COLLISION", b.x)
            b.x = b.rad + abs(b.x - b.rad)
            b.vx = -b.vx

            # input()
            self.look_result(3)
        if b.y > screen_height - b.rad:
            ##print("Y COLLISION", b.y)
            b.y = (screen_height - b.rad) - (b.y - (screen_height - b.rad))
            b.vy = -b.vy

            # input()
            self.look_result(3)
        if b.y < b.rad:
            ##print("Y COLLISION", b.y)
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
    min_radius = 15
    max_radius = 30
    minmass = int(1e15)
    maxmass = int(1e16)
    ret = []

    for i in range(num):
        ##print("Generating object", i)

        found = False
        c = random.randrange(64, 256)
        color = (
            random.randrange(64, 256),
            random.randrange(64, 256),
            random.randrange(64, 256),
        )

        while not found:
            ##print("Generating...")

            rad = random.randrange(min_radius, max_radius + 1)
            test_x = random.randrange(rad, screen_width + 1)
            test_y = random.randrange(rad, screen_height + 1)

            found = True
            i = 0
            #print("Checking collisions")
            for other in ret:
                #print("Check against #", i)
                good = do_not_overlap(
                    (other.x, other.y), (test_x, test_y), other.rad, rad
                )
                i += 1

                if not good:
                    found = False
                    #print("\n\n!!!!!!!!!!!!!!!!! Overlap detected\n\n")
                    break
                else:
                    #print("Is good")
                    pass

        #print("Found, appending result")
        #print("Obj", rad, test_x, test_y)
        ret.append(Body(rad, test_x, test_y, color))
        ret[-1].mass = minmass + ((maxmass - minmass) * rad / max_radius)

        #print("Drawing screen")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        for b in ret:
            b.draw()

        pygame.display.flip()

    #print("Leaving generation...")
    # input()
    return ret


def calc_forces(b):
    for i in range(len(b)):
        #print("\n\nUsing elem", i)
        #print("Mass", b[i].mass, "Center", b[i].x, b[i].y)

        for k in range(len(b)):
            if k == i:
                continue

            #print("Against", k)
            #print("Mass", b[k].mass, "Center", b[k].x, b[k].y)

            d = point_dist(b[i].x, b[i].y, b[k].x, b[k].y)
            #print("Distance", d)

            acc = gravitational_acceleration(
                b[i].mass,
                b[k].mass,
                np.array([b[i].x, b[i].y]),
                np.array([b[k].x, b[k].y]),
                G,
            )
            #print("Acceleration of body", i, acc)


            
            b[i].accel(acc[0] * TIMESTEP, acc[1] * TIMESTEP)

            #print("New velocity", b[i].vx, b[i].vy)

    #print("updating positions for timestep")
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
        
        reset_coll = True
        
        for k in range(len(b)):
            if k == i:
                continue

            if not do_not_overlap(
                (b[i].x, b[i].y), (b[k].x, b[k].y), b[i].rad, b[k].rad
            ):
                #print("Collided")
                reset_coll = False
                b[i].colliding +=1
                
                #print("Centering objects")
                #print("Before", b[i].x, b[i].y, b[k].x, b[k].y)
                b[i].x, b[i].y, b[k].x, b[k].y = separate_circles(b[i].x, b[i].y, b[i].rad, b[k].x, b[k].y, b[k].rad)
                #print("After", b[i].x, b[i].y, b[k].x, b[k].y)
                #input()
                
                if sorted([i, k]) in ind_fixed:
                    #print("Already fixed")
                    #print("Old distance", b[i].coll_distance[k])
                    nd = point_dist(b[i].x, b[i].y, b[k].x, b[k].y)
                    #print("New distance", nd)

                    if nd < b[i].coll_distance[k]:
                        #print("The object got closer, reverting")
                        # b[i].step_back()
                        # b[k].step_back()
                        pass
                    else:
                        #print("The objects are moving away")
                        pass

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
                    #print("New velocities", r)
                    tmp_dist = point_dist(b[i].x, b[i].y, b[k].x, b[k].y)
                    b[i].coll_distance[k] = tmp_dist
                    b[k].coll_distance[i] = tmp_dist   

        if(reset_coll):
            b[i].colliding = 0

    to_delete = []
    try:
        for i in range(len(ind_fixed)):
            if not (ind_fixed[i] in still_broken):
                to_delete.append(i)
    except:
        #print(ind_fixed)
        exit(1)

    tmplist = [a for b, a in enumerate(ind_fixed) if b not in to_delete]

    if found > 0:
        #print("Found collisions:", found)
        # input()
        pass

    return tmplist

control_queue = queue.Queue()

global control_window


def control_thread():
    SIM_PAUSED = threading.Lock()
    control_window = tk.Tk()
    control_window.title("Pygame Controls")
    tk_width=600
    control_window.geometry(str(tk_width)+"x400")
    
    def pause_sim():
        if not SIM_PAUSED.acquire(blocking=False):
            #print("Lock is currently busy, skipping acquisition")
            pass
        
        control_queue.put("paused")
        #print("Paused = ", SIM_PAUSED)
        
        
    def resume_sim():
        try:
            SIM_PAUSED.release()
        except RuntimeError:
            #print("Already unlocked")
            pass
        control_queue.put("resume")
        #print("Paused = ", SIM_PAUSED)
        

    
    button1 = tk.Button(control_window, text="||", width=5, height=2, font=("Arial", 16), bg="blue", fg="white", command=pause_sim)
    button1.grid(row=0, column=1)  # Place the button at row 0, column 1
    
    button2 = tk.Button(control_window, text=">", width=5, height=2, font=("Arial", 16), bg="blue", fg="white", command=resume_sim)
    button2.grid(row=0, column=2)  # Place the button at row 0, column 1

    entries = []
    
    def univ_modified(row, col):
        newdata = entries[row][col].get()
        print("Modified", row, col, newdata)
        
        if(col == 0):
            b[row-1].x = float(newdata)
        elif(col == 1):
            b[row-1].y = float(newdata)
        elif(col == 2):
            b[row-1].vx = float(newdata)
        elif(col == 3):
            b[row-1].vy = float(newdata)
        elif(col == 4):
            b[row-1].mass = float(newdata)
        elif(col == 5):
            b[row-1].radius = float(newdata)
        

    data = ["X", "Y", "vx", "vy", "m", "rad"]
    
    
    rows = BODIES_GEN+1
    cols = len(data)
    print("cols", cols)
    ideal_cell_width = ((tk_width + 100) // cols) // 10
    print(ideal_cell_width)
    
    
    for i in range(rows):
        tmp = []
        
        for j in range(cols):
            entry = tk.Entry(control_window, width=ideal_cell_width)
            entry.grid(row=i+1, column=j)
            entry.config(state="normal")
            entry.insert(0, "")
            tmp.append(entry)
            # Bind function to update data on edit
            if(i>0):
                entry.bind("<Return>", lambda event, row=i, col=j: univ_modified(row, col))
        
        entries.append(tmp)
            
    
    
    for i in range(cols):
        entries[0][i].insert(0, data[i])
        
    # Function to update cell value
    def update_cell(row, col, value):
        entries[row][col].delete(0, tk.END)
        entries[row][col].insert(0, value)
        
    def update_table():
        #print("update table")
        #print("Paused = ", SIM_PAUSED)
        
        row = 1
        for body in b:
            tmp = [round(body.x, 0), round(body.y,0), round(body.vx,1), round(body.vy,1), "{:.1e}".format(body.mass), round(body.radius, 1)]
            for col in range(len(tmp)):
                update_cell(row, col, tmp[col])
            row +=1

    while not tk_terminate.is_set():
        tk_terminate.wait(timeout=0.0)
        
        

        if not SIM_PAUSED.acquire(blocking=False):
            #print("Lock is currently busy, skipping acquisition")
            pass
        else:
            #print("Lock acquired, updating table")
            update_table()
            SIM_PAUSED.release()
            #print("Lock released table updated")

    
        
        
        

        control_window.update()
    

    control_window.destroy()

    

    control_window.mainloop()


pygame_terminate = False 
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)


tk_terminate = threading.Event() 
ct = threading.Thread(target=control_thread)
ct.start()


def pygame_termination_handler(sig, frame):
    global tk_terminate, pygame_terminate
    tk_terminate.set()  # Assuming you have a threading.Event object
    pygame_terminate = True  # Flag for the Pygame thread
    print("Setting tk_terminate", tk_terminate.is_set())
    
signal.signal(signal.SIGINT, pygame_termination_handler)



b = create_bodies(BODIES_GEN)


running = True
i = 0
tmp = []

masses = [x.mass for x in b]
new_calc = True
while not pygame_terminate:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame_terminate = True



    screen.fill(BLACK)

    for elem in b:
        elem.draw()

    pygame.display.flip()

    clock.tick(60)


    
    try:
        item = control_queue.get(block=False)
        if(item == "paused"):
            new_calc = False
            print("Pausing")
        elif(item == "resume"):
            new_calc = True
            print("Resuming")
        # Process the item:
    except queue.Empty:
        # Handle the case where the queue is empty (optional)
        pass
    
    if(new_calc):
        calc_forces(b)
        tmp = univ_collision(b, tmp)


pygame.quit()
