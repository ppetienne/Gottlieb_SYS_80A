# -*- coding: utf-8 -*-
################################################################################
# Display
# 
#
################################################################################
from Contacts import conn
import threading
import time
from Event import event
import Options
import Thread_Manager

REFRESH_DELAY_DISPLAY = 0.1 #0.005 

class Display_Manager(Thread_Manager.Thread_Manager):
	def __init__(self, list_display):
		super().__init__()
		self.list_display = list_display
	
	def _th_function(self):
		while self._end_th == False:
			for display in self.list_display:
				display.refresh()
				
class Display():	
	def __init__(self, nb_digits, segment, list_digits, default_val=""):
		""" Construit un objet Display
		Keyword arguments:
		*** -- ***
		"""
		self.nb_digits = nb_digits
		self.segment = segment
		self.list_digits = list_digits
		self._value = default_val
		self.default_val = default_val
		self.event = event.Event()
		self._displayed = True
					
	def set_value(self, value, increment=False):
		if increment == True:
			self._value = str(self.get_int_value() + int(value))
		else:
			self._value = str(value)
		self.event.fire(self)
	
	def set_displayed(self, level):
		self._displayed = level
		self.event.fire(self)
	
	def get_displayed(self):
		return self._displayed
			 
	def get_value(self):
		return self._value

	def get_int_value(self):
		if self._value.isdigit():
			return int(self._value)
		else:
			return 0
	
	def refresh(self):
		cpt = 0
		if self.get_displayed():
			val = self.get_value() # Permet de sauvegarder en local la variable pour que d'autres thread la modifie sans risque
		else:
			val = ""
		for i in range(len(val)):
			digits.set_digit(self.list_digits, i)
			segments.set_segment(val[-(i+1)], self.segment)
			time.sleep(REFRESH_DELAY_DISPLAY)
			cpt += 1
	
	def attract_mode(self):
		self.set_value(self.default_val)
	
	def set_all_zero(self):
		value = ""
		for i in range(self.nb_digits):
			value += "0"
		self.set_value(value)
	
	def init_val(self):
		self.set_value(self.default_val)
		
################################################################################		
class Segments():
	dict_val_seg = {"1":[8],
                        "2":[1,2,4,5,7],
                        "3":[1,2,3,4,7],
                        "4":[2,4,6,7],
                        "5":[1,3,4,6,7],
                        "6":[3,4,5,6,7],
                        "7":[1,2,3],
                        "8":[1,2,3,4,5,6,7],
                        "9":[1,2,3,4,6,7],
                        "0":[1,2,3,4,5,6],
                        " ":[],
                        }
	def __init__(self):
		""" Construit un objet Segments
		Keyword arguments:
		*** -- ***
		"""
		self.list_list_pins = list()
		self.list_list_pins.append([conn.J2[i] for i in range(1,9)])
		self.list_list_pins.append([conn.J2[i] for i in range(9,17)])
		self.list_list_pins.append([conn.J2[i] for i in range(17,25)])
	
	def set_segment(self, value, segment_number):
		conn.set_level(conn.J2, 0)
		for pin in [self.list_list_pins[segment_number][i-1] for i in Segments.dict_val_seg[value]]:
			pin.set_level(1)
			
segments = Segments()

################################################################################
class Digits():
	def __init__(self):
		""" Construit un objet Segments
		Keyword arguments:
		*** -- ***
		"""
		self.list_list_pins = list()
		list_temp = [conn.J3[i] for i in range(1,7)]
		list_temp.append(conn.J3[16])
		self.list_list_pins.append(list_temp)
		list_temp = [conn.J3[i] for i in range(7,13)]
		list_temp.append(conn.J3[13])
		self.list_list_pins.append(list_temp)
		self.list_list_pins.append([conn.J3[i] for i in range(1,7)])
		self.list_list_pins.append([conn.J3[i] for i in range(7,13)])
		self.list_list_pins.append([conn.J3[i] for i in range(13,17)])
	
	def set_digit(self, list_digits, position):
		conn.set_level(conn.J3, 0)
		self.list_list_pins[list_digits][position].set_level(1)

digits = Digits()	