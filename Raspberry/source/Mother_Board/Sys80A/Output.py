# -*- coding: utf-8 -*-
################################################################################
# Display
# 
#
################################################################################
from Common.Event import Event
from Common.Thread_Manager import Thread_Manager
from Contacts import conn

import time
import operator

################################################################################
class Output():
	def __init__(self, num):
		self.num = num
		self.event = Event.Event()
		self._level = 0
	
	def set_level(self, level):
		self._level = level
		self.event.fire(self)
	
	def get_level(self):
		return self._level
	
	def get_by_num(dict_obj, num):
		return [obj for obj in dict_obj.values() if obj.num == num][0]
	
	def pulse(self, wait_time=0.5):
		self.set_level(1)
		time.sleep(wait_time)
		self.set_level(0)
		time.sleep(wait_time)
	
	def pulse_list(list_to_pulse, wait_time=0.5):
		for output in list_to_pulse:
			output.set_level(1)
		time.sleep(wait_time)
		for output in list_to_pulse:
			output.set_level(0)
		time.sleep(wait_time)
		
################################################################################	
class Mother_Board(Output):
	def __init__(self, pin, num):
		super().__init__(num)
		self.pin = pin
		
	def set_level(self, level):
		self.pin.set_level(level)
		super().set_level(level)		
		
################################################################################
class Solenoid(Mother_Board):
	def __init__(self, num, **args):
		pin=Solenoid.get_pin(num)
		super().__init__(num=num, pin=pin, **args)
	
	def get_pin(num):
		if num == 1:
			pin=conn.J4['S']
		elif num == 2:
			pin=conn.J4['X']
		elif num == 3:
			pin=conn.J4[24]
		elif num == 4:
			pin=conn.J4[23]
		elif num == 5:
			pin=conn.J4['R']
		elif num == 6:
			pin=conn.J4['U']
		elif num == 7:
			pin=conn.J4[22]	
		elif num == 8:
			pin=conn.J4[21]
		elif num == 9:
			pin=conn.J4['T']
		return pin

################################################################################
class Sound(Mother_Board):
	def __init__(self, **args):
		""" Construit un objet Display
		Keyword arguments:
		*** -- ***
		"""
		super().__init__(**args)
 				
################################################################################
class Lamp_Latch(Mother_Board):
	instances = dict()
	def __init__(self, **args):
		""" Construit un objet Display
		Keyword arguments:
		*** -- ***
		"""
		super().__init__(**args)
		Lamp_Latch.instances[self.num] = self
		
Lamp_Latch(pin=conn.J4['P'], num=12)
Lamp_Latch(pin=conn.J4['N'], num=11)
Lamp_Latch(pin=conn.J4['L'], num=10)
Lamp_Latch(pin=conn.J4['M'], num=9)
Lamp_Latch(pin=conn.J4['J'], num=8)
Lamp_Latch(pin=conn.J4['K'], num=7)
Lamp_Latch(pin=conn.J4['F'], num=6)
Lamp_Latch(pin=conn.J4['H'], num=5)
Lamp_Latch(pin=conn.J4['D'], num=4)
Lamp_Latch(pin=conn.J4['E'], num=3)
Lamp_Latch(pin=conn.J4[3], num=2)        
Lamp_Latch(pin=conn.J4['C'], num=1)		

################################################################################
class Lamp_Control(Mother_Board):
	instances = dict()
	def __init__(self, **args):
		""" Construit un objet Display
		Keyword arguments:
		*** -- ***
		"""
		super().__init__(**args)
		Lamp_Control.instances[self.num] = self
		
Lamp_Control(pin=conn.J4[7], num=1)
Lamp_Control(pin=conn.J4[6], num=2)
Lamp_Control(pin=conn.J4[4], num=3)
Lamp_Control(pin=conn.J4[5], num=4)

################################################################################
class Driver_Board(Output):
	def __init__(self, **args):
		""" Construit un objet Display
		Keyword arguments:
		*** -- ***
		"""
		super().__init__(**args)
		(self.lamp_control,self.lamp_latch) = Driver_Board.get_lamp_latch_control(self.num)
    
	def get_lamp_latch_control(num):
		lamp_latch = Lamp_Latch.instances[int(num/4) + 1]
		if num == 10 :
			lamp_control = Lamp_Control.instances[4]
		elif num == 11 :
			lamp_control = Lamp_Control.instances[3]
		else:	
			lamp_control = Lamp_Control.instances[int(num%4) + 1]
		return lamp_latch, lamp_control
	
	def set_level(self, level):
		self.lamp_latch.pin.set_level(1)
		self.lamp_control.pin.set_level(level)
		self.lamp_latch.pin.set_level(0)
		super().set_level(level)
		
