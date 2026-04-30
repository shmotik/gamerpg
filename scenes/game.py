from objects.player.player import Player
from world.locations import LOCATIONS
from world.location1 import Location1
from scenes.base_scene import Scene
from objects.stats import Stats
from scenes.battle import Battle
from UI.message_log import MessageLog

import pygame



class Game(Scene):

    def __init__(self):
        self.player = Player()
        self.location = Location1()
        self.in_battle = False
        self.messages = MessageLog()

    def update_fonts(self):        
        screen = pygame.display.get_surface()
        height = screen.get_height()

        size_big = int(height * 0.08)
        size_small = int(height * 0.05)

        self.font = pygame.font.SysFont(None, size_big)
        self.small = pygame.font.SysFont(None, size_small)

        self.messages.set_font(self.small)

    def update(self, screen, keys, events, dt):
        self.messages.update(dt)

        # камера
        screen_width, screen_height = screen.get_size()

        camera_x = self.player.x - screen_width // 2
        camera_y = self.player.y - screen_height // 2

        camera_x = max(0, camera_x)
        camera_y = max(0, camera_y)

        camera_x = min(camera_x, self.location.width - screen_width)
        camera_y = min(camera_y, self.location.height - screen_height)

        player_rect = pygame.Rect(self.player.x, self.player.y, 32, 32)

        # дроп
        for item in self.location.items[:]:
            if player_rect.colliderect(item.rect):
                self.player.inventory.add(item.item)
                self.location.items.remove(item)
                self.messages.add(f'Вы получили: {item.item.name}')

        # движение игрока
        self.player.move(keys, dt, self.location.walls, self.location.width, self.location.height)
        
        self.player.x = max(0, min(self.player.x, self.location.width - self.player.size))
        self.player.y = max(0, min(self.player.y, self.location.height - self.player.size))

        # события
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "pause"
                if event.key == pygame.K_i:
                    return ("inventory", self.player, self.messages)

        #столкновение с врагом
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.size, self.player.size)

        for enemy in self.location.enemies:

            enemy.update(dt, self.location.walls)

            if enemy.alive and player_rect.colliderect(enemy.rect):

                if not self.in_battle:
                    self.in_battle = True

                    self.current_enemy = enemy
                    return ("battle", enemy.stats, self.messages)

        for exit in self.location.exits:
            if player_rect.colliderect(exit["rect"]):

                self.location = LOCATIONS[exit["target"]]()
                self.player.x, self.player.y = exit["spawn"]

                break
        
        # рендер
        screen.fill((0, 0, 0))

        for wall in self.location.walls:
            wall.draw(screen, camera_x, camera_y)

        for enemy in self.location.enemies:
            enemy.draw(screen, camera_x, camera_y)

        for npc in self.location.npcs:
            npc.draw(screen, camera_x, camera_y)

        for item in self.location.items:
            item.draw(screen, camera_x, camera_y)

        self.player.draw(screen, camera_x, camera_y)

        for exit in self.location.exits:
            pygame.draw.rect(
                screen,
                (0, 0, 255),
                (
                    exit["rect"].x - camera_x,
                    exit["rect"].y - camera_y,
                    exit["rect"].width,
                    exit["rect"].height
                )
            )

        bar_width = 200
        bar_height = 20

        hp_ratio = self.player.stats.hp / self.player.stats.max_hp
        current_width = int(bar_width * hp_ratio)

        # фон (серый)
        pygame.draw.rect(screen, (60, 60, 60), (10, 40, bar_width, bar_height))

        # здоровье (красный)
        pygame.draw.rect(screen, (200, 50, 50), (10, 40, current_width, bar_height))
        
        hp_text = f"HP: {self.player.stats.hp} / {self.player.stats.max_hp}"
        text_surface = self.small.render(hp_text, True, (255, 50, 50))
        screen.blit(text_surface, (10, 10))

        xp_bar_width = 200
        xp_bar_height = 10

        xp = self.player.progress.xp
        xp_next = self.player.progress.xp_to_next()

        xp_ratio = xp / xp_next if xp_next > 0 else 0
        xp_current_width = int(xp_bar_width * xp_ratio)

        # фон
        pygame.draw.rect(screen, (50, 50, 80), (10, 65, xp_bar_width, xp_bar_height))

        # XP
        pygame.draw.rect(screen, (50, 150, 255), (10, 65, xp_current_width, xp_bar_height))

        # текст уровня
        lvl_text = f"LVL {self.player.progress.level}"
        lvl_surface = self.small.render(lvl_text, True, (100, 200, 255))
        screen.blit(lvl_surface, (220, 55))
        
        self.messages.draw(screen)

        return "game"

    def on_enemy_killed(self, enemy):
        enemy_type = enemy.data

        #  опыт
        xp = enemy_type.xp
        leveled = self.player.progress.add_xp(xp)

        self.messages.add(f"+{xp} XP", color=(100, 200, 255))

        if leveled:
            self.messages.add("Уровень повышен!", color=(255, 255, 0))

        #  дроп (заготовка)
        for drop_func, chance in enemy_type.drops:
            import random
            if random.random() <= chance:
                item = drop_func()
                self.player.inventory.add(item)
                self.messages.add(f"Выпал предмет: {item.name}")