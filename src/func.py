from globals import *
from body import *

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