################################################################################
class Relay(Driver_Board):
	def __init__(self, **args):
		super().__init__(**args)

################################################################################
class Blink_Lamp_Manager(Thread_Manager.Thread_Manager):
	def __init__(self, list_lamp):
		super().__init__()
		self._blink_period = 0.5
		self.list_lamp = list_lamp
	
	def set_blink_period(self, value):
		self._blink_period = value
		
	def _th_function(self):
		while self._end_th == False:
			for lamp in self.list_lamp:
				if lamp.blink == True :
					if lamp.num % 2 == 0:
						lamp.set_level(1, ignore_blink=True)
					else:
						lamp.set_level(0, ignore_blink=True)					
					
			time.sleep(self._blink_period/2)
			
			for lamp in self.list_lamp:
				if lamp.blink == True :
					if lamp.num % 2 == 0:
						lamp.set_level(0, ignore_blink=True)
					else:
						lamp.set_level(1, ignore_blink=True)
						
			time.sleep(self._blink_period/2)
				
class Lamp(Driver_Board):
	def __init__(self, **args):
		super().__init__(**args)
		self.blink = False
	
	def set_level(self, level, ignore_blink=False):
		if level == "blink":
			self.blink = True
		else:
			if ignore_blink == False:
				self.blink = False
			super().set_level(level)
			
	def is_blinking(self):
		return self.blink

################################################################################
class Lamp_Playfield(Lamp):
	def __init__(self, **args):
		super().__init__(**args)
	
	def blink_all(value):
	    for lamp in Lamp_Playfield.instances.values():
	        if value == 1:
	            lamp.set_level("blink")
	        else:
	            lamp.set_level(0)
	
# ################################################################################
# class Short_Sound():
# 	def __init__(self, file):
# 		self.file = file
# 	
# 	def play(self):
# 		sound_manager.play_short_sound(pyglet.media.load(self.file))
# 		
# class Sound_Manager():
# 	def __init__(self):
# 		self.background_file = None
# 		self.short_sound_source = None
# 		self.background_state = False
# 		self._th = None
# 		
# 	def start(self):
# 		self._th = threading.Thread(target=self._th_background_sound)
# 		self._end_th = False
# 		self._th.start()
# 		
# 	def stop(self):
# 		self._end_th = True
# 		self._th.join()
# 		   
# 	def set_background_sound(self, background_file):
# 		self.background_file = background_file
# 		
# 	def get_back_ground_sound(self):
# 		return pyglet.media.load(self.background_file)
# 	
# 	def start_background(self):
# 		if self.background_file != None and self._th != None:
# 			self.background_state = True
# 			
# 	def stop_background(self):
# 		if self.background_state == True:
# 			self.background_state = False  
# 	
# 	def play_short_sound(self, short_sound_source):
# 		if self._th != None:
# 			self.short_sound_source = short_sound_source
# 		
# 	def _th_background_sound(self):
# 		old_background_state = self.background_state
# 		old_short_sound_source = None
# 		short_sound_player = pyglet.media.Player()
# 		background_player = pyglet.media.Player()
# 		
# 		while self._end_th == False:
# 			if old_background_state != self.background_state:
# 				if self.background_state == True:
# 					background_player.queue(self.get_back_ground_sound())
# 					background_player.play()
# 				else:
# 					background_player.next_source()
# 			
# 			if old_short_sound_source != self.short_sound_source:
# 				short_sound_player.queue(self.short_sound_source)
# 				if short_sound_player.playing == True:
# 					short_sound_player.next_source()
# 				short_sound_player.play()
# 				
# 				if background_player.playing == True:
# 					background_player.volume = 0
# 				
# 			if short_sound_player.time == 0.0 and background_player.volume == 0:
# 				background_player.volume = 1
# 			
# 			if self.background_state == True and background_player.time == 0.0:
# 				background_player.queue(self.get_back_ground_sound())
# 				background_player.play()
# 			
# 			old_short_sound_source = self.short_sound_source
# 			old_background_state = self.background_state				
# 			time.sleep(0.1)
# 		
# 		del background_player
# 		del short_sound_player
# 	
# 		
# sound_manager = Sound_Manager()