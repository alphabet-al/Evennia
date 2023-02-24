from evennia import AttributeProperty, DefaultObject 
from evennia.utils.utils import make_iter
from .utils import get_obj_stats 
from .enums import WieldLocation, ObjType


class DungeonObject(DefaultObject): 
    """ 
    Base for all Dungeon objects. 
    
    """ 
    inventory_use_slot = WieldLocation.BACKPACK
    # size = AttributeProperty(1, autocreate=False)
    value = AttributeProperty(0, autocreate=False)
    
    # this can be either a single type or a list of types (for objects able to be 
    # act as multiple). This is used to tag this object during creation.
    obj_type = ObjType.GEAR
    
    def at_object_creation(self): 
        """Called when this object is first created. We convert the .obj_type 
        property to a database tag."""
        
        for obj_type in make_iter(self.obj_type):
            self.tags.add(self.obj_type.value, category="obj_type")
        
    def get_help(self):
        """Get any help text for this item"""
        return "No help for this item"

class DungeonTreasure(DungeonObject):
    """Treasure is usually just for selling for coin"""
    obj_type = ObjType.TREASURE
    value = AttributeProperty(100, autocreate=False)

class DungeonConsumable(DungeonObject): 
    """An item that can be used up""" 
    
    obj_type = ObjType.CONSUMABLE
    value = AttributeProperty(0.25, autocreate=False)
    uses = AttributeProperty(1, autocreate=False)
    
    def at_pre_use(self, user, *args, **kwargs):
        """Called before using. If returning False, abort use."""
        return self.uses > 0 
        
    def at_use(self, user, *args, **kwargs):
        """Called when using the item""" 
        pass 
        
    def at_post_use(self, user, *args, **kwargs):
        """Called after using the item""" 
        # detract a usage, deleting the item if used up.
        self.uses -= 1
        if self.uses <= 0: 
            user.msg(f"{self.key} was used up.")
            self.delete()

class DungeonWeapon(DungeonObject): 
    """Base class for all weapons"""

    obj_type = ObjType.WEAPON 
    
    attack_type = AttributeProperty(1, autocreate=False)
    

class DungeonSpellBook(DungeonWeapon, DungeonConsumable): 
    """Base for all magical Spell Books"""
    
    obj_type = (ObjType.WEAPON, ObjType.MAGIC)
    # quality = AttributeProperty(3, autocreate=False)

    # attack_type = AttributeProperty(Ability.INT, autocreate=False)
    # defend_type = AttributeProperty(Ability.DEX, autocreate=False)
    
    # damage_roll = AttributeProperty("1d8", autocreate=False)

    def at_post_use(self, user, *args, **kwargs):
        """Called after usage/spell was cast""" 
        self.uses -= 1 
        # we don't delete the rune stone here, but 
        # it must be reset on next rest.
        
    def refresh(self):
        """Refresh the rune stone (normally after rest)"""
        self.uses = 1

class WeaponEmptyHand:
     obj_type = ObjType.WEAPON
     key = "Empty Fists"
     quality = 100000  # let's assume fists are always available ...
 
     def __repr__(self):
         return "<WeaponEmptyHand>"