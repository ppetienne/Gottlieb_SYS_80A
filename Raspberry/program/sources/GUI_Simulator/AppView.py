# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
import os
import functools

class AppView(QMainWindow):
    
    def __init__(self):
        super(AppView, self).__init__()
        self.build_ui()
        
        temp_list = sorted(self.__dir__())
        self.player_list = list()
        self.player_list.append([getattr(self, value) for value in temp_list if "aff_p1" in value])
        self.player_list.append([getattr(self, value) for value in temp_list if "aff_p2" in value])
        self.player_list.append([getattr(self, value) for value in temp_list if "aff_p3" in value])
        self.player_list.append([getattr(self, value) for value in temp_list if "aff_p4" in value])
        self.bonus = [getattr(self, value) for value in temp_list if "aff_bonus" in value]
        self.timer = [getattr(self, value) for value in temp_list if "aff_timer" in value]
        self.status = [getattr(self, value) for value in temp_list if "aff_status" in value]
       
        self.matrix_dict = dict()
        for matrix in [getattr(self, value) for value in temp_list if "pushButton_sm" in value] :
            self.matrix_dict[matrix.objectName().split("_")[-1]] = matrix
        
        self.pin_dict = dict()
        for pin in [getattr(self, value) for value in temp_list if "checkBox_pin" in value] :
            self.pin_dict[pin.objectName().split("_")[-1]] = pin
            
        self.lamp_dict = dict()
        for lamp in [getattr(self, value) for value in temp_list if "checkBox_lamp" in value] :
            self.lamp_dict[int(lamp.objectName().split("_")[-1])] = lamp
        
        self.relay_dict = dict()
        for relay in [getattr(self, value) for value in temp_list if "checkBox_relay" in value] :
            self.relay_dict[int(relay.objectName().split("_")[-1])] = relay
            
        self.solenoid_dict = dict()
        for solenoid in [getattr(self, value) for value in temp_list if "checkBox_sol" in value] :
            self.solenoid_dict[int(solenoid.objectName().split("_")[-1])] = solenoid
            
        self.sound_dict = dict()
        for sound in [getattr(self, value) for value in temp_list if "checkBox_sound" in value] :
            self.sound_dict[int(sound.objectName().split("_")[-1])] = sound

    def build_ui(self):
        uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + "\\main.ui", self)

        self.show()
        
    def set_connect_ctrl(self, ctrl):
        for matrix in self.matrix_dict.values():
            matrix.clicked.connect(functools.partial(ctrl.onChangedMatrix, matrix))
        for pin in self.pin_dict.values() :
            pin.clicked.connect(functools.partial(ctrl.onChangedPin, pin))
            
    def set_display(self, name, value):
        pass
    
    def set_input(self, name, value):
        if name == "matrix" :
            object_dict = self.matrix_dict
        elif name == "pin" :
            object_dict = self.pin_dict
        else :
           raise Exception("Nom de la liste incorrect") 
        
        object_dict[number].setChecked(value)
        
    def set_output(self, name, number, value):
        if name == "lamp" :
            object_dict = self.lamp_dict
        elif name == "relay" :
            object_dict = self.relay_dict
        elif name == "sound" :
            object_dict = self.sound_dict
        elif name == "solenoid" :
            object_dict = self.solenoid_dict
        else :
           raise Exception("Nom de la liste incorrect") 
        
        object_dict[number].setChecked(value)
          
    def set_label(self, name, dict_label):
        if name == "matrix" :
            object_dict = self.matrix_dict
            dict_label = self.format_matrix_label(dict_label)
        elif name == "lamp" :
            object_dict = self.lamp_dict
        elif name == "sound" :
            object_dict = self.sound_dict
        elif name == "solenoid" :
            object_dict = self.solenoid_dict
        else :
           raise Exception("Nom de la liste incorrect") 
       
        for key in dict_label:
            object_dict[key].setText(dict_label[key])
    
    def lock_matrix_without_label(self):
        for matrix in self.matrix_dict.values():
            if matrix.objectName().split("_")[-1] == matrix.text():
                matrix.setEnabled(False)
                
    def format_matrix_label(self, label_dict):
        width = 8
        for key in label_dict:
            label_dict[key] = "\n".join(label_dict[key].split())
            #label_dict[key] = "\n".join([label_dict[key][i:i+width] for i in range(0, len(label_dict[key]), width)])
        return label_dict