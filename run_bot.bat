@echo off

cd /d C:\Users\Administrator\Documents\Aurum

if not exist logs mkdir logs

set RUN_SUMMARY=false

if /I "%RUN_SUMMARY%"=="true" (
    echo Starting Daily Summary Scheduler...
    start "" venv\Scripts\python.exe src\run_summary.py >> logs\summary.log 2>&1
)

:loop
echo ======================================
echo Starting bot...
echo ======================================

venv\Scripts\python.exe src\main.py >> logs\runner.log 2>&1

echo ======================================
echo Bot crashed. Restarting...
echo ======================================

ping 127.0.0.1 -n 6 > nul
goto loop