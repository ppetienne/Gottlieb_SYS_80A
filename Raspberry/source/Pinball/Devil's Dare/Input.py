# -*- coding: utf-8 -*-
################################################################################
# Input
# 
#
################################################################################
from Sys80A import Input_MB

################################################################################
class Start(Input_MB.Start_MB):
    def __init__(self, **args):
        """ Construit un objet Credit
        Keyword arguments:
        *** -- ***
        """

    
################################################################################
class Test(Input_MB.Test_MB):
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

################################################################################
class OutHole(Playfield):
    def __init__(self, **args):
        """ Construit un objet Hole
        Keyword arguments:
        *** -- ***
        """
        super().__init__(**args)
        
    def ball_in_outhole(self):
        if Common.infos_game['status'] == Common.General_Status.TILT:
            Common.set_tilt_level(0)
            Common.infos_game['status'] = Common.General_Status.START
        
        # todo lors du multiball
        if Common.infos_game['status'] == Common.General_Status.START:
            if Output.Lamp.instances["Shoot Again"].get_level() == 1:
                Common.eject_ball_from_outhole()
                Common.infos_game['extra_ball_in_play'] = True
            if Common.set_next_ball():
                super().event_action(earg)
                Output.Lamp_Playfield.blink_all(1, blink_period=0.2)
                time.sleep(1)
                Output.Lamp_Playfield.blink_all(0)
                Common.eject_ball_from_outhole()       




################################################################################
# Test class for the input Test class 
class Test_Matrix(Thread_Manager.Test):
    def __init__(self):
        super().__init__()
    
    def _th_function(self, wait_time):
        for input in Matrix.instances.values():
            input.activated = True
        
        time.sleep(0.5)
        
        for input in Matrix.instances.values():
            if input.get_level() == 0:
                status = 99
            else:
                status = input.x + input.y*10
            Display.Display.instances["Status"].set_status(status)
            time.sleep(Test.wait_time)

class Test_Display(Thread_Manager.Test):
    def __init__(self):
        super().__init__()
    
    def _th_function(self, wait_time):
        list_display = [Player.instances[display] for display in sorted(Player.instances)]
        list_display.extend([display for display in Display.instances.values() if type(display) != Player ] )

        for display in list_display:
            str_val = ""
            for i in range(display.nb_digits):
                for i in range(10):
                    display.set_value(str(i) + str_val)
                    time.sleep(Test.wait_time)
                str_val += " "

class Test_Lamp(Thread_Manager.Test):
    def __init__(self):
        super().__init__()
    
    def _th_function(self):
        for lamp in sorted(Lamp.instances.values(), key=operator.attrgetter('num')):
            lamp.set_level(1)
            Display.Display.instances["Status"].set_status(lamp.num)
            time.sleep(Test.wait_time/2)
            lamp.set_level(0)
            time.sleep(Test.wait_time/2)
            
class Test_Relay(Thread_Manager.Test):
    def __init__(self, **args):
        super().__init__(**args)
    
    def _th_function(self):
        time.sleep(Test.wait_time)
        for relay in sorted(Relay.instances.values(), key=operator.attrgetter('num')):
            if self._end_th == True:
                break
            Display.Display.instances["Status"].set_status(relay.num)
            relay.pulse(Test.wait_time/2)
            time.sleep(0.2)
            relay.pulse(Test.wait_time/2)
            time.sleep(Test.wait_time)

class Test_Solenoid(Thread_Manager.Test):
    def __init__(self):
        super().__init__()
    
    def _th_function(self):
        time.sleep(Test.wait_time)
        for sol in Solenoid.instances.values():
            if self._end_th == True:
                break
            Display.Display.instances["Status"].set_status(sol.num)
            sol.pulse(Test.wait_time/2)
            time.sleep(Test.wait_time)
            
class Test_Sound(Thread_Manager.Test):
    def __init__(self):
        super().__init__()
    
    def _th_function(self):
        pass