import pygame
import random
import math

class AreaOfEffectSpell:
    def __init__(self, pos, radius, duration):
        self.pos = pos  # (x, y)
        self.radius = radius
        self.duration = duration
        self.age = 0
        self.sparkles = [self._random_sparkle() for _ in range(30)]
        self.color = (218, 112, 214)

    def _random_sparkle(self):
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(0, self.radius)
        x = self.pos[0] + math.cos(angle) * r
        y = self.pos[1] + math.sin(angle) * r
        return [x, y, random.randint(2, 5)]

    def update(self):
        self.age += 1
        if self.age % 5 == 0:  # Refresh sparkles occasionally
            self.sparkles = [self._random_sparkle() for _ in range(30)]
        return self.age < self.duration

    def is_fox_in_range(self, fox_pos):
        dx = fox_pos[0] - self.pos[0]
        dy = fox_pos[1] - self.pos[1]
        distance = math.sqrt(dx**2 + dy**2)
        return distance <= self.radius

    def draw(self, surface):
        # Pulsing transparency
        alpha = max(0, 180 - int((self.age / self.duration) * 180))
        pulse_radius = self.radius + math.sin(self.age * 0.2) * 5

        # Create a temporary surface for alpha blending
        temp_surface = pygame.Surface((self.radius*2 + 20, self.radius*2 + 20), pygame.SRCALPHA)
        temp_center = (temp_surface.get_width() // 2, temp_surface.get_height() // 2)

        # Draw core circle with transparency
        pygame.draw.circle(temp_surface, (*self.color, alpha), temp_center, int(pulse_radius))

        # Add sparkles
        for sparkle in self.sparkles:
            sx = sparkle[0] - self.pos[0] + temp_center[0]
            sy = sparkle[1] - self.pos[1] + temp_center[1]
            sparkle_color = (*self.color, random.randint(100, 200))
            pygame.draw.circle(temp_surface, sparkle_color, (int(sx), int(sy)), sparkle[2])

        # Blit with center alignment
        surface.blit(temp_surface, (self.pos[0] - temp_center[0], self.pos[1] - temp_center[1]))
