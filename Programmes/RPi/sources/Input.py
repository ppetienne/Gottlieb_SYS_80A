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
from PIL.ImageOps import solarize
import Display

LISTEN_DELAY_INPUT = 0.002 # Pas en dessous de 0.002 sinon python plante

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
    def __init__(self, name, object_sim, get_level_object, normal_state=0, external_event=None, **args_event):
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
        self.sim = Input_Sim(object_sim) 
        self.get_level_object = get_level_object 

    def set_external_event(self, external_event, **args):
        self.external_event = external_event
        self.args_event = args
    
    def get_level(self):
        return self.state
    
    def event(self):
        if self.external_event != None:
            self.external_event(**self.args_event)
    
    def end(self):
        pass
    
    def simulate(input_name):
        input = Input.instances[input_name]
        input.sim.start()
        while input.sim.end == False:
            time.sleep(LISTEN_DELAY_INPUT)
        return input
    
################################################################################
class Input_Sim():
    def __init__(self, object_level):
        self.object_level = object_level
        self.end = False
        
    def end_loop(self, earg):
        self.object_level.set_level(0)
        manager.even_end_loop -= self.end_loop
        self.end = True
    
    def begin_loop(self, earg):
        self.object_level.set_level(1)
        manager.even_end_loop += self.end_loop
        manager.even_begin_loop -= self.begin_loop
            
    def start(self):
        self.end = False
        manager.even_begin_loop += self.begin_loop    
        

################################################################################        
class Input_Pin(Input):
    instances = dict()
    def __init__(self, pin, **args):
        """ Construit un objet Input
        Keyword arguments:
        *** -- ***
        """  
        super().__init__(get_level_object=pin, object_sim=pin, **args)     
        Input_Pin.instances[self.name] = self

################################################################################
class Input_Matrix_Sim():
    def __init__(self, x_pin, y_pin):
        self.level = 0
        self.x_pin = x_pin
        self.y_pin = y_pin
        self.y_pin.pin_sim.event_set_value += self.event_set_value_pin
        
    def set_level(self, value):
        self.level = value
    
    def event_set_value_pin(self, value):
        if self.level == 1:
            pin = self.x_pin
            if value == 1:
                pin.set_level(1)
            else:
                pin.set_level(0)
                
################################################################################        
class Input_Matrix(Input):
    instances = dict()
    def __init__(self, x, y, **args):
        """ Construit un objet Input
        Keyword arguments:
        *** -- ***
        """  
        m_point = Matrix_Point(x, y, self)
        super().__init__(get_level_object=m_point, object_sim=Input_Matrix_Sim(m_point.x_pin, m_point.y_pin), **args)     
        Input_Matrix.instances[self.name] = self
    
    def test(wait_time):
        for input in Input_Matrix.instances.values():
            input.activated = True
        
        time.sleep(0.5)
        
        for input in Input_Matrix.instances.values():
            if input.get_level() == 0:
                status = 99
            else:
                status = input.x + input.y*10
            Display.Display.instances["Status"].set_status(status)
            time.sleep(wait_time)
            
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
class Slam(Input_Pin):
    def __init__(self, **args):
        """ Construit un objet Credit
        Keyword arguments:
        *** -- ***
        """
        super().__init__(name=self.__class__.__name__, **args)
        
    def event(self):
        if Common.TEST_MODE == True:    
            Input.instances['Test'].end_test()
        else:
            Common.attract_mode()
            Data_Save.add_slam()
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
        if Common.TEST_MODE == True:    
            Input.instances['Test'].end_test()
        elif Common.infos_game['status'] == Common.General_Status.START:
            Data_Save.add_tilt()
            tilt_level(1)
            for lamp in Output.Lamp.instances.values():
                lamp.set_level(0)
            
            for input_p in Input_Playfield.instances.values():
                input_p.activated = False                     
            super().event()

