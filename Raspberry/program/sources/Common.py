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
import threading

infos_game = dict()
infos_game['nb_players'] = 0
infos_game['current_ball'] = 0
infos_game['current_player'] = 0
infos_game['status'] = None
infos_game['nb_replay'] = 0
infos_game['begin time'] = 0

TEST_MODE = False

################################################################################
# Classes

class General_Status(Enum):
    ATTRACT_MODE = 1
    START = 3
    
class Timer():
    def __init__(self):
        self.event_end = event.Event()
        self._th = None
        self._end_th = False
        
    def start(self, timeout):
        self.stop()
        self._th = threading.Thread(target=self._th_timer, args=(timeout,))
        self._end_th = False
        self._th.start()
    
    def stop(self):
        if self._th != None: 
            self._end_th = True
            self._th.join()
            self._th = None
    
    def _th_timer(self, timeout):
        begin = time.time()
        while time.time() - begin < timeout and self._end_th == False:
            time.sleep(0.1)
        if self._end_th == False:
            self.event_end.fire()
            
class Test():
    def __init__(self):
        self._th = None
        self._end_th = False
        
    def start(self, *args):
        self.stop()
        self._th = threading.Thread(target=self._th_test, args=args)
        self._end_th = False
        self._th.start()
    
    def stop(self):
        if self._th != None: 
            self._end_th = True
            self._th.join()
            self._th = None
    
    def is_finished(self):
        if self._th != None and self._th.is_alive() == True:
            return False
        else:
            return True
    
    def join(self):
        self._th.join()
    
    def _th_test(self, **args):
        raise Exception("Methode non redefinie dans la classe fille")
    
################################################################################
# Fonctions critiques

def power_on():
    start_managers()
    #Activation entrees generales
    for input in [Input.Input.instances[key] for key in Input.Input.instances.keys() if (key not in Input.Input_Playfield.instances.keys())]:
        input.activated = True
        
    Output.Output_Driver.instances["Coin Lockout Coil"].set_level(1)
    attract_mode()
    
def start_managers():
    Display.manager.start()
    Input.manager.start()
    Output.sound_manager.start()
    
def attract_mode():
    infos_game['status'] = General_Status.ATTRACT_MODE
    set_game_over_level(1)
    
    for display in Display.Display.instances.values():
        display.attract_mode()
        
    for input in Input.Input_Playfield.instances.values():
        input.attract_mode()
    
    flash_playfield_lamp(1, 0.5)
    th = threading.Thread(target=_th_show_HGTD_attract_mode)
    #th.start()

def game_over_mode():
    reset_target_drop()
    attract_mode()
    
def start_new_game():
    infos_game['nb_players'] = 0
    
    infos_game['current_ball'] = 1
    infos_game['current_player'] = 1
    infos_game['nb_replay'] = 0
    infos_game['begin time'] = time.time()
    flash_playfield_lamp(0)
    for input in Input.Input_Playfield.instances.values():
        input.new_game()
    
    set_game_over_level(0)
    set_tilt_level(0)
        
def power_off():
    stop_managers()

    for lamp in Output.Lamp.instances.values():
        if lamp.get_level() == "blink":
            lamp.blink(0)
        
    for display in Display.Player.instances.values():
        if display.is_blinking() == True:
            display.blink(0)
            
    for input in Input.Input.instances.values():
        input.end()

def stop_managers():
    Display.manager.stop()
    Input.manager.stop()
    Output.sound_manager.stop()
    
################################################################################
# Fonctions generales
       
def _th_show_HGTD_attract_mode():
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
            
def flash_playfield_lamp(value, *args):
    for lamp in Output.Lamp_Playfield.instances.values():
        lamp.blink(value, *args)
        
def add_credits(value):
    if Display.Display.instances['Status'].get_credit() + value <= Options.get('maximum_credits'):
        Display.Display.instances['Status'].set_credit(value, increment=True)
        Output.Output_Driver.instances["Coin Lockout Coil"].set_level(1)
    else:
        Display.Display.instances['Status'].set_credit(Options.get('maximum_credits'), increment=False)
        Output.Output_Driver.instances["Coin Lockout Coil"].set_level(0)

def add_player():
    if infos_game['nb_players'] < 4:
        infos_game['nb_players'] += 1
        Display.Player.instances[infos_game['nb_players']].set_double_zero()
        return True
    else:
        return False
        
def set_display_players(value):
    for display in Display.Player.instances.values():
        display.set_value(value)
        
def set_display_players_all_zero():
    for display in Display.Player.instances.values():
        display.set_all_zero()

def init_displays():
    for display in Display.Display.instances.values():
        display.init_val()
        
def set_tilt_level(value):
    Output.Output_Driver.instances["Tilt"].set_level(value)

def get_tilt_level():
    return Output.Output_Driver.instances["Tilt"].get_level()

def set_game_over_level(value):
    Output.Output_Driver.instances["Game Over Relay"].set_level(value)
    Output.Lamp.instances["Game Over Light"].set_level(value)

def get_game_over_level():
    return Output.Lamp.instances["Game Over Light"].get_level()
################################################################################
# Fonctions en cours de jeu   

def first_ball():
    if infos_game['status'] == General_Status.START and infos_game['current_ball'] == 1 and infos_game['current_player'] == 1:
        return True
    else:
        return False

def check_next_ball():
    eject = False
    if infos_game['current_ball'] == get('nb_balls') :   
        if infos_game['current_player'] == infos_game['nb_players']:
            save_scores()
            game_over_mode() 
    else:
        if infos_game['current_player'] ==  infos_game['nb_players']:
            infos_game['current_player'] = 1
            infos_game['current_ball'] += 1
        else:
            infos_game['current_player'] += 1
        eject = True
        set_next_ball()
        get_display_player().blink(1)
    return eject

def add_points_current_player(points):
    if Options.get('replay_limit') == 0 or infos_game['nb_replay'] < Options.get('replay_limit'):
        replay = 0
        current_display = get_display_player()
        old_val = current_display.get_int_value()
        current_display.set_int_value(points, increment=True)
        current_val = current_display.get_int_value()
        
        for high_score in Data_Save.get_high_score_level():
            if old_val < high_score and current_val >= high_score:
                replay = 1
                break
        if Data_Save.check_hgtd(old_val) == False and Data_Save.check_hgtd(old_val) == True:
            replay += Options.get("high_play_award")
            
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
        scores.append(Display.Player.instances[i+1].get_int_value())
    return scores
        
def save_scores():
    Data_Save.add_scores(get_all_scores(), (time.time() - infos_game['begin time']))
    
def set_match():
    if Options.get('match') == True:
        rand = random.randrange(10)*10
        Display.Display.instances['Status'].set_status(rand) 
        replay = 0
        for score in get_all_scores():
            if score%100 == rand:
                replay += 1
        
        if replay > 0:
            set_awards(replay)
            
def set_awards(number):
    if Options.get('replay_limit') != 0 and (infos_game['nb_replay'] + replay) > Options.get('replay_limit'):
        replay = Options.get('replay_limit') - infos_game['nb_replay']
    infos_game['nb_replay'] += replay
        
    for i in range(replay):
        impulse_knocker()
        add_credits(1)
        time.sleep(0.5)
    