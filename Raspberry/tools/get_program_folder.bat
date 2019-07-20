@echo off
set COMMANDS="%~dp0\command_files\psftp.bat"
for %%A in ("%~dp0\..") do set "root_parent=%%~fA"
REM rmdir /s /q %root_parent%\program
%root_parent%\remote_exe\psftp.exe pi@192.168.1.21 -pw raspberry -b %COMMANDS%
ren %root_parent%\CM_Pinball program