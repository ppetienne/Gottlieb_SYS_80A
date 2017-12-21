@echo off
for %%A in ("%~dp0\..") do set "root_parent=%%~fA"

REM set /p ip=Veuillez saisir l'adresse IP du RPi : 
set ip=192.168.1.21
echo Connection au RPi via SSH ...
echo %root_parent%\remote_exe\plink.exe
echo y | %root_parent%\remote_exe\plink.exe -ssh -pw raspberry pi@%ip% "exit"

echo Copie des sources sur le RPi ...
%root_parent%\remote_exe\plink.exe pi@%ip% -pw raspberry sudo mkdir /home/pi/Documents /home/pi/Documents/CM_Pinball
%root_parent%\remote_exe\plink.exe pi@%ip% -pw raspberry sudo chmod -R 777 /home/pi/Documents/CM_Pinball
set COMMANDS="%~dp0\command_files\psftp.bat"
%root_parent%\remote_exe\psftp.exe pi@%ip% -pw raspberry -b %COMMANDS%

echo Exécution du script d'installation sur le RPi ...
%root_parent%\remote_exe\plink.exe -ssh -pw raspberry pi@%ip% sudo python3 /home/pi/Documents/ICBL/files/setup_RPi.py

echo Redemarrage du RPi ...
REM %root_parent%\remote_exe\plink.exe -ssh -pw raspberry pi@%ip% sudo reboot

pause