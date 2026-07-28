import pygame
import random
import copy
import os
import heapq

from objects.enemies.combat_ai import CombatAI
from core.utils import load_gif

class Enemy:
    def __init__(self, x, y, enemy_type, location):
        self.spawn_x = x
        self.spawn_y = y

        self.combat_ai = CombatAI(self)

        self.location = location

        self.path = []
        self.path_timer = 0

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

        self.ai_type = enemy_type.ai_type
        self.wander_timer = 0

        self.image = pygame.image.load(
            os.path.join("assets", "images", "enemies", f"{self.type}", f"{self.type}.png")
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40,40))

        self.last_seen_pos = None
        self.memory_timer = 0   

        self.frames = []
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = 0.1
        self.direction = "right"

    def draw(self, screen, camera_x, camera_y):
        if not self.alive:
            return

        x = self.rect.x - camera_x
        y = self.rect.y - camera_y

        if self.frames:
            image = self.frames[self.anim_index]

            if self.direction == "left":
                image = pygame.transform.flip(image, True, False)

            screen.blit(image, (x, y))
        else:
            screen.blit(self.image, (x, y))

    def update(self, dt, walls):
        if self.alive:
            self.move(dt, walls)

            # направление
            if self.dir_x > 0:
                self.direction = "right"
            elif self.dir_x < 0:
                self.direction = "left"

            # анимация
            if self.frames:
                self.anim_timer += dt
                if self.anim_timer > self.anim_speed:
                    self.anim_timer = 0
                    self.anim_index = (self.anim_index + 1) % len(self.frames)

            if not self.stats.is_alive():
                self.die()

        else:
            self.respawn_timer -= dt
            if self.respawn_timer <= 0:
                self.respawn()

    def move(self, dt, walls):

        length = (self.dir_x**2 + self.dir_y**2) ** 0.5
        if length != 0:
            dx = self.dir_x / length
            dy = self.dir_y / length
        else:
            dx, dy = 0, 0

        # движение по X
        new_x = self.x + dx * self.speed * dt
        rect_x = pygame.Rect(int(new_x), int(self.y), self.rect.width, self.rect.height)

        map_w = self.location.width
        map_h = self.location.height

        collide_x = any(rect_x.colliderect(wall.rect) for wall in walls)
        if not collide_x:
            self.x = max(0, min(new_x, map_w - self.rect.width))

        # движение по Y
        new_y = self.y + dy * self.speed * dt
        rect_y = pygame.Rect(int(self.x), int(new_y), self.rect.width, self.rect.height)

        collide_y = any(rect_y.colliderect(wall.rect) for wall in walls)
        if not collide_y:
            self.y = max(0, min(new_y, map_h - self.rect.height))

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

    def update_ai(self, player, dt, walls):
        if not self.alive:
            return

        dist = self.distance_to_player(player)

        if self.ai_type == "aggressive":
            self._ai_aggressive(player, dist, dt, walls)

        elif self.ai_type == "wander":
            self._ai_wander(dt)

        elif self.ai_type == "coward":
            self._ai_coward(player, dist, dt)

    def _ai_aggressive(self, player, dist, dt, walls):

        AGRO_RADIUS = 400
        MEMORY_TIME = 3

        can_see = self.can_see_player(player, walls)

        # обновляем память
        if dist < AGRO_RADIUS and can_see:
            self.last_seen_pos = (player.x, player.y)
            self.memory_timer = MEMORY_TIME

        elif self.memory_timer > 0:
            self.memory_timer -= dt
        else:
            self.last_seen_pos = None

        # если есть цель → строим путь
        if self.last_seen_pos:

            self.path_timer -= dt
            if self.path_timer <= 0:
                tx, ty = self.last_seen_pos
                self.path = self.find_path(tx, ty, walls)
                self.path_timer = 0.5

            if self.path and len(self.path) > 0:
                cell = 40
                gx, gy = self.path[0]
                tx, ty = self.to_world(gx, gy, cell)

                dx = tx - self.x
                dy = ty - self.y

                length = (dx**2 + dy**2) ** 0.5

                if length < 5:
                    self.path.pop(0)
                else:
                    self.dir_x = dx / length
                    self.dir_y = dy / length
            else:
                # если путь не найден — идём напрямую (но аккуратно)
                dx = self.last_seen_pos[0] - self.x
                dy = self.last_seen_pos[1] - self.y

                length = (dx**2 + dy**2) ** 0.5
                if length != 0:
                    self.dir_x = dx / length
                    self.dir_y = dy / length

        else:
            self._ai_wander(dt)

    def _ai_wander(self, dt):

        self.wander_timer -= dt

        if self.wander_timer <= 0:
            self.dir_x = random.choice([-1, 0, 1])
            self.dir_y = random.choice([-1, 0, 1])
            self.wander_timer = random.uniform(1, 3)

    def _ai_coward(self, player, dist, dt):

        FEAR_RADIUS = 120

        if dist < FEAR_RADIUS:
            dx = self.x - player.x
            dy = self.y - player.y

            length = (dx**2 + dy**2) ** 0.5
            if length != 0:
                dx /= length
                dy /= length

            self.dir_x = dx 
            self.dir_y = dy 
        else:
            self._ai_wander(dt)

    def distance_to_player(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        return (dx**2 + dy**2) ** 0.5

    def can_see_player(self, player, walls):

        steps = 20  # чем больше — тем точнее

        for i in range(steps + 1):
            t = i / steps

            x = self.x + (player.x - self.x) * t
            y = self.y + (player.y - self.y) * t

            point_rect = pygame.Rect(int(x), int(y), 2, 2)

            for wall in walls:
                if point_rect.colliderect(wall.rect):
                    return False

        return True

    def to_grid(self, x, y, cell_size):
        return int(x // cell_size), int(y // cell_size)

    def to_world(self, gx, gy, cell_size):
        return gx * cell_size + cell_size // 2, gy * cell_size + cell_size // 2
    
    def is_blocked(self, gx, gy, walls, cell_size):

        rect = pygame.Rect(
            gx * cell_size,
            gy * cell_size,
            cell_size,
            cell_size
        )

        for wall in walls:
            if rect.colliderect(wall.rect):
                return True

        return False

    def find_path(self, target_x, target_y, walls):

        cell = 40

        start = self.to_grid(self.x, self.y, cell)
        goal = self.to_grid(target_x, target_y, cell)

        open_set = []
        heapq.heappush(open_set, (0, start))

        came_from = {}
        g_score = {start: 0}

        def heuristic(a, b):
            return abs(a[0]-b[0]) + abs(a[1]-b[1])

        MAX_ITER = 500
        iterations = 0

        while open_set:
            iterations += 1
            if iterations > MAX_ITER:
                return []

            _, current = heapq.heappop(open_set)

            if current == goal:
                break

            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                neighbor = (current[0]+dx, current[1]+dy)

                if self.is_blocked(neighbor[0], neighbor[1], walls, cell):
                    continue

                tentative = g_score[current] + 1

                if neighbor not in g_score or tentative < g_score[neighbor]:
                    g_score[neighbor] = tentative
                    priority = tentative + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (priority, neighbor))
                    came_from[neighbor] = current

        # восстановление пути
        path = []
        current = goal

        while current in came_from:
            path.append(current)
            current = came_from[current]

        path.reverse()
        return path

    def load_animation(self, path):
        self.frames = load_gif(path)

    



