# -*- coding: utf-8 -*-
################################################################################
# Data Save
# 
#
################################################################################
import os
import pickle
import time
import threading

path = os.path.dirname(os.path.realpath(__file__)) + '/data_save.dat'

protect = threading.Semaphore()

def get(name):
	return [data for data in get_all() if data["name"] == name][0]["value"]

def get_name_by_pos(pos):
	return get_all()[pos]["name"]

def get_by_pos(pos):
	return get_all()[pos]["value"]

def set_by_pos(pos, value):
	set(get_name_by_pos(pos), value)

def set(name, value):
	infos = get_all()
	pos = [i for i in range(len(infos)) if infos[i]["name"] == name][0]
	infos[pos]["value"] = value
	_save_pickle(infos)
	
def get_all():
	protect.acquire()
	with open(path, "rb") as f:
		data = pickle.load(f)
	protect.release()
	return data

def add_score(score, time):
	average_time = get("average time")
	total_play = get("total play")
	
	new_average_time = (average_time*total_play + time)/(total_play + 1)
	add_to_parameter("total play")
	set("average time", new_average_time)

def add_scores(scores, time):
	for score in scores:
		add_score(score, time/len(scores))

def add_to_parameter(name):
	set(name, get(name)+1)

def reset(name):
	set(name, 0)
	if name == "game percentage":
		set("total play", 0)
		set("total replay", 0)
	elif name == "average time":
		set("total play", 0)
 
def add_tilt():
	add_to_parameter("total tilt")

def add_slam():
	add_to_parameter("total slam")	
	
def add_replay():
	add_to_parameter("total replay")
	
def add_extra_ball():
	add_to_parameter("total extra ball") 

def add_coin(position_name):
	add_to_parameter("total coin " + position_name) 

def get_high_score_level():
	return [get("first high score level"), get("second high score level"), get("third high score level")]

def get_time_hgtd():
	if get("time HGTD") == 0:
		return 0
	else:
		return time.time() - get("time HGTD")

def check_hgtd(value):
	if value >= get("HGTD"):
		set("HGTD", value)
		set("time HGTD", time.time())
		return True
	else:
		return False

def _save_pickle(infos):
	protect.acquire()
	with open(path, "wb") as f:
		pickle.dump(infos, f)
	protect.release()
	
def reset():
	infos = list()
	infos.append({"name":"total coin left", "value":0})
	infos.append({"name":"total coin center", "value":0})
	infos.append({"name":"total coin right", "value":0})
	infos.append({"name":"total play", "value":0})
	infos.append({"name":"total replay", "value":0})
	infos.append({"name":"game percentage", "value":0})
	infos.append({"name":"total extra ball", "value":0})
	infos.append({"name":"total tilt", "value":0})
	infos.append({"name":"total slam", "value":0})
	infos.append({"name":"time HGTD", "value":0})
	infos.append({"name":"first high score level", "value":1500000})
	infos.append({"name":"second high score level", "value":1000000})
	infos.append({"name":"third high score level", "value":500000})
	infos.append({"name":"HGTD", "value":0})
	infos.append({"name":"average time", "value":0})
	
	_save_pickle(infos)
		
if not os.path.isfile(path):
	reset()