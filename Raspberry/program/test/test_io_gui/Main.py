#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
PINBALL_NAME = "Devil_Dare"

import os, sys
parent_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(parent_path + '/sources')
sys.path.append(parent_path + '/pinball/' + PINBALL_NAME)

import Pinball
from PyQt5.QtWidgets import QApplication
from App import App
from AppController import AppController
from AppView import AppView

if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        model = App()
        view = AppView()
        ctrl = AppController(model, view)
    except Exception as e:
        raise e
    
    sys.exit(app.exec_())