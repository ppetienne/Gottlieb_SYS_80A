# -*- coding: utf-8 -*-
import General
import Display
import unittest
import time

Display.Timer()
Display.Bonus()
Display.Display(nb_digits=2, name="Test", segment=0, list_digits=0)

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Display.manager.start()
        
    @classmethod
    def tearDownClass(cls):
        Display.manager.stop()
        
    def test_Display(self):
        display = Display.Display.get_by_name("Test")
        display.set_int_value(1, increment=True)
        self.assertEqual(display.get_int_value(), 1)
        display.set_int_value(1, increment=True)
        self.assertEqual(display.get_int_value(), 2)
        display.set_int_value(1)
        self.assertEqual(display.get_int_value(), 1)
        display.set_all_zero()
        self.assertEqual(display.get_value(), "00")
        Display.Display.test.start(0.001)
        
    def test_Player(self):
        display = Display.Display.get_by_name("p1")
        display.set_int_value(1)
        self.assertEqual(display.get_int_value(), 1)
        display.blink(1)
        self.assertEqual(display.is_blinking(), True)
        display.blink(0)
        self.assertEqual(display.is_blinking(), False)
        self.assertEqual(display.get_int_value(), 1)
        display.set_all_zero()
        self.assertEqual(display.get_value(), "0000000")
        
    def test_Bonus(self):
        pass
    
    def test_Timer(self):
        pass
    
    def test_Status(self):
        display = Display.Display.get_by_name("Status")
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