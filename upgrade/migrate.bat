@ECHO OFF
SET source=upgrade\git-repo
SET dest=..\feed-importer

:: copy the configs\credentials from the active  repo to the temp location
XCOPY /E /H /Y /R /i "%dest%\config\credentials" "%source%\config\credentials"

:: remove all files from the active repository except the "upgrade" folder
:: (the upgrade folder holds the latest software)
ATTRIB +H %dest%\upgrade
FOR /D %%i IN ("%dest%\*") DO RD /S /Q "%%i" 
DEL /Q "%dest%\*" 
ATTRIB -H %dest%\upgrade


:: install the software  (stored in the upgrade folder)
XCOPY /E /H /Y /R /i "%source%" "%dest%"

