# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
import os
import functools

class AppView(QMainWindow):
    
    def __init__(self):
        super(AppView, self).__init__()
        self.build_ui()
        self.digits = dict()
        for digit in [getattr(self, value) for value in self.__dir__() if "spinBox_aff_" in value]:
            obj_name = digit.objectName().split('_')
            self.digits[obj_name[2] + '_' + obj_name[3]] = digit
            
        self.checkboxes_lamp = [getattr(self, value) for value in self.__dir__() if "checkBox_lamp" in value]
        
        self.checkboxes_matrix = [getattr(self, value) for value in self.__dir__() if "checkBox_sm" in value]
        
    def build_ui(self):
        uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + "\\main.ui", self)

        self.show()
        
    def set_connect_ctrl(self, ctrl):
        for checkbox in self.checkboxes_matrix:
            checkbox.clicked.connect(functools.partial(ctrl.onMatrix, checkbox))
                                     
    def set_tips_matrix(self, dict_tips):
        for checkbox in self.checkboxes_matrix:
            xy = checkbox.objectName().split('_')[2]
            if xy in dict_tips.keys():    
                checkbox.setToolTip(str(dict_tips[xy]))
            else:
                checkbox.setDisabled(True)
        
    def set_tips_lamp(self, dict_tips):
        for checkbox in self.checkboxes_lamp:
            pos = checkbox.objectName().split('_')[2]
            if int(pos) in dict_tips.keys():    
                checkbox.setToolTip(str(dict_tips[int(pos)]))
            else:
                checkbox.setDisabled(True)
    
    def nb_matrix_checkbox_activated(self):
        cpt = 0
        for checkbox in self.checkboxes_matrix:
            if checkbox.isChecked():
                cpt +=1
        return cpt
    
    def set_display(self, name, value, position):
        if value == " ":
            self.digits[name + '_' + str(position)].setValue(0)
        else:
            self.digits[name + '_' + str(position)].setValue(int(value))
    
    def set_lamp(self, name, value):
        for lamp in self.checkboxes_lamp:
            if name == lamp.toolTip():
                lamp.setChecked(bool(value))