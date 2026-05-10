import pygame
import math

from objects.stats import Stats
from objects.player.inventory import Inventory
from objects.player.player_progress import PlayerProgress
from systems.skills.skill_list import POWER_STRIKE

class Player:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.size = 50
        self.speed = 300

        self.spawn_point = (self.x, self.y)

        self.stats = Stats(
            hp=100, 
            attack_values=[8, 10, 12], 
            defense=3,
            speed=2,
            extra_stats={
                "luck":2,
                "alchemy":1,
                "smithing":0
            }
        )

        self.equipment = {
            "weapon": None,
            "armor": None
        }

        self.inventory = Inventory()
        self.progress = PlayerProgress()
        self.stats.progress = self.progress
        self.progress.player = self

        self.skills = [POWER_STRIKE]

    @property
    def hp(self):
        return self.stats.hp

    @property
    def max_hp(self):
        return self.stats.max_hp

    @property
    def mana(self):
        return self.stats.mana

    @property
    def max_mana(self):
        return self.stats.max_mana


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

    def equip_item(self, item):
        slot = item.slot.lower()

        if slot not in self.equipment:
            return f"Нельзя экипировать в слот: {slot}"

        old_item = self.equipment[slot]

        # снять старый
        if old_item and hasattr(old_item, "stat_bonus"):
            for stat, val in old_item.stat_bonus.items():
                self.stats.remove_bonus(stat, val)

        # надеть новый
        self.equipment[slot] = item

        if hasattr(item, "stat_bonus"):
            for stat, val in item.stat_bonus.items():
                self.stats.add_bonus(stat, val)

        return f"Экипировано: {item.name}"

    def unequip_item(self, slot):
        item = self.equipment.get(slot)

        if not item:
            return "Нечего снимать"

        if hasattr(item, "stat_bonus"):
            for stat, val in item.stat_bonus.items():
                self.stats.remove_bonus(stat, val)

        self.equipment[slot] = None

        return f"Снято: {item.name}"

    def set_spawn(self, x, y):
        self.spawn_point = (x, y)

    def respawn(self):
        self.x, self.y = self.spawn_point
        self.stats.reset()
        self.stats.mana = self.stats.max_mana