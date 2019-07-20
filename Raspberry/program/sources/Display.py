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
import Interface_Test

REFRESH_DELAY_DISPLAY = 0.1 #0.005 

class Test_Display(Interface_Test.Test):
	def __init__(self):
		super().__init__()
	
	def _th_test(self, wait_time):
		list_display = [Player.instances[display] for display in sorted(Player.instances)]
		list_display.extend([display for display in Display.instances.values() if type(display) != Player ] )

		for display in list_display:
			str_val = ""
			for i in range(display.nb_digits):
				for i in range(10):
					display.set_value(str(i) + str_val)
					time.sleep(wait_time)
				str_val += " "
			
class Display():
	instances = dict()
	event_refresh = event.Event()
	test = Test_Display()
	
	def __init__(self, nb_digits, name, segment, list_digits, default_val=""):
		""" Construit un objet Display
		Keyword arguments:
		*** -- ***
		"""
		self.nb_digits = nb_digits
		self.name = name
		self.segment = segment
		self.list_digits = list_digits
		self._value = default_val
		self.default_val = default_val
		Display.instances[name] = self	
		self.event_GUI = event.Event()
					
	def set_value(self, value):
		self._value = value
		self.event_GUI.fire((self.name, self.get_value()))
	
	def set_int_value(self, value, increment=False):
		if increment == True and self.get_value().isdigit() == True:
			new_val = value + int(self.get_value())
		else:
			new_val = value
		self.set_value(str(new_val))
			 
	def get_value(self):
		return self._value

	def get_int_value(self):
		return int(self.get_value())
	
	def refresh(self):
		cpt = 0
		val = self.get_value() # Permet de sauvegarder en local la variable pour que d'autres thread la modifie sans risque
		for i in range(len(val)):
			digits.set_digit(self.list_digits, i)
			segments.set_segment(val[-(i+1)], self.segment)
			Display.event_refresh((self.name, val[-(i+1)], i))
			time.sleep(REFRESH_DELAY_DISPLAY)
			cpt += 1
	
	def attract_mode(self):
		self.value = self.default_val
	
	def set_all_zero(self):
		value = ""
		for i in range(self.nb_digits):
			value += "0"
		self.set_value(value)
	
	def init_val(self):
		self.set_value(self.default_val)
		
	def get_by_name(name):
		return Display.instances[name]
		
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
		
################################################################################
		
class Player(Display):
	instances = dict()
	def __init__(self, num):
		""" Construit un objet Display
		Keyword arguments:
		*** -- ***
		"""
		if num == 1 or num == 2:
			segment_number = 0
		else:
			segment_number = 1
		if num == 1 or num == 3:
			list_digits = 0
		else:
			list_digits = 1
		super().__init__(7, "p" + str(num), segment_number, list_digits)
		Player.instances[self.name] = self
		self.num = num
		self._th_blink = None 
		self._end_th_blink = False
	
	def blink(self, level):
		if self._th_blink != None:
			self._end_th_blink = True
			self._th_blink.join()
			self._th_blink = None
			
		if level == 1: 
			self._th_blink = threading.Thread(target=self._th_manage_blink)
			self._end_th_blink = False
			self._th_blink.start()
			
	def set_double_zero(self):
		self.set_value("00")
	
	def is_blinking(self):
		if self._th_blink != None and self._th_blink.is_alive():
			return True
		else:
			return False
		
	def _th_manage_blink(self):
		init_value = self.get_value()
		while self._end_th_blink == False:
			self.set_value(init_value)
			time.sleep(0.2)
			self.set_value("")
			time.sleep(0.2)
		self.set_value(init_value)
	
	def get_by_num(num):
		return [player for player in Player.instances.values() if player.num == num][0]
		
for i in range(1, 5):
	Player(i)

################################################################################
		
class Bonus(Display):
	def __init__(self):
		""" Construit un objet Display
		Keyword arguments:
		*** -- ***
		"""
		segment_number = 2
		list_digits = 2
		super().__init__(6, "Bonus", segment_number, list_digits, "000000")

################################################################################	

class Timer(Display):
	def __init__(self):
		""" Construit un objet Display
		Keyword arguments:
		*** -- ***
		"""
		segment_number = 2
		list_digits = 3
		super().__init__(6, "Timer", segment_number, list_digits, "000000")		


################################################################################
class Status(Display):
	def __init__(self):
		""" Construit un objet Display
		Keyword arguments:
		*** -- ***
		"""
		segment_number = 2
		list_digits = 4
		super().__init__(4, "Status", segment_number, list_digits, default_val="0  ")
		self.set_credit(self.get_credit())
		
	def attract_mode(self):
		self.set_value(str(self.get_credit()) + "  ")
		
	def set_credit(self, value, increment=False):
		if increment == True:
			new_value = self.get_credit() + value
		else:
			new_value = value
		self.set_value(str(new_value) + self._get_status_str())
		
		Options.set("credits", new_value)
		
	def set_status(self, value):
		if value < 10:
			temp_val = " " + str(value)
		else:
			temp_val = str(int(value/10)) + str(int(value%10))
			
		self.set_value(str(self.get_credit()) + temp_val)
		
	def get_credit(self):
		return Options.get("credits")
	
	def _get_status_str(self):
		return self.get_value()[-2] + self.get_value()[-1]
	
Status()
################################################################################
class Manager():
	def __init__(self):
		""" Construit un objet Display
		Keyword arguments:
		*** -- ***
		"""
		self._th = None
		
	def start(self):
		self._th = threading.Thread(target=self._th_refresh_displays)
		self._end_th = False
		self._th.start()
		
	def stop(self):
		self._end_th = True
		self._th.join()
		
	def _th_refresh_displays(self):
		while self._end_th == False:
			for display in Display.instances.values():
				display.refresh()

manager = Manager()