# -*- coding: utf-8 -*-
################################################################################
# Devil Dare
# 
#
################################################################################   
import Common
import Input_MB
import Output
import Display
import time
import Data_Save
import threading
import Contacts
import Options
from Sys80A import Pinball   
from builtins import False


class Game_Operation(Pinball.Game_Operation):
    def __init__(self, **args):
        super().__init__(**args)
        Input.Input.game_operation = self
        
        self.instanciate_general_matrix()
        self.instanciate_playfield_matrix()
        self.instanciate_output()
        self.instanciate_display()
    
    def set_status(self, status):
        super().set_status(status)
        
        if status == General_Status.ATTRACT_MODE:
            self.blink_lamp_manager.set_blink_period(1)
            Output.Lamp_Playfield.blink_all(1)
            #_th_show_HGTD_attract_mode.start()
        elif status == General_Status.SLAM:
            self.set_game_over_level(1)
            self.dict_relay["Coin Lockout Coil"].set_level(0)
            Input_MB.Matrix.activated = False
            time.sleep(3)
            Input_MB.Matrix.activated = True
            self.dict_relay["Coin Lockout Coil"].set_level(1)
        elif status == General_Status.TEST_MODE:
            pass
        elif status == General_Status.START:
            pass
        elif status == General_Status.TILT:
            pass        
        
    def eject_ball_outhole(self):
        self.dict_lamp["Ball Release"].pulse()
    
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
    
    def set_game_over_level(self, value):
        super().set_game_over_level(value)
        Output.Lamp.instances["Game Over Light"].set_level(value)
        
    def reset_playfield(self):
        Input.Target_Bank_Drop.reset_list(self.list_target_bank)
        reset_lamps()
    
    def reset_lamps(self):
        pass #Todo
        
        
    def instanciate_general_matrix(self):
        Input.Start(x=7, y=4)
        Input.Test(x=7, y=0)
        Input.Tilt(x=7, y=5, external_event=event_Tilt)
        Input.Credit(x=7, y=1, value=Options.get('coin_values')[0]), 
        Input.Credit(x=7, y=2, value=Options.get('coin_values')[1])
        Input.Credit(x=7, y=3, value=Options.get('coin_values')[2])
        
    def instanciate_playfield_matrix(self): 
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
        
        
        
    def instanciate_display(self):
        self.dict_display['Timer'] = Display.Timer()
        self.dict_display['Bonus'] = Display.Bonus() 
        self.dict_display['Status'] = Display.Status()
        for i in range(1, 5):
            Display.Player(i)

