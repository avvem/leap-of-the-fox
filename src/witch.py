import random
import math
from aoe_spell import AreaOfEffectSpell

class WitchClass:
    def __init__(self, x_max, y_max, step_length, width, height, env, aoe_radius, duration):
        self.x_max = x_max
        self.y_max = y_max
        self.step_length = step_length
        self.attack_cooldown = random.randint(5, 20)
        self.cooldown_counter = 0
        self.width = width
        self.height = height
        self.env = env
        self.prev_positions = []
        self.max_prev_positions = 10  # Enough for window = 5
        self.aoe_radius = aoe_radius
        self.duration = duration
        self.teleport_trail = []  # List of (position, alpha)
        self.spawn()
        print(f"Witch object created with position {self.pos}")

    def spawn(self):
        while True:
            spawn_edge = random.randint(1, 4)
            if spawn_edge == 1:
                x = 0
                y = random.randint(0, self.y_max)
            elif spawn_edge == 2:
                x = self.x_max
                y = random.randint(0, self.y_max)
            elif spawn_edge == 3:
                x = random.randint(0, self.x_max)
                y = 0
            else:
                x = random.randint(0, self.x_max)
                y = self.y_max

            if self.env.is_walkable((x, y), self.width, self.height):
                self.pos = (x, y)
                break


    def walk(self, fox_pos):
        old_x = self.pos[0]
        old_y = self.pos[1]

        self.prev_positions.append(self.pos)
        if len(self.prev_positions) > self.max_prev_positions:
            self.prev_positions.pop(0)

        if random.random() < 0.02:  # ~2% chance to teleport randomly every frame
            success = False
            for _ in range(10):  # try up to 10 possible spots
                if not success:
                    offset_x = random.randint(-200, 200)
                    offset_y = random.randint(-200, 200)
                    new_x = fox_pos[0] + offset_x
                    new_y = fox_pos[1] + offset_y

                    if 0 <= new_x <= self.x_max and 0 <= new_y <= self.y_max:
                        if self.env.is_walkable((new_x, new_y), self.width, self.height):
                            self.pos = (new_x, new_y)
                            success = True
                    
                else:
                    steps = 20
                    x = old_x
                    y = old_y
                    dx = (new_x - x) // steps
                    dy = (new_y - y) // steps
                    for i in range(steps):
                        x += dx
                        y += dy

                        x = max(0, min(self.x_max, x))
                        y = max(0, min(self.y_max, y))
                        self.pos = (x, y)

                        # Store trail position with decreasing alpha
                        alpha = int(255 * (1 - i / steps))
                        self.teleport_trail.append(((x, y), alpha))
                    return
        else:
            # Float slowly toward the fox like levitating
            witch_x, witch_y = self.pos
            dx = fox_pos[0] - witch_x
            dy = fox_pos[1] - witch_y
            distance = math.hypot(dx, dy)
            if distance == 0:
                return

            direction = (dx / distance, dy / distance)
            new_x = witch_x + direction[0] * self.step_length * 0.5  # move slower
            new_y = witch_y + direction[1] * self.step_length * 0.5

            if self.env.is_walkable((new_x, new_y), self.width, self.height):
                self.pos = (new_x, new_y)


    def attack(self, fox_pos, aoe_list):
        self.cooldown_counter += 1
        if self.cooldown_counter >= self.attack_cooldown:

            offset_x = random.randint(-400, 400)
            offset_y = random.randint(-400, 400)
            new_x = fox_pos[0] + offset_x
            new_y = fox_pos[1] + offset_y
            
            aoe_spell = AreaOfEffectSpell((new_x, new_y), self.aoe_radius, self.duration)
            aoe_list.append(aoe_spell)

            self.cooldown_counter = 0
            self.attack_cooldown = random.randint(40, 100)
            return True
        return False

    def draw_teleport_trail(self, screen, pygame):
            for (x, y), alpha in self.teleport_trail:
                trail_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
                trail_surface.fill((218, 112, 214, alpha))  # Yellowish glow
                screen.blit(trail_surface, (x + 30, y + 30))  # Centered

            # Optionally clear older trail after rendering
            self.teleport_trail = [((x, y), alpha - 25) for (x, y), alpha in self.teleport_trail if alpha > 25]