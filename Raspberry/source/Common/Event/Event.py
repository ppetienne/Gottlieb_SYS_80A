# -*- coding: utf-8 -*-

class Event(object):
    """
        Cette classe permet de creer des evenements de sorte a pouvoir communiquer entre objets
    """
    
    def __init__(self):
        self.handlers = []
    
    def add(self, handler):
        """
            Ajout d'un slot qui sera appelee quand un signal sera emis
            :param handler: slot a appeler
        """
        self.handlers.append(handler)
        return self
    
    def remove(self, handler):
        """
            Suppression d'un slot 
            :param handler: slot a supprimer
        """
        self.handlers.remove(handler)
        return self
    
    def fire(self, earg=None):
        """
            Emission d'un signal
            :param earg: parametre optionnel lors de l'emission du signal
        """
        for handler in self.handlers:
            handler(earg)
            
    __iadd__ = add
    __isub__ = remove
    __call__ = fire
