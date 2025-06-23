import random
import math
from projectile import Projectile

class HunterClass:
    def __init__(self, x_max, y_max, step_length, bullet_speed, width, height, env):
        self.x_max = x_max
        self.y_max = y_max
        self.step_length = step_length
        self.attack_cooldown = random.randint(5, 20)
        self.cooldown_counter = 0
        self.bullet_speed = bullet_speed
        self.width = width
        self.height = height
        self.env = env
        self.prev_positions = []
        self.max_prev_positions = 10  # Enough for window = 5
        self.spawn()
        # print(f"Hunter object created with position {self.pos}")

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

    @staticmethod
    def distance(p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def is_stuck(self, threshold=10, window=5):
        """Check if average movement over recent frames is low enough to consider the hunter stuck."""
        if len(self.prev_positions) < window + 1:
            return False

        distances = [
            self.distance(self.prev_positions[i], self.prev_positions[i + 1])
            for i in range(-window - 1, -1)
        ]
        avg_distance = sum(distances) / len(distances)
        # print(f"[Hunter] Average movement distance: {avg_distance:.2f}")
        return avg_distance < threshold

    def walk(self, fox_pos):
        fox_x, fox_y = fox_pos
        hunter_x, hunter_y = self.pos

        x_diff = fox_x - hunter_x
        y_diff = fox_y - hunter_y

        x_dir = 1 if x_diff > 0 else -1 if x_diff < 0 else 0
        y_dir = 1 if y_diff > 0 else -1 if y_diff < 0 else 0

        step = self.step_length

        self.prev_positions.append(self.pos)
        if len(self.prev_positions) > self.max_prev_positions:
            self.prev_positions.pop(0)

        stuck = self.is_stuck(threshold=10, window=5)
        
        candidate_moves = []
        randomness_fact = 3

        if stuck:
            # print("[Hunter] Detected stuck — triggering escape behavior.")
            # Try large random moves to escape stuck state
            for _ in range(5):
                dx = random.randint(-1, 1) * step * 5
                dy = random.randint(-1, 1) * step * 5
                candidate_moves.append((dx, dy))
        else:
            # Normal walk with mild randomness
            if x_dir != 0 and y_dir != 0:
                candidate_moves.append((
                    x_dir * step + random.randint(-1, 1) * randomness_fact,
                    y_dir * step + random.randint(-1, 1) * randomness_fact
                ))
            if x_dir != 0:
                candidate_moves.append((
                    x_dir * step + random.randint(-1, 1) * randomness_fact,
                    random.randint(-1, 1) * randomness_fact
                ))
            if y_dir != 0:
                candidate_moves.append((
                    random.randint(-1, 1) * randomness_fact,
                    y_dir * step + random.randint(-1, 1) * randomness_fact
                ))

            # Try alternate and side-step moves
            candidate_moves.extend([
                (-x_dir * step, y_dir * step),
                (x_dir * step, -y_dir * step),
                (-x_dir * step, 0),
                (0, -y_dir * step)
            ])

        # Apply first valid move
        for dx, dy in candidate_moves:
            new_x = max(0, min(hunter_x + dx, self.x_max))
            new_y = max(0, min(hunter_y + dy, self.y_max))
            if self.env.is_walkable((new_x, new_y), self.width, self.height):
                self.pos = (new_x, new_y)
                return

    def attack(self, fox_pos, projectile_list):
        self.cooldown_counter += 1
        if self.cooldown_counter >= self.attack_cooldown:
            hunter_x, hunter_y = self.pos
            fox_x, fox_y = fox_pos

            dx = fox_x - hunter_x
            dy = fox_y - hunter_y
            distance = max((dx ** 2 + dy ** 2) ** 0.5, 1)
            direction = (dx / distance, dy / distance)

            projectile = Projectile(
                (hunter_x + (self.width // 2), hunter_y + (self.height // 2)),
                direction,
                self.bullet_speed
            )
            projectile_list.append(projectile)

            self.cooldown_counter = 0
            self.attack_cooldown = random.randint(5, 20)

            return True
        return False
