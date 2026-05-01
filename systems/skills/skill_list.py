from systems.skills.base_skills import Skill


#  ЭФФЕКТЫ 

def poison_effect(user, target):
    target.add_status("poison", 3)


def buff_defense(user, target):
    user.add_temp("defense", 5, turns=3)


#  СКИЛЛЫ 

POWER_STRIKE = Skill(
    "Power Strike",
    multiplier=1.5,
    mana_cost=10,
    cooldown=2
)

POISON_STRIKE = Skill(
    "Poison Strike",
    multiplier=0.8,
    mana_cost=8,
    cooldown=3,
    effect=poison_effect
)

SHIELD = Skill(
    "Shield",
    multiplier=0,
    mana_cost=5,
    cooldown=4,
    effect=buff_defense
)