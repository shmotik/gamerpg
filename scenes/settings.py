import pygame
import os

from scenes.base_scene import Scene


os.environ["SDL_VIDEO_CENTERED"] = "1"


class Settings(Scene):

    def __init__(self):

        self.resolutions = [
            (800, 600),
            (1024, 768),
            (1280, 720),
            (1600, 900)
        ]

        self.resolution_index = 0

        # -------------------------
        # ZOOM КАМЕРЫ
        # -------------------------

        self.zoom_min = 0.75
        self.zoom_max = 1.50
        self.zoom_step = 0.05
        self.zoom = 1.00

        self.selected = 0

        self.resolution_left_rect = pygame.Rect(0, 0, 0, 0)
        self.resolution_right_rect = pygame.Rect(0, 0, 0, 0)
        self.zoom_slider_rect = pygame.Rect(0, 0, 0, 0)
        self.back_rect = pygame.Rect(0, 0, 0, 0)

        self.update_fonts()

    # ==================================================
    # ШРИФТЫ
    # ==================================================

    def update_fonts(self):

        screen = pygame.display.get_surface()

        if screen:
            height = screen.get_height()
        else:
            height = 600

        self.title_font = pygame.font.SysFont(
            None,
            int(height * 0.08)
        )

        self.font = pygame.font.SysFont(
            None,
            int(height * 0.05)
        )

        self.small_font = pygame.font.SysFont(
            None,
            int(height * 0.035)
        )

    # ==================================================
    # ZOOM ОТ МЫШИ
    # ==================================================

    def set_zoom_from_mouse(self, mouse_x):

        ratio = (
            mouse_x - self.zoom_slider_rect.x
        ) / self.zoom_slider_rect.width

        ratio = max(0.0, min(1.0, ratio))

        self.zoom = (
            self.zoom_min
            + ratio * (
                self.zoom_max - self.zoom_min
            )
        )

        self.zoom = round(
            self.zoom / self.zoom_step
        ) * self.zoom_step

        self.zoom = max(
            self.zoom_min,
            min(self.zoom, self.zoom_max)
        )

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self, screen, keys, events, settings_from):

        for event in events:

            # ------------------------------------------
            # КЛАВИАТУРА
            # ------------------------------------------

            if event.type == pygame.KEYDOWN:

                # ESC
                if event.key == pygame.K_ESCAPE:
                    return ("back", settings_from)

                # Вверх / вниз
                if event.key == pygame.K_UP:
                    self.selected -= 1

                elif event.key == pygame.K_DOWN:
                    self.selected += 1

                self.selected = max(
                    0,
                    min(self.selected, 2)
                )

                # --------------------------------------
                # РАЗРЕШЕНИЕ
                # --------------------------------------

                if self.selected == 0:

                    if event.key == pygame.K_LEFT:

                        self.resolution_index -= 1

                        if self.resolution_index < 0:
                            self.resolution_index = (
                                len(self.resolutions) - 1
                            )

                    elif event.key == pygame.K_RIGHT:

                        self.resolution_index += 1

                        if self.resolution_index >= len(
                            self.resolutions
                        ):
                            self.resolution_index = 0

                    elif event.key == pygame.K_RETURN:

                        return (
                            "apply_resolution",
                            self.resolutions[
                                self.resolution_index
                            ]
                        )

                # --------------------------------------
                # ZOOM
                # --------------------------------------

                elif self.selected == 1:

                    if event.key == pygame.K_LEFT:

                        self.zoom -= self.zoom_step

                    elif event.key == pygame.K_RIGHT:

                        self.zoom += self.zoom_step

                    self.zoom = max(
                        self.zoom_min,
                        min(self.zoom, self.zoom_max)
                    )

                    self.zoom = round(
                        self.zoom / self.zoom_step
                    ) * self.zoom_step

                    if event.key == pygame.K_RETURN:

                        return (
                            "apply_zoom",
                            self.zoom
                        )

                # --------------------------------------
                # НАЗАД
                # --------------------------------------

                elif self.selected == 2:

                    if event.key == pygame.K_RETURN:
                        return ("back", settings_from)

            # ------------------------------------------
            # МЫШЬ
            # ------------------------------------------

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    mouse_x, mouse_y = event.pos

                    # разрешение ←
                    if self.resolution_left_rect.collidepoint(
                        mouse_x,
                        mouse_y
                    ):

                        self.resolution_index -= 1

                        if self.resolution_index < 0:
                            self.resolution_index = (
                                len(self.resolutions) - 1
                            )

                    # разрешение →
                    elif self.resolution_right_rect.collidepoint(
                        mouse_x,
                        mouse_y
                    ):

                        self.resolution_index += 1

                        if self.resolution_index >= len(
                            self.resolutions
                        ):
                            self.resolution_index = 0

                    # zoom
                    elif self.zoom_slider_rect.collidepoint(
                        mouse_x,
                        mouse_y
                    ):

                        self.set_zoom_from_mouse(mouse_x)

                    # назад
                    elif self.back_rect.collidepoint(
                        mouse_x,
                        mouse_y
                    ):

                        return ("back", settings_from)

        # ==================================================
        # РИСОВАНИЕ
        # ==================================================

        width, height = screen.get_size()

        screen.fill((10, 10, 40))

        # -------------------------
        # Заголовок
        # -------------------------

        title = self.title_font.render(
            "НАСТРОЙКИ",
            True,
            (255, 255, 255)
        )

        screen.blit(
            title,
            (
                width // 2 - title.get_width() // 2,
                60
            )
        )

        # ==================================================
        # РАЗРЕШЕНИЕ
        # ==================================================

        resolution_title_y = height // 2 - 150

        title_color = (
            (255, 255, 0)
            if self.selected == 0
            else (255, 255, 255)
        )

        resolution_title = self.font.render(
            "Разрешение экрана",
            True,
            title_color
        )

        screen.blit(
            resolution_title,
            (
                width // 2
                - resolution_title.get_width() // 2,
                resolution_title_y
            )
        )

        resolution = self.resolutions[
            self.resolution_index
        ]

        resolution_text = self.font.render(
            f"{resolution[0]} x {resolution[1]}",
            True,
            (255, 255, 255)
        )

        resolution_x = (
            width // 2
            - resolution_text.get_width() // 2
        )

        resolution_y = resolution_title_y + 55

        screen.blit(
            resolution_text,
            (
                resolution_x,
                resolution_y
            )
        )

        # стрелка <
        self.resolution_left_rect = pygame.Rect(
            resolution_x - 70,
            resolution_y,
            45,
            45
        )

        # стрелка >
        self.resolution_right_rect = pygame.Rect(
            resolution_x
            + resolution_text.get_width()
            + 25,
            resolution_y,
            45,
            45
        )

        left_text = self.font.render(
            "<",
            True,
            (255, 255, 255)
        )

        right_text = self.font.render(
            ">",
            True,
            (255, 255, 255)
        )

        screen.blit(
            left_text,
            (
                self.resolution_left_rect.x + 10,
                self.resolution_left_rect.y - 5
            )
        )

        screen.blit(
            right_text,
            (
                self.resolution_right_rect.x + 10,
                self.resolution_right_rect.y - 5
            )
        )

        # ==================================================
        # ZOOM
        # ==================================================

        zoom_title_y = height // 2 - 20

        zoom_title_color = (
            (255, 255, 0)
            if self.selected == 1
            else (255, 255, 255)
        )

        zoom_title = self.font.render(
            "Масштаб камеры",
            True,
            zoom_title_color
        )

        screen.blit(
            zoom_title,
            (
                width // 2
                - zoom_title.get_width() // 2,
                zoom_title_y
            )
        )

        # линия
        self.zoom_slider_rect = pygame.Rect(
            width // 2 - 200,
            zoom_title_y + 65,
            400,
            8
        )

        pygame.draw.rect(
            screen,
            (100, 100, 100),
            self.zoom_slider_rect
        )

        # положение кружка
        ratio = (
            (self.zoom - self.zoom_min)
            / (self.zoom_max - self.zoom_min)
        )

        knob_x = (
            self.zoom_slider_rect.x
            + int(
                ratio
                * self.zoom_slider_rect.width
            )
        )

        pygame.draw.circle(
            screen,
            (255, 255, 0),
            (
                knob_x,
                self.zoom_slider_rect.centery
            ),
            10
        )

        zoom_text = self.small_font.render(
            f"{self.zoom:.2f}x",
            True,
            (255, 255, 255)
        )

        screen.blit(
            zoom_text,
            (
                width // 2
                - zoom_text.get_width() // 2,
                zoom_title_y + 90
            )
        )

        # ==================================================
        # НАЗАД
        # ==================================================

        self.back_rect = pygame.Rect(
            width // 2 - 100,
            height - 100,
            200,
            50
        )

        back_color = (
            (255, 255, 0)
            if self.selected == 2
            else (255, 255, 255)
        )

        back_text = self.font.render(
            "НАЗАД",
            True,
            back_color
        )

        screen.blit(
            back_text,
            (
                width // 2
                - back_text.get_width() // 2,
                height - 95
            )
        )

        return None