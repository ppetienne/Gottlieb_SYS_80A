# -*- coding: utf-8 -*-
################################################################################
# Devil Dare
# 
#
################################################################################   
import os, sys
parent_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(parent_path + '/sources')

import Common
import Input
import Output
import Display
import time
import Data_Save
import threading
import Contacts
import Options

################################################################################
# Output generales
Output.Lamp(lamp_control=Output.Lamp_Control.instances["LD1"], lamp_latch=Output.Lamp_Latch.instances["DS1"], name="Game Over Relay", playfield=False)
Output.Lamp(lamp_control=Output.Lamp_Control.instances["LD2"], lamp_latch=Output.Lamp_Latch.instances["DS1"], name="Tilt", playfield=False)
Output.Lamp(lamp_control=Output.Lamp_Control.instances["LD3"], lamp_latch=Output.Lamp_Latch.instances["DS1"], name="Coin Lockout Coil", playfield=False)
Output.Lamp(lamp_control=Output.Lamp_Control.instances["LD4"], lamp_latch=Output.Lamp_Latch.instances["DS1"], name="Shoot Again", playfield=False)
Output.Lamp(lamp_control=Output.Lamp_Control.instances["LD2"], lamp_latch=Output.Lamp_Latch.instances["DS4"], name="Multi-Ball Bonus", playfield=False)
Output.Lamp(lamp_control=Output.Lamp_Control.instances["LD3"], lamp_latch=Output.Lamp_Latch.instances["DS4"], name="Multi-Mode Timer", playfield=False)
Output.Lamp(lamp_control=Output.Lamp_Control.instances["LD3"], lamp_latch=Output.Lamp_Latch.instances["DS3"], name="High Game to Date", playfield=False)
Output.Lamp(lamp_control=Output.Lamp_Control.instances["LD4"], lamp_latch=Output.Lamp_Latch.instances["DS3"], name="Game Over Light", playfield=False)
Output.Lamp(lamp_control=Output.Lamp_Control.instances["LD1"], lamp_latch=Output.Lamp_Latch.instances["DS4"], name="Ball release", playfield=False)
Output.Lamp(lamp_control=Output.Lamp_Control.instances["LD3"], lamp_latch=Output.Lamp_Latch.instances["DS10"], name="2X")
Output.Lamp(lamp_control=Output.Lamp_Control.instances["LD4"], lamp_latch=Output.Lamp_Latch.instances["DS10"], name="3X")
Output.Lamp(lamp_control=Output.Lamp_Control.instances["LD4"], lamp_latch=Output.Lamp_Latch.instances["DS11"], name="Extra Ball")
Output.Lamp(lamp_control=Output.Lamp_Control.instances["LD1"], lamp_latch=Output.Lamp_Latch.instances["DS10"], name="2 Left Bottom Target")
Output.Lamp(lamp_control=Output.Lamp_Control.instances["LD2"], lamp_latch=Output.Lamp_Latch.instances["DS10"], name="2 Left Bottom Target")
Output.Lamp(lamp_control=Output.Lamp_Control.instances["LD3"], lamp_latch=Output.Lamp_Latch.instances["DS11"], name="Rollunder")
Output.Lamp(lamp_control=Output.Lamp_Control.instances["LD4"], lamp_latch=Output.Lamp_Latch.instances["DS4"], name="Special")
Output.Lamp(lamp_control=Output.Lamp_Control.instances["LD2"], lamp_latch=Output.Lamp_Latch.instances["DS9"], name="Hole")
Output.Lamp(lamp_control=Output.Lamp_Control.instances["LD3"], lamp_latch=Output.Lamp_Latch.instances["DS9"], name="Hole Capture")
Output.Lamp(lamp_control=Output.Lamp_Control.instances["LD4"], lamp_latch=Output.Lamp_Latch.instances["DS9"], name="Top Kicker Capture")

Output.Solenoid.instances["Sol 1"].set_new_name("Top Drop Target Bank")
Output.Solenoid.instances["Sol 2"].set_new_name("Top Ball Kicker")
Output.Solenoid.instances["Sol 3"].set_new_name("Hole")
Output.Solenoid.instances["Sol 4"].set_new_name("Ball Save Relay")
Output.Solenoid.instances["Sol 5"].set_new_name("Left Drop Target Bank")
Output.Solenoid.instances["Sol 6"].set_new_name("Right Drop Target Bank")
Output.Solenoid.instances["Sol 8"].set_new_name("Knocker")
Output.Solenoid.instances["Sol 9"].set_new_name("Outhole")

