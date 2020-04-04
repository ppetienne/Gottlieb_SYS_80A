#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import os, sys

from PyQt5.QtWidgets import QApplication
from GUI_Simulator.AppController import AppController
from GUI_Simulator.AppView import AppView

def Starter(game_operation):	
	app = QApplication(sys.argv)
	view = AppView()
	AppController(game_operation, view)
	sys.exit(app.exec_())