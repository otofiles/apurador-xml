@echo off
cd /d "%~dp0"
echo ============================================
echo   Recriar o executavel (CalculadoraXml.exe)
echo ============================================
echo.
where python >nul 2>nul
if errorlevel 1 (
    echo ERRO: Python nao encontrado.
    pause
    exit /b 1
)
echo Instalando PyInstaller (so na primeira vez)...
python -m pip install pyinstaller >nul 2>nul
echo Gerando o executavel... pode levar 1 a 2 minutos.
pyinstaller --noconfirm --clean CalculadoraXml.spec
echo.
if exist "dist\CalculadoraXml.exe" (
    echo ============================================
    echo   Pronto! O executavel esta em: dist\CalculadoraXml.exe
    echo ============================================
) else (
    echo ERRO na geracao. Verifique as mensagens acima.
)
pause
