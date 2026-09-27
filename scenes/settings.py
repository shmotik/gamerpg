import pygame

from scenes.base_scene import Scene


class Settings(Scene):

    def __init__(self):
        self.resolutions = [
            (800, 600),
            (1024, 768),
            (1280, 720),
            (1600, 900)
        ]

        self.resolution_index = 0

        self.zoom_min = 0.75
        self.zoom_max = 1.50
        self.zoom_step = 0.05
        self.zoom = 1.0

        self.selected = 0

        self.update_fonts()

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

        self.small = pygame.font.SysFont(
            None,
            int(height * 0.035)
        )

    def update(self, screen, keys, events, settings_from):

        width, height = screen.get_size()

        for event in events:

            if event.type == pygame.KEYDOWN:

                # вверх
                if event.key == pygame.K_UP:
                    self.selected -= 1

                # вниз
                elif event.key == pygame.K_DOWN:
                    self.selected += 1

                # ограничение выбора
                self.selected = max(0, min(self.selected, 2))

                # ENTER
                if event.key == pygame.K_RETURN:

                    # разрешение
                    if self.selected == 0:
                        return (
                            "apply_resolution",
                            self.resolutions[self.resolution_index]
                        )

                    # масштаб
                    elif self.selected == 1:
                        return (
                            "apply_zoom",
                            self.zoom
                        )

                    # назад
                    elif self.selected == 2:
                        return ("back", settings_from)

                # ESC
                if event.key == pygame.K_ESCAPE:
                    return ("back", settings_from)

                # выбор разрешения
                if self.selected == 0:

                    if event.key == pygame.K_LEFT:
                        self.resolution_index -= 1

                    elif event.key == pygame.K_RIGHT:
                        self.resolution_index += 1

                    self.resolution_index %= len(self.resolutions)

                # изменение zoom
                elif self.selected == 1:

                    if event.key == pygame.K_LEFT:
                        self.zoom -= self.zoom_step

                    elif event.key == pygame.K_RIGHT:
                        self.zoom += self.zoom_step

                    self.zoom = max(
                        self.zoom_min,
                        min(self.zoom, self.zoom_max)
                    )

            # мышь
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    mouse_x, mouse_y = event.pos

                    # стрелка влево разрешения
                    if self.resolution_left_rect.collidepoint(
                        mouse_x, mouse_y
                    ):
                        self.resolution_index -= 1
                        self.resolution_index %= len(self.resolutions)

                    # стрелка вправо разрешения
                    elif self.resolution_right_rect.collidepoint(
                        mouse_x, mouse_y
                    ):
                        self.resolution_index += 1
                        self.resolution_index %= len(self.resolutions)

                    # ползунок zoom
                    elif self.zoom_slider_rect.collidepoint(
                        mouse_x, mouse_y
                    ):
                        self.set_zoom_from_mouse(mouse_x)

                    # назад
                    elif self.back_rect.collidepoint(
                        mouse_x, mouse_y
                    ):
                        return ("back", settings_from)

        # =========================
        # РЕНДЕР
        # =========================

        screen.fill((10, 10, 40))

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

        # =========================
        # РАЗРЕШЕНИЕ
        # =========================

        resolution_y = height // 2 - 100

        resolution_title = self.font.render(
            "Разрешение экрана",
            True,
            (255, 255, 255)
        )

        screen.blit(
            resolution_title,
            (
                width // 2 - resolution_title.get_width() // 2,
                resolution_y
            )
        )

        resolution_text = self.resolutions[
            self.resolution_index
        ]

        resolution_surface = self.font.render(
            f"{resolution_text[0]} x {resolution_text[1]}",
            True,
            (255, 255, 0)
        )

        resolution_x = (
            width // 2
            - resolution_surface.get_width() // 2
        )

        screen.blit(
            resolution_surface,
            (
                resolution_x,
                resolution_y + 55
            )
        )

        # стрелки
        self.resolution_left_rect = pygame.Rect(
            resolution_x - 60,
            resolution_y + 50,
            40,
            40
        )

        self.resolution_right_rect = pygame.Rect(
            resolution_x + resolution_surface.get_width() + 20,
            resolution_y + 50,
            40,
            40
        )

        left = self.font.render(
            "<",
            True,
            (255, 255, 255)
        )

        right = self.font.render(
            ">",
            True,
            (255, 255, 255)
        )

        screen.blit(
            left,
            (
                self.resolution_left_rect.x + 10,
                self.resolution_left_rect.y
            )
        )

        screen.blit(
            right,
            (
                self.resolution_right_rect.x + 10,
                self.resolution_right_rect.y
            )
        )

        # =========================
        # ZOOM
        # =========================

        zoom_y = height // 2 + 20

        zoom_title = self.font.render(
            "Масштаб камеры",
            True,
            (255, 255, 255)
        )

        screen.blit(
            zoom_title,
            (
                width // 2 - zoom_title.get_width() // 2,
                zoom_y
            )
        )

        self.zoom_slider_rect = pygame.Rect(
            width // 2 - 200,
            zoom_y + 65,
            400,
            8
        )

        pygame.draw.rect(
            screen,
            (80, 80, 80),
            self.zoom_slider_rect
        )

        # положение ползунка
        ratio = (
            (self.zoom - self.zoom_min)
            / (self.zoom_max - self.zoom_min)
        )

        knob_x = (
            self.zoom_slider_rect.x
            + int(ratio * self.zoom_slider_rect.width)
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

        zoom_text = self.small.render(
            f"{self.zoom:.2f}x",
            True,
            (255, 255, 255)
        )

        screen.blit(
            zoom_text,
            (
                width // 2 - zoom_text.get_width() // 2,
                zoom_y + 90
            )
        )

        # =========================
        # НАЗАД
        # =========================

        self.back_rect = pygame.Rect(
            width // 2 - 100,
            height - 100,
            200,
            50
        )

        back_color = (
            (255, 255, 0)
            if self.selected == 2
            else (200, 200, 200)
        )

        back_text = self.font.render(
            "НАЗАД",
            True,
            back_color
        )

        screen.blit(
            back_text,
            (
                width // 2 - back_text.get_width() // 2,
                height - 95
            )
        )

        return None

    def set_zoom_from_mouse(self, mouse_x):

        ratio = (
            mouse_x - self.zoom_slider_rect.x
        ) / self.zoom_slider_rect.width

        ratio = max(0.0, min(1.0, ratio))

        self.zoom = (
            self.zoom_min
            + ratio * (
                self.zoom_max
                - self.zoom_min
            )
        )

        # округляем до шага 0.05
        self.zoom = round(
            self.zoom / self.zoom_step
        ) * self.zoom_step

        self.zoom = max(
            self.zoom_min,
            min(self.zoom, self.zoom_max)
        )