################################################################################
# Fonctions generales
def th_show_HGTD_attract_mode():
    cpt = 0
    show_hgdt = False
    time_show_hgtd = 2 # duree en s de l'affichage du hgtd
    time_wait = 2 # temps d'attente en s entre 2 affichages de hgtd
    time_refresh = 0.2 # intervalle interne pour la fluidite du programme
    hgtd = str(Data_Save.get_data("HGTD"))
    Common.set_display_players_all_zero()
    
    while Common.infos_game['status'] == Common.General_Status.ATTRACT_MODE:
        time.sleep(time_refresh)
        if cpt == time_wait/time_refresh and show_hgdt == False:
            Common.set_display_players(hgtd)
            show_hgdt = True
            cpt = 0
        elif cpt == time_show_hgtd/time_refresh and show_hgdt == True:
            Common.set_display_players_all_zero()
            show_hgdt = False
            cpt = 0
        else:
            cpt += 1

def power_on():
    Common.power_on()
        
def attract_mode():
    Common.attract_mode()
    Common.flash_playfield_lamp(1, 0.5)
    th = threading.Thread(target=th_show_HGTD_attract_mode)
    th.start()

def game_over_mode():
    Common.reset_target_drop()
    attract_mode()
     
def power_off():
    Common.power_off()


################################################################################
# Fonctions communes
def add_bonus_current_player(points):
    Display.Display.instances['Bonus'].set_value(points)

def get_bonus_current_player():
    return Display.Display.instances['Bonus'].get_value()

def set_Ball_Save(value):
    Output.Solenoid.instances["Ball Save Relay"].set_level(value)
    
################################################################################  
# Evenements externes
def event_common_Drop_Target(target_bank):
    add_bonus_current_player(400) # a definir
    set_Ball_Save(1)
    
    nb_targets_5_complete = [targets for targets in Input.Target_Bank_Drop.instances.values() if (len(targets.children) == 5 and targets.is_complete() == True)]
    targets_3_complete = [targets for targets in Input.Target_Bank_Drop.instances.values() if (len(targets.children) == 3 and targets.is_complete() == True)]
    
    if nb_targets_5_complete == 2 and targets_3_complete == 1:
        Output.Lamp.instances["Right Inside Return Rollover"].set_level(1)
        Output.Lamp.instances["Left Inside Return Rollover"].set_level(1)
        Output.Lamp.instances["3X"].set_level(1)
        Output.Lamp.instances["2X"].set_level(0)
    
    elif nb_targets_5_complete == 1 and targets_3_complete == 1:
        Output.Lamp.instances["2X"].set_level(1)
        
def event_Top_Drop_Target():
    event_common_Drop_Target(Input.Target_Bank.instances["Top Drop Target Bank"])
        
def event_Right_Drop_Target():
    event_common_Drop_Target(Input.Target_Bank.instances["Right Drop Target Bank"])
    Output.Lamp.instances["Hole Capture"].blink(1)
        
def event_Left_Drop_Target():
    event_common_Drop_Target(Input.Target_Bank.instances["Left Drop Target Bank"])
    Output.Lamp.instances["Top Kicker Capture"].blink(1)

def event_Left_Top_Target():
    set_Ball_Save(1)
    Output.Lamp.instances["Special"].set_level(1)

def event_Right_Bottom_Target():
    set_Ball_Save(1)
    Output.Lamp.instances['Extra Ball'].set_level(1)

def event_Bottom_Left_Bottom_Target():
    Output.Lamp.instances['Right Outside Return Rollover'].set_level(1)

def event_Top_Left_Bottom_Target():
    Output.Lamp.instances['Left Ouside Return Rollover'].set_level(1)

def event_Right_Top_Target():
    add_bonus_current_player(500) # a definir  

def event_Right_Outside_Rollover():
    if Output.Lamp.instances["Special"].get_level() == 1:
        Output.Lamp.instances["Special"].set_level(0)
        add_bonus_current_player(5000)    

def event_only_one_shot(lamp):
    lamp.set_level(0)
    
def event_Return_Rollover(lamp):
    lamp.set_level(1)
    Input.Input_Playfield.set_external_unique_event(event_only_one_shot, lamp)
    
def event_Rollunder():
    if Output.Lamp.instances['Extra Ball'].get_level() == 1:
        Output.Lamp.instances["Shoot Again"].set_level(1)
        Data_Save.add_extra_ball()
    if Output.Lamp.instances['Rollunder'].get_level() == 1:
        # lancer Multiball
        pass

def event_Spinner():
    add_bonus_current_player(1000) #todo       
    
def event_Top_Ball_Kicker():
    if Output.Lamp.instances["Top Kicker Capture"].is_blinking() == True and Input.Input_Playfield.instances['Hole'].value == 1:
        #lancer multiball
        pass
    input.eject_ball()
          

def event_Hole():
    if Output.Lamp.instances["Hole Capture"].is_blinking() == True:
        #lancer multiball
        pass
    input.eject_ball()

