# -*- coding: utf-8 -*-
################################################################################
# Interface_Test
# 
#
################################################################################
import threading
           
class Test():
    def __init__(self):
        self._th = None
        self._end_th = False
        
    def start(self, *args):
        self.stop()
        self._th = threading.Thread(target=self._th_test, args=args)
        self._end_th = False
        self._th.start()
    
    def stop(self):
        if self._th != None: 
            self._end_th = True
            self._th.join()
            self._th = None
    
    def is_finished(self):
        if self._th != None and self._th.is_alive() == True:
            return False
        else:
            return True
    
    def join(self):
        self._th.join()
    
    def _th_test(self, **args):
        raise Exception("Methode non redefinie dans la classe fille")
    