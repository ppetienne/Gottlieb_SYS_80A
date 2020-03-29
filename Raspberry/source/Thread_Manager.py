# -*- coding: utf-8 -*-
from Event import event
import time
import threading

class Thread_Manager():
    def __init__(self):
        self.event_end = event.Event()
        self._th = None
        self._end_th = False
        
    def start(self, **args_thread):
        self.stop()
        self._th = threading.Thread(target=self._th_function, kwargs=args_thread)
        self._end_th = False
        self._th.start()
    
    def stop(self):
        if self._th != None: 
            self._end_th = True
            self._th.join()
            self._th = None
    
    def _th_function(self, **args):
        raise Exception("Methode non redefinie dans la classe fille")
    
class Timer(Thread_Manager):
    def __init__(self):
        super().__init__()
        
    def _th_function(self, timeout):
        begin = time.time()
        while time.time() - begin < timeout and self._end_th == False:
            time.sleep(0.1)
        if self._end_th == False:
            self.event_end.fire()
    
class Test(Thread_Manager):
    wait_time = 0.5
    def __init__(self):
        super().__init__()
    
    def set_wait_time(value):
        Test.wait_time = value
    
    def is_finished(self):
        if self._th != None and self._th.is_alive() == True:
            return False
        else:
            return True
    
    def join(self):
        self._th.join()