# -*- coding: utf-8 -*-
################################################################################
# Input
# 
#
################################################################################
import threading
import time
from Contacts import conn
import Output
import Options
import Data_Save
from Event import event
import Common

LISTEN_DELAY_INPUT = 0.001

################################################################################

class Matrix_Point():
    def __init__(self, x, y, input):
        """ Construit un objet Matrix_Point
        Keyword arguments:
        *** -- ***
        """
        self.x = x
        self.y = y
        self.input = input
        self.x_pin = conn.J6[x+10]
        self.y_pin = conn.J6[y+1]
        
    def get_level(self):
        self.y_pin.set_level(1)
        time.sleep(LISTEN_DELAY_INPUT/2)            
        val = self.x_pin.get_level()
        self.y_pin.set_level(0)
        time.sleep(LISTEN_DELAY_INPUT/2)
        return val

################################################################################
class Input():
    instances = dict()
    def __init__(self, name, get_level_object, normal_state=0, external_event=None, **args_event):
        if name not in Input.instances.keys():
            self.name = name
        else:
            raise Exception("L'input " + name + " est deja existant")
        
        self.normal_state = normal_state
        self.state = normal_state
        Input.instances[name] = self 
        self.external_event = external_event 
        self.args_event = args_event  
        self.activated = False  
        self.get_level_object = get_level_object 
    
    def set_external_event(self, external_event, **args):
        self.external_event = external_event
        self.args_event = args
    
    def get_level(self):
        return self.state
    
    def event(self):
        if self.external_event != None:
            self.external_event(**self.args_event)

################################################################################        
class Input_Matrix(Input):
    def __init__(self, x, y, **args):
        """ Construit un objet Input
        Keyword arguments:
        *** -- ***
        """  
        super().__init__(get_level_object=Matrix_Point(x, y, self), **args)     

################################################################################        
class Input_Playfield(Input_Matrix):
    instances = dict()
    external_unique_event = None
    args_unique_event = None
    def __init__(self, **args):
        """ Construit un objet Input
        Keyword arguments:
        *** -- ***
        """
        super().__init__(**args)
        Input_Playfield.instances[self.name] = self 
    
    @staticmethod
    def set_external_unique_event(self, external_unique_event, *args):
        Input_Playfield.external_unique_event = external_unique_event
        Input_Playfield.args_unique_event = args
        
    def attract_mode(self):
        self.activated = False
    
    def tilt(self):
        self.activated = False
        
    def new_game(self):
        self.activated = True
    
    def event(self):
        super().event()
        if Input_Playfield.external_unique_event != None:
            Input_Playfield.external_unique_event(*Input.args_unique_event)
            Input_Playfield.external_unique_event = None
            Input_Playfield.args_unique_event = None
    
################################################################################
class Slam(Input):
    def __init__(self, pin, **args):
        """ Construit un objet Credit
        Keyword arguments:
        *** -- ***
        """
        self.pin = pin
        super().__init__(name=self.__class__.__name__, get_level_object=pin, **args)
    
    def event(self):
        Common.infos_game['status'] = Common.General_Status.SLAM
        super().event()
            
################################################################################
class Tilt(Input_Matrix):
    def __init__(self, **args):
        """ Construit un objet Credit
        Keyword arguments:
        *** -- ***
        """
        super().__init__(name=self.__class__.__name__, **args)
    
    def event(self):
        if Common.infos_game['status'] == Common.General_Status.START:
            Data_Save.add_tilt()
            Common.infos_game['status'] = Common.General_Status.TILT
            
            for input in Input_Playfield.instances.values():
                input.tilt()
            
            Common.tilt_level(1)
                
        super().event()
          
################################################################################
class Start(Input_Matrix):
    def __init__(self, **args):
        """ Construit un objet Credit
        Keyword arguments:
        *** -- ***
        """
        self.event_Start_Test = event.Event()
        super().__init__(name=self.__class__.__name__, **args)
    
    def event(self):
        if Common.infos_game['status'] == Common.General_Status.TEST:
            self.event_Start_Test.fire()
        else:
            if Common.get_credits() > 0:
                if Common.first_ball():
                    self.add_player()
                else:
                    self.start_new_game()             
        super().event()
        
    def add_player(self):
        if Common.add_player() == True:
            Common.add_credits(-1)    # Permet de ne pas utiliser les credits dans les fonctions Common
                 
    def start_new_game(self):
        Common.start_new_game()  
        self.add_player()      
        super().event()
        Common.infos_game['status'] = Common.General_Status.START
        
################################################################################
class Test(Input_Matrix):
    def __init__(self, **args):
        """ Construit un objet Credit
        Keyword arguments:
        *** -- ***
        """
        Input.instances['Start'].event_Start_Test += self.start_pressed
        super().__init__(name=self.__class__.__name__, **args) 
        
    def event(self):
        if Common.infos_game['status'] == Common.General_Status.ATTRACT_MODE:
            Common.infos_game['status'] = Common.General_Status.TEST
        
        super().event()
                
    def start_pressed(self):
        pass        

################################################################################
class Credit(Input_Matrix):
    def __init__(self, value, name, **args):
        """ Construit un objet Credit
        Keyword arguments:
        *** -- ***
        """
        self.value = value
        super().__init__(name=name, **args)
    
    def event(self):
        Common.add_credits(self.value)
        super().event()

