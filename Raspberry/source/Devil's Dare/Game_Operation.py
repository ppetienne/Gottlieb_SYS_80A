# -*- coding: utf-8 -*-
################################################################################
# Devil Dare
# 
#
################################################################################   
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import Common
import Input
import Output
import Display
import time
import Data_Save
import threading
import Contacts
import Options

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/GUI_Simulator')
import Starter

class General_Status(Enum):
    ATTRACT_MODE = 1
    TEST_MODE = 2
    START = 3
    TILT = 4
    SLAM = 5
    
class Pinball():
    def __init__(self, use_gui=False):
        self.use_gui = use_gui
        self.instanciate_input()
        self.instanciate_output()
        self.instanciate_display()
        self.display_manager = Display.Display_Manager()
        self.input_manager = Input.Input_Manager()
        self.blink_lamp_manager = Output.Blink_Lamp_Manager()
        self.status = General_Status.ATTRACT_MODE
        self.game = None
    
    def power_on(self):
        self.display_manager.start()
        self.input_manager.start()
        self.blink_lamp__manager.start()
        Output.Relay.instances["Coin Lockout Coil"].set_level(1)
        self.attract_mode()
        
        if self.use_gui == True:
            Starter.start_GUI()
    
    def power_off(self):
        self.display_manager.stop()
        self.input_manager.stop()
        self.blink_lamp__manager.stop()
            
        for display in Display.Player.instances.values():
            if display.is_blinking() == True:
                display.blink(0)        
        
    def attract_mode(self):
        self.status = General_Status.ATTRACT_MODE
        self.set_game_over_level(1)
        
        for display in Display.Display.instances.values():
            display.attract_mode()
            
        for input in Input.Playfield.instances.values():
            input.attract_mode()
        
        self.blink_lamp_manager.set_blink_period(1)
        Output.Lamp_Playfield.blink_all(1)
        #_th_show_HGTD_attract_mode.start()
        
    def eject_ball_outhole(self):
        Output.Lamp.instances["Ball Release"].pulse()
    
    def set_status_pinball(self, status):
        if not isinstance(status, General_Status):
            raise ("Status " + status + " not General_Status type")
        self.status = status
    
    def get_status_pinball(self):
        return self.status
    
    def _show_HGTD_attract_mode():
        cpt = 0
        show_hgdt = False
        time_show_hgtd = 2 # duree en s de l'affichage du hgtd
        time_wait = 2 # temps d'attente en s entre 2 affichages de hgtd
        time_refresh = 0.2 # intervalle interne pour la fluidite du programme
        hgtd = str(Data_Save.get("HGTD"))
        set_display_players_all_zero()
        
        while infos_game['status'] == General_Status.ATTRACT_MODE:
            time.sleep(time_refresh)
            if cpt == time_wait/time_refresh and show_hgdt == False:
                set_display_players(hgtd)
                show_hgdt = True
                cpt = 0
            elif cpt == time_show_hgtd/time_refresh and show_hgdt == True:
                set_display_players_all_zero()
                show_hgdt = False
                cpt = 0
            else:
                cpt += 1
            
    def add_credits(self, value):
        if Display.Display.instances['Status'].get_credit() + value <= Options.get('maximum_credits'):
            Display.Display.instances['Status'].set_credit(value, increment=True)
        else:
            Display.Display.get_by_name('Status').set_credit(Options.get('maximum_credits'), increment=False)
    
    def start_game(self):
        if self.game != None:
            raise Exception("Game already in play")
        self.set_game_over_level(0)
        self.set_tilt_level(0)
        for input in Input.Playfield.instances.values():
            input.new_game()
        self.status = General_Status.START
        self.game = Game(self)
        
    def end_game(self):
        self.game = None
        
    def add_player(self):
        if self.game.nb_player < 4:
            self.game.nb_player += 1
            Display.Player.get_by_num(self.game.nb_player).set_double_zero()
            player_added = True
        else:
            player_added = False
        
        return player_added
    
    def set_tilt_level(self, value):
        Output.Relay.instances["Tilt"].set_level(value)
    
    def get_tilt_level():
        return Output.Relay.instances["Tilt"].get_level()
    
    def set_game_over_level(self, value):
        Output.Relay.instances["Game Over Relay"].set_level(value)
        Output.Lamp.instances["Game Over Light"].set_level(value)
    
    def get_game_over_level(self):
        return Output.Lamp.instances["Game Over Light"].get_level()
        
    def reset_playfield(self):
        Input.Target_Bank_Drop.reset_all_bank()
        reset_lamps()
    
    def reset_lamps(self):
        pass #Todo
        
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
    
    def event_Start(self, earg):
        pass
        
    def instanciate_input(self):
        Input.Start(x=7, y=4, event_function=self.event_Start)
        Input.Test(x=7, y=0)
        Input.Tilt(x=7, y=5, external_event=event_Tilt)
        Input.Credit(x=7, y=1, name="Credit Left", value=Options.get('coin_values')[0]), 
        Input.Credit(x=7, y=2, name="Credit Center", value=Options.get('coin_values')[1])
        Input.Credit(x=7, y=3, name="Credit Right", value=Options.get('coin_values')[2])
        
        
        temp_targets = Input.Target_Bank_Drop(name="Left Drop Target Bank", external_event=event_Left_Drop_Target)
        for i in range(5):
            Input.Target_Drop(x=0, y=i, parent=temp_targets, position_enfant=i, num_lamp=18+i, points=[300,2000])
        
        temp_targets = Input.Target_Bank_Drop(name="Right Drop Target Bank", external_event=event_Right_Drop_Target)
        for i in range(5):    
            Input.Target_Drop(x=1, y=i, parent=temp_targets, position_enfant=i, num_lamp=26+i, points=[300,2000])
        
        temp_targets = Input.Target_Bank(name="Left Top Target Bank", external_event=event_Left_Top_Target)
        for i in range(4):
            Input.Target(x=2, y=i, parent=temp_targets, nb_states=2, position_enfant=i, num_lamp=44+i, lamp_latch=Output.Lamp_Latch.instances[12], points=[500,2000])
        
        if Options.get("nb_balls") == 3:
            nb_states = 1
        else:
            nb_states = 2
            
        temp_targets = Input.Target_Bank(name="Right Bottom Target Bank", external_event=event_Right_Bottom_Target)
        for i in range(4):
            Input.Target(x=3, y=i, parent=temp_targets, position_enfant=i, num_lamp=4+i, points=[500,2000], nb_states=nb_states)
        
        temp_targets = Input.Target_Bank_Drop(name="Top Drop Target Bank", external_event=event_Top_Drop_Target)
        for i in range(3):
            Input.Target_Drop(x=4, y=i, parent=temp_targets, position_enfant=i, num_lamp=23+i, points=[300,2000])
        
        Input.Spinner(x=5, y=1, name="Left Spin Target", num_lamp=31, points=[300,2000], external_event=event_Spinner)
        Input.Spinner(x=6, y=2, name="Right Spin Target", num_lamp=32, points=[300,2000])
        
        Input.Point(x=5, y=4, name="Top Left Bottom Target", points=2000, external_event=event_Top_Left_Bottom_Target)
        Input.Point(x=6, y=4, name="Bottom Left Bottom Target", points=2000, external_event=event_Bottom_Left_Bottom_Target)               
        
        Input.Playfield(x=5, y=2, name="Right Top Target", external_event=event_Right_Top_Target)
        
        Input.Trough(x=0, y=5, name="1st Trough", pos=1, external_event=event_1st_Trough)
        Input.Trough(x=1, y=5, name="3rd Trough", pos=3, external_event=event_3rd_Trough)
        
        Input.Point(x=6, y=3, name="Right Outside Rollover", points=5000, external_event=event_Right_Outside_Rollover)
        Input.Point(x=2, y=4, name="Left Outside Rollover", points=10000)
                         
        input = Input.Point_Light(x=3, y=5, name="Right Outside Return Rollover", num_lamp=17, points=[500,3000])
        input.set_external_event(event_Return_Rollover, lamp=input.lamp)
        
        input = Input.Point_Light(x=3, y=4, name="Left Outside Return Rollover", num_lamp=41, points=[500,3000])
        input.set_external_event(event_Return_Rollover, lamp=input.lamp)
        
        input = Input.Point_Light(x=4, y=5, name="Right Inside Return Rollover", num_lamp=40, points=[500,3000])
        input.set_external_event(event_Return_Rollover, lamp=input.lamp)
        
        input = Input.Point_Light(x=4, y=4, name="Left Inside Return Rollover", num_lamp=40, points=[500,3000])
        input.set_external_event(event_Return_Rollover, lamp=input.lamp) 
        
        Input.Point(x=6, y=1, name="Rollunder", points=5000, external_event=event_Rollunder)
        
        Input.Point(x=5, y=3, name="10 Points", points=10)
        Input.Point(x=2, y=5, name="Kicking Rubber", points=30)
        
        if Options.get("nb_balls") == 3:
            points = [1000, 3000]
        else:
            points = [100, 300]
        Input.Point_Light(x=4, y=3, name="Pop Bumper", num_lamp=16, points=points, blink_depend=True)
        
        Input.Hole(x=5, y=0, name="Top Ball Kicker", external_event=event_Top_Ball_Kicker)
        Input.Hole(x=6, y=0, name="Hole", external_event=event_Hole)
        
        Input.OutHole(x=5, y=5, name="Outhole", external_event=event_OutHole)
    
    def instanciate_output(self):
        Output.Lamp(num=11, name="Game Over Light")
        Output.Lamp(num=3, name="Shoot Again")
        Output.Lamp(num=13, name="Multi-Ball Bonus")
        Output.Lamp(num=14, name="Multi-Mode Timer")
        Output.Lamp(num=10, name="High Game to Date")
        Output.Lamp(num=12, name="Ball Release")
        Output.Lamp_Playfield(num=38, name="2X")
        Output.Lamp_Playfield(num=39, name="3X")
        Output.Lamp_Playfield(num=43, name="Extra Ball")
        Output.Lamp_Playfield(num=36, name="Top Left Bottom Target")
        Output.Lamp_Playfield(num=37, name="Bottom Left Bottom Target")
        Output.Lamp_Playfield(num=42, name="Rollunder")
        Output.Lamp_Playfield(num=15, name="Right Outside Rollover")
        Output.Lamp_Playfield(num=33, name="Hole")
        Output.Lamp_Playfield(num=34, name="Hole Capture")
        Output.Lamp_Playfield(num=35, name="Top Kicker Capture")
        
        Output.Solenoid(num=1, name="Top Drop Target Bank")
        Output.Solenoid(num=2, name="Top Ball Kicker")
        Output.Solenoid(num=3, name="Hole")
        Output.Solenoid(num=4, name="Ball Save Relay")
        Output.Solenoid(num=5, name="Left Drop Target Bank")
        Output.Solenoid(num=6, name="Right Drop Target Bank")
        Output.Solenoid(num=8, name="Knocker")
        Output.Solenoid(num=9, name="Outhole")
        
        Output.Sound(pin=conn.J4['B'], num=1)
        Output.Sound(pin=conn.J4['A'], num=2)
        Output.Sound(pin=conn.J4['Z'], num=4)
        Output.Sound(pin=conn.J4['Y'], num=8)
        
        Output.Relay(num=0, name="Game Over Relay")
        Output.Relay(num=1, name="Tilt")
        Output.Relay(num=2, name="Coin Lockout Coil")
        
    def instanciate_display(self):
        self.list_display Display.Timer()
        Display.Bonus() 
        Display.Status()
        for i in range(1, 5):
            Display.Player(i)

################################################################################   
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
        
################################################################################   
if __name__ == "__main__":
    pinball = Pinball(use_gui=True)
    pinball.power_on()