import pygame

from objects.wall import Wall
from objects.npc import NPC
from objects.enemy import Enemy
from objects.items.item_drop import ItemDrop
from objects.items.database import get_potion


class Location1:
    def __init__(self):

        self.width = 2000
        self.height = 2000

        self.items = [
            ItemDrop(700, 300, get_potion())
        ]

        self.walls = [
            Wall(300, 200, 200, 50),
            Wall(100, 400, 400, 50)
        ]

        self.npcs = [
            NPC(500, 300)
        ]

        self.enemies = [
            Enemy(600, 200, "slime"),
            Enemy(800, 400, "goblin")
        ]

        self.exits = [
            {
                "rect": pygame.Rect(1900, 900, 100, 200),
                "target": "loc2",
                "spawn":(100, 900)
            }
        ]