@echo off
echo ============================================================
echo  Calculadora de NF-e/NFC-e - Build com Nuitka (nativo)
echo  Gera um EXE unico, menor e mais rapido que PyInstaller.
echo ============================================================
echo.

IF NOT EXIST xml.ico (
    echo ERRO: xml.ico nao encontrado nesta pasta.
    pause
    exit /b 1
)

python -m nuitka --onefile ^
  --windows-disable-console ^
  --enable-plugin=tk-inter ^
  --windows-icon-from-ico=xml.ico ^
  --include-data-files=xml.ico=xml.ico ^
  --output-filename=CalculadoraXml.exe ^
  --remove-output ^
  CalculadoraXml.py

echo.
IF EXIST CalculadoraXml.exe (
    echo Pronto! Executavel gerado: CalculadoraXml.exe
) ELSE (
    echo Falha ao gerar o executavel. Verifique o log acima.
)
pause
