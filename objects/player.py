import pygame
import math

class Player:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.size = 50
        self.speed = 300

    def move(self, keys, dt, walls):
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

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.size, self.size))