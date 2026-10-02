
import pygame

from scenes.base_scene import Scene
from core.save_system import get_save_info, SLOT_COUNT


class SaveLoadScene(Scene):

    def __init__(self):
        self.selected = 0
        self.mode = "load"
        self.return_state = "menu"
        self.update_fonts()

    def update_fonts(self):
        screen = pygame.display.get_surface()
        height = screen.get_height()

        self.title_font = pygame.font.SysFont(None, int(height * 0.08))
        self.font = pygame.font.SysFont(None, int(height * 0.045))
        self.small = pygame.font.SysFont(None, int(height * 0.032))

    def open(self, mode, return_state):
        self.mode = mode
        self.return_state = return_state
        self.selected = 0

    def update(self, screen, keys, events, dt=None):
        width, height = screen.get_size()

        slot_rects = [
            pygame.Rect(width // 2 - 230, 160 + index * 115, 460, 90)
            for index in range(SLOT_COUNT)
        ]

        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return ("back", self.return_state)

                if event.key in (pygame.K_UP, pygame.K_w):
                    self.selected = (self.selected - 1) % SLOT_COUNT

                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected = (self.selected + 1) % SLOT_COUNT

                elif event.key == pygame.K_RETURN:
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

        title_text = "СОХРАНЕНИЕ ИГРЫ" if self.mode == "save" else "ЗАГРУЗКА ИГРЫ"
        title = self.title_font.render(title_text, True, (255, 255, 255))
        screen.blit(title, (width // 2 - title.get_width() // 2, 55))

        for index in range(SLOT_COUNT):
            slot = index + 1

            rect = pygame.Rect(
                width // 2 - 230,
                160 + index * 115,
                460,
                90
            )

            rect = slot_rects[index]

            color = (75, 75, 120) if index == self.selected else (40, 40, 65)
            pygame.draw.rect(screen, color, rect, border_radius=8)

            info = get_save_info(slot)

            name = self.font.render(f"Слот {slot}", True, (255, 255, 255))
            screen.blit(name, (rect.x + 20, rect.y + 12))

            if info:
                details = (
                    f"Уровень: {info['level']}   "
                    f"Локация: {info['location']}"
                )
                date = f"Сохранено: {info['saved_at']}"

                details_text = self.small.render(details, True, (200, 200, 200))
                date_text = self.small.render(date, True, (170, 170, 170))

                screen.blit(details_text, (rect.x + 20, rect.y + 43))
                screen.blit(date_text, (rect.x + 20, rect.y + 65))

            else:
                empty_text = self.small.render("Пустой слот", True, (160, 160, 160))
                screen.blit(empty_text, (rect.x + 20, rect.y + 48))

        hint = self.small.render(
            "Стрелки — выбор   ENTER — подтвердить   ESC — назад",
            True,
            (180, 180, 180)
        )

        screen.blit(
            hint,
            (width // 2 - hint.get_width() // 2, height - 45)
        )

        return "save_load"