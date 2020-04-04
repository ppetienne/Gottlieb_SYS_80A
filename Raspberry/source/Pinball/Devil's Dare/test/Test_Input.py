# -*- coding: utf-8 -*-
import os, sys
import General
import Data_Save
import time
import unittest
import Input
import Options
import Display
import Output
import Contacts
from time import sleep


Input.Start(x=0, y=0)
tilt= Input.Tilt(x=0, y=1)
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
        
class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manager = Input.Input_Manager()
        cls.manager.start()
      
    def setUp(self):
        Data_Save.reset()
        Options.reset()
  
    def tearDown(self):
        pass
      
    @classmethod
    def tearDownClass(cls):
        cls.manager.stop()  
  
class Test_Common_Input(Test):
      
    def test_Input_Matrix(self):
        Input.Matrix.test.start(wait_time=0.001)
  
          
    def test_Start(self):            
        # Sans credit
        start = Input.Input.get_by_name('Start')
        start.sim.simulate()
        self.assertEqual(Common.infos_game['status'], Common.General_Status.ATTRACT_MODE)
          
        # Avec credit
        Common.set_credit(5)
        start.sim.simulate()
        self.assertEqual(Common.infos_game['status'], Common.General_Status.START)
        self.assertEqual(Common.infos_game['nb_players'], 1)
  
        for i in range(3):
            start.sim.simulate()
            self.assertEqual(Common.infos_game['nb_players'], i+2)
          
        self.assertEqual(Options.get("credits"), 1)
          
        # Check max 4 joueurs
        start.sim.simulate()
        self.assertEqual(Options.get("credits"), 1)
        
        Input.Input.get_by_name('Point').sim.simulate()
        start.sim.simulate()
        self.assertEqual(Common.infos_game['nb_players'], 1)
          
    def test_Credit(self):
        pass
           
    def test_Test(self):
        self.assertNotEqual(Common.infos_game['status'], Common.General_Status.TEST_MODE)
        input = Input.Input.instances["Test"]
        input.wait_time_before_end = 1
        input.wait_time_between_test = 0.001
           
        Input.Input.get_by_name('Test').sim.simulate()
        self.assertEqual(Display.Display.instances['Status'].get_credit(), 0)
        self.assertEqual(Common.infos_game['status'], Common.General_Status.TEST_MODE)
        Input.Input.get_by_name('Test').sim.simulate()
        self.assertEqual(Display.Display.instances['Status'].get_credit(), 1)
        time.sleep(1.2)
        self.assertNotEqual(Common.infos_game['status'], Common.General_Status.TEST_MODE)
           
        Input.Input.get_by_name('Test').sim.simulate()
        self.assertEqual(Common.infos_game['status'], Common.General_Status.TEST_MODE)
        Input.Input.get_by_name('Test').sim.simulate()
        Input.Input.get_by_name('Tilt').sim.simulate()
        self.assertNotEqual(Common.infos_game['status'], Common.General_Status.TEST_MODE)
           
        Input.Input.get_by_name('Test').sim.simulate()
        self.assertEqual(Common.infos_game['status'], Common.General_Status.TEST_MODE)
        Input.Input.get_by_name('Test').sim.simulate()
        Input.Input.get_by_name('Slam').set_level(1)
        self.assertNotEqual(Common.infos_game['status'], Common.General_Status.TEST_MODE)
           
    def test_Slam(self):
        Input.slam.set_level(1)
        self.assertEqual(Common.infos_game['status'], Common.General_Status.ATTRACT_MODE)
   
