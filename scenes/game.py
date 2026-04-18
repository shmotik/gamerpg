from objects.player import Player
from world.location1 import Location1
import pygame

class Game:
    def __init__(self):
        self.player = Player()
        self.location = Location1()
        self.in_battle = False

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

            if not self.in_battle:
                self.in_battle = True

                # удалить врага
                self.location.enemies.remove(enemy)

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