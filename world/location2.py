import pygame

from world.Baselocation import Baselocation





class Location2(Baselocation):
    def __init__(self):
        super().__init__()

        self.width = 2000
        self.height = 2000

        self.exits = [
            {
                "rect": pygame.Rect(0, 900, 100, 200),
                "target": "loc1",
                "spawn": (1800, 900)
            }
        ]