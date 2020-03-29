# -*- coding: utf-8 -*-
import Input
import Output
import Display

class AppController():
    
    def __init__(self, view):
        self.view = view
        
        self.view.set_connect_ctrl(self)
        self.view.set_label("matrix", Input.Matrix.get_dict_name())
        self.view.set_label("lamp", Output.get_dict_name(Output.Lamp.instances))
        self.view.set_label("solenoid", Output.get_dict_name(Output.Solenoid.instances))
        
        for lamp in Output.Lamp.instances.values():
            lamp.event += self.onRefreshLamp
        for sol in Output.Solenoid.instances.values():
            sol.event += self.onRefreshSolenoid
        for relay in Output.Relay.instances.values():
            relay.event += self.onRefreshRelay
        for display in Display.Display.instances.values():
            display.event += self.onRefreshDisplay
        for matrix in Input.Matrix.instances.values():
            matrix.event += self.onRefreshMatrix
            matrix.event_end += self.onRefreshMatrix
        
        Input.slam.event += self.onRefreshSlam
        
        #Refresh des displays
        for display in Display.Display.instances.values():
            self.view.set_display(display.name, display.get_value())
        
        #Refresh des relais
        for key in Output.Relay.instances:
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