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
import simpleaudio as sa
import pyglet
import Display
import operator

class Output_CM():
	instances = list()
	def __init__(self, pin, num):
		""" Construit unnumet Display
		Keyword arguments:
		*** -- ***
		"""
		self.pin = pin
		self.num = num
		Output_CM.instances.append(self)
		
	def set_level(self, value):
		self.pin.set_level(value)
		
################################################################################
class Solenoid(Output_CM):
	instances = dict()
	def __init__(self, **args):
		""" Construit un objet Display
		Keyword arguments:
		*** -- ***
		"""
		super().__init__(**args)
		Solenoid.instances[self.num] = self
		self.name = ""
	
	def test(wait_time):
		for sol in Solenoid.instances.values():
			Display.Display.instances["Status"].set_status(sol.num)
			sol.pulse()
			time.sleep(wait_time)
			sol.pulse()
			time.sleep(wait_time)
			
	def pulse(self, wait_time=0.5):
		self.set_level(1)
		time.sleep(wait_time)
		self.set_level(0)
	
	def get_by_name(name):
		return [sol for sol in Solenoid.instances.values() if sol.name == name][0]
	
Solenoid(pin=conn.J4['S'], num=1)
Solenoid(pin=conn.J4['X'], num=2)
Solenoid(pin=conn.J4[24], num=3)
Solenoid(pin=conn.J4[23], num=4)
Solenoid(pin=conn.J4['R'], num=5)
Solenoid(pin=conn.J4['U'], num=6)
Solenoid(pin=conn.J4[22], num=7)
Solenoid(pin=conn.J4[21], num=8)
Solenoid(pin=conn.J4['T'], num=9)  

################################################################################
# class Sound(Output_CM):
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
class Lamp_Latch(Output_CM):
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
class Lamp_Control(Output_CM):
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
class Output_Driver():
	instances = dict()
	def __init__(self, lamp_control, lamp_latch, name):
		""" Construit un objet Display
		Keyword arguments:
		*** -- ***
		"""
		self.lamp_control = lamp_control
		self.lamp_latch = lamp_latch
		self.name = name
		Output_Driver.instances[name] = self
		self.value = 0
            
	def set_level(self, value):
		self.lamp_latch.pin.set_level(1)
		self.lamp_control.pin.set_level(value)
		self.lamp_latch.pin.set_level(0)
		self.value = value
	
	def get_level(self):
		return self.value

Output_Driver(lamp_control=Lamp_Control.instances[1], lamp_latch=Lamp_Latch.instances[1], name="Game Over Relay")
Output_Driver(lamp_control=Lamp_Control.instances[2], lamp_latch=Lamp_Latch.instances[1], name="Tilt")
Output_Driver(lamp_control=Lamp_Control.instances[3], lamp_latch=Lamp_Latch.instances[1], name="Coin Lockout Coil")

################################################################################
class Lamp(Output_Driver):
	instances = dict()
	def __init__(self, **args):
		super().__init__(**args)
		self.num = Lamp.get_num(self.lamp_control.num, self.lamp_latch.num)
		self._th_blink = None 
		self._end_th_blink = False
		Lamp.instances[self.name] = self
	
	def test(wait_time):
		for lamp in [lamp for lamp in (sorted(Lamp.instances.values(), key=operator.attrgetter('num'))) if lamp.num != None]:
			lamp.set_level(1)
			Display.Display.instances["Status"].set_status(lamp.num)
			time.sleep(wait_time)
			lamp.set_level(0)
			
	def get_num(lamp_control, lamp_latch):
		if lamp_control == 4 and lamp_latch == 1:
			num = 3
		elif lamp_control == 1 and lamp_latch == 3:
			num = 8
		elif lamp_control == 3 and lamp_latch == 3:
			num = 11
		elif lamp_control == 4 and lamp_latch == 3:
			num = 10
		elif lamp_latch == 2:
			num = 3 + lamp_control
		elif lamp_latch > 3:
			num = 11 + 4*(lamp_latch-4) + lamp_control
		else:
			raise Exception("Ce n'est pas une lampe qui est instanciee")
		
		return num
	
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
		
Lamp(lamp_control=Lamp_Control.instances[4], lamp_latch=Lamp_Latch.instances[3], name="Game Over Light")
Lamp(lamp_control=Lamp_Control.instances[4], lamp_latch=Lamp_Latch.instances[1], name="Shoot Again")

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