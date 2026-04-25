from dataclasses import dataclass
from objects.stats import Stats
from objects.items.database import get_potion

@dataclass
class EnemyType:
    name: str
    stats: Stats
    drops: list


SLIME = EnemyType(
    "slime",
    Stats(
        hp=30, 
        attack_values = [4, 5], 
        defense=1,
        extra_stats={"luck":0}
    ),
    drops = [(get_potion, 0.7),]
)

GOBLIN = EnemyType(
    "goblin",
    Stats(hp=50, attack_values = [7, 8, 9], defense=3),
    drops = [(get_potion, 0.5),]
)

ENEMY_TYPES = {
    "slime": SLIME,
    "goblin": GOBLIN
}