import pygame

from objects.wall import Wall
from objects.npc.npc import NPC
from objects.enemies.enemy import Enemy
from objects.enemies.enemy_types import ENEMY_TYPES
from objects.items.item_drop import ItemDrop
from objects.items.database import get_potion
from objects.items.database import get_sword
from systems.quest import Quest, KillObjective
from systems.rewards import RewardSkill
from systems.skills.skill_list import POISON_STRIKE


class Location1:
    def __init__(self):

        quest = Quest(
            "Помощь алхимику",
            objectives=[KillObjective("slime", 5)],
            rewards=[RewardSkill(POISON_STRIKE)]
        )

        self.width = 2000
        self.height = 2000

        self.items = [
            ItemDrop(700, 300, get_potion()),
            ItemDrop(700, 400, get_sword())
        ]

        self.walls = [
            Wall(300, 200, 200, 50),
            Wall(100, 400, 400, 50)
        ]

        self.npcs = [
            NPC(500, 300, "Привет, помоги мне...", quest)
        ]

        self.enemies = []

        enemy = Enemy(600, 200, ENEMY_TYPES["slime"], self)
        enemy.load_animation("assets/images/enemies/slime/slime_jump.gif")
        self.enemies.append(enemy)

        enemy = Enemy(400, 300, ENEMY_TYPES["goblin"], self)
        #enemy.load_animation("assets/images/enemies/goblin/goblin_attack.gif")
        self.enemies.append(enemy)

        self.exits = [
            {
                "rect": pygame.Rect(1900, 900, 100, 200),
                "target": "loc2",
                "spawn":(100, 900)
            }
        ]

        