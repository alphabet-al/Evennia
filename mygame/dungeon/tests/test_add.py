import unittest
from evennia.utils.test_resources import BaseEvenniaTest
from .. import calc 

class TestAdd(unittest.TestCase):
   
    # def setUp(self):
    #     """Called before every test method"""
    #     super().setUp()
    
    def test_add(self):
        result = calc.add(10, 5)
        self.assertEqual(result, 15)

if __name__ == '__main__':
    unittest.main()