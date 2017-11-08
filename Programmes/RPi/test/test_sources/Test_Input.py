# -*- coding: utf-8 -*-
import os, sys
import General
import Data_Save
import time

import unittest
import Input
import Options


import Common
import Display
import Output
import Contacts
from Common import infos_game, General_Status
import json

lc = Output.Lamp_Control.instances["LD1"]
ll = Output.Lamp_Latch.instances["DS1"]

def create_lamp(name, playfield=False):
    Output.Lamp(lamp_control=lc, lamp_latch=ll, name=name, playfield=playfield)

create_lamp("Game Over Relay")
create_lamp("Game Over Light")
create_lamp("Tilt")
create_lamp("Coin Lockout Coil")

Input.Start(x=0, y=0)
Input.Slam(Contacts.conn.J5[10])
Input.Tilt(x=0, y=0)
Input.Test(x=0, y=0)
Input.Credit(x=0, y=0, name="Credit", value=2)

def external(x, y):
    raise AttributeError()

class Test():
    def get_level(self):
        return 0
Input.Input(name="External_event", external_event=external, get_level_object=Test(), x=1, y=2)
Input.Input(name="External_event_2", get_level_object=Test())

# Input Playfield
Input.Point(x=0, y=0, name="Point", points=1)
Input.Point_Light_Blink(x=0, y=0, name="Point_Light_Blink", lamp_control=lc, lamp_latch=ll, points=[1,2])
Input.Point_Light(x=0, y=0, name="Point_Light", lamp_control=lc, lamp_latch=ll, points=[1,2])
Input.Spinner(x=0, y=0, name="Spinner", lamp_control=lc, lamp_latch=ll, points=[1,2])

Output.Solenoid.instances["Sol 1"].set_new_name("Drop_Target_Bank")
temp_targets = Input.Target_Bank_Drop(name="Drop_Target_Bank")

Input.Target_Drop(x=0, y=0, parent=temp_targets, position_enfant=0, lamp_control=lc, lamp_latch=ll, points=[1,2])
Input.Target_Drop(x=0, y=0, parent=temp_targets, position_enfant=1, lamp_control=lc, lamp_latch=ll, points=[1,2])

temp_targets = Input.Target_Bank(name="Target_Bank")
Input.Target(x=0, y=0, parent=temp_targets, position_enfant=0, lamp_control=lc, lamp_latch=ll, points=[1,2])
Input.Target(x=0, y=0, parent=temp_targets, position_enfant=1, lamp_control=lc, lamp_latch=ll, points=[1,2])

temp_targets = Input.Target_Bank(name="Target_Bank_2_states")
Input.Target(x=0, y=0, parent=temp_targets, position_enfant=0, lamp_control=lc, lamp_latch=ll, points=[1,2], nb_states=2)
Input.Target(x=0, y=0, parent=temp_targets, position_enfant=1, lamp_control=lc, lamp_latch=ll, points=[1,2], nb_states=2)

Output.Solenoid.instances["Sol 2"].set_new_name("Hole")
Input.Hole(x=0, y=0, name="Hole")

Output.Solenoid.instances["Sol 3"].set_new_name("Outhole")
Input.OutHole(x=0, y=0, name="Outhole")

