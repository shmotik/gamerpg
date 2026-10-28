import pygame

from scenes.base_scene import Scene
from core import controls
from core.config import UserSettings, RESOLUTIONS, ZOOM_MIN, ZOOM_MAX, ZOOM_STEP
from localization.manager import tr, set_language, LANGUAGES, LANGUAGE_NAMES
from UI.text import get_font, fit_text, draw_hint


class Settings(Scene):
    def __init__(self, config=None):
        self.config = config if config is not None else UserSettings()
        self.resolutions = list(RESOLUTIONS)
        self.resolution_index = self.resolutions.index(tuple(self.config.data["resolution"]))
        self.zoom_min, self.zoom_max, self.zoom_step = ZOOM_MIN, ZOOM_MAX, ZOOM_STEP
        self.zoom = self.config.data["zoom"]
        self.language = self.config.data["language"]
        self.options = ["resolution", "zoom", "language", "back"]
        self.selected = 0
        self.resolution_left_rect = pygame.Rect(0, 0, 0, 0)
        self.resolution_right_rect = pygame.Rect(0, 0, 0, 0)
        self.zoom_slider_rect = pygame.Rect(0, 0, 0, 0)
        self.language_left_rect = pygame.Rect(0, 0, 0, 0)
        self.language_right_rect = pygame.Rect(0, 0, 0, 0)
        self.back_rect = pygame.Rect(0, 0, 0, 0)
        self.update_fonts()

    def update_fonts(self):
        screen = pygame.display.get_surface()
        height = screen.get_height() if screen else 600
        self.title_font = get_font(height * 0.06)
        self.font = get_font(height * 0.038)
        self.small_font = get_font(height * 0.028)

    def set_zoom_from_mouse(self, mouse_x):
        if self.zoom_slider_rect.width <= 0:
            return
        ratio = (mouse_x - self.zoom_slider_rect.x) / self.zoom_slider_rect.width
        value = self.zoom_min + max(0, min(1, ratio)) * (self.zoom_max - self.zoom_min)
        self.zoom = round(round(value / self.zoom_step) * self.zoom_step, 2)
        self.zoom = max(self.zoom_min, min(self.zoom, self.zoom_max))

    def change_value(self, direction):
        option = self.options[self.selected]
        if option == "resolution":
            self.resolution_index = (self.resolution_index + direction) % len(self.resolutions)
            value = self.resolutions[self.resolution_index]
        elif option == "zoom":
            self.zoom = round(max(self.zoom_min, min(
                self.zoom_max, self.zoom + direction * self.zoom_step
            )), 2)
            value = self.zoom
        elif option == "language":
            index = (LANGUAGES.index(self.language) + direction) % len(LANGUAGES)
            self.language = LANGUAGES[index]
            set_language(self.language)
            value = self.language
        else:
            return None
        self.config.set(option, value)
        return (f"apply_{option}", value)

    def update(self, screen, keys, events, settings_from):
        # Вычисляем области кликов также на первом кадре нового разрешения.
        self.layout(screen)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in controls.BACK or event.key in controls.CONFIRM:
                    return ("back", settings_from)
                if event.key in controls.UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key in controls.DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key in controls.LEFT:
                    return self.change_value(-1)
                elif event.key in controls.RIGHT:
                    return self.change_value(1)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, option, direction in (
                    (self.resolution_left_rect, 0, -1),
                    (self.resolution_right_rect, 0, 1),
                    (self.language_left_rect, 2, -1),
                    (self.language_right_rect, 2, 1),
                ):
                    if rect.collidepoint(event.pos):
                        self.selected = option
                        return self.change_value(direction)
                if self.zoom_slider_rect.collidepoint(event.pos):
                    self.selected = 1
                    self.set_zoom_from_mouse(event.pos[0])
                    self.config.set("zoom", self.zoom)
                    return ("apply_zoom", self.zoom)
                if self.back_rect.collidepoint(event.pos):
                    return ("back", settings_from)
        self.draw(screen)
        return None

    def layout(self, screen):
        width, height = screen.get_size()
        resolution_y = int(height * 0.29)
        language_y = int(height * 0.67)
        self.resolution_left_rect = pygame.Rect(width // 2 - 200, resolution_y, 45, 40)
        self.resolution_right_rect = pygame.Rect(width // 2 + 155, resolution_y, 45, 40)
        self.language_left_rect = pygame.Rect(width // 2 - 200, language_y, 45, 40)
        self.language_right_rect = pygame.Rect(width // 2 + 155, language_y, 45, 40)
        self.zoom_slider_rect = pygame.Rect(width // 2 - 200, int(height * 0.48), 400, 24)
        self.back_rect = pygame.Rect(width // 2 - 150, int(height * 0.82), 300, 45)

    def draw(self, screen):
        self.layout(screen)
        width, height = screen.get_size()
        screen.fill((10, 10, 40))
        title = fit_text(self.title_font, tr("settings.title"), (255, 255, 255), width - 40)
        screen.blit(title, ((width - title.get_width()) // 2, int(height * 0.07)))
        for index, option in enumerate(self.options):
            color = (255, 255, 0) if self.selected == index else (255, 255, 255)
            key = "common.back" if option == "back" else f"settings.{option}"
            text = fit_text(self.font, tr(key), color, width - 40)
            y = self.back_rect.y if option == "back" else int(height * (0.21 + index * 0.19))
            screen.blit(text, ((width - text.get_width()) // 2, y))
        resolution = self.resolutions[self.resolution_index]
        for value, left, right in (
            (f"{resolution[0]} x {resolution[1]}", self.resolution_left_rect, self.resolution_right_rect),
            (LANGUAGE_NAMES[self.language], self.language_left_rect, self.language_right_rect),
        ):
            text = fit_text(self.font, value, (230, 230, 230), 290)
            screen.blit(text, ((width - text.get_width()) // 2, left.y))
            screen.blit(self.font.render("<", True, (255, 255, 255)), left.topleft)
            screen.blit(self.font.render(">", True, (255, 255, 255)), right.topleft)
        pygame.draw.line(screen, (120, 120, 120),
                         self.zoom_slider_rect.midleft, self.zoom_slider_rect.midright, 6)
        ratio = (self.zoom - self.zoom_min) / (self.zoom_max - self.zoom_min)
        pygame.draw.circle(screen, (255, 255, 0), (
            self.zoom_slider_rect.x + int(ratio * self.zoom_slider_rect.width),
            self.zoom_slider_rect.centery
        ), 9)
        text = self.small_font.render(f"{self.zoom:.2f}x", True, (255, 255, 255))
        screen.blit(text, ((width - text.get_width()) // 2, self.zoom_slider_rect.bottom + 2))
        if self.config.save_error:
            text = fit_text(self.small_font, tr("settings.save_error"), (255, 120, 100), width - 40)
            screen.blit(text, ((width - text.get_width()) // 2, height - 70))
        draw_hint(screen, "hint.settings")
