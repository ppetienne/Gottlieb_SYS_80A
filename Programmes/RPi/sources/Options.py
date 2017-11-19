import os
import json 
import threading

filename = "options.json"
path = os.path.dirname(os.path.realpath(__file__)) + '\\' + filename

protect = threading.Semaphore()

def get_all_options():
    protect.acquire()
    with open(path) as options_file:    
        options = json.load(options_file)
    protect.release()
    _check_all_options(options)
    return options

def set_all_options(options_dict):
    _check_all_options(options_dict)
    _save_json(options)

def get_option(name):  
    return get_all_options()[name]

def set_option(name, value):
    _check_option(name, value)
    options = get_all_options()
    options[name] = value
    _save_json(options)

def _save_json(options_dict):
    protect.acquire()
    with open(path, 'w') as options_file:
        json.dump(options_dict, options_file, sort_keys=True, indent=4)
    protect.release()
    
def _check_all_options(options_dict):
    for key in options_dict.keys():
        _check_option(key, options_dict[key])
        
def _check_option(name, value):
    str_exception = "Erreur fichier " + filename + " : le parametre " + name + " "
    def raise_exception():
        raise AttributeError(str_exception + "est incorrect (valeur: " + value + ")")
    
    if (name not in ['pinball_name', 'nb_balls', 'hardware', 'maximum_credits', 'playfield_special', 'high_play_award', 'match', 'replay_limit', 'novelty', 'game_mode', 'high_scores_replay'] 
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
    
    if name == "credit" and len([credit for credit in value if credit < 0]) > 0:
        raise_exception('credit')
    
    if name == 'high_scores_replay' and (len(value) > 3 or sorted(value) != value):
        raise_exception()

def reset_options():
    options = dict()
    options["pinball_name"] = "Devil_Dare"
    options["hardware"] = False
    options["nb_balls"] = 3
    options["maximum_credits"] = 99
    options["playfield_special"] = True
    options["high_play_award"] = 2
    options["match"] = True
    options["replay_limit"] = 0
    options["novelty"] = True
    options["game_mode"] = "Extra Ball"
    options["high_scores_replay"] = [500000, 1000000, 1500000]
    options["credits"] = [1, 2, 1]
    
    _check_all_options(options)
    _save_json(options)
        
if not os.path.isfile(path):
    reset_options()