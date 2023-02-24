from evennia import DefaultCharacter, AttributeProperty
from .rules import dice
from evennia.utils.utils import lazy_property
from .equipment import EquipmentHandler

class LivingMixin:

    def at_pay(self, amount):
        """When paying coins, make sure to never detract more than we have"""
        amount = min(amount, self.coins)
        self.coins -= amount
        return amount
        
    def at_defeat(self): 
        """Called when defeated. By default this means death."""
        self.at_death()
        
    def at_death(self):
        """Called when this thing dies."""
        # this will mean different things for different living things
        pass 
        
    def at_do_loot(self, looted):
        """Called when looting another entity""" 
        looted.at_looted(self)
        
    def at_looted(self, looter):
        """Called when looted by another entity""" 
        
        # default to stealing some coins 
        max_steal = dice.roll("1d10") 
        stolen = self.at_pay(max_steal)
        looter.coins += stolen

class DungeonCharacter(LivingMixin, DefaultCharacter):
    coins = AttributeProperty(0)
    inventory = []

    def at_defeat(self):
        """Characters roll on the death table"""
        if self.location.allow_death:
            # this allow rooms to have non-lethal battles
            dice.roll_death(self)
        else:
            self.location.msg_contents(
                "$You() $conj(collapse) in a heap, alive but beaten.",
                from_obj=self)
            self.heal(self.hp_max)
            
    def at_death(self):
        """We rolled 'killed' on the monster attack table."""
        self.location.msg_contents(
            "$You() collapse in a heap, embraced by death.",
            from_obj=self) 
        # TODO - go back into chargen to make a new character! 

    def at_seriously_wounded(self):
        """We rolled 'seriously wounded' on the monster attack table."""
        self.location.msg_contents(
            "$You() suffer a grave wound! Barely alive, you are found bleeding out and are rushed to the Great Hall.",
            from_obj=self)  
        # TODO - teleport character to Great hall, lose half tresure.

    def at_wounded(self):
        """We rolled 'wounded' on the monster attack table."""
        self.location.msg_contents(
            "$You() are wounded! The monster batters you from all sides and are forced to retreat!",
            from_obj=self)  
        # TODO - lose 1 random treasure , move hero back 1 space and lose a turn.

    def at_stunned(self):
        """We rolled 'stunned' on the monster attack table."""
        self.location.msg_contents(
            "Glancing blow! $You() are stunned! you manage to deflect the attack using your Shield",
            from_obj=self)  
        # TODO - lose 1 random treasure.

    def at_miss(self):
        """We rolled 'miss' on the monster attack table."""
        self.location.msg_contents(
            "$You() are unharmed! The monster flails wildly and misses!",
            from_obj=self)  
     
    @lazy_property
    def equipment(self):
        return EquipmentHandler(self)

    def at_object_receive(self, moved_object, source_location, **kwargs): 
        """ 
        Called by Evennia when an object arrives 'in' the character.
        
        """
        self.equipment.add(moved_object)

    def at_object_leave(self, moved_object, destination, **kwargs):
        """ 
        Called by Evennia when object leaves the Character. 
        
        """
        self.equipment.remove(moved_object)