from random import randint
from . import random_tables

class DungeonRollEngine:

    def roll(self, roll_string):
        """ 
        Roll XdY dice, where X is the number of dice 
        and Y the number of sides per die. 
        
        Args:
            roll_string (str): A dice string on the form XdY.
        Returns:
            int: The result of the roll. 
            
        """ 
        
        # split the XdY input on the 'd' one time
        number, diesize = roll_string.split("d", 1)     
        
        # convert from string to integers
        number = int(number) 
        diesize = int(diesize)
            
        # make the roll
        return sum(randint(1, diesize) for _ in range(number))

    def roll_random_table(self, dieroll, table_choices):
        """
        Make a roll on a random table.

        Args:
            dieroll (str): The dice to roll, like 1d6, 1d20, 3d6 etc).
            table_choices (iterable): If a list of single elements, the die roll
                should fully encompass the table, like a 1d20 roll for a table
                with 20 elements. If each element is a tuple, the first element
                of the tuple is assumed to be a string 'X-Y' indicating the
                range of values that should match the roll.

        Returns:
            Any: The result of the random roll.

        Example:
            `roll table_choices = [('1-5', "Blue"), ('6-9': "Red"), ('10', "Purple")]`

        Notes:
            If the roll is outside of the listing, the closest edge value is used.

        """
        roll_result = self.roll(dieroll)
        if not table_choices:
            return None

        if isinstance(table_choices[0], (tuple, list)):
            # tuple with range conditional, like ('1-5', "Blue") or ('10', "Purple")
            max_range = -1
            min_range = 10**6
            for (valrange, choice) in table_choices:

                minval, *maxval = valrange.split("-", 1)
                minval = abs(int(minval))
                maxval = abs(int(maxval[0]) if maxval else minval)

                # we store the largest/smallest values so far in case we need to use them
                max_range = max(max_range, maxval)
                min_range = min(min_range, minval)

                if minval <= roll_result <= maxval:
                    return choice

            # if we have no result, we are outside of the range, we pick the edge values. It is also
            # possible the range contains 'gaps', but that'd be an error in the random table itself.
            if roll_result > max_range:
                return table_choices[-1][1]
            else:
                return table_choices[0][1]
        else:
            # regular list - one line per value.
            roll_result = max(1, min(len(table_choices), roll_result))
            return table_choices[roll_result - 1]

    def roll_death(self, character):

        """
        Happens when hitting <= 0 hp. unless dead,

        """
        
        result = self.roll_random_table("2d6", random_tables.monster_attack)
        if result == "Killed":
            character.at_death()
        elif result == "Seriously Wounded":
            character.at_seriously_wounded()
        elif result == "Wounded":
            character.at_wounded()
        elif result == "Stunned":
            character.at_stunned()
        elif result == "Miss":
            # Monster misses
            character.at_miss()

    # specific rolls / actions

dice = DungeonRollEngine()

# print(dice.roll_random_table("2d6", random_tables.monster_attack))

# if dice.roll_random_table("2d6", random_tables.monster_attack) == "Stunned":