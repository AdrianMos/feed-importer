@ECHO OFF
SET source=git-repo
SET dest=..

:: copy the configs\credentials from the active  repo to the temp location
XCOPY /E /H /Y /R /i "%dest%\config\credentials" "%source%\config\credentials"

:: remove all files from the active repository except the "upgrade" folder
:: (the upgrade folder holds the latest software)
ATTRIB +H ..\upgrade
FOR /D %%i IN ("..\*") DO RD /S /Q "%%i" 
DEL /Q "..\*" 
ATTRIB -H ..\upgrade


:: install the software  (stored in the upgrade folder)
XCOPY /E /H /Y /R /i "%source%" "%dest%"

