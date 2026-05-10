import json

def save_game(player):
    data = {
        "hp": player.hp,
        "mana": player.mana,
        "x": player.x,
        "y": player.y,
        "skills": [s.name for s in player.skills],
    }

    with open("save.json", "w") as f:
        json.dump(data, f)

def load_game(player):
    with open("save.json", "r") as f:
        data = json.load(f)

    player.x = data["x"]
    player.y = data["y"]
    player.stats.hp = data["hp"]