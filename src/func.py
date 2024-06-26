from globals import *
from body import *

import numpy as np
from math import pow

def ke(m, vx, vy):
    #print("KE CALCULATING WITH m", m, "vx", vx, "vy", vy)
    return 1/2*m*(pow(vx,2) + pow(vy,2))


def elastic_collision_2d(m1, v1x, v1y, m2, v2x, v2y):
    """
    Calculates the final velocities after an elastic collision in 2D.

    Args:
        m1 (float): Mass of the first object.
        v1x (float): Initial x-velocity of the first object.
        v1y (float): Initial y-velocity of the first object.
        m2 (float): Mass of the second object.
        v2x (float): Initial x-velocity of the second object.
        v2y (float): Initial y-velocity of the second object.

    Returns:
        tuple: A tuple containing the final x and y velocities of both objects (v1fx, v1fy, v2fx, v2fy).
    """

    # Combined momentum in x and y directions
    p_x = m1 * v1x + m2 * v2x
    p_y = m1 * v1y + m2 * v2y

    # Apply conservation of momentum to find final velocities
    v1fx = (p_x - m2 * v2x) / (m1 + m2)
    v1fy = (p_y - m2 * v2y) / (m1 + m2)
    v2fx = (p_x + m1 * v1x) / (m1 + m2)
    v2fy = (p_y + m1 * v1y) / (m1 + m2)

    return v1fx, v1fy, v2fx, v2fy


def get_velocity(m, E_k, vx_sample=0.0, vy_sample=0.0):
    """
    This function calculates the velocities vx and vy of an object with mass m
    given its expected kinetic energy E_k. It assumes equal distribution
    of kinetic energy in the x and y directions. It also scales the output
    velocities based on the ratio of the provided sample velocity (vx_sample, vy_sample).

    Args:
        m: mass of the object
        E_k: expected kinetic energy of the object
        vx_sample: sample velocity in the x direction (default: 0.0)
        vy_sample: sample velocity in the y direction (default: 0.0)

    Returns:
        vx: scaled velocity in the x direction
        vy: scaled velocity in the y direction
    """

    # Calculate the ideal speed based on kinetic energy
    v_ideal = math.sqrt(2 * E_k / m)
    total_v = vx_sample+vy_sample
    
    if(total_v != 0):
        vx = vx_sample/total_v *v_ideal
        vy = vy_sample/total_v *v_ideal
    else:
        vx = v_ideal /2
        vy = v_ideal / 2

    return vx, vy

def elastic_collision(m1, v1x, v1y, m2, v2x, v2y):
    """
    This function performs an elastic collision in 2D for two points with masses and velocities.

    Args:
        m1: Mass of the first point.
        v1x: x-component of the velocity of the first point.
        v1y: y-component of the velocity of the first point.
        m2: Mass of the second point.
        v2x: x-component of the velocity of the second point.
        v2y: y-component of the velocity of the second point.

    Returns:
        v1x_new, v1y_new, v2x_new, v2y_new: The new x and y components of the velocities for both points after the collision.
    """
    k1 = ke(m1, v1x, v1y)
    k2 = ke(m2, v2x, v2y)
    kt = k1 + k2
    v1 = (0,)
    v2 = v1

    #print("V2", v2x, v2y, "V1", v1x, v1y)
    if (abs(v2x)+abs(v2y))>0:
        v1 = get_velocity(m1, k2, v2x, v2y)
    else:
        v1 = (0, 0)
    
    if (abs(v1x)+abs(v1y))>0:
        v2 = get_velocity(m2, k1, v1x, v1y)
    else:
        v2 = (0, 0)
    
    #print("returning", v1+v2)
    return v1+v2



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

    v1fx, v1fy, v2fx, v2fy = elastic_collision(mass1, velocity1x, velocity1y, mass2, velocity2x, velocity2y)

    #print("Elastic collision")

    oldk = (ke(mass1, velocity1x, velocity1y), ke(mass2, velocity2x, velocity2y))
    newk = (ke(mass1, v1fx, v1fy), ke(mass2, v2fx, v2fy))
    
    print("Masses", mass1, mass2, "Ratio", mass1/mass2)
    print("Original velocity:", velocity1x, velocity1y, "/", velocity2x, velocity2y)
    print("New values", v1fx, v1fy, "/", v2fx, v2fy)
    print("KE before",oldk[0] , "/", oldk[1], "sum = ", sum(oldk))
    print("KE after", newk[0]  ,"/", newk[1], "sum = ", sum(newk) )
    #input()
    
    return v1fx, v1fy, v2fx, v2fy





