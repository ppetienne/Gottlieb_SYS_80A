# -*- coding: utf-8 -*-
################################################################################
# Display
# 
#
################################################################################
from Event import event
from Contacts import conn
import time
import threading
import pyglet
import Display
import operator
import Common
import Interface_Test

################################################################################
# General functions

def get_dict_name(instance_dict):
		dict_name = dict()
		for object in instance_dict.values():
			dict_name[object.num] = object.name
		return dict_name
	
################################################################################	
class Mother_Board():
	instances = list()
	def __init__(self, pin, num):
		""" Construit unnumet Display
		Keyword arguments:
		*** -- ***
		"""
		self.pin = pin
		self.num = num
		Mother_Board.instances.append(self)
		self.event_GUI = event.Event()
		
	def set_level(self, value):
		self.pin.set_level(value)
		self.event_GUI.fire((self.num, value))
		
################################################################################
class Test_Solenoid(Interface_Test.Test):
	def __init__(self):
		super().__init__()
	
	def _th_test(self, wait_time):
		time.sleep(wait_time)
		for sol in Solenoid.instances.values():
			if self._end_th == True:
				break
			Display.Display.instances["Status"].set_status(sol.num)
			sol.pulse(wait_time/2)
			time.sleep(wait_time)
			
class Solenoid(Mother_Board):
	instances = dict()
	test = Test_Solenoid()
	def __init__(self, name, **args):
		""" Construit un objet Display
		Keyword arguments:
		*** -- ***
		"""
		args['pin'] = Solenoid.get_pin(args['num'])
		self.name = name
		super().__init__(**args)
		Solenoid.instances[self.name] = self
			
	def pulse(self, wait_time=0.5):
		self.set_level(1)
		time.sleep(wait_time)
		self.set_level(0)
		time.sleep(wait_time)
	
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

	def get_by_name(name):
		return Solenoid.instances[name]
	
	def get_by_num(num):
		return [sol for sol in Solenoid.instances.values() if sol.num == num][0]
       
################################################################################
# class Sound(Mother_Board):
# 	instances = dict()
# 	def __init__(self, **args):
# 		""" Construit un objet Display
# 		Keyword arguments:
# 		*** -- ***
# 		"""
# 		super().__init__(**args)
# 		Sound.instances[self.name] = self
# 				
# Sound(pin=conn.J4['B'], name="S1")
# Sound(pin=conn.J4['A'], name="S2")
# Sound(pin=conn.J4['Z'], name="S4")
# Sound(pin=conn.J4['Y'], name="S8")
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
class Driver_Board():
	instances = dict()
	def __init__(self, num, name):
		""" Construit un objet Display
		Keyword arguments:
		*** -- ***
		"""
		(self.lamp_control,self.lamp_latch) = Driver_Board.get_lamp_latch_control(num)
		self.name = name
		Driver_Board.instances[name] = self
		self.value = 0
		self.num = num
		self.event_GUI = event.Event()
    
	def get_lamp_latch_control(num):
		lamp_latch = Lamp_Latch.instances[int(num/4) + 1]
		if num == 10 :
			lamp_control = Lamp_Control.instances[4]
		elif num == 11 :
			lamp_control = Lamp_Control.instances[3]
		else:	
			lamp_control = Lamp_Control.instances[int(num%4) + 1]
		return lamp_latch, lamp_control
	
	def set_level(self, value):
		self.lamp_latch.pin.set_level(1)
		self.lamp_control.pin.set_level(value)
		self.lamp_latch.pin.set_level(0)
		self.value = value
		self.event_GUI.fire((self.num, value))
	
	def get_level(self):
		return self.value
	
	def get_by_name(name):
		return Lamp.instances[name]
	
	def get_by_num(num):
		return [driver for driver in Driver_Board.instances.values() if driver.num == num][0]
		
################################################################################
class Test_Relay(Interface_Test.Test):
	def __init__(self, **args):
		super().__init__(**args)
	
	def _th_test(self, wait_time):
		time.sleep(wait_time)
		for relay in sorted(Relay.instances.values(), key=operator.attrgetter('num')):
			if self._end_th == True:
				break
			Display.Display.instances["Status"].set_status(relay.num)
			relay.pulse(wait_time/2)
			time.sleep(0.2)
			relay.pulse(wait_time/2)
			time.sleep(wait_time)

class Relay(Driver_Board):
	instances = dict()
	test = Test_Relay()
	def __init__(self, **args):
		super().__init__(**args)
		Relay.instances[self.name] = self
	
	def pulse(self, wait_time=0.5):
		self.set_level(1)
		time.sleep(wait_time)
		self.set_level(0)
		time.sleep(wait_time)
		
