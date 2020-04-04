# -*- coding: utf-8 -*-
import os, sys
from enum import Enum
import Display
import Output
import Input
from GUI_Simulator import Starter

class General_Status(Enum):
    ATTRACT_MODE = 1
    TEST_MODE = 2
    START = 3
    TILT = 4
    SLAM = 5
    
class Game_Operation_MB():
    def __init__(self, slam, use_gui=False):
        Input.Input.game_operation = self
        self.use_gui = use_gui
        self.status = General_Status.ATTRACT_MODE
        
        self.game = None
        self.dict_matrix = dict()
        self.dict_matrix_playfield = dict()
        self.list_target_bank = list()
        self.dict_solenoid = dict()
        self.dict_lamp = dict()
        self.dict_relay = dict()
        self.dict_display = dict()
        self.slam = slam
        self.instanciate_relay()
        
        self.display_manager = Display.Display_Manager(self.dict_display.values())
        self.input_manager = Input.Input_Manager(self.dict_matrix.values(), self.slam)
        self.blink_lamp_manager = Output.Blink_Lamp_Manager(self.dict_lamp.values())
    
    def power_on(self):
        self.display_manager.start()
        self.input_manager.start()
        self.blink_lamp_manager.start()
        self.attract_mode()
        self.dict_relay["Coin Lockout Coil"].set_level(1)
        
        if self.use_gui == True:
            Starter.Starter(self)
    
    def power_off(self):
        self.display_manager.stop()
        self.input_manager.stop()
        self.blink_lamp_manager.stop()
        
    def attract_mode(self):
        self.status = General_Status.ATTRACT_MODE
        
        for display in self.dict_display.values():
            display.attract_mode()
            
        for input in self.dict_matrix.values():
        	input.attract_mode()
	
    def set_tilt_level(self, value):
        self.dict_relay["Tilt"].set_level(value)
    
    def get_tilt_level():
        self.dict_relay["Tilt"].get_level()
    
    def set_game_over_level(self, value):
        self.dict_relay["Game Over Relay"].set_level(value)
    
    def get_game_over_level(self):
        return self.dict_relay["Game Over Relay"].get_level()
    
    def set_status_pinball(self, status):
        self.status = status
    
    def get_status_pinball(self):
        return self.status
    
    def start_game(self):
        if self.game != None:
            raise Exception("Game already in play")
        self.set_game_over_level(0)
        self.set_tilt_level(0)
        for input in self.input_playfield.values():
            input.new_game()
        self.status = General_Status.START
        self.game = Game_Play_MB(self)
        
    def end_game(self):
        self.game = None
        
    def add_player(self):
        if self.game.nb_player < 4:
            self.game.nb_player += 1
            Display.Player.get_by_num(self.game.nb_player).set_double_zero()
            player_added = True
        else:
            player_added = False
        
        return player_added
    
    def instanciate_relay(self):
        self.dict_relay["Game Over Relay"] = Output.Relay(num=0)
        self.dict_relay["Tilt"] = Output.Relay(num=1)
        self.dict_relay["Coin Lockout Coil"] = Output.Relay(num=2)
        
    def instanciate_matrix_playfield(self, name, obj):
        self.dict_matrix_playfield[name] = obj
        self.dict_matrix[name] = obj
        
class Game_Play_MB():
	def __init__(self, game_operation):
		pass