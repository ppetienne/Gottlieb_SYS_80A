# -*- coding: utf-8 -*-
import General
import Output
import unittest
import time
import os

class Test(unittest.TestCase):
    def test_Lamp_Latch(self):
        self.assertEqual(len(Output.Lamp_Latch.instances), 12)
    
    def test_Lamp_Control(self):
        self.assertEqual(len(Output.Lamp_Control.instances), 4)
    
    def test_Output_Driver(self): 
        output = Output.Output_Driver(name="Test", lamp_control=Output.Lamp_Control.instances[1], lamp_latch=Output.Lamp_Latch.instances[1])
        output.set_level(1)
        self.assertEqual(output.get_level(), 1)
        output.set_level(0)
        self.assertEqual(output.get_level(), 0)
        
    def test_Lamp(self):
        lamp = Output.Lamp(name="Test", lamp_control=Output.Lamp_Control.instances[4], lamp_latch=Output.Lamp_Latch.instances[1])
        lamp.set_level(1)
        self.assertEqual(lamp.get_level(), 1)
        lamp.set_level(0)
        self.assertEqual(lamp.get_level(), 0)
        lamp.blink(1)
        self.assertEqual(lamp.get_level(), "blink")
        lamp.blink(0)
        self.assertEqual(lamp.get_level(), 0)
        lamp.blink(1, speed=0.1, timeout=0.5)
        time.sleep(1)
        self.assertEqual(lamp.get_level(), 0)
        lamp.blink(1)
        lamp.blink(1)
        self.assertEqual(lamp.get_level(), "blink")
        lamp.blink(0)
        
        lamp.blink(1)
        off = False
        on = False 
        begin_time = time.time()  
        timer = 0     
        while (off == False or on == False) and timer < 2:
            level = lamp.get_level(ignore_blink=True)    
            if level == 0 and off == False: 
                off = True
            if level == 1 and on == False:
                on = True
            timer = time.time() - begin_time
        self.assertTrue(timer < 2) 
        lamp.reset()
        Output.Lamp.test(0.01)
        
    def test_Solenoid(self):
        sol = Output.Solenoid.instances[9] # arbitraire
        sol.name = "test"
        self.assertEqual(sol.name, "test")
        sol.set_level(1)
        sol.set_level(0) # Pas possible de tester, juste verifier qu'aucune exception remonte
        sol.pulse()
        Output.Solenoid.test(0.001)
    
    def test_Sound(self):
        #Sequence : background > short_sound > nouveau short_sound avant fin ancien > background)
        Output.sound_manager.start()
        Output.sound_manager.set_background_sound(os.path.dirname(os.path.abspath(__file__)) + "\\files\\background.wav")
        sound = Output.Short_Sound(os.path.dirname(os.path.abspath(__file__)) + "\\files\\son1.wav")
        Output.sound_manager.start_background()
        time.sleep(1)
        sound.play()
        time.sleep(0.5)
        sound.play()
        time.sleep(3)
        Output.sound_manager.stop_background()
        Output.sound_manager.stop()
        
####################################################################################################################################

if __name__ == "__main__": 
    unittest.main()   