"""Переводы загружаются один раз; текст запрашивается при каждой отрисовке."""

import json
from pathlib import Path

LANGUAGES = ("en", "ru")
LANGUAGE_NAMES = {"en": "English", "ru": "Русский"}


class Localization:
    def __init__(self, directory=None):
        directory = Path(directory) if directory else Path(__file__).resolve().parent
        self.language = "en"
        self.translations = {}
        for language in LANGUAGES:
            try:
                data = json.loads((directory / f"{language}.json").read_text(encoding="utf-8"))
            except (OSError, ValueError, UnicodeError):
                data = {}
            self.translations[language] = {
                key: value for key, value in data.items() if isinstance(value, str)
            } if isinstance(data, dict) else {}

    def set_language(self, language):
        self.language = language if language in LANGUAGES else "en"

    def text(self, key, **values):
        english = self.translations["en"].get(key, key)
        text = self.translations[self.language].get(key, english)
        # Ошибка в переводе или недостающий параметр не должны прерывать игру.
        for template in (text, english):
            try:
                return template.format(**values)
            except (KeyError, ValueError, IndexError, AttributeError):
                pass
        return key


localization = Localization()


def tr(key, **values):
    return localization.text(key, **values)


def set_language(language):
    localization.set_language(language)
