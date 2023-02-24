from .objects import WeaponEmptyHand
from .enums import WieldLocation


class EquipmentError(TypeError):
    """ All types of equipment-errors"""
    pass

class EquipmentHandler: 
    save_attribute = "inventory_slots"
    
    def __init__(self, obj): 
        # here obj is the character we store the handler on 
        self.obj = obj 
        self._load() 
        
    def _load(self):
        """Load our data from an Attribute on `self.obj`"""
        self.slots = self.obj.attributes.get(
            self.save_attribute,
            category="inventory",
            default={
                WieldLocation.WEAPON_HAND: None, 
                WieldLocation.BACKPACK: []
            } 
        )
    
    def _save(self):
        """Save our data back to the same Attribute"""
        self.obj.attributes.add(self.save_attribute, self.slots, category="inventory") 

    def add(self, obj):
        """
        Put something in the backpack.
        """
        self.slots[WieldLocation.BACKPACK].append(obj)
        self._save()

    def remove(self, slot):
        """
        Remove contents of a particular slot, for
        example `equipment.remove(WieldLocation.SHIELD_HAND)`
        """
        slots = self.slots
        ret = []
        if slot is WieldLocation.BACKPACK:
            # empty entire backpack! 
            ret.extend(slots[slot])
            slots[slot] = []
        else:
            ret.append(slots[slot])
            slots[slot] = None
        if ret:
            self._save()
        return ret

    def move(self, obj): 
        """Move object from backpack to its intended `inventory_use_slot`.""" 
        
        # make sure to remove from equipment/backpack first, to avoid double-adding
        self.remove(obj) 
        
        slots = self.slots
        use_slot = getattr(obj, "inventory_use_slot", WieldLocation.BACKPACK)

        to_backpack = []
        if use_slot is WieldLocation.TWO_HANDS:
            # two-handed weapons can't co-exist with weapon/shield-hand used items
            to_backpack = [slots[WieldLocation.WEAPON_HAND], slots[WieldLocation.SHIELD_HAND]]
            slots[WieldLocation.WEAPON_HAND] = slots[WieldLocation.SHIELD_HAND] = None
            slots[use_slot] = obj
        elif use_slot in (WieldLocation.WEAPON_HAND, WieldLocation.SHIELD_HAND):
            # can't keep a two-handed weapon if adding a one-handed weapon or shield
            to_backpack = [slots[WieldLocation.TWO_HANDS]]
            slots[WieldLocation.TWO_HANDS] = None
            slots[use_slot] = obj
        elif use_slot is WieldLocation.BACKPACK:
            # it belongs in backpack, so goes back to it
            to_backpack = [obj]
        else:
            # for others (body, head), just replace whatever's there
            replaced = [obj]
            slots[use_slot] = obj
        
        for to_backpack_obj in to_backpack:
            # put stuff in backpack
            slots[use_slot].append(to_backpack_obj)
        
        # store new state
        self._save() 

    def all(self):
        """
        Get all objects in inventory, regardless of location.
        """
        slots = self.slots
        lst = [(slots[WieldLocation.WEAPON_HAND], WieldLocation.WEAPON_HAND)
            ] + [(item, WieldLocation.BACKPACK) for item in slots[WieldLocation.BACKPACK]]
        return lst

    @property
    def weapon(self):
        # first checks two-handed wield, then one-handed; the two
        # should never appear simultaneously anyhow (checked in `move` method).
        slots = self.slots
        weapon = slots[WieldLocation.WEAPON_HAND]
        if not weapon:
            weapon = WeaponEmptyHand()
        return weapon 