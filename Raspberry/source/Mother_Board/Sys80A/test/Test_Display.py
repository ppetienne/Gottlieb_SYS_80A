# -*- coding: utf-8 -*-
import os, sys
import General
import Display_MB
import unittest
import time

dict_display = dict()
dict_display["Display"] = Display_MB.Display(nb_digits=2, segment=0, list_digits=0)

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manager = Display_MB.Display_Manager(dict_display.values())
        cls.manager.start()
        
    @classmethod
    def tearDownClass(cls):
        cls.manager.stop()
        
    def test_Display(self):
        display = dict_display["Display"]
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
        
####################################################################################################################################

if __name__ == "__main__": 
    unittest.main()   