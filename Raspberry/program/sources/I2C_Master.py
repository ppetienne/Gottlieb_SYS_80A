#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# I2C_RPi
# Master I2C permettant de piloter un bus I2C avec le kernel du RPi
#
################################################################################
import smbus2

class I2C_RPi():
	
	def __init__(self):
		""" Construit un objet I2C_RPi
		"""
		self.bus = smbus2.SMBus(1)
	
	def read(self, address, register, nb_bytes):
		""" Lit un registre d'un esclave
		Keyword arguments:
		address -- adresse du composant esclave
		register -- registre a lire
		nb_bytes -- nombre de bytes dans le registre
		"""		
		if nb_bytes > 1 :
			val = self.bus.read_word_data(address, register)
		else:
			val = self.bus.read_byte_data(address, register)
		
		return val

	def write(self, address, register, value, nb_bytes):
		""" Ecrit dans un registre d'un esclave
		Keyword arguments:
		address -- adresse du composant esclave
		register -- registre a lire
		value -- valeur a modifier dans le registre
		nb_bytes -- nombre de bytes dans le registre
		"""	
		if nb_bytes > 1 :
			val = self.bus.write_word_data(address, register, value)
		else:
			val = self.bus.write_byte_data(address, register, value)	
		return val