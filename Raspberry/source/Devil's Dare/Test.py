################################################################################
def event_Slam(self, earg):
        if Common.infos_game['status'] == Common.General_Status.TEST_MODE:    
            Input.instances['Test'].end_test()
        else:
            Common.attract_mode()
            Data_Save.add_slam()
            super().event_action(earg)
################################################################################
def event_Tilt(self, earg):
        if Common.infos_game['status'] == Common.General_Status.TEST_MODE:    
            Input.instances['Test'].end_test()
        elif Common.infos_game['status'] == Common.General_Status.START:
            Data_Save.add_tilt()
            Common.set_tilt_level(1)
            for lamp in Output.Lamp.instances.values():
                lamp.set_level(0)
            
            for input_p in Playfield.instances.values():
                input_p.activated = False                     
            super().event_action(earg)
################################################################################
    
    def event_Start(self, earg):
        if Common.infos_game['status'] == Pinball.General_Status.TEST_MODE:
            Input.instances['Test'].start_pressed()
            
        elif Common.infos_game['status'] == Common.General_Status.ATTRACT_MODE:
            if Display.Display.instances['Status'].get_credit() > 0:
                Common.start_new_game()
                Common.add_credits(-1)
                
        elif Common.infos_game['status'] == Common.General_Status.START:    
            if Display.Display.instances['Status'].get_credit() > 0:
                if Common.first_ball():
                    if Common.add_player():
                        Common.add_credits(-1)
                else:
                    Common.start_new_game()
                    Common.add_credits(-1)
           
        super().event_action(earg)
################################################################################
    def event_Credit(self, earg):
        Common.add_credits(self.value)
        super().event_action(earg)
################################################################################
    def event_Point(self, earg):
        Common.add_points_current_player(self.points)
        super().event_action(earg)
################################################################################
    def event_Point_Light(self, earg):
        if self.normal_state == "blink":
            if self.lamp.get_level() == 1:
                points = self.points[1]
            else:
                points = self.points[0]
        else:
            if self.lamp.is_blinking() == True or self.lamp.get_level() == 0:
                points = self.points[0]
            else:
                points = self.points[1]
        Common.add_points_current_player(points)
        super().event_action(earg)
################################################################################
def event_action(self, earg):
        self.level = 1
        super().event_action(earg)
################################################################################
def event_Spinner(self, earg):
        super().event_action(earg)
        if self.lamp.get_level() == 1:
            self.lamp.set_level(0)
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
def event_Target(self, earg):
        super().event_action(earg)
        if self.nb_states == 1:
            self.lamp.set_level(1)
        elif self.nb_states == 2:
            if self.lamp.is_blinking() == True:
                self.lamp.set_level(1)
            else:
                self.lamp.set_level("blink")
        self.parent.check_action()
        
################################################################################

def event_Test(self, earg):
        # Premier appuie
        if Common.infos_game['status'] == Common.General_Status.ATTRACT_MODE:
            self.current_step = 0
            Common.attract_mode()
            Common.infos_game['status'] = Common.General_Status.TEST_MODE
            Common.init_displays()
        elif self.start_pressed_reset == True:
            Data_Save.reset_by_pos(self.current_step)
        else:
            vale = Display.Player.get_by_num(1).get_value()
            if vale  != "" and self.current_step < 16:
                Data_Save.set_by_pos(self.current_step, Display.Display.get_by_name("p1").get_value())
            self.current_step += 1
            self.start_step()
    
    def end(self):
        self.timer.stop()
        super().end()
        
    def start_step(self):
        self.timer.start(self.wait_time_before_end)
        Display.Display.get_by_name("Status").set_credit(self.current_step)
        Display.Player.get_by_num(3).set_value(self.current_step)
        Display.Player.get_by_num(4).set_value(self.current_step)
        
        if self.current_step < 16:
           val = Data_Save.get_by_pos(self.current_step-1)        
           Display.Player.get_by_num(1).set_value(val)
        else:
            if self.current_step == 16:
                Output.Lamp.test.start(self.wait_time_between_test)
                Output.Relay.test.start(self.wait_time_between_test)
            elif self.current_step == 17:
                Output.Lamp.test.stop()
                Output.Relay.test.stop()
                Output.Solenoid.test.start()(self.wait_time_between_test)
                #Output.Sound.test()
            elif self.current_step == 18:
                Output.Relay.test.stop()
                Matrix.test.start(wait_time_between_test) 
            elif self.current_step == 19:
                Display.Display.instances["Status"].value("")
                Display.Display.test(wait_time_between_test) 
    
    def end_test(self, earg=None):
        Common.TEST_MODE = False
        Common.attract_mode()
        
    def start_pressed(self):
        if self.current_step == 0:
           self.current_step = 16        
           self.start_step()
        else:
            if self.current_step < 16:
                Display.Player.get_by_num(1).set_all_zero()
                if self.current_step < 11 or self.current_step > 14:
                    self.start_pressed = True
                else:
                    Display.Player.get_by_num(3).set_value(100000, increment=True)
            else:
                self.start_step()
                
    def get_list_tests(self):
        dict_tests = dict()
        dict_tests["Matrix"] = [input.name for input in Matrix.instances.values()]
        dict_tests["Lamp"] = [lamp.name for lamp in Output.Lamp.instances.values()]
        dict_tests["Solenoid"] = [sol.name for sol in Output.Solenoid.instances.values()]
        dict_tests["Display"] = [display.name for display in Display.Display.instances.values()]
        return dict_tests
    
    def start_test(self, name):
        pass
   
    
    
    
    
