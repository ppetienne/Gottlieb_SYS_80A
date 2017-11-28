# -*- coding: utf-8 -*-
################################################################################
# Contacts
# Package contenant differentes classe permettant de faire un lien physique
# entre les objets
#
################################################################################
import Options
from Event import event

class Pin():
	def __init__(self, pin_hard=None):
		self.pin_hard = pin_hard
		self.pin_sim = Pin_Sim()
	
	def set_level(self, value):
		if self.pin_hard != None :
			self.pin_hard.set_level(value)
		self.pin_sim.set_level(value)
	
	def get_level(self):
		level = self.pin_sim.get_level()
		if self.pin_hard != None and level == 0:
			level = self.pin_hard.get_level()
		return level
	
class Pin_Sim(Pin):
	def __init__(self):
		self.value = 0
		self.event_set_value = event.Event()
		
	def set_level(self, value):
		self.value = value
		self.event_set_value.fire(value)
	
	def get_level(self):
		return self.value
	
if Options.get("hardware") == True:
	import RPi.GPIO as GPIO
	from I2C_Master import I2C_RPi
	from I2C_Components import PCF8575
		
	master = I2C_RPi()
	io_0 = PCF8575(master, 0)
	io_1 = PCF8575(master, 1)
	io_2 = PCF8575(master, 2)
	io_3 = PCF8575(master, 3)
	io_4 = PCF8575(master, 4)
	
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
			
	class Pin_IO_I2C(Pin):
		""" Represente une pin d'un connecteur de la carte CM """
		def __init__(self, pos_io, io, mode):
			""" Construit un objet Display
			Keyword arguments:
			*** -- ***
			"""  
			self.io = io
			self.pos_io = pos_io
			self.io.set_pin_mode(self.pos_io, mode)
			
		def set_level(self, value):
			self.io.set_pin_val(self.pos_io, value)
		
		def get_level(self):
			return self.io.get_pin_val(self.pos_io)
	################################################################################	
	class Pin_GPIO(Pin):
		""" Represente une pin d'un connecteur de la carte CM """
		def __init__(self, pin_GPIO, mode):
			""" Construit un objet Display
			Keyword arguments:
			*** -- ***
			"""
			self.pin_GPIO = pin_GPIO
			if mode == 0:
				GPIO.setup(self.pin_GPIO, GPIO.OUT)
			else:
				GPIO.setup(self.pin_GPIO, GPIO.IN)
			
			GPIO.output(self.__pos, GPIO.LOW)
					
		def set_level(self, value):
			GPIO.output(self.__pos, GPIO.LOW)
		
		def get_level(self):
			return self.io.get_pin_val(self.pos_io)
		
################################################################################
class Connectors():
	""" Represente un connecteur de la CM """
	def __init__(self):
		""" Construit un objet Display
		Keyword arguments:
		*** -- ***
		"""
		def instanciate_new_pin(type="IO_I2C", *args):
			if Options.get("hardware") == False:
				return Pin()
			elif type == "GPIO":
				return Pin(Pin_GPIO(*args))
			elif type == "IO_I2C":
				return Pin(Pin_IO_I2C(*args))
			else:
				raise Exception("Type pin inexistant")
		
		self.J2 = dict()
		for i in range(1, 25):
			self.J2[i] = instanciate_new_pin("GPIO", i+3, 0)
		
		self.J6 = dict()
		for i in range(1, 19):
			if i != 18 and i != 9:
				if i > 9:
					pos = i-2
				else:
					pos = i-1
				if i >= 10 :
					mode = 1
				else:
					mode = 0
				self.J6[i] = instanciate_new_pin(pos, 0, mode)
		
		self.J5 = dict()
		self.J5[1] = self.J6[17]
		self.J5[8] = self.J6[16]
		self.J5[9] = self.J6[8]
		self.J5[10] = instanciate_new_pin(13, 3, 1)
		for i in range(2, 8):
			self.J5[i] = self.J6[i-1]
		
		
				
		self.J3 = dict()
		for i in range(1, 17):
			self.J3[i] = instanciate_new_pin(i-1, 4, 0)
		
		self.J4 = dict()
		self.J4['S'] = instanciate_new_pin(0, 4, 0, 0, 0)
		self.J4['X'] = instanciate_new_pin(1, 3, 0)
		self.J4[24] = instanciate_new_pin(2, 3, 0)
		self.J4[23] = instanciate_new_pin(3, 3, 0)
		self.J4['R'] = instanciate_new_pin(4, 3, 0)
		self.J4['U'] = instanciate_new_pin(5, 3, 0)
		self.J4[22] = instanciate_new_pin(6, 3, 0)
		self.J4[21] = instanciate_new_pin(7, 3, 0)
		self.J4['T'] = instanciate_new_pin(8, 3, 0)
		self.J4['B'] = instanciate_new_pin(9, 3, 0)
		self.J4['A'] = instanciate_new_pin(10, 3, 0)
		self.J4['Z'] = instanciate_new_pin(11, 3, 0)
		self.J4['Y'] = instanciate_new_pin(12, 3, 0)
		self.J4[7] = instanciate_new_pin(0, 4, 0)
		self.J4[6] = instanciate_new_pin(1, 4, 0)
		self.J4[4] = instanciate_new_pin(2, 4, 0)
		self.J4[5] = instanciate_new_pin(3, 4, 0)
		self.J4['P'] = instanciate_new_pin(4, 4, 0)
		self.J4['N'] = instanciate_new_pin(5, 4, 0)
		self.J4['L'] = instanciate_new_pin(6, 4, 0)
		self.J4['M'] = instanciate_new_pin(7, 4, 0)
		self.J4['J'] = instanciate_new_pin(8, 4, 0)
		self.J4['K'] = instanciate_new_pin(9, 4, 0)
		self.J4['F'] = instanciate_new_pin(10, 4, 0)
		self.J4['H'] = instanciate_new_pin(11, 4, 0)
		self.J4['D'] = instanciate_new_pin(12, 4, 0)
		self.J4['E'] = instanciate_new_pin(13, 4, 0)
		self.J4[3] = instanciate_new_pin(14, 4, 0)
		self.J4['C'] = instanciate_new_pin(15, 4, 0)
			
	def set_level(self, connector, value):
		for pin in connector.values():
			pin.set_level(value)


conn = Connectors()