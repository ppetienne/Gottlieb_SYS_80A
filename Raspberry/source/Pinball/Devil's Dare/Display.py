# -*- coding: utf-8 -*-
################################################################################
# Display
# 
#
################################################################################

class Player(Display):
    def __init__(self, num):
        """ Construit un objet Display
        Keyword arguments:
        *** -- ***
        """
        if num == 1 or num == 2:
            segment_number = 0
        else:
            segment_number = 1
        if num == 1 or num == 3:
            list_digits = 0
        else:
            list_digits = 1
        super().__init__(7, segment_number, list_digits)
        self.num = num
        self._th_blink = None 
        self._end_th_blink = False
    
    def blink(self, level):
        if self._th_blink != None:
            self._end_th_blink = True
            self._th_blink.join()
            self._th_blink = None
            
        if level == 1: 
            self._th_blink = threading.Thread(target=self._th_manage_blink)
            self._end_th_blink = False
            self._th_blink.start()
            
    def set_double_zero(self):
        self.set_value("00")
    
    def is_blinking(self):
        if self._th_blink != None and self._th_blink.is_alive():
            return True
        else:
            return False
        
    def _th_manage_blink(self):
        while self._end_th_blink == False:
            self.set_displayed(True)
            time.sleep(0.5)
            self.set_displayed(False)
            time.sleep(0.5)
        self.set_displayed(True)
    
    def get_by_num(num):
        return [player for player in Player.instances.values() if player.num == num][0]

###########################
class Bonus(Display):
    def __init__(self):
        """ Construit un objet Display
        Keyword arguments:
        *** -- ***
        """
        segment_number = 2
        list_digits = 2
        super().__init__(6, segment_number, list_digits, "000000")

###########################   
class Timer(Display):
    def __init__(self):
        """ Construit un objet Display
        Keyword arguments:
        *** -- ***
        """
        segment_number = 2
        list_digits = 3
        super().__init__(6, segment_number, list_digits, "000000")        


###########################
class Status(Display):
    def __init__(self):
        """ Construit un objet Display
        Keyword arguments:
        *** -- ***
        """
        segment_number = 2
        list_digits = 4
        super().__init__(4, segment_number, list_digits, default_val="0  ")
        self.set_credit(self.get_credit())
        
    def attract_mode(self):
        self.set_value(str(self.get_credit()) + "  ")
        
    def set_credit(self, value, increment=False):
        if increment == True:
            new_value = self.get_credit() + value
        else:
            new_value = value
        self.set_value(str(new_value) + self._get_status_str())
        
        Options.set("credits", new_value)
        
    def set_status(self, value):
        if value < 10:
            temp_val = " " + str(value)
        else:
            temp_val = str(int(value/10)) + str(int(value%10))
            
        self.set_value(str(self.get_credit()) + temp_val)
        
    def get_credit(self):
        return Options.get("credits")
    
    def _get_status_str(self):
        return self.get_value()[-2] + self.get_value()[-1]