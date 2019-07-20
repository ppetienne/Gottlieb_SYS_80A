#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import os, sys
parent_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(parent_path + '/sources')

from PyQt5.QtWidgets import QApplication
from AppController import AppController
from AppView import AppView

def start_GUI():
    try:
        app = QApplication(sys.argv)
        view = AppView()
        AppController(view)
        sys.exit(app.exec_())
    except Exception as e:
        raise e