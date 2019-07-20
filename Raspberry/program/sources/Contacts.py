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

class Pin_Sim():
	def __init__(self):
		self.value = 0
		self.event_set_value = event.Event()
		
	def set_level(self, value):
		self.value = value
		self.event_set_value.fire(value)
	
	def get_level(self):
		return self.value
		
if Options.get("hardware") == True:	
	from I2C_Master import I2C_RPi
	from I2C_Components import PCF8575			
	
	class Pin_IO_I2C():
		instances = dict()
		master = I2C_RPi()
		io_0 = PCF8575(master, 0)
		io_1 = PCF8575(master, 1)
		io_2 = PCF8575(master, 2)
		io_3 = PCF8575(master, 3)
		#io_4 = PCF8575(master, 4)
	
		""" Represente une pin d'un connecteur de la carte CM """
		def __init__(self, pos_io, io, mode):
			""" Construit un objet Display
			Keyword arguments:
			*** -- ***
			"""  
			self.io = getattr(Pin_IO_I2C, "io_" + str(io))
			pin_name = str(pos_io) + "_" + str(io)
			if pin_name in Pin_IO_I2C.instances.keys():
				raise Exception("Pin deja utilisee")
			Pin_IO_I2C.instances[pin_name] = self
			self.pos_io = pos_io
			
		def set_level(self, value):
			self.io.set_pin_val(self.pos_io, value)
		
		def get_level(self):
			return self.io.get_pin_val(self.pos_io)
	
	################################################################################	
	import RPi.GPIO as GPIO
	class Pin_GPIO():
		
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		
		""" Represente une pin d'un connecteur de la carte CM """
		def __init__(self, pin_GPIO, mode):
			""" Construit un objet Display
			Keyword arguments:
			*** -- ***
			"""
			self.pin_GPIO = pin_GPIO
			if mode == 0:
				GPIO.setup(self.pin_GPIO, GPIO.OUT, initial=GPIO.LOW)
			else:
				GPIO.setup(self.pin_GPIO, GPIO.IN)
					
		def set_level(self, value):
			GPIO.output(self.pin_GPIO, value)
		
		def get_level(self):
			return GPIO.input(self.pin_GPIO)
		
################################################################################
class Connectors():
	""" Represente un connecteur de la CM """
	def __init__(self):
		""" Construit un objet Display
		Keyword arguments:
		*** -- ***
		"""
		def instanciate_new_pin(type, *args):
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
				
		self.J3 = dict()
		for i in range(1, 17):
			self.J3[i] = instanciate_new_pin("IO_I2C", i-1, 0, 0)
		
		self.J4 = dict()
		self.J4['S'] = instanciate_new_pin("IO_I2C", 0, 1, 0)
		self.J4['X'] = instanciate_new_pin("IO_I2C", 1, 1, 0)
		self.J4[24] = instanciate_new_pin("IO_I2C", 2, 1, 0)
		self.J4[23] = instanciate_new_pin("IO_I2C", 3, 1, 0)
		self.J4['R'] = instanciate_new_pin("IO_I2C", 4, 1, 0)
		self.J4['U'] = instanciate_new_pin("IO_I2C", 5, 1, 0)
		self.J4[22] = instanciate_new_pin("IO_I2C", 6, 1, 0)
		self.J4[21] = instanciate_new_pin("IO_I2C", 7, 1, 0)
		self.J4['T'] = instanciate_new_pin("IO_I2C", 8, 1, 0)
		self.J4['B'] = instanciate_new_pin("IO_I2C", 9, 1, 0)
		self.J4['A'] = instanciate_new_pin("IO_I2C", 10, 1, 0)
		self.J4['Z'] = instanciate_new_pin("IO_I2C", 11, 1, 0)
		self.J4['Y'] = instanciate_new_pin("IO_I2C", 12, 1, 0)
		self.J4[7] = instanciate_new_pin("IO_I2C", 0, 2, 0)
		self.J4[6] = instanciate_new_pin("IO_I2C", 1, 2, 0)
		self.J4[4] = instanciate_new_pin("IO_I2C", 2, 2, 0)
		self.J4[5] = instanciate_new_pin("IO_I2C", 3, 2, 0)
		self.J4['P'] = instanciate_new_pin("IO_I2C", 4, 2, 0)
		self.J4['N'] = instanciate_new_pin("IO_I2C", 5, 2, 0)
		self.J4['L'] = instanciate_new_pin("IO_I2C", 6, 2, 0)
		self.J4['M'] = instanciate_new_pin("IO_I2C", 7, 2, 0)
		self.J4['J'] = instanciate_new_pin("IO_I2C", 8, 2, 0)
		self.J4['K'] = instanciate_new_pin("IO_I2C", 9, 2, 0)
		self.J4['F'] = instanciate_new_pin("IO_I2C", 10, 2, 0)
		self.J4['H'] = instanciate_new_pin("IO_I2C", 11, 2, 0)
		self.J4['D'] = instanciate_new_pin("IO_I2C", 12, 2, 0)
		self.J4['E'] = instanciate_new_pin("IO_I2C", 13, 2, 0)
		self.J4[3] = instanciate_new_pin("IO_I2C", 14, 2, 0)
		self.J4['C'] = instanciate_new_pin("IO_I2C", 15, 2, 0)
		
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
				self.J6[i] = instanciate_new_pin("IO_I2C", pos, 3, mode)
		
		self.J5 = dict()
		self.J5[1] = self.J6[17]
		self.J5[8] = self.J6[16]
		self.J5[9] = self.J6[8]
		self.J5[10] = instanciate_new_pin("IO_I2C", 13, 1, 1)
		for i in range(2, 8):
			self.J5[i] = self.J6[i-1]
			
	def set_level(self, connector, value):
		for pin in connector.values():
			pin.set_level(value)


conn = Connectors()