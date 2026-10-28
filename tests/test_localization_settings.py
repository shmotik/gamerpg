"""Запуск из корня: python -B -m unittest discover -s tests -v.

Вместо настоящего окна используется SDL dummy, а конфигурация пишется
только во временную папку. Игровые сохранения тесты не записывают.
"""

import copy
import json
import os
from pathlib import Path
import runpy
import sys
import tempfile
import unittest
from unittest.mock import patch

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
from core import controls
from core.config import UserSettings, CONFIG_PATH, RESOLUTIONS, validate_settings
from core.game import Game
from core.battle import Battle
from localization.manager import Localization, localization, set_language, tr
from scenes.menu import Menu
from scenes.pause import Pause
from scenes.settings import Settings
from scenes.save_load import SaveLoadScene
from scenes.inventory_scene import InventoryScene
from UI.text import get_font

ROOT = Path(__file__).resolve().parents[1]


def keys(*values):
    return [pygame.event.Event(pygame.KEYDOWN, key=value) for value in values]


class ConfigTests(unittest.TestCase):
    def test_defaults_and_independent_invalid_fields(self):
        defaults = {"language": "en", "resolution": [800, 600], "zoom": 1.0}
        for value in (None, [], "bad", {}, {"language": [], "resolution": [True, 600], "zoom": False},
                      {"zoom": float("nan")}, {"zoom": 10 ** 400}):
            self.assertEqual(validate_settings(value), defaults)
        self.assertEqual(validate_settings({"language": "ru", "resolution": [0, 0], "zoom": "bad"}),
                         {**defaults, "language": "ru"})

    def test_load_save_and_corrupt_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "config.json"
            config = UserSettings(path)
            self.assertEqual(config.data["language"], "en")
            self.assertFalse(path.exists())
            for key, value in (("language", "ru"), ("resolution", [1280, 720]), ("zoom", 1.25)):
                self.assertTrue(config.set(key, value))
            self.assertEqual(UserSettings(path).data, config.data)
            self.assertFalse(path.with_suffix(".json.tmp").exists())
            for content in ('{"language":', '[]', 'null', '{"zoom": NaN}'):
                path.write_text(content, encoding="utf-8")
                self.assertEqual(UserSettings(path).data, validate_settings({}))
            path.write_bytes(b'\xff\xfe\xff')
            self.assertEqual(UserSettings(path).data, validate_settings({}))

    def test_paths_do_not_depend_on_working_directory(self):
        previous = Path.cwd()
        with tempfile.TemporaryDirectory() as folder:
            try:
                os.chdir(folder)
                self.assertEqual(UserSettings().path, ROOT / "config.json")
                self.assertEqual(CONFIG_PATH, ROOT / "config.json")
                self.assertEqual(Localization().text("battle.run"), "Run")
            finally:
                # На Windows нельзя удалить временную папку, пока она является cwd.
                os.chdir(previous)

    def test_write_error_is_reported_without_crash(self):
        with tempfile.TemporaryDirectory() as folder:
            config = UserSettings(Path(folder) / "config.json")
            with patch.object(Path, "replace", side_effect=OSError("read-only")):
                self.assertFalse(config.set("language", "ru"))
            self.assertTrue(config.save_error)
            self.assertEqual(config.data["language"], "ru")


class TranslationTests(unittest.TestCase):
    def test_complete_dictionaries_and_placeholders(self):
        manager = Localization()
        en, ru = manager.translations["en"], manager.translations["ru"]
        self.assertEqual(en.keys(), ru.keys())
        from string import Formatter
        for key in en:
            fields = lambda text: {field for _, field, _, _ in Formatter().parse(text) if field}
            self.assertEqual(fields(en[key]), fields(ru[key]), key)

    def test_fallback_missing_and_bad_format(self):
        manager = Localization()
        manager.set_language("ru")
        del manager.translations["ru"]["battle.run"]
        self.assertEqual(manager.text("battle.run"), "Run")
        self.assertEqual(manager.text("missing.key"), "missing.key")
        manager.translations["ru"]["save.slot"] = "{wrong}"
        self.assertEqual(manager.text("save.slot", slot=2), "Slot 2")
        manager.set_language("unknown")
        self.assertEqual(manager.language, "en")


