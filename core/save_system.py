import json
import os

SAVE_DIR = "saves"


def save_game(game, slot=1):
    os.makedirs(SAVE_DIR, exist_ok=True)

    data = {
        "player": {
            "x": game.player.x,
            "y": game.player.y,
            "location": game.current_location_name,
            "hp": game.player.stats.hp
        },
        "inventory": game.player.inventory.items,
        "stats": game.player.stats.to_dict(),
        "world": game.world_state,
        "quests": game.quests
    }

    with open(f"{SAVE_DIR}/save{slot}.json", "w") as f:
        json.dump(data, f, indent=4)

def load_game(game, slot=1):
    with open(f"saves/save{slot}.json", "r") as f:
        data = json.load(f)

    # игрок
    game.player.x = data["player"]["x"]
    game.player.y = data["player"]["y"]
    game.player.stats.hp = data["player"]["hp"]

    # локация
    game.location = game.locations[data["player"]["location"]]

    # инвентарь
    game.player.inventory.items = data["inventory"]

    # статы
    game.player.stats.from_dict(data["stats"])

    # мир
    game.world_state = data["world"]

    # квесты
    game.quests = data["quests"]