import pygame
import math

class Player:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.size = 50
        self.speed = 300

    def move(self, keys, dt, walls, world_width, world_height):
        dx, dy = 0, 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1

        length = math.hypot(dx, dy)
        if length != 0:
            dx /= length
            dy /= length

        # движение по X
        self.x += dx * self.speed * dt
        self._collide(walls, dx, 0)

        # движение по Y
        self.y += dy * self.speed * dt
        self._collide(walls, 0, dy)

        # ограничения
        self.x = max(0, min(self.x, world_width - self.size))
        self.y = max(0, min(self.y, world_height - self.size))

    def _collide(self, walls, dx, dy):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)

        for wall in walls:
            if rect.colliderect(wall.rect):
                if dx > 0:
                    self.x = wall.rect.left - self.size
                if dx < 0:
                    self.x = wall.rect.right
                if dy > 0:
                    self.y = wall.rect.top - self.size
                if dy < 0:
                    self.y = wall.rect.bottom

    def draw(self, screen, camera_x, camera_y):

        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (
                self.x - camera_x,
                self.y - camera_y,
                self.size,
                self.size
            )
        )
        screen_width, screen_height = screen.get_size()