def draw_axes(screen, width, height, offset, color=(0, 0, 0), tick_size=20, label_distance=15):
    """
    Draws X and Y axes with tickmarks, numbers, and arrows on the Pygame screen.

    Args:
        screen: The Pygame screen surface.
        width: The width of the screen.
        height: The height of the screen.
        color: The color of the axes (default black).
        tick_size: The size of the tick marks (default 10 pixels).
        label_distance: The distance between the axis and the labels (default 5 pixels).
    """
    # Draw X-axis
    #print("Height",  height // 2)
    pygame.draw.line(screen, color,
                     (0, int((height // 2)+offset[1])),
                     (width,int((height // 2)+offset[1])),
                    2)

    # Draw Y-axis
    pygame.draw.line(screen, color,
                     ( int((width // 2)+offset[0]), 0),
                     (int((width // 2)+offset[0]), height),
                    2)

    tickmarks = False
    # Draw tick marks and labels on X-axis
    for i in range(1, width // tick_size + 1):
        if(not tickmarks):
            break 
        
        x = i * tick_size
        pygame.draw.line(
            screen,
            color,
            (x, height // 2 - tick_size // 2),
            (x, height // 2 + tick_size // 2),
            1,
        )
        
        # Draw label (avoid drawing at the end)
        if i != width // tick_size:
            label_surface = pygame.font.Font(None, 15).render(
                str(i * tick_size), True, color
            )
            screen.blit(
                label_surface,
                (x - label_surface.get_width() // 2, height // 2 + label_distance),
            )

    # Draw tick marks and labels on Y-axis
    for i in range(1, height // tick_size + 1):
        if(not tickmarks):
            break

        y = i * tick_size
        pygame.draw.line(
            screen,
            color,
            (width // 2 - tick_size // 2, y),
            (width // 2 + tick_size // 2, y),
            1,
        )
        # Draw label (avoid drawing at the end)
        if i != height // tick_size:
            label_surface = pygame.font.Font(None, 15).render(
                str(i * tick_size), True, color
            )
            screen.blit(
                label_surface,
                (
                    width // 2 - label_surface.get_width() - label_distance,
                    y - label_surface.get_height() // 2,
                ),
            )

    # Draw arrows at the end of axes
    arrow_size = 10
    pygame.draw.polygon(
        screen,
        color,
        [
            (width - arrow_size, height // 2 - arrow_size // 2),
            (width, height // 2),
            (width - arrow_size, height // 2 + arrow_size // 2),
        ],
        2,
    )




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
    minmass = MIN_MASS
    maxmass = MAX_MASS
    ret = []

    for i in range(num):
        found = False
        c = random.randrange(64, 256)
        
        color = (
            random.randrange(64, 256),
            random.randrange(64, 256),
            random.randrange(64, 256),
        )
        
        if(COLOR_PALETTE == "scientific"):
            color = (c, c, c)
        

        while not found:
            rad = random.randrange(min_radius, max_radius + 1)
            test_x = random.randrange(rad, screen_width + 1)
            test_y = random.randrange(rad, screen_height + 1)

            found = True
            
            for other in ret:
                good = do_not_overlap((other.x, other.y), (test_x, test_y), other.rad, rad)

                if not good:
                    found = False
                    break
            
        ret.append(Body(rad, test_x, test_y, color))
        ret[-1].mass = minmass + ((maxmass - minmass) * rad / max_radius)

    return ret


def calc_forces(b):

        
    for i in range(len(b)):
        if (not GRAVITY_ENABLED):
            break
        
        for k in range(len(b)):
            if k == i:
                continue

            d = point_dist(b[i].x, b[i].y, b[k].x, b[k].y)

            acc = gravitational_acceleration(
                b[i].mass,
                b[k].mass,
                np.array([b[i].x, b[i].y]),
                np.array([b[k].x, b[k].y]),
                G,
            )


            
            b[i].accel(acc[0] * TIMESTEP, acc[1] * TIMESTEP)

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


def is_click_in_circle(mouse_x, mouse_y, center_x, center_y, radius):
    """
    Checks if a mouse click at (mouse_x, mouse_y) is within a circle centered at (center_x, center_y) with radius 'radius'.

    Args:
        mouse_x: X-coordinate of the mouse click.
        mouse_y: Y-coordinate of the mouse click.
        center_x: X-coordinate of the circle's center.
        center_y: Y-coordinate of the circle's center.
        radius: Radius of the circle.

    Returns:
        True if the click is within the circle, False otherwise.
    """
    # Calculate distance between click and center
    distance = ((mouse_x - center_x) ** 2 + (mouse_y - center_y) ** 2) ** 0.5

    # Check if distance is less than or equal to radius
    return distance <= radius

def smooth_mouse_data(mouse_data, window_size):
    """
    Applies a simple moving average filter to smooth mouse movement data.

    Args:
        mouse_data: A list of dictionaries containing mouse position and timestamp.
            Each dictionary should have keys 'x', 'y', and 'timestamp'.
        window_size: The size of the smoothing window (number of samples to average).

    Returns:
        A new list of dictionaries with smoothed X and Y positions.
    """

    if len(mouse_data) < window_size:
        return mouse_data  # Not enough data for smoothing

    smoothed_data = []
    for i in range(len(mouse_data)):
        # Get window of data (consider edge cases)
        start_index = max(0, i - window_size + 1)
        window_data = mouse_data[start_index : i + 1]

        # Calculate average X and Y positions within the window
        average_x = sum(sample["x"] for sample in window_data) / len(window_data)
        average_y = sum(sample["y"] for sample in window_data) / len(window_data)

        # Create new entry with smoothed positions and original timestamp
        smoothed_data.append(
            {"x": average_x, "y": average_y, "timestamp": mouse_data[i]["timestamp"]}
        )

    return smoothed_data


def get_drag_acceleration(raw_mouse_data, max_acceleration):
    """
    Calculates acceleration based on a list of historical mouse movements.

    Args:
        mouse_data: A list of dictionaries containing mouse position and timestamp.
            Each dictionary should have keys 'x', 'y', and 'timestamp'.
        max_acceleration: Maximum acceleration limit (positive value).

    Returns:
        A tuple containing the final X and Y acceleration values.
    """

    if len(raw_mouse_data) < 4:
        print("Missing data")
        return 0, 0  # Not enough data for acceleration
    
    mouse_data = smooth_mouse_data(raw_mouse_data, 4)

    print("len mouse data", len(mouse_data), "raw data", len(raw_mouse_data))

    # Get recent samples (consider adjusting window size)
    window_size = 5  # Experiment with this value for smoothness
    
    if(window_size >= len(mouse_data)):
        window_size = len(mouse_data)
        
    recent_data = mouse_data[-window_size:]
    print("len mouse data", len(mouse_data), "len recent data", len(recent_data))

    # Calculate total time difference
    total_time_delta = abs(recent_data[0]['timestamp'] - recent_data[-1]['timestamp'])
    #print("Times", recent_data[0]['timestamp'], recent_data[-1]['timestamp'])
    #print("Time delta", total_time_delta)
    if total_time_delta <= 0:
        print("Time delta 0")
        return 0, 0  # No time difference
        

    # Calculate average movement (delta)
    average_delta_x = 0
    average_delta_y = 0
    for i in range(1, len(recent_data)):
        delta_x = recent_data[i]['x'] - recent_data[i - 1]['x']
        delta_y = recent_data[i]['y'] - recent_data[i - 1]['y']
        average_delta_x += delta_x
        average_delta_y += delta_y

    average_delta_x /= (window_size - 1)
    average_delta_y /= (window_size - 1)

    # Normalize movement vector (avoid division by zero)
    if abs(average_delta_x) + abs(average_delta_y) > 0:
        movement_norm = (average_delta_x ** 2 + average_delta_y ** 2) ** 0.5
        average_delta_x /= movement_norm
        average_delta_y /= movement_norm

    # Scale movement to desired acceleration considering total time difference
    acceleration_x = (average_delta_x / total_time_delta) * max_acceleration
    acceleration_y = (average_delta_y / total_time_delta) * max_acceleration

    return acceleration_x, acceleration_y