class Test_Playfield(Test):
    def setUp(self):
        Test.setUp(self)
        Common.start_new_game()
   
    def test_Point(self):
        input = Input.Input.get_by_name('Point')
        input.sim.simulate()
        self.assertEqual(Common.get_all_scores()[0], input.points)
            
    def test_Point_Light(self):
        input = Input.Input.get_by_name('Point_Light')
        input.sim.simulate()
        pts = input.points[0]
        self.assertEqual(Common.get_all_scores()[0],  pts)
        input.lamp.set_level(1)
        Input.Input.get_by_name('Point_Light').sim.simulate()
        pts += input.points[1]
        self.assertEqual(Common.get_all_scores()[0], pts)
            
    def test_Point_Light_Blink(self):
        input = Input.Input.get_by_name('Point_Light_Blink')
        self.assertEqual(input.lamp.get_level(), "blink")
        off = False
        on = False
    
        while off == False or on == False:
            level = input.lamp.get_level(ignore_blink=True)    
            if level == 0 and off == False: 
                Input.Input.get_by_name('Point_Light_Blink').sim.simulate()
                off = True
            if level == 1 and on == False: 
                Input.Input.get_by_name('Point_Light_Blink').sim.simulate()
                on = True
                    
        self.assertEqual(Common.get_all_scores()[0], input.points[0] + input.points[1])
        
    def test_Spinner(self):
        input = Input.Input.get_by_name('Spinner')
        Input.Input.get_by_name('Spinner').sim.simulate()
        input.lamp.set_level(1)
        Input.Input.get_by_name('Spinner').sim.simulate()
        self.assertEqual(input.lamp.get_level(), 0)
              
    def test_Target_Bank(self):
        target_0 = Input.Input.get_by_name('1 Target_Bank')
        target_1 = Input.Input.get_by_name('2 Target_Bank')
            
        self.assertEqual(target_0.lamp.get_level(), "blink")
        self.assertEqual(target_1.lamp.get_level(), "blink")
            
        target_0.sim.simulate()
        pts = target_0.points[0]
        self.assertEqual(target_0.lamp.get_level(), 1)
            
        target_1.sim.simulate()
        pts += target_1.points[0]
        self.assertEqual(target_1.lamp.get_level(), 1)
            
        self.assertEqual(Common.get_all_scores()[0], pts)
        self.assertEqual(target_1.parent.is_complete(), True)
            
        self.assertEqual(target_1.lamp.get_level(), 1)
        self.assertEqual(target_0.lamp.get_level(), 1)
            
        target_0.sim.simulate()
        pts += target_0.points[1]
        self.assertEqual(Common.get_all_scores()[0], pts)
        target_1.sim.simulate()
        pts += target_1.points[1]
            
        self.assertEqual(Common.get_all_scores()[0], pts)
            
    def test_Drop_Target_Bank(self):
        target_0 = Input.Input.get_by_name('1 Drop_Target_Bank')
        target_1 = Input.Input.get_by_name('2 Drop_Target_Bank')
            
        Input.Input.get_by_name(target_1.name).sim.simulate()
        self.assertEqual(target_1.level, 1)
        Input.Input.get_by_name(target_0.name).sim.simulate() # Reset execute apres la chute de la derniere cible
        self.assertEqual(target_0.level, 0)
            
    def test_Target_Bank_2_states(self):
        target_0 = Input.Input.get_by_name('1 Target_Bank_2_states')
        target_1 = Input.Input.get_by_name('2 Target_Bank_2_states')
            
        self.assertEqual(target_0.lamp.get_level(), 0)
        self.assertEqual(target_0.lamp.get_level(), 0)
            
        target_0.sim.simulate()
        pts = target_0.points[0]
        target_1.sim.simulate()
        pts += target_1.points[0]
        self.assertEqual(target_0.lamp.get_level(), "blink")
        self.assertEqual(target_1.lamp.get_level(), "blink")
        target_1.sim.simulate()
        pts += target_1.points[0]
        target_0.sim.simulate()
        pts += target_0.points[0]
        self.assertEqual(target_1.parent.is_complete(), True)
        self.assertEqual(target_0.lamp.get_level(), 1)
        self.assertEqual(target_1.lamp.get_level(), 1)
        target_1.sim.simulate()
        pts += target_1.points[1]
        target_0.sim.simulate()
        pts += target_0.points[1]
        self.assertEqual(Common.get_all_scores()[0], pts)       
            
    def test_Hole(self):
        pass        
       
    def test_OutHole(self):
        outhole = Input.Input.get_by_name('OutHole')
        outhole_sol = Output.Solenoid.instances["OutHole"]
           
        #Quand autre balle doit sortir, cas general
        self.assertEqual(Common.infos_game['current_ball'], 1)
        outhole.sim.simulate()
        self.assertEqual(Common.infos_game['current_ball'], 2)
        #Avec tilt active
        #Quand derniere ball plusieurs joueurs
        #Avec shoot again active      
      
####################################################################################################################################
def suite(test_General=True, test_Common_Input=True, test_Playfield=True):
    suite = unittest.TestSuite()
    if test_General:
        suite.addTest(Test_General('test_general'))
    if test_Common_Input:
        suite.addTest(Test_Common_Input('test_Start'))
        suite.addTest(Test_Common_Input('test_Credit'))
        suite.addTest(Test_Common_Input('test_Test'))
        suite.addTest(Test_Common_Input('test_Slam'))
    if test_Playfield:
        suite.addTest(Test_Playfield('test_Point'))
        suite.addTest(Test_Playfield('test_Point_Light'))
        suite.addTest(Test_Playfield('test_Point_Light_Blink'))
        suite.addTest(Test_Playfield('test_Spinner'))
        suite.addTest(Test_Playfield('test_Target_Bank'))
        suite.addTest(Test_Playfield('test_Drop_Target_Bank'))
        suite.addTest(Test_Playfield('test_Target_Bank_2_states'))
        suite.addTest(Test_Playfield('test_Hole'))
        suite.addTest(Test_Playfield('test_OutHole'))
    return suite

def unit_suite_general(name):
    return unittest.TestSuite().addTest(Test_General(name))
def unit_suite_common(name):
    return unittest.TestSuite().addTest(Test_Common_Input(name))
def unit_suite_playfield(name):
    return unittest.TestSuite().addTest(Test_Playfield(name))

if __name__ == "__main__": 
    runner = unittest.TextTestRunner()
    runner.run(suite())   