from objects.player.player import Player
from world.locations import LOCATIONS
from world.location1 import Location1
from scenes.base_scene import Scene
from objects.enemies.enemy_types import ENEMY_TYPES
from objects.stats import Stats
from scenes.battle import Battle

import pygame



class Game(Scene):

    def __init__(self):
        self.player = Player()
        self.location = Location1()
        self.in_battle = False

    def update_fonts(self):
        screen = pygame.display.get_surface()
        height = screen.get_height()

        size_big = int(height * 0.08)
        size_small = int(height * 0.05)

        self.font = pygame.font.SysFont(None, size_big)
        self.small = pygame.font.SysFont(None, size_small)

    def update(self, screen, keys, events, dt):

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
                print(f"picked up {item.item.name}")

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
                    return "inventory"

        #столкновение с врагом
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.size, self.player.size)

        for enemy in self.location.enemies:
            if player_rect.colliderect(enemy.rect):

                if not self.in_battle:
                    self.in_battle = True

                    enemy_data = ENEMY_TYPES[enemy.type]

                    self.battle_enemy_stats = Stats(
                        enemy_data.stats.max_hp,
                        enemy_data.stats.attack_values,
                        enemy_data.stats.defense
                    )

                    # удалить врага
                    self.current_enemy = enemy

                    return ("battle", self.battle_enemy_stats)

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

        return "game"