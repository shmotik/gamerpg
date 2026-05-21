import pygame
from scenes.base_scene import Scene

class QuestMenu(Scene):

    def __init__(self, player):
        self.player = player
        self.font = pygame.font.SysFont(None, 36)

    def update(self, screen, keys, events, dt):

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                    return "game"

        self.draw(screen)
        return "quest_menu"

    def draw(self, screen):
        screen.fill((20, 20, 40))

        y = 50

        for quest in self.player.progress.quests:

            title = self.font.render(quest.name, True, (255,255,0))
            screen.blit(title, (50, y))
            y += 40

            text = quest.get_text(self.player.progress)

            for line in text.split(" | "):
                t = self.font.render(line, True, (255,255,255))
                screen.blit(t, (70, y))
                y += 30

            y += 20