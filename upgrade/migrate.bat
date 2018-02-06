@ECHO OFF
SET source=..\..\temp-git-repo
SET dest=..\..\feed-importer

COPY /Y "%dest%\config\*.*" "%source%\config"
RMDIR /S /Q "%dest%"
MKDIR "%dest%"
COPY /Y "%source%\*.*" "%dest%\"
RMDIR /S /Q "%source%"
