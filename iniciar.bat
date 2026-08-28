@echo off
cd /d "%~dp0"
where pythonw >nul 2>nul
if errorlevel 1 (
    echo.
    echo ERRO: Python nao encontrado.
    echo Rode antes o arquivo "instalar.bat" ou instale o Python.
    echo.
    pause
    exit /b 1
)
start "" pythonw CalculadoraXml.py
