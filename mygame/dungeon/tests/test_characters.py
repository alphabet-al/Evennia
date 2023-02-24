from evennia.utils import create
from evennia.utils.test_resources import BaseEvenniaTest 

from ..characters import DungeonCharacter 

class TestCharacters(BaseEvenniaTest):
    def setUp(self):
        super().setUp()
        self.character = create.create_object(DungeonCharacter, key="testchar")

    def test_at_pay(self):
        self.character.coins = 100 
        
        result = self.character.at_pay(60)
        self.assertEqual(result, 60) 
        self.assertEqual(self.character.coins, 40)
        
        # can't get more coins than we have 
        result = self.character.at_pay(100)
        self.assertEqual(result, 40)
        self.assertEqual(self.character.coins, 0)
        
    # tests for other methods ... 