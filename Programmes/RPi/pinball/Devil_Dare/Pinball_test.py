import os, sys
parent_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_path + "/sources")

import Pinball
import unittest
import Input
import Options
import Output
import time

def simulate_input(name):
    input = Input.Input.instances[name]
    input.event()
    return input

def simulate_target_bank_complete(name, nb=1):
    for i in range(nb):
        for child in Input.Target_Bank.instances[name].children:
            simulate_input(child.name)
            
class Test(unittest.TestCase):
    def setUp(self):
        Pinball.power_on()
        simulate_input('Credit Left')
        simulate_input('Start')
        
    def tearDown(self):
        Pinball.power_off()
    
    def test_Special(self):
        Input.Target_Bank.instances["Left Top Target Bank"].children
        self.assertEqual(Output.Lamp.instances['Special'].get_level(), 0)
        simulate_target_bank_complete("Left Top Target Bank", 2)
        self.assertEqual(Output.Lamp.instances['Special'].get_level(), 1)
        
        bonus = Pinball.get_bonus_current_player()
        simulate_input("Right Outside Rollover")
        self.assertEqual(Pinball.get_bonus_current_player(), bonus + 5000)    
    
    def test_Extra_Ball(self):
        self.assertEqual(Output.Lamp.instances['Extra Ball'].get_level(), 0)
        simulate_target_bank_complete("Right Bottom Target Bank")
        self.assertEqual(Output.Lamp.instances['Extra Ball'].get_level(), 1)
        
        self.assertEqual(Output.Lamp.instances['Shoot Again'].get_level(), 0)
        simulate_input("Rollunder")
        self.assertEqual(Output.Lamp.instances['Shoot Again'].get_level(), 1)
        
    def test_Multi_Ball(self):
        self.assertEqual(Output.Lamp.instances['Hole Capture'].get_level(), 0)
        simulate_target_bank_complete("Right Drop Target Bank")
        self.assertEqual(Output.Lamp.instances['Hole Capture'].get_level(), "blink")
        
        self.assertEqual(Output.Lamp.instances['Top Kicker Capture'].get_level(), 0)
        simulate_target_bank_complete("Left Drop Target Bank")
        self.assertEqual(Output.Lamp.instances['Top Kicker Capture'].get_level(), "blink")
        
    """def test_Ball_Save(self):
        pass
    
    def test_Multiplier(self):
        pass
    
    def test_Multi_Mode(self):
        pass
    
    def test_Right_Outlane(self):
        pass
    
    def test_Return_Lane(self):
        pass
    
    def test_Left_Side_Spot_Target(self):
        pass
    
    def test_Top_Spot_Target_Bank(self):
        pass
    
    def test_Right_Spot_Target_Bank(self):
        pass
    
    def test_Capture_Cave_Pit(self):
        pass"""
        
####################################################################################################################################

if __name__ == "__main__": 
    unittest.main() 
    