import pygame

class ItemDrop:
    def __init__(self, x, y, item):
        self.item = item
        self.rect = pygame.Rect(x, y, 30, 30)

    def draw(self, screen, camera_x, camera_y):
        rect = pygame.Rect(
            self.rect.x - camera_x,
            self.rect.y - camera_y,
            self.rect.width,
            self.rect.height
        )

        pygame.draw.rect(screen, (255, 255, 0), rect)  # жёлтый квадратик