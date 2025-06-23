class Projectile:
    def __init__(self, pos, direction, speed):
        self.pos = list(pos)  # Convert tuple to list
        self.direction = direction
        self.speed = speed
        

    def move(self):
        dx, dy = self.direction
        self.pos[0] += dx * self.speed
        self.pos[1] += dy * self.speed