class UITests(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.temp = tempfile.TemporaryDirectory()
        self.config = UserSettings(Path(self.temp.name) / "config.json")
        set_language("en")
        self.game = Game()
        self.game.update_fonts()
        for skill in self.game.player.skills:
            skill.current_cd = 0

    def tearDown(self):
        pygame.quit()
        self.temp.cleanup()
        set_language("en")

    def test_language_changes_existing_interfaces(self):
        objects = [Menu(), Pause(), Pause(True), SaveLoadScene(),
                   InventoryScene(self.game.player, self.game.messages),
                   Battle(self.game.player, self.game.location.enemies[0], self.game.messages)]
        for scene in objects:
            pictures = []
            for language in ("en", "ru", "en"):
                set_language(language)
                scene.update(self.screen, None, [], 0)
                pictures.append(pygame.image.tostring(self.screen, "RGB"))
            self.assertNotEqual(pictures[0], pictures[1], type(scene).__name__)
            self.assertEqual(pictures[0], pictures[2], type(scene).__name__)

    def test_settings_keyboard_mouse_and_immediate_persistence(self):
        scene = Settings(self.config)
        for up, down, left, right in (
            (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d),
            (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT),
        ):
            scene.selected = 0
            scene.update(self.screen, None, keys(down, down), "battle")
            self.assertEqual(scene.options[scene.selected], "language")
            self.assertEqual(scene.update(self.screen, None, keys(right), "battle"), ("apply_language", "ru"))
            self.assertEqual(localization.language, "ru")
            self.assertEqual(UserSettings(self.config.path).data["language"], "ru")
            scene.update(self.screen, None, keys(left), "battle")
            self.assertEqual(localization.language, "en")
            scene.update(self.screen, None, keys(up), "battle")
            self.assertEqual(scene.options[scene.selected], "zoom")
        scene.draw(self.screen)
        for rect, action in ((scene.resolution_right_rect, "apply_resolution"),
                             (scene.language_right_rect, "apply_language"),
                             (scene.zoom_slider_rect, "apply_zoom")):
            event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=rect.center)
            self.assertEqual(scene.update(self.screen, None, [event], "battle")[0], action)
        self.assertEqual(UserSettings(self.config.path).data, self.config.data)
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=scene.back_rect.center)
        self.assertEqual(scene.update(self.screen, None, [event], "battle"), ("back", "battle"))

    def test_navigation_and_inventory_submenu_escape(self):
        for up, down in zip(controls.UP, controls.DOWN):
            for scene in (Menu(), Pause(), Pause(True), SaveLoadScene()):
                scene.update(self.screen, None, keys(down), 0)
                self.assertEqual(scene.selected, 1)
                scene.update(self.screen, None, keys(up), 0)
                self.assertEqual(scene.selected, 0)
        inventory = InventoryScene(self.game.player, self.game.messages)
        for left, right in zip(controls.LEFT, controls.RIGHT):
            inventory.update(self.screen, None, keys(right), 0)
            self.assertEqual(inventory.tab, "equipment")
            inventory.update(self.screen, None, keys(left), 0)
            self.assertEqual(inventory.tab, "inventory")
        inventory.tab_index, inventory.tab = 2, "stats"
        self.game.player.progress.stat_points = 1
        inventory.update(self.screen, None, keys(pygame.K_RETURN), 0)
        inventory.update(self.screen, None, keys(pygame.K_s), 0)
        self.assertEqual(inventory.selected_stat, 1)
        self.assertEqual(inventory.update(self.screen, None, keys(pygame.K_ESCAPE), 0), "inventory")
        self.assertFalse(inventory.in_upgrade)
        self.assertEqual(inventory.update(self.screen, None, keys(pygame.K_ESCAPE), 0), "game")

    def test_save_slot_mouse_route(self):
        scene = SaveLoadScene()
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(400, 180))
        self.assertEqual(scene.update(self.screen, None, [event]), ("load", 1, "menu"))

    def test_battle_pause_surrender_and_escape_regression(self):
        enemy = self.game.location.enemies[0]
        battle = Battle(self.game.player, enemy, self.game.messages)
        for up, down in zip(controls.UP, controls.DOWN):
            battle.handle_event(keys(down)[0])
            self.assertEqual(battle.actions[battle.selected], "skill")
            battle.handle_event(keys(pygame.K_RETURN)[0])
            battle.handle_event(keys(down)[0])
            self.assertEqual(battle.skill_index, 1)
            battle.handle_event(keys(up)[0])
            self.assertEqual(battle.skill_index, 0)
            battle.handle_event(keys(pygame.K_ESCAPE)[0])
            self.assertEqual(battle.state, "player_turn")
            battle.handle_event(keys(up)[0])
        self.assertEqual(battle.handle_event(keys(pygame.K_ESCAPE)[0]), ("battle_pause",))
        pause = Pause(True)
        pause.selected = 1
        pause.update(self.screen, None, keys(pygame.K_RETURN))
        self.assertEqual(pause.update(self.screen, None, keys(pygame.K_s, pygame.K_RETURN)), ("battle_surrender",))
        self.assertEqual(battle.surrender(), ("battle_end", "lose"))
        self.assertEqual(self.game.player.hp, 0)
        self.assertIsNone(battle.finish("win"))
        self.game.player.respawn()
        battle = Battle(self.game.player, enemy, self.game.messages)
        with patch("core.battle.random.random", return_value=0):
            self.assertEqual(battle.player_action("run"), ("battle_end", "run"))
        self.assertTrue(enemy.alive)
        self.assertEqual(self.game.player.progress.xp, 0)

    def test_all_resolutions_and_cyrillic(self):
        for resolution in RESOLUTIONS:
            self.screen = pygame.display.set_mode(resolution)
            font = get_font(resolution[1] * .04)
            self.assertTrue(all(metric is not None for metric in font.metrics("Русский Язык Ёжик")))
            for language in ("en", "ru"):
                set_language(language)
                self.config.data["language"] = language
                scenes = [Menu(), Pause(), Pause(True), SaveLoadScene(),
                          InventoryScene(self.game.player, self.game.messages), Settings(self.config)]
                for scene in scenes:
                    scene.update(self.screen, None, [], "battle" if isinstance(scene, Settings) else 0)
                inventory = scenes[4]
                for tab in inventory.tabs:
                    inventory.tab = tab
                    inventory.update(self.screen, None, [], 0)

    def test_failed_run_win_and_exit_confirmation(self):
        enemy = self.game.location.enemies[0]
        battle = Battle(self.game.player, enemy, self.game.messages)
        with patch("core.battle.random.random", return_value=.99), \
                patch("core.battle.calculate_damage", return_value=(5, "HIT")):
            self.assertIsNone(battle.player_action("run"))
            self.assertEqual(self.game.player.hp, 95)
            self.game.player.stats.hp = 1
            self.assertEqual(battle.player_action("run"), ("battle_end", "lose"))
        self.game.player.respawn()
        battle = Battle(self.game.player, enemy, self.game.messages)
        with patch("core.battle.calculate_damage", return_value=(100, "HIT")):
            self.assertEqual(battle.handle_event(keys(pygame.K_RETURN)[0]), ("battle_end", "win"))
            self.assertIsNone(battle.handle_event(keys(pygame.K_RETURN)[0]))
        pause = Pause(True)
        pause.selected = 3
        pause.update(self.screen, None, keys(pygame.K_RETURN))
        self.assertEqual(pause.update(self.screen, None, keys(pygame.K_RETURN)), "battle_pause")
        self.assertIsNone(pause.confirm_action)
        pause.update(self.screen, None, keys(pygame.K_RETURN))
        self.assertEqual(pause.update(self.screen, None, keys(pygame.K_s, pygame.K_RETURN)), "exit")


class MainLoopTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "config.json"

    def tearDown(self):
        pygame.quit()
        self.temp.cleanup()
        set_language("en")

    def run_script(self, script):
        driver = script()
        def events():
            self.ctx = sys._getframe(1).f_globals
            return next(driver)
        # Подменяется только путь конфигурации и ввод, а не игровой цикл.
        with patch("core.config.UserSettings", side_effect=lambda: UserSettings(self.path)), \
                patch("pygame.event.get", new=events):
            result = runpy.run_path(str(ROOT / "main.py"), run_name="__main__")
        self.assertIsNone(next(driver, None))
        return result

    def test_first_start_then_restart_restores_all_settings(self):
        def first():
            self.assertEqual(localization.language, "en")
            self.assertEqual(self.ctx["screen"].get_size(), (800, 600))
            yield keys(pygame.K_s, pygame.K_s, pygame.K_RETURN)
            game = self.ctx["game"]
            yield keys(pygame.K_s, pygame.K_s)
            yield keys(pygame.K_d)
            self.assertEqual(localization.language, "ru")
            self.assertIs(self.ctx["game"], game)
            yield keys(pygame.K_w, pygame.K_w)
            yield keys(pygame.K_d)
            self.assertEqual(self.ctx["screen"].get_size(), (1024, 768))
            yield keys(pygame.K_s)
            yield keys(pygame.K_d)
            self.assertEqual(game.zoom, 1.05)
            yield [pygame.event.Event(pygame.QUIT)]
        self.run_script(first)
        def second():
            self.assertEqual(localization.language, "ru")
            self.assertEqual(self.ctx["screen"].get_size(), (1024, 768))
            self.assertEqual(self.ctx["game"].zoom, 1.05)
            yield [pygame.event.Event(pygame.QUIT)]
        self.run_script(second)

    def test_corrupt_config_still_starts(self):
        self.path.write_text('{bad json', encoding="utf-8")
        def script():
            self.assertEqual(localization.language, "en")
            self.assertEqual(self.ctx["screen"].get_size(), (800, 600))
            self.assertEqual(self.ctx["game"].zoom, 1.0)
            yield [pygame.event.Event(pygame.QUIT)]
        self.run_script(script)

    def test_settings_return_to_world_and_existing_battle(self):
        def script():
            yield keys(pygame.K_RETURN)
            yield keys(pygame.K_ESCAPE)
            yield keys(pygame.K_s, pygame.K_s, pygame.K_s, pygame.K_RETURN)
            self.assertEqual(self.ctx["state"], "settings")
            yield keys(pygame.K_ESCAPE)
            self.assertEqual(self.ctx["state"], "pause")
            yield keys(pygame.K_ESCAPE)
            self.assertEqual(self.ctx["state"], "game")
            game = self.ctx["game"]
            enemy = game.location.enemies[0]
            for other in game.location.enemies:
                other.speed = 0
            game.player.x, game.player.y = enemy.x, enemy.y
            yield []
            battle = self.ctx["battle"]
            self.assertIsNotNone(battle)
            snapshot = copy.deepcopy(game.player.stats.to_dict())
            yield keys(pygame.K_ESCAPE)
            yield keys(pygame.K_s, pygame.K_s, pygame.K_RETURN)
            yield keys(pygame.K_s, pygame.K_s)
            yield keys(pygame.K_d)
            yield keys(pygame.K_ESCAPE)
            self.assertEqual(self.ctx["state"], "battle")
            self.assertIs(self.ctx["battle"], battle)
            self.assertEqual(game.player.stats.to_dict(), snapshot)
            self.assertEqual(game.player.progress.xp, 0)
            yield keys(pygame.K_ESCAPE)
            yield keys(pygame.K_s, pygame.K_RETURN)
            yield keys(pygame.K_s, pygame.K_RETURN)
            self.assertEqual(self.ctx["state"], "game")
            self.assertEqual(game.player.hp, 0)
            yield []
            self.assertEqual(game.player.hp, game.player.max_hp)
            self.assertTrue(enemy.alive)
            self.assertEqual(game.player.progress.xp, 0)
            yield [pygame.event.Event(pygame.QUIT)]
        self.run_script(script)


if __name__ == "__main__":
    unittest.main()
