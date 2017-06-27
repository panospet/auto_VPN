@ECHO OFF
SETLOCAL ENABLEEXTENSIONS
SET me=%~n0
SET parent=%~dp0

:: BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
    IF "%PROCESSOR_ARCHITECTURE%" EQU "amd64" (
>nul 2>&1 "%SYSTEMROOT%\SysWOW64\cacls.exe" "%SYSTEMROOT%\SysWOW64\config\system"
) ELSE (
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
)

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params = %*:"=""
    echo UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
:--------------------------------------    

SET username=admin
SET password=admin
SET server_ip=83.212.116.170

:: TODO check for invalid credentials

:: install python

if exist "c:\Python27\python.exe" (
    echo Python2.7 is already installed.
) else (
    echo installing python...
    msiexec.exe /i python-2.7.13.msi
)

c:\Python27\python.exe %parent%/get-pip.py
c:\Python27\python.exe -m pip install pycurl
c:\Python27\python.exe -m pip install certifi
c:\Python27\python.exe %parent%/script.py

start "" /wait cmd /c "echo Script is about to install and run OpenVPN LOCALLY. New files will be generated only inside the parent folder AND NOWHERE ELSE.&echo(&pause"

%parent%OpenVPNPortable_1.8.2.paf.exe
OpenVPNPortable\OpenVPNPortable.exe --connect client.ovpn --config_dir %parent%