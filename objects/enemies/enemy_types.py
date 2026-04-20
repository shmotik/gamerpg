from dataclasses import dataclass
from objects.stats import Stats

@dataclass
class EnemyType:
    name: str
    stats: Stats


SLIME = EnemyType(
    "slime",
    Stats(hp=30, attack_values = [4, 5], defense=1)
)

GOBLIN = EnemyType(
    "goblin",
    Stats(hp=50, attack_values = [7, 8, 9], defense=3)
)

ENEMY_TYPES = {
    "slime": SLIME,
    "goblin": GOBLIN
}