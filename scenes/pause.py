import pygame

from scenes.base_scene import Scene
from core import controls
from localization.manager import tr
from UI.text import get_font, fit_text, draw_hint


class Pause(Scene):

    def update_fonts(self):
        screen = pygame.display.get_surface()
        height = screen.get_height()

        font_size_big = int(height * 0.08)
        font_size_small = int(height * 0.05)

        self.font = get_font(font_size_big)
        self.small = get_font(font_size_small)

    def __init__(self, battle_mode=False):

        self.update_fonts()
        self.battle_mode = battle_mode
        self.scene_name = "battle_pause" if battle_mode else "pause"
        self.return_state = "battle" if battle_mode else "game"
        self.confirm_action = None
        self.confirm_selected = 0

        self.up_keys = controls.UP
        self.down_keys = controls.DOWN

        self.buttons = [
            "resume",
            "save",
            "load",
            "settings",
            "menu"
        ]
        if battle_mode:
            self.buttons = ["resume", "surrender", "settings", "exit"]
        self.selected = 0

    def open(self):
        self.selected = 0
        self.confirm_action = None
        self.confirm_selected = 0

    def update(self, screen, keys, events, dt=None):

        # выбор и переход сцен
        for event in events:
            if event.type == pygame.KEYDOWN:

                if self.confirm_action:
                    if event.key in controls.BACK:
                        self.confirm_action = None
                        break
                    if event.key in self.up_keys + self.down_keys:
                        self.confirm_selected = 1 - self.confirm_selected
                    elif event.key in controls.CONFIRM:
                        action = self.confirm_action
                        self.confirm_action = None
                        if self.confirm_selected == 1:
                            if action == "surrender":
                                return ("battle_surrender",)
                            return "exit"
                        break
                    continue

                if event.key in controls.BACK:
                    return self.return_state

                if event.key in self.up_keys:
                    self.selected -= 1

                if event.key in self.down_keys:
                    self.selected += 1

                if self.selected < 0:
                    self.selected = len(self.buttons) - 1
                if self.selected >= len(self.buttons):
                    self.selected = 0

                if event.key in controls.CONFIRM:

                    selected_button = self.buttons[self.selected]

                    if selected_button == "resume":
                        return self.return_state

                    elif selected_button == "save":
                        return ("save_load", "save", "pause")

                    elif selected_button == "load":
                        return ("save_load", "load", "pause")

                    elif selected_button == "settings":
                        return ("settings", "battle" if self.battle_mode else "pause")

                    elif selected_button in ("surrender", "exit"):
                        self.confirm_action = selected_button
                        self.confirm_selected = 0
                        break

                    elif selected_button == "menu":
                        return "menu"

        # рендер
        screen.fill((10, 10, 40))

        width, height = screen.get_size()

        title_text = tr("pause.battle_title" if self.battle_mode else "pause.title")
        title = fit_text(self.font, title_text, (255, 255, 255), width - 40)
        screen.blit(title, (width // 2 - title.get_width() // 2, int(height * 0.12)))

        buttons = self.buttons
        selected = self.selected
        labels = {action: tr(f"pause.{action}") for action in self.buttons}
        if self.battle_mode:
            labels["resume"] = tr("pause.resume_battle")
        if self.confirm_action:
            question = tr(f"confirm.{self.confirm_action}")
            prompt = fit_text(self.small, question, (255, 200, 100), width - 40)
            screen.blit(prompt, (width // 2 - prompt.get_width() // 2, int(height * 0.26)))
            buttons = ["no", "yes"]
            labels = {action: tr(f"common.{action}") for action in buttons}
            selected = self.confirm_selected

        for i, btn in enumerate(buttons):

            color = (255, 255, 0) if i == selected else (200, 200, 200)

            text = fit_text(self.small, labels[btn], color, width - 40)

            x = width // 2 - text.get_width() // 2
            y = int(height * (0.38 + i * 0.09))
            screen.blit(text, (x, y))

        draw_hint(screen)
        return self.scene_name
