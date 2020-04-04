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
from Common.Event import Event
from Common.Thread_Manager import Thread_Manager

LISTEN_DELAY_INPUT = 0.005

################################################################################
class Input_Manager(Thread_Manager.Thread_Manager):
    def __init__(self, list_matrix, slam):
        super().__init__()
        self.list_matrix = list_matrix
        self.slam = slam
    
    def _th_function(self):
        while self._end_th == False:
            for y in range(8):
                if Matrix.activated == True:
                    Matrix.get_y_pin(y).set_level(1)
                    for x in range(8):                                    
                        val = Matrix.get_x_pin(x).get_level()
                        matrix_obj = Matrix.get_by_xy(self.list_matrix, x, y)
                        if matrix_obj != None:
                            if val == 1 and matrix_obj.get_level() == 0:
                                matrix_obj.set_level(1)
                            elif val == 0 and matrix_obj.get_level() == 1:
                                matrix_obj.set_level(0)
                    Matrix.get_y_pin(y).set_level(0)
                time.sleep(LISTEN_DELAY_INPUT)
            self.slam.set_level(self.slam.pin.get_level())
            
class Input():
    def __init__(self, high_function_event=None, low_function_event=None):
        self.level = 0
        self.high_event = Event.Event()
        self.low_event = Event.Event()
        self.test_variable = None
        if high_function_event != None:
            self.set_high_function_event(high_function_event)  
        if low_function_event != None:
            self.set_low_function_event(low_function_event)      
    
    def set_high_function_event(self, function):
        self.high_event += function
        
    def set_low_function_event(self, function):
        self.low_event += function
        
    def get_level(self):
        return self.level
    
    def set_level(self, value):
        self.level = value
        if self.get_level() == 1:
            self.high_event.fire(self)
            self.high_event_action()
        else:
            self.low_event.fire(self)
            self.low_event_action()
    
    def high_event_action(self):
        pass
    
    def low_event_action(self):
        pass

################################################################################
class Matrix_Sim():
    MAX_ALLOWED_DELAY = 0.15
    def __init__(self, x_pin, y_pin, matrix_obj):
        self.x_pin = x_pin
        self.y_pin = y_pin
        self.matrix_obj = matrix_obj
        self.level_to_set = 0
        self.y_pin.pin_sim.event_set_value += self.event_set_value_x_pin
    
    def simulate(self, value=None):
        if value == None:
            self.level_to_set = 1
            time.sleep(Matrix_Sim.MAX_ALLOWED_DELAY)
            self.level_to_set = 0
            time.sleep(Matrix_Sim.MAX_ALLOWED_DELAY)
        else:
            self.level_to_set = value
            time.sleep(Matrix_Sim.MAX_ALLOWED_DELAY)
            
    
    def event_set_value_x_pin(self, earg):
        if earg == 1:
            self.x_pin.set_level(self.level_to_set)
        else:
            self.x_pin.set_level(0)
                
################################################################################      
class Matrix(Input):
    activated = True
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
    
    def new_game(self):
        pass

################################################################################
class Slam_MB(Input):
    def __init__(self):
        """ Construit un objet Credit
        Keyword arguments:
        *** -- ***
        """
        super().__init__()
        self.pin = conn.J5[10]

################################################################################
class Start_MB(Matrix):
    def __init__(self, **args):
        """ Construit un objet Credit
        Keyword arguments:
        *** -- ***
        """
        super().__init__(**args)

################################################################################
class Tilt_MB(Matrix):
    def __init__(self, **args):
        """ Construit un objet Credit
        Keyword arguments:
        *** -- ***
        """
        super().__init__(**args)
            
################################################################################
class Test_MB(Matrix):
    def __init__(self, **args):
        """ Construit un objet Credit
        Keyword arguments:
        *** -- ***
        """
        super().__init__(**args)
        self.timer = Thread_Manager.Timer()
        self.start_pressed_reset = False
        self.wait_time_between_test = 0.5

################################################################################
class Credit_MB(Matrix):
    def __init__(self, credit_value, nb_coin_needed, **args):
        """ Construit un objet Credit
        Keyword arguments:
        *** -- ***
        """
        super().__init__(**args)
        self.credit_value = credit_value
        self.nb_coin_needed = nb_coin_needed
        self.curent_nb_coins = 0
    
    def high_event_action(self):
        super().high_event_action()
        self.curent_nb_coins += 1
    
    def check_nb_coin_for_credit(self, reset=True):
        if self.curent_nb_coins == self.nb_coin_needed:
            self.curent_nb_coins = 0
            return True
        else:
            return False    

################################################################################
class Point_MB(Playfield):
    def __init__(self, points, **args):
        """ Construit un objet Points
        Keyword arguments:
        *** -- ***
        """
        self.points = points
        super().__init__(**args)
        
################################################################################
class Point_Light_MB(Playfield):
    def __init__(self, points, lamp, normal_state=0, **args):
        """ Construit un objet Points
        Keyword arguments:
        *** -- ***
        """
        super().__init__(**args)
        self.points = points
        self.normal_state = normal_state
        self.lamp = lamp
    
    def new_game(self):
        super().new_game()
        self.lamp.set_level(self.normal_state)

################################################################################
class Point_Light_Blink_MB(Point_Light_MB):
    def __init__(self, **args):
        """ Construit un objet Points
        Keyword arguments:
        *** -- ***
        """
        super().__init__(normal_state="blink", **args)
        
################################################################################
class Target_Bank_MB():
    def __init__(self):
        """ Construit un objet Targets
        Keyword arguments:
        *** -- ***
        """
        self.targets = list()
    
    def add_target(self, target):
        self.targets.append(target)
        
    def is_complete(self):
        cpt = 0
        for target in self.targets:
            if target.get_level() == 1 :
                cpt += 1
        if cpt == len(self.targets):
            state =  True
        else:
            state = False
        return state    
    
class Target_MB(Point_Light_MB):
    def __init__(self, target_bank, **args):
        """ Construit un objet Target
        Keyword arguments:
        *** -- ***
        """
        super().__init__(**args)
        self.target_bank = target_bank
        self.target_bank.add_target(self)
        
################################################################################
class Target_Bank_Drop_MB(Target_Bank_MB):
    def __init__(self, solenoid, **args):     
        super().__init__(**args)
        self.solenoid = solenoid
    
    def add_target(self, target):
        self.targets.append(target)
        target.high_event += self._check_reset
            
    def _check_reset(self, earg):
        if self.is_complete():
            self.solenoid.pulse()
        
    def reset_list(list_target_bank):
        list_sol = list()
        for target_bank in list_target_bank:
            list_sol.append(target_bank.solenoid)
        Output.Output.pulse_list(list_sol)

class Target_Drop_MB(Target_MB):
    def __init__(self, **args):
        """ Construit un objet Target
        Keyword arguments:
        *** -- ***
        """
        super().__init__(**args)

################################################################################
class Playfield_Hole_MB(Playfield):
    def __init__(self, solenoid, **args):
        """ Construit un objet Playfield_Hole_MB
        Keyword arguments:
        *** -- ***
        """
        super().__init__(**args)
        self.solenoid = solenoid
    
    def eject_ball(self):
        self.solenoid.pulse()
        
################################################################################
class OutHole_MB(Matrix):
    def __init__(self, solenoid, **args):
        """ Construit un objet OutHole_MB
        Keyword arguments:
        *** -- ***
        """
        super().__init__(**args)
        self.solenoid = solenoid
    
    def eject_ball(self):
        self.solenoid.pulse()
        
    