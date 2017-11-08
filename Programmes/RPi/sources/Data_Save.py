# -*- coding: utf-8 -*-
################################################################################
# Data Save
# 
#
################################################################################
import os
import pickle
import time

path = os.path.dirname(os.path.realpath(__file__)) + '\\pickle.dat'

def get_data(name):
	return get_all_data()[name]

def set_data(name, value):
	data = get_all_data()
	data[name] = value
	with open(path, "wb") as f:
		pickle.dump(data, f)

def get_all_data():
	with open(path, "rb") as f:
		data = pickle.load(f)
	return data

def add_score(score, time):
	average_score = get_data("average score")
	average_time = get_data("average time")
	total_play = get_data("total play")
	
	new_average_score = (average_score*total_play + score)/(total_play + 1)
	new_average_time = (average_time*total_play + time)/(total_play + 1)
	add_to_parameter("total play")
	set_data("average score", new_average_score)
	set_data("average time", new_average_time)

def add_scores(scores, time):
	for score in scores:
		add_score(score, time/len(scores))

def add_to_parameter(name):
	set_data(name, get_data(name)+1)
		
def add_tilt():
	add_to_parameter("total tilt")

def add_slam():
	add_to_parameter("total slam")	
	
def add_replay():
	add_to_parameter("total replay")
	
def add_extra_ball():
	add_to_parameter("extra ball") 

def get_time_hgtd():
	if get_data("time HGTD") == 0:
		return 0
	else:
		return time.time() - get_data("time HGTD")

def check_hgtd(value):
	if value >= get_data("HGTD"):
		set_data("HGTD", value)
		set_data("time HGTD", time.time())
		return True
	else:
		return False
	
def reset_data():
	data = dict()
	data["HGTD"] = 0
	data["credits"] = 0
	data["total play"] = 0
	data["average score"] = 0
	data["total replay"] = 0
	data["total extra ball"] = 0
	data["total tilt"] = 0
	data["total slam"] = 0
	data["time HGTD"] = 0
	data["average time"] = 0
	
	with open(path, "wb") as f:		
		pickle.dump(data, f)
		
if not os.path.isfile(path):
	reset_data()
	
