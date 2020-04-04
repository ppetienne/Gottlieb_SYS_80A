# -*- coding: utf-8 -*-
################################################################################
# Contacts
# Package contenant differentes classe permettant de faire un lien physique
# entre les objets
#
################################################################################
import hug
import os, sys

@hug.get()
@hug.cli()
@hug.local()
def get_all_options():
    return Options.get_all_options()

@hug.get()
@hug.cli()
@hug.local()
def get_all_data_save():
    return Data_Save.get_all_datas()

@hug.get()
@hug.cli()
@hug.local()
def set_all_options(options):
    Options.set_all_options(options)

@hug.get()
@hug.cli()
@hug.local()
def reset_data_save(name):
    Data_Save.reset_data(name)
    
@hug.get()
@hug.cli()
@hug.local()
def get_all_tests():
    return Input.Input.instances['Test'].get_list_tests()

def start_test(name):
    Pinball.game_over_mode()
    Input.Input.instances['Test'].start_tests(name)

def test_one_io(name_test, name_io):
    Pinball.game_over_mode()
    Input.Input.instances['Test'].start_tests(name_test, name_io)
    
if __name__ == '__main__':
    pass