"""Пользовательские настройки, независимые от сохранений персонажа."""

import json
import math
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.json"
RESOLUTIONS = ((800, 600), (1024, 768), (1280, 720), (1600, 900))
ZOOM_MIN, ZOOM_MAX, ZOOM_STEP = 0.75, 1.50, 0.05


def validate_settings(data):
    result = {"language": "en", "resolution": [800, 600], "zoom": 1.0}
    if not isinstance(data, dict):
        return result
    if data.get("language") in ("en", "ru"):
        result["language"] = data["language"]
    resolution = data.get("resolution")
    if (isinstance(resolution, (list, tuple)) and len(resolution) == 2
            and all(type(value) is int for value in resolution)
            and tuple(resolution) in RESOLUTIONS):
        result["resolution"] = list(resolution)
    zoom = data.get("zoom")
    if (type(zoom) in (int, float) and ZOOM_MIN <= zoom <= ZOOM_MAX
            and math.isfinite(zoom)):
        result["zoom"] = round(round(zoom / ZOOM_STEP) * ZOOM_STEP, 2)
    return result


class UserSettings:
    def __init__(self, path=None):
        self.path = Path(path).resolve() if path is not None else CONFIG_PATH
        self.save_error = False
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError, UnicodeError):
            data = {}
        self.data = validate_settings(data)

    def set(self, key, value):
        self.data = validate_settings({**self.data, key: value})
        return self.save()

    def save(self):
        temporary = self.path.with_suffix(".json.tmp")
        try:
            temporary.write_text(
                json.dumps(self.data, ensure_ascii=False, indent=4) + "\n",
                encoding="utf-8"
            )
            temporary.replace(self.path)
        except OSError:
            self.save_error = True
            return False
        self.save_error = False
        return True
