class Explosion:
    def __init__(self, position, pygame):
        self.position = position
        self.frame = 0
        self.max_frame = 8
        self.pygame = pygame

    def draw(self, screen):
        if self.frame < self.max_frame:
            radius = 10 + self.frame * 4
            alpha = max(0, 255 - self.frame * 40)
            explosion_surface = self.pygame.Surface((radius*2, radius*2), self.pygame.SRCALPHA)
            self.pygame.draw.circle(explosion_surface, (255, 50, 0, alpha), (radius, radius), radius)
            screen.blit(explosion_surface, (self.position[0] - radius, self.position[1] - radius))
            self.frame += 1
            return True  # Still animating
        return False  # Done
