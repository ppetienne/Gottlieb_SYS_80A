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

NB_BALL_SAVE = 0

################################################################################
# Output generales
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

################################################################################
# Fonctions generale   

################################################################################
# Fonctions communes
def add_bonus_current_player(points):
    Display.Display.instances['Bonus'].set_int_value(points, increment=True)

def get_bonus_current_player():
    return Display.Display.instances['Bonus'].get_value()

def eject_ball():
    Output.Lamp.instances["Ball Release"].set_level(1)
    time.sleep(0.5)
    Output.Lamp.instances["Ball Release"].set_level(0) 

def set_ball_save():
    Output.Solenoid.get_by_name("Ball Save Relay").set_level(1)
    
def add_ball_save():
    NB_BALL_SAVE += 1
    if NB_BALL_SAVE == 1:
        set_ball_save()
    
################################################################################  
# Evenements externes
def event_common_Drop_Target(target_bank):
    add_bonus_current_player(400) # a definir
    add_ball_save()
    
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
    add_ball_save()
    Output.Lamp.instances["Right Outside Rollover"].set_level(1)

def event_Right_Bottom_Target():
    add_ball_save()
    Output.Lamp.instances['Extra Ball'].set_level(1)

def event_Bottom_Left_Bottom_Target():
    Output.Lamp.instances['Right Outside Return Rollover'].set_level(1)

def event_Top_Left_Bottom_Target():
    Output.Lamp.instances['Left Ouside Return Rollover'].set_level(1)

def event_Right_Top_Target():
    add_bonus_current_player(500) # a definir  

def event_Right_Outside_Rollover():
    if Output.Lamp.instances["Right Outside Rollover"].get_level() == 1:
        Output.Lamp.instances["Right Outside Rollover"].set_level(0)
        add_bonus_current_player(5000)

def event_Left_Outside_Rollover():
    if NB_BALL_SAVE > 0:
        NB_BALL_SAVE -= 1
        set_ball_save()

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
    Input.Input_Playfield.instances["Top Ball Kicker"].eject_ball()
          

def event_Hole():
    if Output.Lamp.instances["Hole Capture"].is_blinking() == True:
        #lancer multiball
        pass
    else:
        Input.Input_Playfield.instances["Hole"].eject_ball()

def event_OutHole():
    Input.Input_Playfield.instances["OutHole"].eject_ball()
    
    
def event_Start():
    pass

def event_Tilt():
    pass
    
def event_1st_Trough():
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
            Common.add_points_current_player(get_bonus_current_player()*multiplier)
            
            if Input.Input_Playfield.instances["Hole"].get_level() == 1:
                Input.Input_Playfield.instances["Hole"].eject_ball()
            if Input.Input_Playfield.instances["Top Ball Kicker"].get_level() == 1:
                Input.Input_Playfield.instances["Top_Ball_Kicker"].eject_ball()
                
            eject = Common.check_next_ball()
        else:
            eject = True
            
        
        if eject == True:
            Common.flash_playfield_lamp(1, 0.1)
            time.sleep(2)
            Common.flash_playfield_lamp(0)
            eject_ball()
    
def event_3rd_Trough():
    pass 

################################################################################
# Input Generales
Input.Start(x=7, y=4, external_event=event_Start)
Input.Test(x=7, y=0)
Input.Slam(pin=Contacts.conn.J5[10])
Input.Tilt(x=7, y=5, external_event=event_Tilt)
Input.Credit(x=7, y=1, name="Credit Left", value=Options.get('coin_values')[0]), 
Input.Credit(x=7, y=2, name="Credit Center", value=Options.get('coin_values')[1])
Input.Credit(x=7, y=3, name="Credit Right", value=Options.get('coin_values')[2])

################################################################################
# Input Playfield
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

Input.Playfield(x=0, y=5, name="1st Trough", external_event=event_1st_Trough)
Input.Playfield(x=1, y=5, name="3rd Trough", external_event=event_3rd_Trough)

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


################################################################################
# Display
Display.Timer()
Display.Bonus()

if __name__ == "__main__":
    Common.power_on()   