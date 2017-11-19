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


class Output_CM():
	instances = list()
	event_new_state = event.Event()
	def __init__(self, pin, name=""):
		""" Construit un objet Display
		Keyword arguments:
		*** -- ***
		"""
		self.pin = pin
		self.name = name
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
		Solenoid.instances[self.name] = self
	
	def set_new_name(self, name):
		del Solenoid.instances[self.name]
		self.name = name
		Solenoid.instances[self.name] = self		
		
	def activate(self, value):
		self.pin.set_level(value)
	
	def pulse(self, wait_time=0.5):
		self.activate(1)
		time.sleep(wait_time)
		self.activate(0)
		
Solenoid(pin=conn.J4['S'], name="Sol 1")
Solenoid(pin=conn.J4['X'], name="Sol 2")
Solenoid(pin=conn.J4[24], name="Sol 3")
Solenoid(pin=conn.J4[23], name="Sol 4")
Solenoid(pin=conn.J4['R'], name="Sol 5")
Solenoid(pin=conn.J4['U'], name="Sol 6")
Solenoid(pin=conn.J4[22], name="Sol 7")
Solenoid(pin=conn.J4[21], name="Sol 8")
Solenoid(pin=conn.J4['T'], name="Sol 9")  

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
		Lamp_Latch.instances[self.name] = self
		
Lamp_Latch(pin=conn.J4['P'], name="DS12")
Lamp_Latch(pin=conn.J4['N'], name="DS11")
Lamp_Latch(pin=conn.J4['L'], name="DS10")
Lamp_Latch(pin=conn.J4['M'], name="DS9")
Lamp_Latch(pin=conn.J4['J'], name="DS8")
Lamp_Latch(pin=conn.J4['K'], name="DS7")
Lamp_Latch(pin=conn.J4['F'], name="DS6")
Lamp_Latch(pin=conn.J4['H'], name="DS5")
Lamp_Latch(pin=conn.J4['D'], name="DS4")
Lamp_Latch(pin=conn.J4['E'], name="DS3")
Lamp_Latch(pin=conn.J4[3], name="DS2")        
Lamp_Latch(pin=conn.J4['C'], name="DS1")		
################################################################################
class Lamp_Control(Output_CM):
	instances = dict()
	def __init__(self, **args):
		""" Construit un objet Display
		Keyword arguments:
		*** -- ***
		"""
		super().__init__(**args)
		Lamp_Control.instances[self.name] = self
		
Lamp_Control(pin=conn.J4[7], name="LD1")
Lamp_Control(pin=conn.J4[6], name="LD2")
Lamp_Control(pin=conn.J4[4], name="LD3")
Lamp_Control(pin=conn.J4[5], name="LD4")

################################################################################
class Lamp():
	instances = dict()
	instances_playfield = dict()
	position = 0
	def __init__(self, lamp_control, lamp_latch, name, playfield=True):
		""" Construit un objet Display
		Keyword arguments:
		*** -- ***
		"""
		self.lamp_control = lamp_control
		self.lamp_latch = lamp_latch
		self.name = name
		Lamp.instances[name] = self
		if playfield == True:
			Lamp.instances_playfield[name] = self
		self._th_blink = None 
		self._end_th_blink = False
		self.position = Lamp.position
		Lamp.position += 1
		self.value = 0
		
	def set_level(self, value):
		self.lamp_latch.pin.set_level(1)
		self.lamp_control.pin.set_level(value)
		self.lamp_latch.pin.set_level(0)
		self.value = value
		Output_CM.event_new_state.fire((self.name, value)) # Pour le controle externe de la valeur de la lampe
	
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
		if self.position % 2 == 0: # Pour faire flasher les lamps en quinconce
			time.sleep(speed/2)
		time_refresh = 0.001
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