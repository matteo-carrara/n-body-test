from globals import *

def point_dist(x1, y1, x2, y2):
    # Calculate the squared difference in x and y coordinates
    delta_x = (x2 - x1) ** 2
    delta_y = (y2 - y1) ** 2

    # Apply the Pythagorean theorem and return the distance
    distance = math.sqrt(delta_x + delta_y)
    return distance

class CircleHandle:
    def __init__(self):
        pass  # No attributes initialized here

    def draw(self, surface, center, radius, handle_offset, handle_radius, handle_color, line_color, line_thickness):
        self.center = center
        self.radius = radius
        self.handle_offset = handle_offset  # Distance of handle from center
        self.handle_radius = handle_radius
        self.handle_color = handle_color
        self.line_color = line_color
        self.line_thickness = line_thickness

        # Calculate handle position based on offset and direction (optional)
        handle_direction = (1, 0)  # Adjust for desired direction (e.g., up: (0, -1))
        handle_pos = (
            self.center[0] + handle_direction[0] * (self.radius + self.handle_offset),
            self.center[1] + handle_direction[1] * (self.radius + self.handle_offset)
        )

        # Draw handle circle and connecting line
        pygame.draw.circle(surface, handle_color, handle_pos, handle_radius)
        pygame.draw.line(
            surface, line_color, self.center, handle_pos, line_thickness
        )

    def is_clicked(self, mouse_pos):
        # Check collision with handle circle (consider handle_radius)
        handle_pos = (
            self.center[0] + self.handle_direction[0] * (self.radius + self.handle_offset),
            self.center[1] + self.handle_direction[1] * (self.radius + self.handle_offset)
        )
        distance = ((mouse_pos[0] - handle_pos[0])**2 + (mouse_pos[1] - handle_pos[1])**2)**0.5
        return distance <= self.handle_radius



class Body:
    coll_distance = {}  # first the index, then the distance
    skip = False
    mass = 0
    vx = 0
    vy = 0
    border = False
    border_cnt = 0
    colliding = 0
    MAX_HISTORY_SIZE = 600
    circle_history = []
    handle = CircleHandle()

    def add_to_history(self, new_value):
        """
        This function adds a new value to the circle_history list,
        keeping only the most recent MAX_HISTORY_SIZE elements.

        Args:
            circle_history: A list containing the circle history.
            new_value: The new value to add to the history.

        Returns:
            The updated circle_history list.
        """
        self.circle_history.append(new_value)  # Add the new value
        tmp = self.circle_history[-self.MAX_HISTORY_SIZE:]  # Return only the most recent elements
        self.circle_history = tmp


    def clear_trajectory(self):
        print("Clearing trjectory")
        self.circle_history = []
        

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
        
        for i in range(len(self.circle_history)-1):
            trail_c = self.color
            
            x = self.circle_history[i][0]
            y = self.circle_history[i][1]
            
            nx = self.circle_history[i+1][0]
            ny = self.circle_history[i+1][1]
            
            if(point_dist(x, y, self.x, self.y) < self.radius):
                trail_c = (70, 70, 70)
                
            pygame.draw.line(screen, trail_c, (x, y), (nx, ny), 1)
        
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

        mypos = (self.x, self.y)
        #print("center", mypos, "opposite", opposite)
        self.add_to_history(mypos)
        
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
