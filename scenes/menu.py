import pygame

from scenes.base_scene import Scene
from core import controls
from localization.manager import tr
from UI.text import get_font, fit_text, draw_hint


class Menu(Scene):

    def update_fonts(self):
        screen = pygame.display.get_surface()
        height = screen.get_height()

        font_size_big = int(height * 0.08)
        font_size_small = int(height * 0.05)

        self.font = get_font(font_size_big)
        self.small = get_font(font_size_small)

    def __init__(self):

        self.update_fonts()

        self.up_keys = controls.UP
        self.down_keys = controls.DOWN

        self.buttons = [
            "start",
            "load",
            "settings",
            "exit"
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
                    self.selected = len(self.buttons) - 1
                if self.selected >= len(self.buttons):
                    self.selected = 0

                if event.key in controls.BACK:
                    self.selected = self.buttons.index("exit")

                if event.key in controls.CONFIRM:

                    if self.buttons[self.selected] == "start":
                        self.switch_to("game")
                        return "game"

                    if self.buttons[self.selected] == "load":
                        return ("save_load", "load", "menu")

                    if self.buttons[self.selected] == "settings":
                        return ("settings", "menu")

                    if self.buttons[self.selected] == "exit":
                        self.switch_to("exit")
                        return "exit"

        # рендер
        screen.fill((20, 20, 20))

        width, height = screen.get_size()

        title = fit_text(self.font, tr("menu.title"), (255, 255, 255), width - 40)
        screen.blit(title, ((width - title.get_width()) // 2, int(height * 0.15)))

        for i, btn in enumerate(self.buttons):

            color = (255, 255, 0) if i == self.selected else (200, 200, 200)

            text = fit_text(self.small, tr(f"menu.{btn}"), color, width - 40)

            x = width // 2 - text.get_width() // 2
            y = int(height * (0.38 + i * 0.09))
            screen.blit(text, (x, y))
            

        draw_hint(screen)
        return "menu"
