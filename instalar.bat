@echo off
cd /d "%~dp0"
echo ============================================
echo   Calculadora de NF-e / NFC-e - Instalador
echo ============================================
echo.
where python >nul 2>nul
if errorlevel 1 (
    echo.
    echo ERRO: Python nao encontrado.
    echo Instale o Python em https://www.python.org/downloads/
    echo (marque a opcao "Add Python to PATH" durante a instalacao).
    echo.
    pause
    exit /b 1
)
echo Instalando dependencias... (pode levar alguns segundos)
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo.
echo ============================================
echo   Instalacao concluida com sucesso!
echo   Agora execute o arquivo "iniciar.bat".
echo ============================================
echo.
pause
