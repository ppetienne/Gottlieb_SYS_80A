#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#########################################################################################
# setup.py 
#
# Installateur CM_Pinball
#
#########################################################################################

import os, sys
import subprocess
from shutil import copyfile
import time

if __name__ == "__main__":
    print("Changement de l'heure ...")
    subprocess.check_call(['sudo', 'timedatectl', 'set-timezone', 'Europe/Paris'])

    print("Activation du bus I2C ...")
    # Prendre en compte lorsque la ligne est commentee
    os.system("sudo sed /boot/config.txt -i -r -e \"s/^((device_tree_param|dtparam)=([^,]*,)*i2c(_arm)?)(=[^,]*)?/\1=on/\"")
    
    print("\nInstallation de divers packages ...")
    os.system('sudo apt-get -y install python3-pip')
    os.system('sudo pip3 install hug==2.3.2 smbus2==0.2.0 simple_audio')