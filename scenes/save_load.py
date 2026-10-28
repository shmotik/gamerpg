
import pygame

from scenes.base_scene import Scene
from core.save_system import get_save_info, SLOT_COUNT
from core import controls
from localization.manager import tr
from UI.text import get_font, fit_text, draw_hint


class SaveLoadScene(Scene):

    def __init__(self):
        self.selected = 0
        self.mode = "load"
        self.return_state = "menu"
        self.update_fonts()

    def update_fonts(self):
        screen = pygame.display.get_surface()
        height = screen.get_height()

        self.title_font = get_font(height * 0.06)
        self.font = get_font(height * 0.04)
        self.small = get_font(height * 0.028)

    def open(self, mode, return_state):
        self.mode = mode
        self.return_state = return_state
        self.selected = 0

    def update(self, screen, keys, events, dt=None):
        width, height = screen.get_size()

        card_width = min(width - 80, 700)
        slot_rects = [
            pygame.Rect((width - card_width) // 2, int(height * (0.25 + index * 0.19)),
                        card_width, int(height * 0.16))
            for index in range(SLOT_COUNT)
        ]

        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.key in controls.BACK:
                    return ("back", self.return_state)

                if event.key in controls.UP:
                    self.selected = (self.selected - 1) % SLOT_COUNT

                elif event.key in controls.DOWN:
                    self.selected = (self.selected + 1) % SLOT_COUNT

                elif event.key in controls.CONFIRM:
                    slot = self.selected + 1

                    if self.mode == "save":
                        return ("save", slot, self.return_state)

                    return ("load", slot, self.return_state)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for index, rect in enumerate(slot_rects):
                    if rect.collidepoint(event.pos):
                        self.selected = index

                        slot = index + 1

                        if self.mode == "save":
                            return ("save", slot, self.return_state)

                        return ("load", slot, self.return_state)

        screen.fill((15, 15, 35))

        title_text = tr("save.title" if self.mode == "save" else "load.title")
        title = fit_text(self.title_font, title_text, (255, 255, 255), width - 40)
        screen.blit(title, (width // 2 - title.get_width() // 2, 55))

        for index in range(SLOT_COUNT):
            slot = index + 1

            rect = slot_rects[index]

            color = (75, 75, 120) if index == self.selected else (40, 40, 65)
            pygame.draw.rect(screen, color, rect, border_radius=8)

            info = get_save_info(slot)

            name = fit_text(self.font, tr("save.slot", slot=slot), (255, 255, 255), rect.width - 40)
            screen.blit(name, (rect.x + 20, rect.y + 6))

            if info:
                details = tr("save.details", level=info['level'], location=info['location'])
                date = tr("save.date", date=info['saved_at'])

                details_text = fit_text(self.small, details, (200, 200, 200), rect.width - 40)
                date_text = fit_text(self.small, date, (170, 170, 170), rect.width - 40)

                screen.blit(details_text, (rect.x + 20, rect.y + int(rect.height * 0.43)))
                screen.blit(date_text, (rect.x + 20, rect.y + int(rect.height * 0.70)))

            else:
                empty_text = self.small.render(tr("save.empty"), True, (160, 160, 160))
                screen.blit(empty_text, (rect.x + 20, rect.y + 48))

        draw_hint(screen)

        return "save_load"