################################################################################
class Start(Input_Matrix):
    def __init__(self, **args):
        """ Construit un objet Credit
        Keyword arguments:
        *** -- ***
        """
        super().__init__(name=self.__class__.__name__, **args)
    
    def event(self):
        if Common.TEST_MODE == True:
            Input.instances['Test'].start_pressed()
        else:
            if Display.Display.instances['Status'].get_credit() > 0:
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
        super().__init__(name=self.__class__.__name__, **args)
        self.current_step = 0
        self.wait_time_before_end = 60
        self.timer = Common.Timer()
        self.timer.event_end += self.end_test
        self.start_pressed_reset = False
        self.wait_time_between_test = 0.5
        
    def event(self):
        # Premier appuie
        if Common.TEST_MODE == False:
            self.current_step = 0
            Common.attract_mode()
            Common.TEST_MODE = True
            Common.init_displays()
        elif self.start_pressed_reset == True:
            Data_Save.reset_by_pos(self.current_step)
        else:
            vale = Display.Player.instances[1].get_value()
            if vale  != "" and self.current_step < 16:
                Data_Save.set_by_pos(self.current_step, Display.Player.instances[1].get_value())
            self.current_step += 1
            self.start_step()
    
    def end(self):
        self.timer.stop()
        super().end()
        
    def start_step(self):
        self.timer.start(self.wait_time_before_end)
        Display.Display.instances["Status"].set_credit(self.current_step)
        Display.Player.instances[3].set_int_value(self.current_step)
        Display.Player.instances[4].set_int_value(self.current_step)
        
        if self.current_step < 16:
           val = Data_Save.get_by_pos(self.current_step-1)        
           Display.Player.instances[1].set_int_value(val)
        else:
            if self.current_step == 16:
                Output.Lamp.test(self.wait_time_between_test)
            elif self.current_step == 17:
                Output.Lamp.test(self.wait_time_between_test)
                #Output.Sound.test()
            elif self.current_step == 18:
                Input_Matrix.test(wait_time_between_test) 
            elif self.current_step == 19:
                Display.Display.instances["Status"].value("")
                Display.Display.test(wait_time_between_test) 
    
    def end_test(self, earg=None):
        Common.TEST_MODE = False
        Common.attract_mode()
        
    def start_pressed(self):
        if self.current_step == 0:
           self.current_step = 16        
           self.start_step()
        else:
            if self.current_step < 16:
                Display.Player.instances[1].set_all_zero()
                if self.current_step < 11 or self.current_step > 14:
                    self.start_pressed = True
                else:
                    Display.Player.instances[3].set_value(100000, increment=True)
            else:
                self.start_step()
                
    def get_list_tests(self):
        dict_tests = dict()
        dict_tests["Matrix"] = [input.name for input in Input_Matrix.instances.values()]
        dict_tests["Lamp"] = [lamp.name for lamp in Output.Lamp.instances.values()]
        dict_tests["Solenoid"] = [sol.name for sol in Output.Solenoid.instances.values()]
        dict_tests["Display"] = [display.name for display in Display.Display.instances.values()]
        return dict_tests
    
    def start_test(self, name):
        pass
    
    def test_one_io(self, name_test, name_io):
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
        self.lamp = Output.Lamp_Playfield(lamp_control=lamp_control, lamp_latch=lamp_latch, name=self.name)      
    
    def tilt(self):
        self.lamp.reset()
        super().tilt()
            
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
        Input_Playfield.event(self)
        
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
        self.solenoid = Output.Solenoid.get_by_name(self.name)
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
        self.solenoid = Output.Solenoid.get_by_name(self.name)
    
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
    
    def event(self):
        self.eject_ball()
        
################################################################################
class Manager():
    def __init__(self):
        """ Construit un objet Display
        Keyword arguments:
        *** -- ***
        """
        self._th = None
        self.even_begin_loop = event.Event()
        self.even_end_loop = event.Event()
        
    def start(self):
        self._th = threading.Thread(target=self._th_listen_input)
        self._end_th = False
        self._th.start()
    
    def stop(self):
        self._end_th = True
        self._th.join()
        
    def _th_listen_input(self):
        while self._end_th == False:
            self.even_begin_loop.fire()
            for input in Input.instances.values():
                if input.activated == True:    
                    new_state = input.get_level_object.get_level()
                    if new_state != input.state :
                        input.state = new_state
                        if new_state != input.normal_state :
                            input.event()
                else:
                    time.sleep(LISTEN_DELAY_INPUT)    
            self.even_end_loop.fire()
                  
manager = Manager()  