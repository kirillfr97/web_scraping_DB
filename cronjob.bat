@echo off
setlocal

REM Проверяем наличие переменной среды PYTHON_PATH
echo Checking environment variable PYTHON_PATH
if "%PYTHON_PATH%"=="" (
    echo Environment variable PYTHON_PATH doesn't set.
    exit /b
) else (
	echo OK
)

REM Проверяем существование файла python.exe
echo Checking python.exe in PYTHON_PATH
if not exist "%PYTHON_PATH%\python.exe" (
    echo File python.exe couldn't be found in path: %PYTHON_PATH%
    exit /b
) else (
	echo OK
)


REM Запускаем main.py
echo Start
"%PYTHON_PATH%\python.exe" "D:\MyPython WorkFiles\MongoDBProject\main.py"
echo End