def event_OutHole():
    # verifier presence ensemble ball todo
    if Common.infos_game['status'] == Common.General_Status.TILT:
        Common.tilt_level(0)
        Common.infos_game['status'] = Common.General_Status.START
        
    if Common.infos_game['status'] == Common.General_Status.START:
        eject = False
        # todo lors du multiball
        if Output.Lamp.instances["Shoot Again"].get_level() != 1:
            Common.get_display_player().blink(0)
            multiplier = 1
            if Output.Lamp.instances["2X"].get_level() == 1:
                multiplier = 2
            if Output.Lamp.instances["3X"].get_level() == 1:
                multiplier = 3
            Common.set_display_players(get_bonus_current_player()*multiplier)
            
            if Input.Input_Playfield.instances["Hole"].get_level() == 1:
                Input.Input_Playfield.instances["Hole"].eject_ball()
            if Input.Input_Playfield.instances["Top Ball Kicker"].get_level() == 1:
                Input.Input_Playfield.instances["Top_Ball_Kicker"].eject_ball()
                
            if Common.infos_game['current_ball'] == Options.get_option('nb_balls') :
                
                if Common.infos_game['current_player'] == Common.infos_game['nb_players']:
                    Common.save_scores()
                    game_over_mode() 
            else:
                if Common.infos_game['current_player'] ==  Common.infos_game['nb_players']:
                    Common.infos_game['current_player'] = 1
                    Common.infos_game['current_ball'] += 1
                else:
                    Common.infos_game['current_player'] += 1
                eject = True
                Common.set_next_ball()
                Common.get_display_player().blink(1)
        else:
            eject = True
            
        
        if eject == True:
            Common.flash_playfield_lamp(1, 0.1)
            time.sleep(2)
            Common.flash_playfield_lamp(0)
            Input.Input_Playfield.instances["Outhole"].eject_ball()
    
def event_Start():
    pass

def event_Tilt():
    pass
    
def event_1st_Trough():
    #Common.infos_game['status'] = Common.General_Status.START
    #Input.Input_Playfield.set_external_unique_event(event_stop_blink_zero)
    pass
    
def event_3rd_Trough():
    pass 

################################################################################
# Input Generales
Input.Start(x=7, y=4, external_event=event_Start)
Input.Test(x=7, y=0)
Input.Slam(Contacts.conn.J5[10])
Input.Tilt(x=7, y=5, external_event=event_Tilt)
Input.Credit(x=7, y=1, name="Credit Left", value=Options.get_option('credits')[0]), 
Input.Credit(x=7, y=2, name="Credit Center", value=Options.get_option('credits')[1])
Input.Credit(x=7, y=3, name="Credit Right", value=Options.get_option('credits')[2])

################################################################################
# Input Playfield
temp_targets = Input.Target_Bank_Drop(name="Left Drop Target Bank", external_event=event_Left_Drop_Target)
for i in range(5):
    if i < 2:
        lamp_control = Output.Lamp_Control.instances["LD" + str(i+3)]
        lamp_latch = Output.Lamp_Latch.instances["DS5"]
    else:
        lamp_control = Output.Lamp_Control.instances["LD" + str(i-1)]
        lamp_latch = Output.Lamp_Latch.instances["DS6"]
    Input.Target_Drop(x=0, y=i, parent=temp_targets, position_enfant=i, lamp_control=lamp_control, lamp_latch=lamp_latch, points=[300,2000])

temp_targets = Input.Target_Bank_Drop(name="Right Drop Target Bank", external_event=event_Right_Drop_Target)
for i in range(5):
    if i < 2:
        lamp_control = Output.Lamp_Control.instances["LD" + str(i+3)]
        lamp_latch = Output.Lamp_Latch.instances["DS7"]
    else:
        lamp_control = Output.Lamp_Control.instances["LD" + str(i-1)]
        lamp_latch = Output.Lamp_Latch.instances["DS8"]
    Input.Target_Drop(x=1, y=i, parent=temp_targets, position_enfant=i, lamp_control=lamp_control, lamp_latch=lamp_latch, points=[300,2000])

temp_targets = Input.Target_Bank(name="Left Top Target Bank", external_event=event_Left_Top_Target)
for i in range(4):
    Input.Target(x=2, y=i, parent=temp_targets, nb_states=2, position_enfant=i, lamp_control=Output.Lamp_Control.instances["LD" + str(i+1)], lamp_latch=Output.Lamp_Latch.instances["DS12"], points=[500,2000])

if Options.get_option("nb_balls") == 3:
    nb_states = 1
else:
    nb_states = 2
    
