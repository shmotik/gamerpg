
import json
import os
from datetime import datetime

from objects.items.items import Item
from systems.skills.skill_list import POWER_STRIKE, POISON_STRIKE, SHIELD


SAVE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "saves"
)

SLOT_COUNT = 3

SKILLS = {
    skill.name: skill
    for skill in [POWER_STRIKE, POISON_STRIKE, SHIELD]
}


def get_save_path(slot):
    if slot < 1 or slot > SLOT_COUNT:
        raise ValueError("Неверный номер слота")

    return os.path.join(SAVE_DIR, f"save{slot}.json")


def item_to_dict(item):
    return {
        "name": item.name,
        "type": item.type,
        "value": item.value,
        "description": item.description,
        "stat_bonus": item.stat_bonus,
        "slot": item.slot
    }


def item_from_dict(data):
    return Item(
        name=data["name"],
        item_type=data["type"],
        value=data.get("value", 0),
        description=data.get("description", ""),
        stat_bonus=data.get("stat_bonus", {}),
        slot=data.get("slot")
    )


def collect_quest_states(game):
    result = {}

    for location_name, location in game.locations.items():
        result[location_name] = []

        for npc in location.npcs:
            if npc.quest:
                result[location_name].append({
                    "given": npc.quest.given,
                    "completed": npc.quest.completed
                })

    return result


def collect_enemy_states(game):
    result = {}

    for location_name, location in game.locations.items():
        result[location_name] = []

        for enemy in location.enemies:
            result[location_name].append({
                "alive": enemy.alive,
                "respawn_timer": enemy.respawn_timer,

                "x": enemy.x,
                "y": enemy.y,

                "stats": enemy.stats.to_dict()
            })

    return result


def save_game(game, slot=1):
    os.makedirs(SAVE_DIR, exist_ok=True)

    progress = game.player.progress

    data = {
        "version": 1,
        "saved_at": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),

        "player": {
            "x": game.player.x,
            "y": game.player.y,
            "location": game.current_location_name,
            "stats": game.player.stats.to_dict()
        },

        "inventory": [
            item_to_dict(item)
            for item in game.player.inventory.items
        ],

        "equipment": {
            slot_name: item_to_dict(item) if item else None
            for slot_name, item in game.player.equipment.items()
        },

        "progress": {
            "level": progress.level,
            "xp": progress.xp,
            "stat_points": progress.stat_points,
            "stats": progress.stats,
            "total_kills": progress.total_kills,
            "total_items": progress.total_items,
            "quest_kills": progress.quest_kills,
            "quest_items": progress.quest_items
        },

        "skills": [
            skill.name for skill in game.player.skills
        ],

        "world": game.world_state,
        "quests": collect_quest_states(game),
        "enemies": collect_enemy_states(game)
    }

    path = get_save_path(slot)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    game.save_slot = slot
    print(f"[SAVE] Слот {slot} сохранён")
    return True


def load_game(game, slot=1):
    path = get_save_path(slot)

    if not os.path.exists(path):
        print(f"[LOAD] Слот {slot} пуст")
        return False

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        player = game.player
        player_data = data["player"]

        # Позиция и локация
        location_name = player_data["location"]

        if location_name not in game.locations:
            print("[LOAD] Неизвестная локация")
            return False

        game.current_location_name = location_name
        game.location = game.locations[location_name]

        player.x = player_data["x"]
        player.y = player_data["y"]

        # Характеристики
        player.stats.from_dict(player_data["stats"])

        # Инвентарь
        player.inventory.items = [
            item_from_dict(item_data)
            for item_data in data.get("inventory", [])
        ]

        # Экипировка
        equipment_data = data.get("equipment", {})

        player.equipment = {
            slot_name: (
                item_from_dict(item_data)
                if item_data else None
            )
            for slot_name, item_data in equipment_data.items()
        }

        # Прогресс персонажа
        progress = player.progress
        progress_data = data.get("progress", {})

        progress.level = progress_data.get("level", 1)
        progress.xp = progress_data.get("xp", 0)
        progress.stat_points = progress_data.get("stat_points", 0)
        progress.stats = progress_data.get("stats", progress.stats)
        progress.total_kills = progress_data.get("total_kills", {})
        progress.total_items = progress_data.get("total_items", {})
        progress.quest_kills = progress_data.get("quest_kills", {})
        progress.quest_items = progress_data.get("quest_items", {})

        # Навыки
        player.skills = [
            SKILLS[name]
            for name in data.get("skills", [])
            if name in SKILLS
        ]

        # Состояние мира
        game.world_state = data.get("world", game.world_state)

        # Состояние квестов
        quest_states = data.get("quests", {})
        progress.quests = []

        for location_name, location in game.locations.items():
            saved_quests = quest_states.get(location_name, [])

            for index, npc in enumerate(location.npcs):
                if not npc.quest:
                    continue

                if index < len(saved_quests):
                    quest_data = saved_quests[index]
                    npc.quest.given = quest_data.get("given", False)
                    npc.quest.completed = quest_data.get("completed", False)

                if npc.quest.given:
                    progress.quests.append(npc.quest)

        # Состояние врагов
        enemy_states = data.get("enemies", {})

        for location_name, location in game.locations.items():
            saved_enemies = enemy_states.get(location_name, [])

            for index, enemy in enumerate(location.enemies):
                if index >= len(saved_enemies):
                    continue

                enemy_data = saved_enemies[index]
                enemy.alive = enemy_data.get("alive", True)
                enemy.respawn_timer = enemy_data.get("respawn_timer", 0)
                
                enemy.x = enemy_data.get("x", enemy.spawn_x)
                enemy.y = enemy_data.get("y", enemy.spawn_y)

                enemy.rect.x = int(enemy.x)
                enemy.rect.y = int(enemy.y)

                if "stats" in enemy_data:
                    enemy.stats.from_dict(enemy_data["stats"])

        # Убираем уже подобранные предметы с карт
        game.apply_world_state()

        game.quest_ui = game.quest_ui.__class__(player)
        game.save_slot = slot
        game.in_battle = False

        print(f"[LOAD] Слот {slot} загружен")
        return True

    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"[LOAD] Ошибка чтения сохранения: {error}")
        return False


def get_save_info(slot):
    path = get_save_path(slot)

    if not os.path.exists(path):
        return None

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        player = data.get("player", {})
        progress = data.get("progress", {})

        return {
            "slot": slot,
            "saved_at": data.get("saved_at", "Дата неизвестна"),
            "location": player.get("location", "Неизвестно"),
            "level": progress.get("level", 1)
        }

    except (OSError, json.JSONDecodeError):
        return None