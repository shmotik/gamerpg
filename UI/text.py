"""Общие шрифты и размещение коротких надписей интерфейса."""

import pygame
from localization.manager import tr


def get_font(size):
    # Эти системные шрифты содержат кириллицу; последний резерв — шрифт Pygame.
    return pygame.font.SysFont("segoeui,dejavusans,arial", max(12, int(size)))


def fit_text(font, text, color, max_width):
    surface = font.render(text, True, color)
    if surface.get_width() > max_width:
        ratio = max_width / surface.get_width()
        surface = pygame.transform.smoothscale(
            surface, (max(1, int(max_width)), max(1, int(surface.get_height() * ratio)))
        )
    return surface


def draw_hint(screen, key="hint.menu"):
    width, height = screen.get_size()
    font = get_font(min(22, height * 0.03))
    text = fit_text(font, tr(key), (180, 180, 180), width - 40)
    screen.blit(text, ((width - text.get_width()) // 2, height - text.get_height() - 12))
