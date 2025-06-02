@echo off
pyinstaller --onefile --noconsole ^
--add-data "assets\delete_icon.png;assets" ^
--add-data "assets\download_icon.png;assets" ^
main.py

timeout /t 2 >nul

rmdir /s /q build
rmdir /s /q input
rmdir /s /q logs
rmdir /s /q output
del /q main.spec

xcopy /E /I /Y assets dist\assets

ren dist shared

ren "shared\main.exe" PLCWatchTableReader-win11-24H2x64.exe

echo Finished!.
pause
