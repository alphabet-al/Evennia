from evennia.utils import create 
from evennia.utils.test_resources import BaseEvenniaTest 

from ..objects import DungeonWeapon, DungeonTreasure
from ..characters import DungeonCharacter
from ..enums import WieldLocation

class TestEquipment(BaseEvenniaTest): 
    
    def setUp(self): 
        self.character = create.create_object(DungeonCharacter, key='testchar')
        self.weapon = create.create_object(DungeonWeapon, key="weapon") 
        self.goblet = create.create_object(DungeonTreasure, key="goblet")
         
    def test_add_remove(self): 
        self.character.equipment.add(self.goblet)
        self.assertEqual(
            self.character.equipment.slots[WieldLocation.BACKPACK],
            [self.goblet]
        )
        self.character.equipment.remove(self.goblet)
        self.assertEqual(self.character.equipment.slots[WieldLocation.BACKPACK], []) 
        