@echo off
setlocal

REM Checking existance of environment variable PYTHON_PATH
if "%PYTHON_PATH%"=="" (
    echo Environment variable PYTHON_PATH doesn't set.
    exit /b
)

REM Checking python.exe in PYTHON_PATH
if not exist "%PYTHON_PATH%\python.exe" (
    echo File python.exe couldn't be found in path: %PYTHON_PATH%
    exit /b
)

REM batch-file folder
set "batch_folder=%~dp0"

REM Start main.py
"%PYTHON_PATH%\python.exe" "%batch_folder%\main.py"

echo Done