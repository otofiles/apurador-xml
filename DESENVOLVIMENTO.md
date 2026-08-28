# Documentação para desenvolvedores

Este arquivo reúne as informações técnicas do projeto. Para o uso comum do
programa, veja o `README.md`.

## Visão geral

Aplicação desktop em Python (CustomTkinter) que apura impostos de XMLs de
NF-e (modelo 55) e NFC-e (modelo 65). O parsing é feito em `nfe_parser.py`
e a interface/exportação em `CalculadoraXml.py`.

## Pré-requisitos

- Python 3.10+
- Windows

## Como rodar a partir do código-fonte

```bat
pip install -r requirements.txt
python CalculadoraXml.py
```

`requirements.txt`:
```
customtkinter>=5.2.0
Pillow>=10.0.0
openpyxl>=3.1.0
```

## Como gerar o executável (EXE)

O build recomendado usa **Nuitka** (binário nativo, ~26 MB, sem janela de
console):

```bat
pip install "nuitka[onefile]"
criar_exe_nuitka.bat
```

Comando equivalente:

```bat
python -m nuitka --onefile --assume-yes-for-downloads ^
  --windows-disable-console ^
  --enable-plugin=tk-inter ^
  --windows-icon-from-ico=xml.ico ^
  --include-data-files=xml.ico=xml.ico ^
  --output-filename=CalculadoraXml.exe --remove-output CalculadoraXml.py
```

Alternativa (PyInstaller):

```bat
pip install pyinstaller openpyxl
pyinstaller --noconfirm --clean CalculadoraXml.spec
```

O executável gerado (`CalculadoraXml.exe`) está no `.gitignore` e não é
versionado; ele é distribuído via **GitHub Releases**.

## Estrutura do projeto

```
Calculadora XML FINAL/
├── CalculadoraXml.py        # Interface (CustomTkinter), abas e exportação XLSX
├── nfe_parser.py            # Parser dos XMLs e agregação de impostos
├── CalculadoraXml.spec      # Configuração PyInstaller
├── requirements.txt         # Dependências
├── criar_exe.bat            # Build PyInstaller
├── criar_exe_nuitka.bat     # Build Nuitka (recomendado)
├── iniciar.bat              # Roda via Python
├── instalar.bat             # Instala dependências
├── xml.ico                  # Ícone do aplicativo
├── Exemplos/                # XMLs de exemplo
├── README.md                # Guia do usuário comum
├── DESENVOLVIMENTO.md       # Este arquivo
├── LICENSE
└── .gitignore
```

## Campos apurados

A constante `TRIBUTOS` em `nfe_parser.py` define 33 campos (19 tradicionais
+ 14 da Reforma Tributária). Eles são lidos de `infNFe/total/ICMSTot`,
`infNFe/total/IBSCBSTot` (NT 2025.002) e `infNFe/total/vNFTot`, e agregados
em `resumir()`.

| Grupo | Campos |
|-------|-------|
| ICMS | BC ICMS, ICMS, ICMS Desonerado, BC ICMS-ST, ICMS-ST, FCP, FCP-ST, FCP-ST Retido |
| Outros | Produtos, Frete, Seguro, Desconto, Imp. Importação, IPI, IPI Devolvido, PIS, COFINS, Outras, Total Tributos |
| Reforma Tributária | BC IBS/CBS, IBS UF, IBS Município, IBS Total, Crédito Presumido IBS, CBS, Crédito Presumido CBS, IBS/CBS Monofásico e retenções, Total NF |

## Otimizações aplicadas

- **Lazy import do `openpyxl`**: carregado só na exportação XLSX.
- **Parsing paralelo** em `escanear_pasta` (`ThreadPoolExecutor`), liberando
  o GIL no decode/parse em C.
- **`_base_dir()`** robusto para PyInstaller (`_MEIPASS`) e Nuitka
  (`sys.executable`), garantindo que `xml.ico` seja encontrado em runtime.

## Como versionar e atualizar

```bat
git add .
git commit -m "Descrição da alteração"
git push
```

Para publicar uma nova versão do executável, gere o EXE e crie um
**GitHub Release** anexando o `CalculadoraXml.exe`.
