from objects.items.items import Item

def get_potion():
    return Item("Potion", "heal", 20)

def get_big_potion():
    return Item("Big Potion", "heal", 50)

def get_lucky_charm():
    return Item(
        "lucky_charm",
        "buff",
        stat_bonus={"luck":3},
        slot="charm"
    )

def get_sword():
    return Item(
        "Sword",
        "buff",
        stat_bonus={"attack": 5},
        slot="weapon"
    )

def get_boots():
    return Item(
        "Boots",
        "buff",
        stat_bonus={"speed": 2},
        slot="armor"
    )