################################################################################
class Point(Input_Playfield):
    def __init__(self, points, **args):
        """ Construit un objet Points
        Keyword arguments:
        *** -- ***
        """
        self.points = points
        super().__init__(**args)        
    
    def tilt(self):
        super().tilt()
        
    def event(self):
        Common.add_points_current_player(self.points)
        super().event()
        
################################################################################
class Point_Light(Input_Playfield):
    def __init__(self, points, lamp_control, lamp_latch, **args):
        """ Construit un objet Points
        Keyword arguments:
        *** -- ***
        """
        super().__init__(**args)
        self.points = points
        self.lamp = Output.Lamp(lamp_control, lamp_latch, self.name)      
    
    def tilt(self):
        self.lamp.reset()
        super().tilt()
    
    def new_game(self):
        super().new_game()
            
    def event(self):
        if self.lamp.get_level() == "blink" or self.lamp.get_level() == 0:
            points = self.points[0]
        else:
            points = self.points[1]
        Common.add_points_current_player(points)
        super().event()

################################################################################
class Point_Light_Blink(Point_Light):
    def __init__(self, **args):
        """ Construit un objet Points
        Keyword arguments:
        *** -- ***
        """
        super().__init__(**args)     
    
    def new_game(self):
        super().new_game()
        self.lamp.blink(1)
            
    def event(self):
        if self.lamp.get_level(ignore_blink=True) == 1:
            points = self.points[1]
        else:
            points = self.points[0]
            
        Common.add_points_current_player(points)
        super().event()
        
################################################################################
class Target(Point_Light):
    def __init__(self, parent, position_enfant, nb_states=1, **args):
        """ Construit un objet Target
        Keyword arguments:
        *** -- ***
        """
        self.parent = parent
        self.nb_states = nb_states
        self.position_enfant = position_enfant
        self.parent.children.append(self)
        name = str(self.position_enfant) + "_" + self.parent.name
        super().__init__(name=name, **args)
    
    def new_game(self):
        super().new_game()
        if self.nb_states == 1:
            self.lamp.blink(1)
    
    def event(self):
        super().event()
        if self.nb_states == 1:
            self.lamp.reset()
            self.lamp.set_level(1)
        elif self.nb_states == 2:
            if self.lamp.get_level() == "blink":
                self.lamp.blink(0)
                self.lamp.set_level(1)
            else:
                self.lamp.blink(1)
        self.parent.check_action()

################################################################################
class Target_Drop(Target):
    instances = dict()
    def __init__(self, **args):
        """ Construit un objet Target
        Keyword arguments:
        *** -- ***
        """
        self.level = 0
        super().__init__(**args)
        Target_Drop.instances[self.name] = self
        
    def reset(self):
        self.level = 0
    
    def event(self):
        self.level = 1
        super().event()
        
        
################################################################################
class Target_Bank():
    instances = dict()
    def __init__(self, name, external_event=None):
        """ Construit un objet Targets
        Keyword arguments:
        *** -- ***
        """
        self.name = name
        self.external_event = external_event
        self.children = list()
        Target_Bank.instances[name] = self
    
    def check_action(self):
        complete = self.is_complete()
        if complete == True and self.external_event != None:
            self.external_event()
        return complete
    
    def is_complete(self):
        cpt = 0
        for child in self.children:
            if child.lamp.get_level() == 1 :
                cpt += 1
        if cpt == len(self.children):
            state =  True
        else:
            state = False
        return state     

################################################################################
class Target_Bank_Drop(Target_Bank):
    instances = dict()
    def __init__(self, **args):     
        super().__init__(**args)
        self.solenoid = Output.Solenoid.instances[self.name]
        Target_Bank_Drop.instances[self.name] = self
    
    def check_action(self):
        if super().check_action() == True:
            self.reset()
            
    def reset(self):
        self.solenoid.pulse()
        for child in self.children:
            child.reset()  
               
################################################################################
class Spinner(Point_Light):
    def __init__(self, **args):
        """ Construit un objet Rollover
        Keyword arguments:
        *** -- ***
        """
        super().__init__(**args)
    
    def event(self):
        super().event()
        if self.lamp.get_level() == 1:
            self.lamp.set_level(0)
                      
################################################################################
class Hole(Input_Playfield):
    def __init__(self, **args):
        """ Construit un objet Hole
        Keyword arguments:
        *** -- ***
        """
        super().__init__(**args)
        self.solenoid = Output.Solenoid.instances[self.name]
    
    def eject_ball(self):
        self.solenoid.pulse()
        
################################################################################
class OutHole(Hole):
    def __init__(self, **args):
        """ Construit un objet Hole
        Keyword arguments:
        *** -- ***
        """
        super().__init__(**args)
        
################################################################################
class Trough(Input_Playfield):
    def __init__(self, **args):
        """ Construit un objet Trough
        Keyword arguments:
        *** -- ***
        """
        super().__init__(**args)
            
################################################################################
class Manager():
    def __init__(self):
        """ Construit un objet Display
        Keyword arguments:
        *** -- ***
        """
        self._th = None
        
    def start(self):
        self._th = threading.Thread(target=self._th_listen_input)
        self._end_th = False
        self._th.start()
    
    def stop(self):
        self._end_th = True
        self._th.join()
        
    def _th_listen_input(self):
        while self._end_th == False:
            for input in Input.instances.values():
                if input.activated == True:    
                    new_state = input.get_level_object.get_level()
                    if new_state != input.state :
                        input.state = new_state
                        if new_state != input.normal_state :
                            input.event()
                else:
                    time.sleep(LISTEN_DELAY_INPUT)
                        
manager = Manager()       