Input.Trough(x=0, y=0, name="Trough")

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Common.power_on()
    
    def setUp(self):
        Data_Save.reset_data()
        Options.reset_options()
        Common.attract_mode()

    def tearDown(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        Common.power_off()    
    
    def simulate_input(self, name):
        input = Input.Input.instances[name]
        input.event()
        return input    
    
    def test_external_event(self):
        self.assertRaises(AttributeError, lambda: self.simulate_input("External_event"))
        input = Input.Input.instances["External_event_2"]
        input.set_external_event(external, x=1, y=2)
        self.assertRaises(AttributeError, lambda: self.simulate_input("External_event"))
        
    def test_Start(self):            
        ## Test Start ##
        # Sans credit
        Data_Save.set_data("credit", 0)
        self.simulate_input('Start')
        self.assertEqual(infos_game['status'], General_Status.ATTRACT_MODE)
        
        # Avec credit
        Data_Save.set_data("credits", 5)
        self.simulate_input('Start')
        self.assertEqual(infos_game['status'], General_Status.START)
        self.assertEqual(infos_game['nb_players'], 1)

        for i in range(3):
            self.simulate_input('Start')
            if i == 3:
                self.assertEqual(infos_game['nb_players'], i+1)
            else:
                self.assertEqual(infos_game['nb_players'], i+2)
        self.assertEqual(Data_Save.get_data("credits"), 1)
        
        for input in Input.Input_Playfield.instances.values():
            self.assertEqual(input.activated, True)
        
    def test_Credit(self):
        pass
        
    def test_Test(self):
        self.simulate_input('Test')
        self.assertEqual(Common.infos_game['status'], Common.General_Status.TEST)
        
    def test_Slam(self):
        self.simulate_input('Slam')
        self.assertEqual(Common.infos_game['status'], Common.General_Status.SLAM)

class Test_Playfield(Test):
    def setUp(self):
        Test.setUp(self)
        Common.start_new_game()
        Common.add_player() 
    
    def test_unique_external_event(self):
        pass 
    
    def test_Point(self):
        input = self.simulate_input('Point')
        self.assertEqual(Common.get_all_scores()[0], input.points)
        
    def test_Point_Light(self):
        input = self.simulate_input('Point_Light')
        pts = input.points[0]
        self.assertEqual(Common.get_all_scores()[0],  pts)
        input.lamp.set_level(1)
        self.simulate_input('Point_Light')
        pts += input.points[1]
        self.assertEqual(Common.get_all_scores()[0], pts)
        
    def test_Point_Light_Blink(self):
        input = Input.Input.instances['Point_Light_Blink']
        self.assertEqual(input.lamp.get_level(), "blink")
        off = False
        on = False   
        while off == False or on == False:
            level = input.lamp.get_level(ignore_blink=True)    
            if level == 0 and off == False: 
                self.simulate_input('Point_Light_Blink')
                off = True
            if level == 1 and on == False: 
                self.simulate_input('Point_Light_Blink')
                on = True
                
        self.assertEqual(Common.get_all_scores()[0], input.points[0] + input.points[1])
    
    def test_Spinner(self):
        input = Input.Input.instances['Spinner']
        self.simulate_input('Spinner')
        input.lamp.set_level(1)
        self.simulate_input('Spinner')
        self.assertEqual(input.lamp.get_level(), 0)
          
    def test_Target_Bank(self):
        target_0 = Input.Input.instances['0_Target_Bank']
        target_1 = Input.Input.instances['1_Target_Bank']
        
        self.assertEqual(target_0.lamp.get_level(), "blink")
        self.assertEqual(target_1.lamp.get_level(), "blink")
        
        input = self.simulate_input(target_0.name)
        pts = input.points[0]
        self.assertEqual(target_0.lamp.get_level(), 1)
        
        input = self.simulate_input(target_1.name)
        pts += input.points[0]
        self.assertEqual(target_1.lamp.get_level(), 1)
        
        self.assertEqual(target_1.parent.is_complete(), True)
        
        input = self.simulate_input(target_0.name)
        pts += input.points[1]
        input = self.simulate_input(target_0.name)
        pts += input.points[1]
        
        self.assertEqual(Common.get_all_scores()[0], pts)
        
    def test_Drop_Target_Bank(self):
        target_0 = Input.Input.instances['0_Drop_Target_Bank']
        target_1 = Input.Input.instances['1_Drop_Target_Bank']
        
        self.simulate_input(target_1.name)
        self.assertEqual(target_1.level, 1)
        self.simulate_input(target_0.name) # Reset execute apres la chute de la derniere cible
        self.assertEqual(target_0.level, 0)
        
    def test_Target_Bank_2_states(self):
        target_0 = Input.Input.instances['0_Target_Bank_2_states']
        target_1 = Input.Input.instances['1_Target_Bank_2_states']
        
        self.assertEqual(target_0.lamp.get_level(), 0)
        self.assertEqual(target_0.lamp.get_level(), 0)
        
        input = self.simulate_input(target_1.name)
        pts = input.points[0]
        input = self.simulate_input(target_0.name)
        pts += input.points[0]
        self.assertEqual(target_0.lamp.get_level(), "blink")
        self.assertEqual(target_1.lamp.get_level(), "blink")
        input = self.simulate_input(target_1.name)
        pts += input.points[0]
        input = self.simulate_input(target_0.name)
        pts += input.points[0]
        self.assertEqual(target_0.lamp.get_level(), 1)
        self.assertEqual(target_1.lamp.get_level(), 1)
        self.assertEqual(target_1.parent.is_complete(), True)
        input = self.simulate_input(target_1.name)
        pts += input.points[1]
        input = self.simulate_input(target_0.name)
        pts += input.points[1]
        self.assertEqual(Common.get_all_scores()[0], pts)       
        
    def test_Hole(self):
        pass
    
    def Outhole(self):
        pass
    
    def Trough(self):
        pass
        
        
####################################################################################################################################

if __name__ == "__main__": 
    unittest.main()   