# -*- coding: utf-8 -*-
import Input
import Output
import Display

class AppController():
    
    def __init__(self, view):
        self.view = view
        
        self.view.set_connect_ctrl(self)
        self.view.set_label("matrix", Input.Matrix.get_dict_name())
        self.view.lock_matrix_without_label()
        self.view.set_label("lamp", Output.get_dict_name(Output.Lamp.instances))
        self.view.set_label("solenoid", Output.get_dict_name(Output.Solenoid.instances))
        for lamp in Output.Lamp.instances.values():
            lamp.event_GUI += self.onRefreshLamp
        for sol in Output.Solenoid.instances.values():
            sol.event_GUI += self.onRefreshSolenoid
        for relay in Output.Relay.instances.values():
            relay.event_GUI += self.onRefreshRelay
        for display in Display.Display.instances.values():
            display.event_GUI += self.onRefreshDisplay
        for matrix in Input.Matrix.instances.values():
            matrix.event_GUI += self.onRefreshMatrix
        for pin in Input.Simple_Pin.instances.values():
            pin.event_GUI += self.onRefreshPin

######################################################################################################
# Slots pour le model
    def onRefreshDisplay(self, earg):
        self.view.set_display(earg[0], earg[1])
    
    def onRefreshLamp(self, earg):
        self.view.set_output("lamp", earg[0], earg[1])
    
    def onRefreshSolenoid(self, earg):
        self.view.set_output("solenoid", earg[0], earg[1])
    
    def onRefreshRelay(self, earg):
        self.view.set_output("relay", earg[0], earg[1])
        
    def onRefreshSound(self, earg):
        self.view.set_output("sound", earg[0], earg[1])
    
    def onRefreshMatrix(self, earg):
        self.view.set_input("matrix", earg[0], earg[1])
        
    def onRefreshPin(self, earg):
        self.view.set_input("pin", earg[0], earg[1])
    
    
######################################################################################################
# Slots pour la vue
    def onChangedMatrix(self, earg):
        object_name = earg.objectName().split("_")
        try:
            if earg.isChecked() == True:
                earg.setChecked(False)
                Input.Matrix.get_by_yx(int(object_name[-1][0]), int(object_name[-1][1])).simulate(1)
            else:
                Input.Matrix.get_by_yx(int(object_name[-1][0]), int(object_name[-1][1])).simulate(0)
        except Exception as e :
            raise e
        
    
    def onChangedPin(self, earg):
        earg.setChecked(False)