# -*- coding: utf8 -*-
import Output 
import Input
import operator

class App():

    def __init__(self):
        pass
        
    def set_input(self, x, y, value):
        input = [input for input in Input.Input.instances.values() if (input.matrix_point.x == x and input.matrix_point.y == y)][0]
        input.simulate_actions.append(value)
    
    def get_list_name_output(self):
        dict_tips = dict()
        for input in Input.Input.instances.values():
            x = input.matrix_point.x
            y = input.matrix_point.y
            dict_tips[str(y)+str(x)] =  input.name
        return dict_tips
    
    def get_list_name_lamp(self):
        dict_tips = dict()
        try:
            cpt = 0
            for lamp in sorted(Output.Lamp.instances.values(), key=operator.attrgetter('position')):
                dict_tips[cpt] = lamp.name
                cpt += 1
        except Exception as e:
            raise e
        return dict_tips
        