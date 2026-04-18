import pygame
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

class Settings:

    def __init__(self):
        self.font = pygame.font.SysFont(None, 50)

        self.up_keys = [pygame.K_UP, pygame.K_w]
        self.down_keys = [pygame.K_DOWN, pygame.K_s]

        self.resolutions = [
            (800, 600),
            (1024, 768),
            (1280, 720),
            (1600, 900)
        ]

        self.selected = 0

    def update(self, screen, keys, events):

        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.key in self.up_keys:
                    self.selected -= 1

                if event.key in self.down_keys:
                    self.selected += 1

                if self.selected < 0:
                    self.selected = len(self.resolutions) - 1
                if self.selected >= len(self.resolutions):
                    self.selected = 0

                if event.key == pygame.K_RETURN:
                    w, h = self.resolutions[self.selected]
                    return ("menu", (w, h))

                if event.key == pygame.K_ESCAPE:
                    return "menu"

        # render
        screen.fill((10, 10, 40))

        title = self.font.render("SETTINGS", True, (255, 255, 255))
        screen.blit(title, (300, 100))

        for i, res in enumerate(self.resolutions):

            color = (255, 255, 0) if i == self.selected else (200, 200, 200)

            text = self.font.render(f"{res[0]} x {res[1]}", True, color)
            screen.blit(text, (300, 200 + i * 50))

        return "settings"