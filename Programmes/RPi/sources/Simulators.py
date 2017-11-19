# -*- coding: utf-8 -*-
################################################################################
# Simulators
# 
#
################################################################################
from Event import event
import time

class Pin_Sim():
	def __init__(self):
		self.value = 0
		self.event_set_value = event.Event()
						
	def set_level(self, value):
		self.value = value
		self.event_set_value.fire(value)
	
	def get_level(self):
		return self.value

################################################################################
class Input_Sim():
	instances = dict()
	wait_time = 0
	def __init__(self, input_obj):
		self.input_obj = input_obj
		Input_Sim.instances[input_obj.name] = self
		
	def set_level(self, value):
		self.input_obj.get_level_object.set_level(value)
	
	def simulate(name):
		wait_time = Input_Sim.wait_time*5
		input = Input_Matrix_Sim.instances[name]
		input.set_level(1)
		time.sleep(wait_time)
		input.set_level(0)
		time.sleep(wait_time)
	 
	def generate_input_simulator(inputs, inputs_matrix, wait_time):
		Input_Sim.wait_time = wait_time
		
		for input in inputs_matrix.values():
		    Input_Matrix_Sim(input)
		
		for input in [input for input in inputs.values() if input.name not in inputs_matrix.keys()]:
		    Input_Sim(input)
	
class Input_Matrix_Sim(Input_Sim):
	def __init__(self, input_obj):
		super().__init__(input_obj)
		self.level = 0
		self.input_obj.get_level_object.y_pin.event_set_value += self.event_set_value_pin
		
	def set_level(self, value):
		self.level = value
	
	def event_set_value_pin(self, value):
		if self.level == 1:
			pin = self.input_obj.get_level_object.x_pin
			if value == 1:
				pin.set_level(1)
			else:
				pin.set_level(0)
	
	
################################################################################