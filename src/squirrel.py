import random

class SquirrelClass:

    # position is tuple with x and y coordinates (0,0) is top left
    # direction is string with left, right, up or down

    def __init__(self, x_max, y_max, env, width, height):
        self.x_max = x_max
        self.y_max = y_max
        self.env=env
        self.width = width
        self.height = height
        self.spawn()
        print(f"Squirrel object created with position {self.pos}")

    def get_random_walkable_position(self):
        while True:
            x = random.randint(0, self.x_max)
            y = random.randint(0, self.y_max)
            if self.env.is_walkable((x, y), self.width, self.height):
                return (x, y)

    def spawn(self):
        self.pos = self.get_random_walkable_position()


    def jitter_walk(self):
        while True:
            x_jitter = random.randint(-5, 5) * 10
            y_jitter = random.randint(-5, 5) * 10

            new_x = self.pos[0] + x_jitter
            new_y = self.pos[1] + y_jitter

            new_x = max(0, min(new_x, self.x_max))
            new_y = max(0, min(new_y, self.y_max))

            if self.env.is_walkable((new_x, new_y), self.width, self.height):
                self.pos = (new_x, new_y)
                break


