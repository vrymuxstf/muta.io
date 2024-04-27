@echo off
setlocal

:: Check if virtual environment folder exists
set VENV_DIR=.venv
if not exist %VENV_DIR% (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

:: Activate the virtual environment
echo Activating virtual environment...
call %VENV_DIR%\Scripts\activate.bat
echo Virtual environment activated.

:: Generate requirements.txt with installed packages
echo Generating requirements.txt...
pip freeze > requirements.txt
echo requirements.txt generated.

:: Install packages from requirements.txt
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
echo Dependencies installed.

:: Additional script operations
echo Setup complete. You can start your application.

:: Keep the console window open
pause
