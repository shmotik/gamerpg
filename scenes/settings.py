import pygame
import os

from scenes.base_scene import Scene

os.environ['SDL_VIDEO_CENTERED'] = '1'

class Settings(Scene):

    def update_fonts(self):
        height = pygame.display.get_surface().get_height()
        fonts_size = int(height * 0.06)
        self.fonts = pygame.font.SysFont(None, fonts_size)

    def __init__(self):

        self.update_fonts()

        self.up_keys = [pygame.K_UP, pygame.K_w]
        self.down_keys = [pygame.K_DOWN, pygame.K_s]

        self.resolutions = [
            (800, 600),
            (1024, 768),
            (1280, 720),
            (1600, 900)
        ]

        self.selected = 0

    def update(self, screen, keys, events, dt=None):

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
                    return ("apply", (w, h))

                if event.key == pygame.K_ESCAPE:
                    return "close"

        # render
        width, height = screen.get_size()

        screen.fill((10, 10, 40))

        title = self.fonts.render("SETTINGS", True, (255, 255, 255))
        x = width // 2 - title.get_width() // 2
        screen.blit(title, (x, 80))

        for i, res in enumerate(self.resolutions):

            color = (255, 255, 0) if i == self.selected else (200, 200, 200)

            text = self.fonts.render(f"{res[0]} x {res[1]}", True, color)
            
            x = width // 2 - text.get_width() // 2
            y = height // 2 - 100 + i * 50

            screen.blit(text, (x, y))

        return None