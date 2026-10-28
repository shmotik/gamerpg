import pygame
from UI.text import get_font, fit_text

class BattleLog:
    def __init__(self):
        self.lines = []
        self.font = get_font(22)

    def add(self, text):
        self.lines.append(text)

        if len(self.lines) > 6:
            self.lines.pop(0)

    def draw(self, screen, area=None):
        area = area or pygame.Rect(20, screen.get_height() - 240, screen.get_width() - 40, 200)
        x, y = area.topleft
        line_height = max(20, area.height // 6)

        for line in self.lines:
            surf = fit_text(self.font, line, (255, 100, 100), area.width)
            screen.blit(surf, (x, y))
            y += line_height
