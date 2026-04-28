import pygame
import random
import copy
import os

class Enemy:
    def __init__(self, x, y, enemy_type):
        self.spawn_x = x
        self.spawn_y = y

        self.x = float(x)
        self.y = float(y)

        self.rect = pygame.Rect(x, y, 40, 40)

        self.data = enemy_type
        self.type = enemy_type.name

        self.stats = copy.deepcopy(enemy_type.stats)

        self.alive = True
        self.respawn_timer = 0

        self.dir_x = 0
        self.dir_y = 0
        self.move_timer = 0
        self.speed = 50 #пик/сек

        self.image = pygame.image.load(
            os.path.join("assets", "images", "enemies", f"{self.type}.png")
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40,40))

    def draw(self, screen, camera_x, camera_y):
        if not self.alive:
            return

        x = self.rect.x - camera_x
        y = self.rect.y - camera_y

        screen.blit(self.image, (x,y))

        rect = pygame.Rect(
            self.rect.x - camera_x,
            self.rect.y - camera_y,
            self.rect.width,
            self.rect.height
        )

    def update(self, dt, walls):
        if self.alive:
            self.move(dt, walls)

            if not self.stats.is_alive():
                self.die()
            
        else:
            self.respawn_timer -=dt
            if self.respawn_timer <=0:
                self.respawn()

    def move(self, dt, walls):
        self.move_timer -= dt

        if self.move_timer <= 0:
            self.dir_x = random.choice([-1, 0, 1])
            self.dir_y = random.choice([-1, 0, 1])
            self.move_timer = random.uniform(1, 3)

        length = (self.dir_x**2 + self.dir_y**2) ** 0.5
        if length != 0:
            dx = self.dir_x / length
            dy = self.dir_y / length
        else:
            dx, dy = 0, 0

        new_x = self.x + dx * self.speed * dt
        new_y = self.y + dy * self.speed * dt

        test_rect = pygame.Rect(int(new_x), int(new_y), self.rect.width, self.rect.height)
        collide = False
        for wall in walls:
            if test_rect.colliderect(wall.rect):
                collide = True
                break

        if not collide:
            self.x = new_x
            self.y = new_y

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def die(self):
        self.alive = False
        self.respawn_timer = 5

    def respawn(self):
        self.alive = True
        self.stats.reset()

        self.rect.x = self.spawn_x
        self.rect.y = self.spawn_y