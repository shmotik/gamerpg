import pygame

class QuestLogUI:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.SysFont(None, 26)

    def draw(self, screen):
        x = screen.get_width() - 300
        y = 20

        for quest in self.player.progress.quests:
            if quest.completed:
                continue

            text = quest.get_text(self.player.progress)

            lines = text.split(" | ")

            for line in lines:
                surf = self.font.render(line, True, (255, 255, 100))
                screen.blit(surf, (x, y))
                y += 25

            y += 10