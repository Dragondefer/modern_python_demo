@echo off
SETROOT=%~dp0\..
SET VENV=%ROOT%\.venv
IF NOT EXIST "%ROOT%\.venv\Scripts\python.exe" (
    echo Creating virtual environment .venv...
    python -m venv "%ROOT%\.venv"
)

"%ROOT%\.venv\Scripts\python.exe" -m pip install --upgrade pip
"%ROOT%\.venv\Scripts\python.exe" -m pip install -r "%ROOT%\requirements.txt"

"%ROOT%\.venv\Scripts\python.exe" -m modern_python_demo %*
