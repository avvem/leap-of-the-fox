import pygame
import random

class Environment:
    def __init__(self, grid_width, grid_height, grid_size, total_obstacles, min_blobs, max_blobs, buffer_radius=5):
        self.grid_width = grid_width            # number of grid cells horizontally
        self.grid_height = grid_height          # number of grid cells vertically
        self.grid_size = grid_size              # size of one tile in pixels ← MISSING
        self.total_obstacles = total_obstacles
        self.min_blobs = min_blobs
        self.max_blobs = max_blobs
        self.buffer_radius = buffer_radius
        self.obstacle_image_indices = {}  # New: maps obstacle grid_pos to a fixed image index
        self.obstacle_positions = set()
        self.generate()


    def _get_safe_zone(self, center_grid, radius=2):
        """Return grid positions around the player/NPC that should be free of obstacles."""
        safe_zone = set()
        cx, cy = center_grid
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                safe_zone.add((cx + dx, cy + dy))
        return safe_zone
    
    def is_valid_position(self, x, y):
        center_x, center_y = self.grid_width // 2, self.grid_height // 2
        distance = abs(x - center_x) + abs(y - center_y)
        return (
            0 <= x < self.grid_width and
            0 <= y < self.grid_height and
            distance > self.buffer_radius and
            (x, y) not in self.obstacle_positions
        )

    def generate_blob(self, start_x, start_y, size):
        blob_tiles = [(start_x, start_y)]
        self.obstacle_positions.add((start_x, start_y))
        self.obstacle_image_indices[(start_x, start_y)] = random.randint(0, 4)


        for _ in range(size - 1):
            base_x, base_y = random.choice(blob_tiles)
            offsets = [(-1, 0), (1, 0), (0, -1), (0, 1),
                       (-1, -1), (-1, 1), (1, -1), (1, 1)]

            random.shuffle(offsets)
            placed = False
            for dx, dy in offsets:
                nx, ny = base_x + dx, base_y + dy
                if self.is_valid_position(nx, ny):
                    self.obstacle_positions.add((nx, ny))
                    self.obstacle_image_indices[(nx, ny)] = random.randint(0, 4)
                    blob_tiles.append((nx, ny))
                    placed = True
                    break
            if not placed:
                # Can't place new tile near current blob tile, pick a new base next iteration
                continue

        return blob_tiles

    def generate(self):
        # Randomize number of blobs
        num_blobs = random.randint(self.min_blobs, self.max_blobs)
        base_blob_size = self.total_obstacles // num_blobs
        leftover = self.total_obstacles % num_blobs

        for i in range(num_blobs):
            blob_size = base_blob_size + (1 if i < leftover else 0)
            attempts = 0
            while attempts < 100:
                x = random.randint(0, self.grid_width - 1)
                y = random.randint(0, self.grid_height - 1)
                if self.is_valid_position(x, y):
                    self.generate_blob(x, y, blob_size)
                    break
                attempts += 1

    def _pixel_to_grid(self, pixel_pos):
        """Convert pixel position to grid coordinates."""
        px, py = pixel_pos
        return px // self.grid_size, py // self.grid_size  # use tile size here

    def _grid_to_pixel(self, grid_pos):
        """Convert grid position to pixel coordinates."""
        gx, gy = grid_pos
        return gx * self.grid_size, gy * self.grid_size  # use tile size here

    def draw(self, screen, rock_image_list, color=(100, 100, 100)):
        """Draw all obstacles to the screen."""
        for grid_pos in self.obstacle_positions:
            px, py = self._grid_to_pixel(grid_pos)
            # rect = pygame.Rect(px, py, self.grid_size, self.grid_size)  # width & height = tile size
            # pygame.draw.rect(screen, color, rect)
            index = self.obstacle_image_indices.get(grid_pos, 0)
            rock_image = rock_image_list[index]
            screen.blit(rock_image, (px, py))

    def is_walkable(self, pixel_pos, width, height):
        """
        Check if a rectangle at `pixel_pos` with given width and height
        collides with any obstacle tiles.
        """
        player_rect = pygame.Rect(pixel_pos[0], pixel_pos[1], width, height)

        for grid_pos in self.obstacle_positions:
            obs_x, obs_y = self._grid_to_pixel(grid_pos)
            obstacle_rect = pygame.Rect(obs_x, obs_y, self.grid_size, self.grid_size)
            
            if player_rect.colliderect(obstacle_rect):
                return False  # Collision detected

        return True  # No collision, space is walkable
