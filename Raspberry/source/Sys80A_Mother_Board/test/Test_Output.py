# -*- coding: utf-8 -*-
import General
import Display
import Output
import unittest
import time
import os

class Test(unittest.TestCase):
    def tes_Output(self):
        output = Output.Output(num=1)
        output.set_level(1)
        self.assertEqual(output.get_level(), 1)
        output.pulse()
        
        output_filtered = Output.Output.get_by_num({"Output":output}, 1)
        self.assertEqual(output, output_filtered)
        
        Output.Output.pulse_list((output))
    
    def test_Lamp_Latch(self):
        self.assertEqual(len(Output.Lamp_Latch.instances), 12)
    
    def test_Lamp_Control(self):
        self.assertEqual(len(Output.Lamp_Control.instances), 4)
    
    def test_Driver_Board(self): 
        output = Output.Driver_Board(num=1)
        output.set_level(1)
        self.assertEqual(output.get_level(), 1)
        output.set_level(0)
        self.assertEqual(output.get_level(), 0)
    
    def test_Relay(self):
        relay = Output.Relay(num=1)
        relay.set_level(1)
        relay.set_level(0) # Pas possible de tester, juste verifier qu'aucune exception remonte
        relay.pulse()
    
    def test_Lamp(self):
        lamp = Output.Lamp(num=4)
        manager = Output.Blink_Lamp_Manager((lamp,))
        manager.start()
        lamp.set_level(1)
        self.assertEqual(lamp.get_level(), 1)
        lamp.set_level(0)
        self.assertEqual(lamp.get_level(), 0)
        lamp.set_level("blink")
        self.assertEqual(lamp.is_blinking(), True)
        lamp.set_level(0)
        self.assertEqual(lamp.get_level(), 0)
        self.assertEqual(lamp.is_blinking(), False)
        
        lamp.set_level("blink")
        off = False
        on = False 
        begin_time = time.time()  
        timer = 0     
        while (off == False or on == False) and timer < 2:
            level = lamp.get_level()    
            if level == 0 and off == False: 
                off = True
            if level == 1 and on == False:
                on = True
            timer = time.time() - begin_time
        self.assertTrue(timer < 2) 
        lamp.set_level(0)
        
        manager.stop()
        
    def test_Solenoid(self):
        sol = Output.Solenoid(num=1) # arbitraire
        sol.set_level(1)
        sol.set_level(0) # Pas possible de tester, juste verifier qu'aucune exception remonte
        sol.pulse()
    
#     def test_Sound(self):
#         #Sequence : background > short_sound > nouveau short_sound avant fin ancien > background)
#         Output.sound_manager.start()
#         Output.sound_manager.set_background_sound(os.path.dirname(os.path.abspath(__file__)) + r"/files/background.wav")
#         sound = Output.Short_Sound(os.path.dirname(os.path.abspath(__file__)) + r"/files/son1.wav")
#         Output.sound_manager.start_background()
#         time.sleep(1)
#         sound.play()
#         time.sleep(0.5)
#         sound.play()
#         time.sleep(3)
#         Output.sound_manager.stop_background()
#         Output.sound_manager.stop()
        
####################################################################################################################################

if __name__ == "__main__": 
    unittest.main()   