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


Input.Start(x=0, y=0)
Input.Slam(pin=Contacts.Pin())
Input.Tilt(x=0, y=1)
Input.Test(x=0, y=2)
Input.Credit(x=0, y=3, name="Credit", value=2)

# Input Playfield
Input.Point(x=0, y=4, name="Point", points=1)
Input.Point_Light_Blink(x=0, y=5, name="Point_Light_Blink", num_lamp=1, points=[1,2])
Input.Point_Light(x=0, y=6, name="Point_Light", num_lamp=10, points=[1,2])
Input.Spinner(x=0, y=7, name="Spinner", num_lamp=10, points=[1,2])

Output.Solenoid(num=1, name="Drop_Target_Bank")
temp_targets = Input.Target_Bank_Drop(name="Drop_Target_Bank")

Input.Target_Drop(x=1, y=0, parent=temp_targets, position_enfant=0, num_lamp=2, points=[1,2])
Input.Target_Drop(x=1, y=1, parent=temp_targets, position_enfant=1, num_lamp=3, points=[2,3])

temp_targets = Input.Target_Bank(name="Target_Bank")
Input.Target(x=1, y=2, parent=temp_targets, position_enfant=0, num_lamp=4, points=[1,2])
Input.Target(x=1, y=3, parent=temp_targets, position_enfant=1, num_lamp=5, points=[2,3])
             
temp_targets = Input.Target_Bank(name="Target_Bank_2_states")
Input.Target(x=1, y=4, parent=temp_targets, position_enfant=0, num_lamp=6, points=[1,2], nb_states=2)
Input.Target(x=1, y=5, parent=temp_targets, position_enfant=1, num_lamp=7, points=[2,3], nb_states=2)

Output.Solenoid(num=2, name="Hole")
Input.Hole(x=1, y=6, name="Hole")

Output.Solenoid(num=3, name="OutHole")
Input.OutHole(x=1, y=7, name="OutHole")

class General(unittest.TestCase):
    
    def test_general(self):
        Data_Save.reset()
        Options.reset()
        
        Common.power_on()
        
        for i in range(4):
            Input.General_Input.get_by_name('Credit').simulate()
            Input.General_Input.get_by_name('Start').simulate()
        
        for i in range(Options.get('nb_balls')):
            for i in range(4):
                #Input.General_Input.simulate('OutHole')
                pass
        
        Common.power_off()
        
