class MuzzleFlash:
    def __init__(self, position, pygame):
        self.position = position
        self.frame = 0
        self.max_frame = 5
        self.pygame = pygame

    def draw(self, screen):
        if self.frame < self.max_frame:  # Only show for a few frames
            alpha = max(0, 255 - self.frame * 40)
            self.pygame.draw.circle(screen, (255, 255, 255, alpha), self.position, 8 + self.frame * 2)  # Expanding flash
            self.frame += 1
            return True
        return False
