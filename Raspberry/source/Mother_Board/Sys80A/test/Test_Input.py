# -*- coding: utf-8 -*-
import os, sys
import General
import time
import unittest
from Output import Lamp, Solenoid
import Input_MB

def test_set_high_level(input):
    input.test_variable = 1

def test_set_low_level(input):
    input.test_variable = 0

lamp = Lamp(num=4)
solenoid = Solenoid(num=1)
target_bank = Input_MB.Target_Bank_MB()
target_bank_drop = Input_MB.Target_Bank_Drop_MB(solenoid)

slam = Input_MB.Slam_MB()

dict_input_matrix = dict()
dict_input_matrix["Matrix"] = Input_MB.Matrix(x=0, y=0)
dict_input_matrix["Matrix_Playfield"] = Input_MB.Playfield(x=0, y=1)
dict_input_matrix["Start"] = Input_MB.Start_MB(x=0, y=2)
dict_input_matrix["Test"] = Input_MB.Test_MB(x=0, y=3)
dict_input_matrix["Credit"] = Input_MB.Credit_MB(credit_value=1, nb_coin_needed=2, x=0, y=4)
dict_input_matrix["Tilt"] = Input_MB.Tilt_MB(x=0, y=5)
dict_input_matrix["Point"] = Input_MB.Point_MB(points=1, x=0, y=6)
dict_input_matrix["Point_Light"] = Input_MB.Point_Light_MB(points=1, lamp=lamp, x=0, y=7)
dict_input_matrix["Point_Light_Blink"] = Input_MB.Point_Light_Blink_MB(points=1, lamp=lamp, x=1, y=0)
dict_input_matrix["Target"] = Input_MB.Target_MB(points=1, lamp=lamp, target_bank=target_bank, x=1, y=1)
dict_input_matrix["Target_Drop"] = Input_MB.Target_Drop_MB(points=1, lamp=lamp, target_bank=target_bank_drop, x=1, y=2)
dict_input_matrix["Playfield_Hole"] = Input_MB.Playfield_Hole_MB(solenoid=solenoid, x=1, y=3)
dict_input_matrix["OutHole"] = Input_MB.OutHole_MB(solenoid=solenoid, x=1, y=4)

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manager = Input_MB.Input_Manager(dict_input_matrix.values(), slam)
        cls.manager.start()
        
    def test_Input(self):
        input = Input_MB.Input(test_set_high_level, test_set_low_level)
        input2 = Input_MB.Input()
 
        self.assertEqual(input.test_variable, None)
        self.assertEqual(input.get_level(), 0)
         
        input.set_level(1)
        self.assertEqual(input.get_level(), 1)
        self.assertEqual(input.test_variable, 1)
         
        input.set_level(0)
        self.assertEqual(input.get_level(), 0)
        self.assertEqual(input.test_variable, 0)
         
        input2.set_high_function_event(test_set_high_level)
        input2.set_low_function_event(test_set_low_level)
         
        input2.set_level(1)
        self.assertEqual(input2.test_variable, 1)
         
        input2.set_level(0)
        self.assertEqual(input2.test_variable, 0)
    
    def test_Matrix_Sim(self):
        matrix_obj = dict_input_matrix["Matrix"]
         
        matrix_obj.sim.simulate(1)
        begin_time = time.time()
        while matrix_obj.get_level() == 0 and time.time() - begin_time < Input_MB.Matrix_Sim.MAX_ALLOWED_DELAY:
            time.sleep(0.001)
        self.assertEqual(matrix_obj.get_level(), 1)
         
        matrix_obj.sim.simulate(0)
        begin_time = time.time()
        while matrix_obj.get_level() == 1 and time.time() - begin_time < Input_MB.Matrix_Sim.MAX_ALLOWED_DELAY:
            time.sleep(0.01)
        self.assertEqual(matrix_obj.get_level(), 0)
         
        matrix_obj.set_high_function_event(test_set_high_level)
        matrix_obj.sim.simulate()
        self.assertEqual(matrix_obj.test_variable, 1)
         
        matrix_obj.set_low_function_event(test_set_low_level)
        matrix_obj.sim.simulate()
        self.assertEqual(matrix_obj.test_variable, 0)
    
    def test_Matrix(self):
        matrix_obj = dict_input_matrix["Matrix"]
        matrix_obj2 = Input_MB.Matrix.get_by_xy(dict_input_matrix.values(), matrix_obj.x, matrix_obj.y)
        self.assertEqual(matrix_obj, matrix_obj)
        
        matrix_obj.set_high_function_event(test_set_high_level)
        
        Input_MB.Matrix.activated = False
        matrix_obj.sim.simulate()
        self.assertEqual(matrix_obj.test_variable, None)

        Input_MB.Matrix.activated = True
        matrix_obj.sim.simulate()
        self.assertEqual(matrix_obj.test_variable, 1)
        
    def test_Start(self):
        pass
    
    def test_Tilt(self):
        pass
    
    def test_Test(self):
        pass
    
    def test_Credit(self):
        credit_obj = dict_input_matrix["Credit"]
        credit_obj.sim.simulate()
        self.assertEqual(credit_obj.curent_nb_coins, 1)
        credit_obj.sim.simulate()
        self.assertEqual(credit_obj.curent_nb_coins, 2)
        self.assertEqual(credit_obj.check_nb_coin_for_credit(), True)
        self.assertEqual(credit_obj.curent_nb_coins, 0)
    
    def test_Point(self):
        pass
    
    def test_Point_Light(self):
        pass
    
    def test_Point_Light_Blink(self):
        pass
    
    def test_Target(self):
        target_obj = dict_input_matrix["Target"]
        target_obj.sim.simulate(1)
        self.assertEqual(target_obj.target_bank.is_complete(), True)
    
    def test_Target_Drop(self):
        target_obj = dict_input_matrix["Target_Drop"]
        target_obj.sim.simulate(1)
        self.assertEqual(target_obj.target_bank.is_complete(), True)

        begin_time = time.time()
        while target_obj.target_bank.solenoid.get_level() == 0 and time.time() - begin_time < 1:
            time.sleep(0.01)
        self.assertEqual(target_obj.target_bank.solenoid.get_level(), 1)
        begin_time = time.time()
        while target_obj.target_bank.solenoid.get_level() == 1 and time.time() - begin_time < 1:
            time.sleep(0.01)
        self.assertEqual(target_obj.target_bank.solenoid.get_level(), 0)
        
    def test_Playfield_Hole(self):
        hole_obj = dict_input_matrix["Playfield_Hole"]
        hole_obj.eject_ball()
    
    def test_OutHole(self):
        hole_obj = dict_input_matrix["OutHole"]
        hole_obj.eject_ball()
    
    @classmethod
    def tearDownClass(cls):
        cls.manager.stop()  


if __name__ == "__main__":
    unittest.main()  