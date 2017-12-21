# -*- coding: utf-8 -*-
from Display import Display
from Output import Output_CM
class AppController():
    
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        self.view.set_tips_matrix(self.model.get_list_name_output())
        self.view.set_tips_lamp(self.model.get_list_name_lamp())
        Display.event_refresh += self.onRefreshDisplay
        Output_CM.event_new_state += self.onRefreshLamp
        self.view.set_connect_ctrl(self)


######################################################################################################
# Slots pour la vue
    def onRefreshDisplay(self, earg):
        self.view.set_display(earg[0].lower(), earg[1], earg[2])
    
    def onRefreshLamp(self, earg):
        self.view.set_lamp(earg[0], earg[1])
            
    def onMatrix(self, earg):
        if self.view.nb_matrix_checkbox_activated() < 3:
            yx = earg.objectName().split('_')[2]
            self.model.set_input(int(yx[1]), int(yx[0]), int(earg.isChecked()))
        else:
            earg.setChecked(False)
