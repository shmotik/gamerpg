import pygame

class BattleLog:
    def __init__(self):
        self.lines = []
        self.font = pygame.font.SysFont(None, 28)

    def add(self, text):
        self.lines.append(text)

        if len(self.lines) > 6:
            self.lines.pop(0)

    def draw(self, screen):
        x = 20
        y = screen.get_height() - 200

        for line in self.lines:
            surf = self.font.render(line, True, (255, 100, 100))
            screen.blit(surf, (x, y))
            y += 30