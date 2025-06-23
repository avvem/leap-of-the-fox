class FoxClass:

    # position is tuple with x and y coordinates (0,0) is top left
    # direction is string with left, right, up or down

    def __init__(self, position, direction, step_length, jump_length, x_max, y_max, latest_horizontal, stamina, health, jump_stamina):
        self.pos = position
        self.dir = direction
        self.step_length = step_length
        self.jump_length = jump_length
        self.x_max = x_max
        self.y_max = y_max
        self.latest_horizontal = latest_horizontal
        self.stamina = stamina
        self.health = health
        self.jump_stamina = jump_stamina
        self.jump_trail = []  # List of (position, alpha)
        print(f"Fox object created with position {self.pos} and direction {self.dir}. Step length {self.step_length}.")

    def handle_movement(self, keys_pressed, pygame):
        dir_x = 0
        dir_y = 0

        if keys_pressed[pygame.K_a]:  # left
            dir_x = -1
            self.latest_horizontal = "left"
        if keys_pressed[pygame.K_d]:  # right
            dir_x = 1
            self.latest_horizontal = "right"
        if keys_pressed[pygame.K_w]:  # up
            dir_y = -1
        if keys_pressed[pygame.K_s]:  # down
            dir_y = 1

        if dir_x != 0 or dir_y != 0:
            self.set_direction(dir_x, dir_y)
            self.walk(self.dir)

    def set_direction(self, dx, dy):
        if dx == -1 and dy == -1:
            self.dir = "up-left"
        elif dx == 1 and dy == -1:
            self.dir = "up-right"
        elif dx == -1 and dy == 1:
            self.dir = "down-left"
        elif dx == 1 and dy == 1:
            self.dir = "down-right"
        elif dx == -1:
            self.dir = "left"
        elif dx == 1:
            self.dir = "right"
        elif dy == -1:
            self.dir = "up"
        elif dy == 1:
            self.dir = "down"

    
    def walk(self, direction):
        x, y = self.pos

        if direction == "left":
            x = max(0, x - self.step_length)
            self.latest_horizontal = "left"
        elif direction == "right":
            x = min(self.x_max, x + self.step_length)
            self.latest_horizontal = "right"
        elif direction== "up":
            y = max(0, y - self.step_length)
        elif direction == "down":
            y = min(self.y_max, y + self.step_length)
        elif direction == "up-left":
            x = max(0, x - self.step_length)
            y = max(0, y - self.step_length)
            self.latest_horizontal = "left"
        elif direction == "up-right":
            x = min(self.x_max, x + self.step_length)
            y = max(0, y - self.step_length)
            self.latest_horizontal = "right"
        elif direction == "down-left":
            x = max(0, x - self.step_length)
            y = min(self.y_max, y + self.step_length)
            self.latest_horizontal = "left"
        elif direction == "down-right":
            x = min(self.x_max, x + self.step_length)
            y = min(self.y_max, y + self.step_length)
            self.latest_horizontal = "right"
        else:
            print(f"Unknown direction: {self.dir}")
            return

        self.pos = (x, y)
        self.dir = direction

    def jump(self, jump_sound):
        if self.stamina < self.jump_stamina:
            return False

        dx, dy = self.get_direction_vector()
        steps = 20
        step_size = self.jump_length / steps

        x, y = self.pos

        for i in range(steps):
            x += dx * step_size
            y += dy * step_size

            x = max(0, min(self.x_max, x))
            y = max(0, min(self.y_max, y))
            self.pos = (x, y)

            # Store trail position with decreasing alpha
            alpha = int(255 * (1 - i / steps))
            self.jump_trail.append(((x, y), alpha))

        self.stamina -= self.jump_stamina
        jump_sound.play()
        return True

    def draw_jump_trail(self, screen, pygame):
        for (x, y), alpha in self.jump_trail:
            trail_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
            trail_surface.fill((255, 180, 100, alpha))  # Yellowish glow
            screen.blit(trail_surface, (x + 30, y + 30))  # Centered

        # Optionally clear older trail after rendering
        self.jump_trail = [((x, y), alpha - 25) for (x, y), alpha in self.jump_trail if alpha > 25]

    def get_direction_vector(self):
        direction_map = {
            "left": (-1, 0),
            "right": (1, 0),
            "up": (0, -1),
            "down": (0, 1),
            "up-left": (-1, -1),
            "up-right": (1, -1),
            "down-left": (-1, 1),
            "down-right": (1, 1)
        }

        dx, dy = direction_map.get(self.dir, (0, 0))

        # Normalize diagonals to keep speed consistent
        if dx != 0 and dy != 0:
            norm = (2 ** 0.5)
            dx /= norm
            dy /= norm

        return dx, dy


    def stamina_recovery(self, stamina_recovery, max_stamina):
        self.stamina = min(self.stamina + stamina_recovery, max_stamina)

    def hit(self):
        self.health -= 10