temp_targets = Input.Target_Bank(name="Right Bottom Target Bank", external_event=event_Right_Bottom_Target)
for i in range(4):
    Input.Target(x=3, y=i, parent=temp_targets, position_enfant=i, lamp_control=Output.Lamp_Control.instances["LD" + str(i+1)], lamp_latch=Output.Lamp_Latch.instances["DS2"], points=[500,2000], nb_states=nb_states)

temp_targets = Input.Target_Bank_Drop(name="Top Drop Target Bank", external_event=event_Top_Drop_Target)
for i in range(3):
    if i < 1:
        lamp_control = Output.Lamp_Control.instances["LD" + str(i+4)]
        lamp_latch = Output.Lamp_Latch.instances["DS6"]
    else:
        lamp_control = Output.Lamp_Control.instances["LD" + str(i)]
        lamp_latch = Output.Lamp_Latch.instances["DS7"]
    Input.Target_Drop(x=4, y=i, parent=temp_targets, position_enfant=i, lamp_control=lamp_control, lamp_latch=lamp_latch, points=[300,2000])

Input.Spinner(x=5, y=1, name="Left Spin Target", lamp_control=Output.Lamp_Control.instances["LD4"], lamp_latch=Output.Lamp_Latch.instances["DS8"], points=[300,2000], external_event=event_Spinner)
Input.Spinner(x=6, y=2, name="Right Spin Target", lamp_control=Output.Lamp_Control.instances["LD1"], lamp_latch=Output.Lamp_Latch.instances["DS9"], points=[300,2000])

Input.Point(x=5, y=4, name="Top Left Bottom Target", points=2000, external_event=event_Top_Left_Bottom_Target)
Input.Point(x=6, y=4, name="Bottom Left Bottom Target", points=2000, external_event=event_Bottom_Left_Bottom_Target)               

Input.Input_Playfield(x=5, y=2, name="Right Top Target", external_event=event_Right_Top_Target)

Input.Trough(x=0, y=5, name="1st Trough", external_event=event_1st_Trough)
Input.Trough(x=1, y=5, name="3rd Trough", external_event=event_3rd_Trough)

Input.Point(x=6, y=3, name="Right Outside Rollover", points=5000, external_event=event_Right_Outside_Rollover)
Input.Point(x=2, y=4, name="Left Outside Rollover", points=10000)
                 
Input.Point_Light(x=3, y=5, name="Right Outside Return Rollover", lamp_control=Output.Lamp_Control.instances["LD2"], lamp_latch=Output.Lamp_Latch.instances["DS5"], points=[500,3000])
Input.Input_Playfield.instances["Right Outside Return Rollover"].set_external_event(event_Return_Rollover, lamp=Output.Lamp.instances['Right Outside Return Rollover']) 

Input.Point_Light(x=3, y=4, name="Left Outside Return Rollover", lamp_control=Output.Lamp_Control.instances["LD2"], lamp_latch=Output.Lamp_Latch.instances["DS11"], points=[500,3000])
Input.Input_Playfield.instances["Left Outside Return Rollover"].set_external_event(event_Return_Rollover, lamp=Output.Lamp.instances['Right Outside Return Rollover']) 

Input.Point_Light(x=4, y=5, name="Right Inside Return Rollover", lamp_control=Output.Lamp_Control.instances["LD1"], lamp_latch=Output.Lamp_Latch.instances["DS11"], points=[500,3000])
Input.Input_Playfield.instances["Right Inside Return Rollover"].set_external_event(event_Return_Rollover, lamp=Output.Lamp.instances['Right Outside Return Rollover']) 

Input.Point_Light(x=4, y=4, name="Left Inside Return Rollover", lamp_control=Output.Lamp_Control.instances["LD1"], lamp_latch=Output.Lamp_Latch.instances["DS11"], points=[500,3000])
Input.Input_Playfield.instances["Left Inside Return Rollover"].set_external_event(event_Return_Rollover, lamp=Output.Lamp.instances['Right Outside Return Rollover']) 

Input.Point(x=6, y=1, name="Rollunder", points=5000, external_event=event_Rollunder)

Input.Point(x=5, y=3, name="10 Points", points=10)
Input.Point(x=2, y=5, name="Kicking Rubber", points=30)

if Options.get_option("nb_balls") == 3:
    points = [1000, 3000]
else:
    points = [100, 300]
Input.Point_Light(x=4, y=3, name="Pop Bumper", lamp_control=Output.Lamp_Control.instances["LD1"], lamp_latch=Output.Lamp_Latch.instances["DS5"], points=points, blink_depend=True)

Input.Hole(x=5, y=0, name="Top Ball Kicker", external_event=event_Top_Ball_Kicker)
Input.Hole(x=6, y=0, name="Hole", external_event=event_Hole)

Input.OutHole(x=5, y=5, name="Outhole", external_event=event_OutHole)


################################################################################
# Display
Display.Timer()
Display.Bonus()