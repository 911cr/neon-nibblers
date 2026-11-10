@echo off
cd /d "%~dp0"
call run_windows.bat --arena 0 --palette 4 --simulate-controllers --data-dir duel-data --tuning tuning.keyboard-playtest.json --event-log duel-data/latest-match.json %*
