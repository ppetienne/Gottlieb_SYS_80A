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
        
        self.slam = [getattr(self, value) for value in temp_list if "checkBox_slam" in value][0]
            
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
        #self.showMaximized()
        
    def set_connect_ctrl(self, ctrl):
        for matrix in self.matrix_dict.values():
            matrix.pressed.connect(functools.partial(ctrl.onChangedMatrix, matrix))
            matrix.released.connect(functools.partial(ctrl.onChangedMatrix, matrix))
        self.slam.clicked.connect(functools.partial(ctrl.onSlam, self.slam))
            
    def set_display(self, name, value):
        if name == "Status" :
            display = self.status
        elif name == "Bonus" :
            display = self.bonus
        elif name == "Timer":
            display = self.timer
        elif name[0] == "p" :
            display = self.player_list[int(name[1])-1]
        else :
            raise Exception("Nom " + name + " incorrect") 
        
        for index in range(len(value)):
            digit = value[-(index+1)]
            if digit.isdigit() == False:
                digit = 0
            display[index].setValue(int(digit))
    
    def set_matrix(self, name, value):        
        self.matrix_dict[name].setChecked(value)
    
    def set_slam(self, value):
        self.slam.setChecked(value)
        
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
           raise Exception("Nom " + name + " incorrect") 
        
        object_dict[number].setChecked(value)
        if value == 1:
            object_dict[number].setStyleSheet("color: green")
        else :
            object_dict[number].setStyleSheet("color: gray")
          
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
        
        for matrix in self.matrix_dict.values():
            if matrix.objectName().split("_")[-1] == matrix.text():
                matrix.setEnabled(False)
        
    @staticmethod    
    def format_matrix_label(label_dict):
        width = 8
        for key in label_dict:
            label_dict[key] = "\n".join(label_dict[key].split())
            #label_dict[key] = "\n".join([label_dict[key][i:i+width] for i in range(0, len(label_dict[key]), width)])
        return label_dict