class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Common.power_on()
    
    def setUp(self):
        Data_Save.reset()
        Options.reset()
        Common.attract_mode()

    def tearDown(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        Common.power_off()    

class Test_Common_Input(Test):
    
    def test_Input_Matrix(self):
        Input.Matrix.test.start(0.001)
        
    def test_Start(self):            
        # Sans credit
        Options.set("credits", 0)
        Input.General_Input.get_by_name('Start').simulate()
        self.assertEqual(Common.infos_game['status'], Common.General_Status.ATTRACT_MODE)
        
        # Avec credit
        Options.set("credits", 5)
        Input.General_Input.get_by_name('Start').simulate()
        self.assertEqual(Common.infos_game['status'], Common.General_Status.START)
        self.assertEqual(Common.infos_game['nb_players'], 1)

        for i in range(3):
            Input.General_Input.get_by_name('Start').simulate()
            if i == 3:
                self.assertEqual(Common.infos_game['nb_players'], i+1)
            else:
                self.assertEqual(Common.infos_game['nb_players'], i+2)
        self.assertEqual(Options.get("credits"), 1)
        
        for input in Input.Playfield.instances.values():
            self.assertEqual(input.activated, True)
        
    def test_Credit(self):
        pass
        
    def test_Test(self):
        self.assertEqual(Common.TEST_MODE, False)
        input = Input.General_Input.instances["Test"]
        input.wait_time_before_end = 1
        input.wait_time_between_test = 0.001
        
        Input.General_Input.get_by_name('Test').simulate()
        self.assertEqual(Display.Display.instances['Status'].get_credit(), 0)
        self.assertEqual(Common.TEST_MODE, True)
        Input.General_Input.get_by_name('Test').simulate()
        self.assertEqual(Display.Display.instances['Status'].get_credit(), 1)
        time.sleep(1.2)
        self.assertEqual(Common.TEST_MODE, False)
        
        Input.General_Input.get_by_name('Test').simulate()
        self.assertEqual(Common.TEST_MODE, True)
        Input.General_Input.get_by_name('Test').simulate()
        Input.General_Input.get_by_name('Tilt').simulate()
        self.assertEqual(Common.TEST_MODE, False)
        
        Input.General_Input.get_by_name('Test').simulate()
        self.assertEqual(Common.TEST_MODE, True)
        Input.General_Input.get_by_name('Test').simulate()
        Input.General_Input.get_by_name('Slam').simulate()
        self.assertEqual(Common.TEST_MODE, False)
        
    def test_Slam(self):
        Input.General_Input.get_by_name('Slam').simulate()
        self.assertEqual(Common.infos_game['status'], Common.General_Status.ATTRACT_MODE)

class Test_Playfield(Test):
    def setUp(self):
        Test.setUp(self)
        Common.start_new_game()
        Common.add_player() 

    def test_Point(self):
        input = Input.General_Input.get_by_name('Point')
        input.simulate()
        self.assertEqual(Common.get_all_scores()[0], input.points)
        
    def test_Point_Light(self):
        input = Input.General_Input.get_by_name('Point_Light')
        input.simulate()
        pts = input.points[0]
        self.assertEqual(Common.get_all_scores()[0],  pts)
        input.lamp.set_level(1)
        Input.General_Input.get_by_name('Point_Light').simulate()
        pts += input.points[1]
        self.assertEqual(Common.get_all_scores()[0], pts)
        
    def test_Point_Light_Blink(self):
        input = Input.General_Input.get_by_name('Point_Light_Blink')
        self.assertEqual(input.lamp.get_level(), "blink")
        off = False
        on = False

        while off == False or on == False:
            level = input.lamp.get_level(ignore_blink=True)    
            if level == 0 and off == False: 
                Input.General_Input.get_by_name('Point_Light_Blink').simulate()
                off = True
            if level == 1 and on == False: 
                Input.General_Input.get_by_name('Point_Light_Blink').simulate()
                on = True
                
        self.assertEqual(Common.get_all_scores()[0], input.points[0] + input.points[1])
    
    def test_Spinner(self):
        input = Input.General_Input.get_by_name('Spinner')
        Input.General_Input.get_by_name('Spinner').simulate()
        input.lamp.set_level(1)
        Input.General_Input.get_by_name('Spinner').simulate()
        self.assertEqual(input.lamp.get_level(), 0)
          
    def test_Target_Bank(self):
        target_0 = Input.General_Input.get_by_name('1 Target_Bank')
        target_1 = Input.General_Input.get_by_name('2 Target_Bank')
        
        self.assertEqual(target_0.lamp.get_level(), "blink")
        self.assertEqual(target_1.lamp.get_level(), "blink")
        
        target_0.simulate()
        pts = target_0.points[0]
        self.assertEqual(target_0.lamp.get_level(), 1)
        
        target_1.simulate()
        pts += target_1.points[0]
        self.assertEqual(target_1.lamp.get_level(), 1)
        
        self.assertEqual(Common.get_all_scores()[0], pts)
        self.assertEqual(target_1.parent.is_complete(), True)
        
        self.assertEqual(target_1.lamp.get_level(), 1)
        self.assertEqual(target_0.lamp.get_level(), 1)
        
        target_0.simulate()
        pts += target_0.points[1]
        self.assertEqual(Common.get_all_scores()[0], pts)
        target_1.simulate()
        pts += target_1.points[1]
        
        self.assertEqual(Common.get_all_scores()[0], pts)
        
    def test_Drop_Target_Bank(self):
        target_0 = Input.General_Input.get_by_name('1 Drop_Target_Bank')
        target_1 = Input.General_Input.get_by_name('2 Drop_Target_Bank')
        
        Input.General_Input.get_by_name(target_1.name).simulate()
        self.assertEqual(target_1.level, 1)
        Input.General_Input.get_by_name(target_0.name).simulate() # Reset execute apres la chute de la derniere cible
        self.assertEqual(target_0.level, 0)
        
    def test_Target_Bank_2_states(self):
        target_0 = Input.General_Input.get_by_name('1 Target_Bank_2_states')
        target_1 = Input.General_Input.get_by_name('2 Target_Bank_2_states')
        
        self.assertEqual(target_0.lamp.get_level(), 0)
        self.assertEqual(target_0.lamp.get_level(), 0)
        
        target_0.simulate()
        pts = target_0.points[0]
        target_1.simulate()
        pts += target_1.points[0]
        self.assertEqual(target_0.lamp.get_level(), "blink")
        self.assertEqual(target_1.lamp.get_level(), "blink")
        target_1.simulate()
        pts += target_1.points[0]
        target_0.simulate()
        pts += target_0.points[0]
        self.assertEqual(target_1.parent.is_complete(), True)
        self.assertEqual(target_0.lamp.get_level(), 1)
        self.assertEqual(target_1.lamp.get_level(), 1)
        target_1.simulate()
        pts += target_1.points[1]
        target_0.simulate()
        pts += target_0.points[1]
        self.assertEqual(Common.get_all_scores()[0], pts)       
        
    def test_Hole(self):
        pass        
    
    def test_OutHole(self):
        pass
      
####################################################################################################################################

if __name__ == "__main__": 
    unittest.main()   