# -*- coding: utf-8 -*-
################################################################################
# Game
################################################################################
import sys
import os
import json
from enum import Enum
import Display
import Input
import Output
import Data_Save
import time
import Options
import random

class Game_Play_MB():
    def __init__(self, pinball):
        self.pinball = pinball
        self.nb_player = 1
        self.current_ball = 1
        self.current_player = 1
        self.nb_free_replay = 0
        self.begin_time = time.time()
        self.free_extra_ball = False
        self.extra_ball_in_play = False           
            
    def set_display_players(self, value):
        for display in Display.Player.instances.values():
            display.set_value(value)
            
    def set_display_players_all_zero(self):
        for display in Display.Player.instances.values():
            display.set_all_zero()
    
    def init_displays(self):
        for display in Display.Display.instances.values():
            display.init_val()
 
    def set_extra_ball(self):
        self.extra_ball = True
        
    def is_(self):
        if self.current_ball == 1 and self.current_player == 1:
            return True
        else:
            return False
    
    def set_next_ball():
        to_eject = True
        if next_ball_to_eject():   
            if infos_game['current_player'] ==  infos_game['nb_players']: #Nouvelle balle+1
                infos_game['current_player'] = 1
                infos_game['current_ball'] += 1
                Display.Display.instances['Status'].set_status(infos_game['current_ball'])
            else:
                infos_game['current_player'] += 1
            get_display_player().blink(1)
        else:
            save_scores()
            game_over_mode()
            to_eject = False
        
        return to_eject
    
    def eject_ball(new_player=True):
        if new_player == True:
            Output.Lamp_Playfield.blink_all(1, blink_period=1)
            time.sleep(1)
            Output.Lamp_Playfield.blink_all(0)
        
        
    def next_ball_to_eject():
        if infos_game['current_ball'] == Options.get('nb_balls') and infos_game['current_player'] == infos_game['nb_players']:
            return False
        else :
            return True
        
    def add_points_current_player(points):
        replay = 0
        current_display = get_display_player()
        old_val = current_display.get_int_value()
        current_display.set_value(points, increment=True)
        current_val = current_display.get_int_value()
        
        for high_score in Data_Save.get_high_score_level():
            if old_val < high_score and current_val >= high_score:
                replay = 1
                break
        if Data_Save.check_hgtd(old_val) == False and Data_Save.check_hgtd(current_val) == True:
            replay += Options.get("high_play_award")
            
        if replay > 0:
            set_awards(replay)
    
    def get_display_player():
        return Display.Player.get_by_num(infos_game['current_player'])
        
    def impulse_knocker():
        Output.Solenoid.instances["Knocker"].set_level(1)
        time.sleep(0.5)
        Output.Solenoid.instances["Knocker"].set_level(0)
        Data_Save.add_replay()
        Display.Display.instances['Status'].set_credit(1, increment=True)
        
    def get_all_scores():
        scores = list()
        for i in range(infos_game['nb_players']):
            scores.append(Display.Player.get_by_num(i+1).get_int_value())
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
        replay = number
        if Options.get('replay_limit') != 0 and (infos_game['nb_replay'] + replay) > Options.get('replay_limit'):
            replay = Options.get('replay_limit') - infos_game['nb_replay']
        infos_game['nb_replay'] += replay
            
        for i in range(replay):
            impulse_knocker()
            add_credits(1)
  
    def activate_ball_saved():
        Output.Solenoid["Ball Save Relay"].pulse()
