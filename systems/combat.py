import random

def calculate_damage(attacker, defender):
    # --- 1. Проверка уклонения ---
    dodge_chance = defender.get("speed") * 0.01

    if random.random() < dodge_chance:
        return 0, "DODGE"

    #  2. Базовый урон 
    min_atk, max_atk = attacker.get_attack_range()
    base_damage = random.randint(min_atk, max_atk)

    #  3. Крит 
    crit_chance = attacker.get("luck") * 0.02
    is_crit = random.random() < crit_chance

    if is_crit:
        base_damage *= 1.7

    #  Защита (процентная) 
    defense = defender.get("defense")
    damage = base_damage * (100 / (100 + defense))

    damage = int(damage)

    #  Минимальный урон 
    damage = max(1, damage)

    if is_crit:
        return damage, "CRIT"

    return damage, "HIT"