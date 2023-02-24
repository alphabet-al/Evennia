from enum import Enum

class WieldLocation(Enum):
    BACKPACK = "backpack"
    WEAPON_HAND = "weapon_hand"

class ObjType(Enum):

    WEAPON = "weapon"
    TREASURE = "treasure"
    MAGIC = "magic"
    GEAR = "gear"
    CONSUMABLE = 'consumable'