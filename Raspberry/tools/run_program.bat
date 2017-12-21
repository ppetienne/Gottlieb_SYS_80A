@echo off
for %%A in ("%~dp0\..\..") do set "root_parent=%%~fA"
echo y | %root_parent%\Tools\plink.exe -ssh -pw raspberry pi@192.168.25.100 "exit"
REM %root_parent%\Tools\plink.exe -ssh -pw raspberry pi@192.168.25.100 sudo python3 /home/pi/Documents/ICBL/sources/main.py
%root_parent%\Tools\plink.exe -ssh -pw raspberry pi@192.168.25.100 sudo python3 /home/pi/Documents/ICBL/sources/main.py