Relay(num=0, name="Game Over Relay")
Relay(num=1, name="Tilt")
Relay(num=2, name="Coin Lockout Coil")

################################################################################
class Test_Lamp(Interface_Test.Test):
	def __init__(self):
		super().__init__()
	
	def _th_test(self, wait_time):
		for lamp in sorted(Lamp.instances.values(), key=operator.attrgetter('num')):
			lamp.set_level(1)
			Display.Display.instances["Status"].set_status(lamp.num)
			lamp.set_level(0)
			time.sleep(wait_time)
			
class Lamp(Driver_Board):
	instances = dict()
	test = Test_Lamp()
	def __init__(self, **args):
		super().__init__(**args)
		self._th_blink = None 
		self._end_th_blink = False
		Lamp.instances[self.name] = self
	
	def get_level(self, ignore_blink=False):
		if self._th_blink != None and self._th_blink.is_alive() and ignore_blink == False:
			return "blink"
		else:
			return self.value
	
	def blink(self, level, speed=0.5, timeout=0):
		if self._th_blink != None and self._th_blink.is_alive():
			self._end_th_blink = True
			self._th_blink.join()
			self._th_blink = None
			self.set_level(0)
		if level == 1: 
			self._th_blink = threading.Thread(target=self._th_manage_blink, args=(speed, timeout))
			self._end_th_blink = False
			self._th_blink.start()	
			
	def reset(self):
		if self.get_level() == "blink":
			self.blink(0)
		else:
			self.set_level(0)
			
	def _th_manage_blink(self, speed, timeout):
		begin_time = time.time()
		if self.num != None and self.num % 2 == 0: # Pour faire flasher les lamps en quinconce
			time.sleep(speed/2)
		time_refresh = 0.05
		cpt = 0
		while self._end_th_blink == False:
			if cpt == int(speed/time_refresh) :
				cpt = 0
				if self.value == 0:	
					self.set_level(1)
				else:
					self.set_level(0)
				if timeout > 0 and (time.time() > (begin_time + timeout)):
					break
			else:
				cpt += 1
				time.sleep(time_refresh)
		self.set_level(0)
       
Lamp(num=11, name="Game Over Light")
Lamp(num=3, name="Shoot Again")

################################################################################
class Lamp_Playfield(Lamp):
	instances = dict()
	def __init__(self, **args):
		super().__init__(**args)
		Lamp_Playfield.instances[self.name] = self
		
################################################################################
class Short_Sound():
	def __init__(self, file):
		self.file = file
	
	def play(self):
		sound_manager.play_short_sound(pyglet.media.load(self.file))
		
class Sound_Manager():
	def __init__(self):
		self.background_file = None
		self.short_sound_source = None
		self.background_state = False
		self._th = None
		
	def start(self):
		self._th = threading.Thread(target=self._th_background_sound)
		self._end_th = False
		self._th.start()
		
	def stop(self):
		self._end_th = True
		self._th.join()
		   
	def set_background_sound(self, background_file):
		self.background_file = background_file
		
	def get_back_ground_sound(self):
		return pyglet.media.load(self.background_file)
	
	def start_background(self):
		if self.background_file != None and self._th != None:
			self.background_state = True
			
	def stop_background(self):
		if self.background_state == True:
			self.background_state = False  
	
	def play_short_sound(self, short_sound_source):
		if self._th != None:
			self.short_sound_source = short_sound_source
		
	def _th_background_sound(self):
		old_background_state = self.background_state
		old_short_sound_source = None
		short_sound_player = pyglet.media.Player()
		background_player = pyglet.media.Player()
		
		while self._end_th == False:
			if old_background_state != self.background_state:
				if self.background_state == True:
					background_player.queue(self.get_back_ground_sound())
					background_player.play()
				else:
					background_player.next_source()
			
			if old_short_sound_source != self.short_sound_source:
				short_sound_player.queue(self.short_sound_source)
				if short_sound_player.playing == True:
					short_sound_player.next_source()
				short_sound_player.play()
				
				if background_player.playing == True:
					background_player.volume = 0
				
			if short_sound_player.time == 0.0 and background_player.volume == 0:
				background_player.volume = 1
			
			if self.background_state == True and background_player.time == 0.0:
				background_player.queue(self.get_back_ground_sound())
				background_player.play()
			
			old_short_sound_source = self.short_sound_source
			old_background_state = self.background_state				
			time.sleep(0.1)
		
		del background_player
		del short_sound_player
	
		
sound_manager = Sound_Manager()