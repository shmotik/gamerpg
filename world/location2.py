import pygame

from world.Baselocation import Baselocation
from objects.items.item_drop import ItemDrop
from objects.items.database import get_heavy_mace


class Location2(Baselocation):
    def __init__(self):
        super().__init__()

        self.items.append(
            ItemDrop(300, 900, get_heavy_mace(), "loc2_heavy_mace_1")
        )

        self.width = 2000
        self.height = 2000

        self.exits = [
            {
                "rect": pygame.Rect(0, 900, 100, 200),
                "target": "loc1",
                "spawn": (1800, 900)
            }
        ]