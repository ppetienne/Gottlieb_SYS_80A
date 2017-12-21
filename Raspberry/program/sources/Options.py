# -*- coding: utf-8 -*-
################################################################################
# Options
# 
#
################################################################################
import os
import json 
import threading

filename = "infos.json"
path = os.path.dirname(os.path.realpath(__file__)) + '\\' + filename

protect = threading.Semaphore()

def get_all():
    protect.acquire()
    with open(path) as f:    
        infos = json.load(f)
    protect.release()
    _check_all(infos)
    return infos

def set_all(infos):
    _check_all(infos)
    _save_json(infos)

def get(name):  
    return get_all()[name]

def set(name, value):
    _check(name, value)
    infos = get_all()
    infos[name] = value
    _save_json(infos)

def _save_json(infos):
    protect.acquire()
    with open(path, 'w') as f:
        json.dump(infos, f, sort_keys=True, indent=4)
    protect.release()
    
def _check_all(infos):
    for key in infos.keys():
        _check(key, infos[key])
        
def _check(name, value):
    str_exception = "Erreur fichier " + filename + " : le parametre " + name + " "
    def raise_exception():
        raise AttributeError(str_exception + "est incorrect (valeur: " + value + ")")
    
    if (name not in ['coin_values', 'pinball_name', 'nb_balls', 'hardware', 'maximum_credits', 'playfield_special', 'high_play_award', 'match', 'replay_limit', 'novelty', 'game_mode'] 
        and "credit" not in name):
        raise AttributeError(str_exception + "n'existe pas")
    
    if name == 'nb_balls' and (value != 3 and value != 5):
        raise_exception()
    if name == 'hardware' and (value != True and value != False):
        raise_exception()
    if name == 'maximum_credits' and (value > 99 or value < 1):
        raise_exception()
    if name == 'playfield_special' and (value != True and value != False):
        raise_exception()
    if name == 'high_play_award' and (value > 2 or value < 0):
        raise_exception()
    if name == 'match' and (value != True and value != False):
        raise_exception()
    if name == 'replay_limit' and (value < 0):
        raise_exception()
    if name == 'novelty' and (value != True and value != False):
        raise_exception('novelty')
    if name == 'game_mode' and (value != "Extra Ball" and value != "Replay"):
        raise_exception()
    if name == "coin_values" and len([credit for credit in value if credit < 0]) > 0:
        raise_exception()
    
    if name == "credits" and (value < 0):
        raise_exception()

def reset():
    infos = dict()
    infos["coin_values"] = [1, 1, 1]
    infos["pinball_name"] = "Devil_Dare"
    infos["credits"] = 0
    infos["hardware"] = False
    infos["nb_balls"] = 3
    infos["maximum_credits"] = 99
    infos["playfield_special"] = True
    infos["high_play_award"] = 2
    infos["match"] = True
    infos["replay_limit"] = 0
    infos["novelty"] = True
    infos["game_mode"] = "Extra Ball"
    
    
    _check_all(infos)
    _save_json(infos)
        
if not os.path.isfile(path):
    reset()