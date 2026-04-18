from objects.wall import Wall
from objects.npc import NPC
from objects.enemy import Enemy

class Location1:
    def __init__(self):

        self.walls = [
            Wall(300, 200, 200, 50),
            Wall(100, 400, 400, 50)
        ]

        self.npcs = [
            NPC(500, 300)
        ]

        self.enemies = [
            Enemy(600, 200)
        ]