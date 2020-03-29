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

import Display
import Thread_Manager

LISTEN_DELAY_INPUT = 0.005

################################################################################
class Input_Manager():
    def __init__(self):
        super().__init__()
    
    def _th_function(self):
        while self._end_th == False:
            for y in range(8):
                Matrix.get_y_pin(y).set_level(1)
                for x in range(8):                                    
                    val = Matrix.get_x_pin(x).get_level()
                    matrix_obj = Matrix.get_by_xy(x, y)
                    if matrix_obj != None and matrix_obj.activated == True:
                        if val == 1 and matrix_obj.get_level() == 0:
                            matrix_obj.set_level(1)
                        elif val == 0 and matrix_obj.get_level() == 1:
                            matrix_obj.set_level(0)
                Matrix.get_y_pin(y).set_level(0)
                time.sleep(LISTEN_DELAY_INPUT)
            slam.set_level(slam.pin.get_level())
            
class Input():
    thread = None
    end_tread = False
    def __init__(self, high_function_event=None, low_function_event=None):
        self.state = 0
        self.high_event = event.Event()
        self.low_event = event.Event()
        if high_function_event != None:
            self.set_lowfunction_event(high_function_event)  
        if low_function_event != None:
            self.set_lowfunction_event(low_function_event)      
    
    def set_high_function_event(self, function):
        self.event += function
        
    def set_lowfunction_event(self, function):
        self.event += function
        
    def get_level(self):
        return self.state
    
    def set_level(self, value):
        self.state = value
        if self.get_level() == 1:
            self.event.fire(self)
    
    def get_by_name(name):
        return Input.instances[name]

################################################################################
class Matrix_Sim():
    def __init__(self, x_pin, y_pin, matrix_obj):
        self.x_pin = x_pin
        self.y_pin = y_pin
        self.matrix_obj = matrix_obj
        self.level_to_set = 0
        self.y_pin.pin_sim.event_set_value += self.event_set_value_x_pin
    
    def simulate(self, value=None):
        if value == None:
            self.level_to_set = 1
            while self.matrix_obj.get_level() == 0: time.sleep(0.01)
            self.level_to_set = 0
            while self.matrix_obj.get_level() == 1: time.sleep(0.01)
        else:
            self.level_to_set = value
    
    def event_set_value_x_pin(self, earg):
        if earg == 1:
            self.x_pin.set_level(self.level_to_set)
        else:
            self.x_pin.set_level(0)
                
################################################################################      
class Matrix(Input):
    test = Test_Matrix()
    def __init__(self, x, y, activated=True, **args):
        super().__init__(**args)
        self.x = x
        self.y = y
        self.yx_str = str(y) + str(x)
        self.sim = Matrix_Sim(Matrix.get_x_pin(x), Matrix.get_y_pin(y), self)
    
    def get_x_pin(num):
        return conn.J6[num+10]
        
    def get_y_pin(num):
        return conn.J6[num+1]
    
    def get_by_xy(list_matrix, x, y):
        for matrix in list_matrix:
            if matrix.x == x and matrix.y == y:
                return matrix
        return None
              
################################################################################        
class Playfield(Matrix):
    def __init__(self, **args):
        """ Construit un objet Input
        Keyword arguments:
        *** -- ***
        """
        super().__init__(activated=False, **args)
        Playfield.instances[self.name] = self
        
    def attract_mode(self):
        self.activated = False
    
    def tilt(self):
        self.activated = False
        
    def new_game(self):
        self.activated = True
    
################################################################################
class Slam(Input):
    def __init__(self, pin):
        """ Construit un objet Credit
        Keyword arguments:
        *** -- ***
        """
        super().__init__()
        self.pin = pin

slam = Slam(pin=conn.J5[10])     
################################################################################
class Test(Matrix):
    def __init__(self, **args):
        """ Construit un objet Credit
        Keyword arguments:
        *** -- ***
        """
        super().__init__(**args)
        self.current_step = 0
        self.wait_time_before_end = 60
        self.timer = Thread_Manager.Timer()
        self.timer.event_end += self.end_test
        self.start_pressed_reset = False
        self.wait_time_between_test = 0.5

################################################################################
class Credit(Matrix):
    def __init__(self, value, **args):
        """ Construit un objet Credit
        Keyword arguments:
        *** -- ***
        """
        self.value = value
        super().__init__(**args)

################################################################################
class Point(Playfield):
    def __init__(self, points, **args):
        """ Construit un objet Points
        Keyword arguments:
        *** -- ***
        """
        self.points = points
        super().__init__(**args)
        
################################################################################
class Point_Light(Playfield):
    def __init__(self, points, num_lamp, normal_state=0, **args):
        """ Construit un objet Points
        Keyword arguments:
        *** -- ***
        """
        super().__init__(**args)
        self.points = points
        self.normal_state = normal_state
        self.lamp = Output.Lamp_Playfield(num=num_lamp, name=self.name)

################################################################################
class Point_Light_Blink(Point_Light):
    def __init__(self, **args):
        """ Construit un objet Points
        Keyword arguments:
        *** -- ***
        """
        super().__init__(normal_state="blink", **args)     
    
    def new_game(self):
        super().new_game()
        self.lamp.set_level("blink")
        
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
        name = str(self.position_enfant + 1) + " " + self.parent.name
        super().__init__(name=name, **args)
    
    def new_game(self):
        super().new_game()
        if self.nb_states == 1:
            self.lamp.set_level("blink")
        
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
        
################################################################################
class Target_Bank():
    instances = dict()
    def __init__(self):
        """ Construit un objet Targets
        Keyword arguments:
        *** -- ***
        """
        self.children = list()
        Target_Bank.instances[name] = self
    
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
    def __init__(self, **args):     
        super().__init__(**args)
        self.solenoid = Output.Solenoid.get_by_name(self.name)
    
    def check_action(self):
        if super().check_action() == True:
            self.reset()
            
    def reset(self):
        self.solenoid.pulse()
        for child in self.children:
            child.reset() 
    
    def reset_list(list_target_bank):
        Output.Output.pulse_list(list_target_bank)
                      
################################################################################
class Hole(Playfield):
    def __init__(self, **args):
        """ Construit un objet Hole
        Keyword arguments:
        *** -- ***
        """
        super().__init__(**args)
        self.solenoid = Output.Solenoid.get_by_name(self.name)
    
    def eject_ball(self):
        self.solenoid.pulse()

################################################################################
class Trough(Playfield):
    first_object = None
    third_object = None
    def __init__(self, pos, **args):
        super().__init__(**args)
        if pos == 1:
            Trough.first_object = self
        if pos == 3:
            Trough.third_object = self               
    