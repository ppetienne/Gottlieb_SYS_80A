# -*- coding: utf-8 -*-
################################################################################
# Common
# Fonctions et parametres communs pouvant eventuellement etre utilises pour tous
# type de flipper SYS80A
################################################################################
import os
import json
from enum import Enum
import Display
import Input
import Output
import Data_Save
from Event import event
import time
import Options
import random

infos_game = dict()
infos_game['nb_players'] = 0
infos_game['current_ball'] = 0
infos_game['current_player'] = 0
infos_game['status'] = None
infos_game['nb_replay'] = 0
infos_game['begin time'] = 0

################################################################################
# Classes

class General_Status(Enum):
    TILT = 0
    ATTRACT_MODE = 1
    READY_TO_START = 2
    BALL_READY = 3
    START = 4
    TEST = 5
    SLAM = 6
    WAITING_BALLS = 7

################################################################################
# Fonctions critiques

def power_on():
    start_managers()
    #Activation entrees generales
    for input in [Input.Input.instances[key] for key in Input.Input.instances.keys() if (key not in Input.Input_Playfield.instances.keys())]:
        input.activated = True
        
    Output.Lamp.instances["Coin Lockout Coil"].set_level(1)
    attract_mode()
    
def start_managers():
    Display.manager.start()
    Input.manager.start()
    Output.sound_manager.start()
    
def attract_mode():
    infos_game['status'] = General_Status.ATTRACT_MODE
    game_over_level(1)
    
    for display in Display.Display.instances.values():
        display.attract_mode()
        
    for input in Input.Input_Playfield.instances.values():
        input.attract_mode()

def start_new_game():
    infos_game['nb_players'] = 0
    
    infos_game['current_ball'] = 1
    infos_game['current_player'] = 1
    infos_game['nb_replay'] = 0
    infos_game['begin time'] = time.time()
    
    for input in Input.Input_Playfield.instances.values():
        input.new_game()
    
    game_over_level(0)
    tilt_level(0)
        
def power_off():
    stop_managers()

    for lamp in Output.Lamp.instances.values():
        if lamp.get_level() == "blink":
            lamp.blink(0)
        
    for display in Display.Player.instances.values():
        if display.is_blinking() == True:
            display.blink(0)

def stop_managers():
    Display.manager.stop()
    Input.manager.stop()
    Output.sound_manager.stop()
    
################################################################################
# Fonctions generales

def flash_playfield_lamp(value, *args):
    for lamp in Output.Lamp.instances_playfield.values():
        lamp.blink(value, *args)
        
def add_credits(value):
    if get_credits() + value <= Options.get_option('maximum_credits'):
        Display.Display.instances['Status'].set_credit(value, increment=True)
    else:
        Display.Display.instances['Status'].set_credit(Options.get_option('maximum_credits'), increment=False)

def get_credits():
    return Data_Save.get_data('credits')

def add_player():
    if infos_game['nb_players'] < 4:
        infos_game['nb_players'] += 1
        Display.Player.instances[infos_game['nb_players']].set_double_zero()
        return True
    else:
        return False
        
def set_display_players(value):
    for display in Display.Player.instances.values():
        display.set_value(value, increment=False)
        
def set_display_players_all_zero():
    for display in Display.Player.instances.values():
        display.set_all_zero()

def tilt_level(value):
    Output.Lamp.instances["Tilt"].set_level(value)
    
def game_over_level(value):
    Output.Lamp.instances["Game Over Relay"].set_level(value)
    Output.Lamp.instances["Game Over Light"].set_level(value)

################################################################################
# Fonctions en cours de jeu   

def first_ball():
    if infos_game['status'] == General_Status.START and infos_game['current_ball'] == 1 and infos_game['current_player'] == 1:
        return True
    else:
        return False
      
def add_points_current_player(points):
    if Options.get_option('replay_limit') == 0 or infos_game['nb_replay'] < Options.get_option('replay_limit'):
        replay = 0
        current_display = get_display_player()
        old_val = current_display.get_value()
        current_display.set_value(points)
        current_val = current_display.get_value()
        
        for high_score in Options.get_option('high_scores_replay'):
            if old_val < high_score and current_val >= high_score:
                replay = 1
                break
        if Data_Save.check_hgtd(old_val) == False and Data_Save.check_hgtd(old_val) == True:
            replay += Options.get_option("high_play_award")
            
        if replay > 0:
            set_awards(replay)

def get_display_player():
    number = infos_game['current_player']
    return Display.Player.instances[number]

def set_next_ball():
    infos_game['current_ball'] += 1
    Display.Display.instances['Status'].set_status(infos_game['current_ball'])    
    
def impulse_knocker():
    Output.Solenoid.instances["Knocker"].set_level(1)
    time.sleep(0.5)
    Output.Solenoid.instances["Knocker"].set_level(0)
    Data_Save.add_replay()
    Display.Display.instances['Status'].set_credit(1, increment=True)

def reset_target_drop():
    for targets in Input.Target_Bank_Drop.instances.values():
        targets.reset()
        
def get_all_scores():
    scores = list()
    for i in range(infos_game['nb_players']):
        scores.append(Display.Player.instances[i+1].get_value())
    return scores
        
def save_scores():
    Data_Save.add_scores(get_all_scores(), (time.time() - Common.infos_game['begin time']))
    
def set_match():
    if Options.get_option('match') == True:
        rand = random.randrange(10)*10
        Display.Display.instances['Status'].set_status(rand) 
        replay = 0
        for score in get_all_scores():
            if score%100 == rand:
                replay += 1
        
        if replay > 0:
            set_awards(replay)
            
def set_awards(number):
    if Options.get_option('replay_limit') != 0 and (infos_game['nb_replay'] + replay) > Options.get_option('replay_limit'):
        replay = Options.get_option('replay_limit') - infos_game['nb_replay']
    infos_game['nb_replay'] += replay
        
    for i in range(replay):
        impulse_knocker()
        add_credits(1)
        time.sleep(0.5)
    