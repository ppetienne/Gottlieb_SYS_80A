# -*- coding: utf-8 -*-
import Input
import Output
import Display

class AppController():
    
    def __init__(self, game_operation, view):
        self.view = view
        
        self.view.set_connect_ctrl(self)
        self.view.set_label("matrix", game_operation.dict_matrix)
        self.view.set_label("lamp", game_operation.dict_lamp)
        self.view.set_label("solenoid", game_operation.dict_solenoid)
        
        for lamp in game_operation.dict_lamp.values():
            lamp.event += self.onRefreshLamp
        for sol in game_operation.dict_solenoid.values():
            sol.event += self.onRefreshSolenoid
        for relay in game_operation.dict_relay.values():
            relay.event += self.onRefreshRelay
        for display in game_operation.dict_display.values():
            display.event += self.onRefreshDisplay
        for matrix in game_operation.dict_matrix.values():
            matrix.high_event += self.onRefreshMatrix
            matrix.low_event += self.onRefreshMatrix
        
        game_operation.slam.low_event += self.onRefreshSlam
        game_operation.slam.high_event += self.onRefreshSlam
        
        #Refresh des displays
        for display in game_operation.dict_display.values():
            self.view.set_display(display.name, display.get_value())
        
        #Refresh des relais
        for key in game_operation.dict_relay:
            relay = Output.Relay.instances[key]
            self.view.set_output("relay", relay.num, relay.get_level())

######################################################################################################
# Slots pour le model
    def onRefreshDisplay(self, earg):
        self.view.set_display(earg.name, earg.get_value())
    
    def onRefreshLamp(self, earg):
        self.view.set_output("lamp", earg.num, earg.get_level())
    
    def onRefreshSolenoid(self, earg):
        self.view.set_output("solenoid", earg.num, earg.get_level())
    
    def onRefreshRelay(self, earg):
        self.view.set_output("relay", earg.num, earg.get_level())
        
    def onRefreshSound(self, earg):
        self.view.set_output("sound", earg.num, earg.get_level())
    
    def onRefreshMatrix(self, earg):
        self.view.set_matrix(earg.yx_str, earg.get_level())
        
    def onRefreshSlam(self, earg):
        self.view.set_slam(earg.get_level())
    
    
######################################################################################################
# Slots pour la vue
    def onChangedMatrix(self, earg):
        object_name = earg.objectName().split("_")
        try:
            if earg.isChecked() == True:
                earg.setChecked(False)
                Input.Matrix.get_by_xy(int(object_name[-1][1]), int(object_name[-1][0])).sim.simulate(1)
            else:
                Input.Matrix.get_by_xy(int(object_name[-1][1]), int(object_name[-1][0])).sim.simulate(0)
        except Exception as e :
            raise e
    
    def onSlam(self, earg):
        if earg.isChecked() == True:
            Input.slam.simulate(1)
        else:
            Input.slam.simulate(0)