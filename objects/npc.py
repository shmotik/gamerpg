import pygame

class NPC:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)