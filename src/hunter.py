import random
from projectile import Projectile

class HunterClass:

    # position is tuple with x and y coordinates (0,0) is top left
    # direction is string with left, right, up or down

    def __init__(self, x_max, y_max, step_length, bullet_speed, width, height):
        self.x_max = x_max
        self.y_max = y_max
        self.step_length = step_length
        self.spawn()
        self.attack_cooldown = random.randint(5, 20)  # Frames between attacks
        self.cooldown_counter = 0
        self.bullet_speed = bullet_speed
        self.width = width
        self.height = height
        print(f"Hunter object created with position {self.pos}")

    def spawn(self):
        spawn_edge = random.randint(1,4)
        if(spawn_edge == 1):
            self.pos = (0, random.randint(0, self.y_max))
        elif(spawn_edge == 2):
            self.pos = (self.x_max, random.randint(0, self.y_max))
        elif(spawn_edge == 3):
            self.pos = (random.randint(0, self.x_max), 0)
        elif(spawn_edge == 4):
            self.pos = (random.randint(0, self.x_max), self.y_max)


    def walk(self, fox_pos):
        fox_x, fox_y = fox_pos
        hunter_x, hunter_y = self.pos

        x_diff = fox_x - hunter_x
        y_diff = fox_y - hunter_y

        new_step_x = random.randint(-5,5)
        new_step_y = random.randint(-5,5)

        if((not x_diff == 0) and (not y_diff == 0)):
            if(abs(x_diff) >= abs(y_diff)):
                new_step_x += (x_diff / abs(x_diff)) * self.step_length
            else:
                new_step_y += (y_diff / abs(y_diff)) * self.step_length

        self.pos = (hunter_x + new_step_x, hunter_y + new_step_y)

    def attack(self, fox_pos, projectile_list):
        self.cooldown_counter += 1
        if self.cooldown_counter >= self.attack_cooldown:
            hunter_x, hunter_y = self.pos
            fox_x, fox_y = fox_pos

            # Calculate direction unit vector
            dx = fox_x - hunter_x
            dy = fox_y - hunter_y
            distance = max((dx ** 2 + dy ** 2) ** 0.5, 1)
            direction = (dx / distance, dy / distance)

            # Create and add projectile
            projectile = Projectile((hunter_x + (self.width // 2), hunter_y + (self.height // 2)), direction, self.bullet_speed)
            projectile_list.append(projectile)

            # Reset cooldown
            self.cooldown_counter = 0
            self.attack_cooldown = random.randint(5, 20)  # Next cooldown

            return True
        return False

