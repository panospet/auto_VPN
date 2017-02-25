@ECHO OFF
SETLOCAL ENABLEEXTENSIONS
SET me=%~n0
SET parent=%~dp0

rem set /p id="Enter ID: "
rem echo %id%

SET username=admin
SET password=admin
SET server_ip=83.212.116.170

rem for /f %%i in ('wget64.exe -qO- --no-check-certificate --post-data="username=%username%&password=%password%" https://%server_ip%/login') do set VAR=%%i
rem echo %i%

:: TODO check for invalid credentials

:: check if openssl is installed
:: Prompt -> you are about to install openSSL
rem Win64OpenSSL_Light-1_1_0e.exe

:: install python

rem c:\Python27\python.exe -m pip install pycurl

if exist "c:\Python27\python.exe" (
    echo Python2.7 is already installed.
) else (
    echo installing python...
    msiexec.exe /i python-2.7.13.msi
)

c:\Python27\python.exe get-pip.py
c:\Python27\python.exe -m pip install pycurl
c:\Python27\python.exe -m pip install certifi
c:\Python27\python.exe test.py


OpenVPNPortable\OpenVPNPortable.exe --connect client.ovpn --config_dir %parent%
