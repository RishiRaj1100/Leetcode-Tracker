@echo off
echo Setting up LeetCode Progress Tracker...

:: Create and activate virtual environment
python -m venv venv
call venv\Scripts\activate

:: Install requirements
pip install -r requirements.txt

:: Run the simpler setup script
python setup_simple.py

:: Keep the window open
pause 