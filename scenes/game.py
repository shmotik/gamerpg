from objects.player import Player
from objects.wall import Wall
from objects.npc import NPC
from objects.enemy import Enemy
from world.location1 import Location1
import pygame

class Game:
    def __init__(self):
        self.player = Player()

        self.location = Location1()

    def update(self, screen, keys, events, dt):

        # движение игрока
        self.player.move(keys, dt, self.location.walls)

        # события
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "pause"

        #столкновение с врагом
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.size, self.player.size)

        for enemy in self.location.enemies:
            if player_rect.colliderect(enemy.rect):
                return "battle"

        # рендер
        screen.fill((0, 0, 0))

        for wall in self.location.walls:
            wall.draw(screen)

        for enemy in self.location.enemies:
            enemy.draw(screen)

        for npc in self.location.npcs:
            npc.draw(screen)

        self.player.draw(screen)

        return "game"