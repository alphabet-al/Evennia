from unittest.mock import patch 
from evennia.utils.test_resources import BaseEvenniaTest
from .. import rules, random_tables

class TestDungeonRuleEngine(BaseEvenniaTest):
   
    def setUp(self):
        """Called before every test method"""
        super().setUp()
        self.roll_engine = rules.DungeonRollEngine()
    
    @patch("dungeon.rules.randint")
    def test_roll(self, mock_randint):
        mock_randint.return_value = 4 
        self.assertEqual(self.roll_engine.roll("1d6"), 4, "test_roll")     
        self.assertEqual(self.roll_engine.roll("2d6"), 2 * 4)

    @patch("dungeon.rules.randint")
    def test_roll_random_table(self, mock_randint):
        mock_randint.return_value = 1
        self.assertEqual(self.roll_engine.roll_random_table("2d6", random_tables.monster_attack), "Miss")

        mock_randint.return_value = 12
        self.assertEqual(self.roll_engine.roll_random_table("2d6", random_tables.monster_attack), "Killed")

        mock_randint.return_value = -10
        self.assertEqual(self.roll_engine.roll_random_table("2d6", random_tables.monster_attack), "Miss")

        mock_randint.return_value = 15
        self.assertEqual(self.roll_engine.roll_random_table("2d6", random_tables.monster_attack), "Killed")




