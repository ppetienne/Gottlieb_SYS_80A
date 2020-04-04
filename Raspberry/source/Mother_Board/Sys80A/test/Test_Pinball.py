# -*- coding: utf-8 -*-
import os, sys
import General
import Pinball
import Input
import unittest
import time

class Test_Game_Operation_MB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass
        
    @classmethod
    def tearDownClass(cls):
        pass
        
    def test_General(self):
        game_operation_obj = Pinball.Game_Operation_MB(slam=Input.Slam_MB())
        game_operation_obj.power_on()
        self.assertEqual(game_operation_obj.status, Pinball.General_Status.ATTRACT_MODE)
        game_operation_obj.power_off()

class Test_Game_Play_MB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass
        
    @classmethod
    def tearDownClass(cls):
        pass
    
    def test_General(self):
        game_play_obj = Pinball.Game_Play()
        
####################################################################################################################################

if __name__ == "__main__": 
    unittest.main()   