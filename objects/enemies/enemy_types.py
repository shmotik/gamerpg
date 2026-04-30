from dataclasses import dataclass
from objects.stats import Stats
from objects.items.database import get_potion

@dataclass
class EnemyType:
    name: str
    stats: Stats
    drops: list
    xp: int


SLIME = EnemyType(
    "slime",
    Stats(
        hp=30, 
        attack_values = [4, 5], 
        defense=1,
        speed=3,
        extra_stats={"luck":0}
    ),
    drops = [(get_potion, 0.7),],
    xp=20
)

GOBLIN = EnemyType(
    "goblin",
    Stats(hp=50, attack_values = [7, 8, 9], defense=3, speed = 6, extra_stats={"luck":0}),
    drops = [(get_potion, 0.5),],
    xp=50
)

ENEMY_TYPES = {
    "slime": SLIME,
    "goblin": GOBLIN
}