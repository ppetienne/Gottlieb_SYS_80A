# -*- coding: utf-8 -*-
import os, sys
import General
print(sys.path)
import Display
import unittest
import time

dict_display = dict()
dict_display["Test"] = Display.Display(nb_digits=2, segment=0, list_digits=0)
dict_display["Status"] = Display.Status()
dict_display["Timer"] = Display.Timer()
dict_display["Bonus"] = Display.Bonus()
dict_display["Player"] = Display.Player(1)

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manager = Display.Display_Manager(dict_display.values())
        cls.manager.start()
        
    @classmethod
    def tearDownClass(cls):
        cls.manager.stop()
        
    def test_Display(self):
        display = dict_display["Test"]
        display.set_value(1, increment=True)
        self.assertEqual(display.get_int_value(), 1)
        display.set_value(1, increment=True)
        self.assertEqual(display.get_int_value(), 2)
        display.set_value(1)
        self.assertEqual(display.get_int_value(), 1)
        display.set_value("")
        self.assertEqual(display.get_int_value(), 0)
        self.assertEqual(display.get_value(), "")
        display.set_all_zero()
        self.assertEqual(display.get_value(), "00")
        self.assertEqual(display.get_displayed(), True)
        display.set_displayed(False)
        self.assertEqual(display.get_displayed(), False)
        
    def test_Player(self):
        display = dict_display["Player"]
        display.set_value(1)
        self.assertEqual(display.get_int_value(), 1)
        display.blink(1)
        self.assertEqual(display.is_blinking(), True)
        display.blink(0)
        self.assertEqual(display.get_displayed(), True)
        self.assertEqual(display.is_blinking(), False)
        
        self.assertEqual(display.get_int_value(), 1)
        display.set_all_zero()
        self.assertEqual(display.get_value(), "0000000")
        
    def test_Bonus(self):
        display = Display.Bonus()
    
    def test_Timer(self):
        display = Display.Timer()
    
    def test_Status(self):
        display = Display.Status()
        display.set_credit(10)
        self.assertEqual(display.get_value(), "10  ")
        display.set_credit(5)
        self.assertEqual(display.get_value(), "5  ")
        display.set_status(10)
        self.assertEqual(display.get_value(), "510")
        display.set_status(5)
        self.assertEqual(display.get_value(), "5 5")
        
####################################################################################################################################

if __name__ == "__main__": 
    unittest.main()   