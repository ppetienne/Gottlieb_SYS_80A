# -*- coding: utf-8 -*-
import General
import Common
import Options
import time
import unittest
import Display
import Output
import Contacts
import Options
import Data_Save

lc = Output.Lamp_Control.instances["LD1"]
ll = Output.Lamp_Latch.instances["DS1"]

def create_lamp(name, playfield=False):
    Output.Lamp(lamp_control=lc, lamp_latch=ll, name=name, playfield=playfield)

create_lamp("Game Over Relay")
create_lamp("Game Over Light")
create_lamp("Tilt")
create_lamp("Coin Lockout Coil")

class Test_Common(unittest.TestCase):
    
    def setUp(self):
        Data_Save.reset_data()
        Options.reset_options()
        
    def test_criticals_functions(self):
        Common.power_on()
        Common.start_new_game()
        Common.power_off()
    
    def test_generals_functions(self):
        # Credits
        Common.add_credits(1)
        self.assertEqual(Common.get_credits(), 1)
        max = Options.get_option("maximum_credits")
        Common.add_credits(max) 
        self.assertEqual(Common.get_credits(), max)
        for i in range(5):
            Common.add_player()
        
        Common.set_display_players(10)
        Common.set_display_players_all_zero()
        
        Common.tilt_level(1)
        Common.tilt_level(0)
        
        Common.game_over_level(1)
        Common.game_over_level(0)
        
####################################################################################################################################

if __name__ == "__main__": 
    unittest.main()   