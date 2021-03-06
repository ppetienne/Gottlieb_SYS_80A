#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# I2C_Slave
# Classe mere pour tous les objets esclave du bus I2C
#
################################################################################
import threading


################################################################################
# Permet de proteger le bus I2C et ainsi interdit les acces concurrents
read_value = threading.Semaphore()

class I2C_Slave():
    
    def __init__(self, master, address, identifier):
        """ Construit un objet I2C_Slave
        Keyword arguments:
        master -- objet I2C_Master
        address -- adresse de l'esclave
        id -- id de l'esclave
        """    
        self.address = address + identifier
        self.master = master
        
    def read(self, register, nb_bytes=1):
        """ Lit un registre
        Keyword arguments:
        register -- registre a lire
        nb_bytes -- nombre de bytes dans le registre
        """ 
        read_value.acquire()
        val = self.master.read(self.address, register, nb_bytes)
        read_value.release()
        return val
    
    def write(self, register, value, nb_bytes=1):
        """ Ecrit dans un registre
        Keyword arguments:
        register -- registre a lire
        value -- valeur a modifier dans le registre
        nb_bytes -- nombre de bytes dans le registre
        """    
        read_value.acquire()
        self.master.write(self.address, register, value, nb_bytes)
        read_value.release()
        
################################################################################
ADDRESS = 0x20

class PCF8575(I2C_Slave):
    def __init__(self, master, identifier=0x00):
        """ Construit un objet PCF8575
        Keyword arguments:
        master -- master I2C utilise pour communiquer avec le composant
        id -- adresse propre au composant
        """
        super().__init__(master, ADDRESS, identifier)

    def set_port_val(self, val):
        """ Configure la valeur du port
        Keyword arguments:
        val -- valeur a configurer
        """
        self.write(val&0xFF, (val & 0xFF00) >> 8)
        
    def set_pin_val(self, pin, val):
        """ Configure une seule pin du port
        Keyword arguments:
        pin -- position de la pin
        val -- valeur a configurer
        """
        values = self.get_port_val()
        values = values & ~(1 << pin) # mise a zero du bit a assigner
        values = values | (val << pin) # affectation du bit a assigner
        self.set_port_val(values)
        
    def get_port_val(self):
        """ Recupere la valeur du port
        """
        temp_block = self.read(0x00, nb_bytes=2)
        return temp_block[0] + (temp_block[1] << 8) 

    def get_pin_val(self, pin):
        """ Recupere la valeur d'une seule pin du port
        Keyword arguments:
        pin -- position de la pin
        return -- valeur de la pin
        """
        values = self.get_port_val()
        return (values & (1 << pin)) >> pin