import pygame

from objects.wall import Wall
from objects.npc import NPC
from objects.enemies.enemy import Enemy
from objects.items.item_drop import ItemDrop
from objects.items.database import get_potion





class Baselocation:
    def __init__(self):

        self.walls = []
        self.enemies = []
        self.npcs = []
        self.items = []