# Apurador de XML de NF-e / NFC-e

Aplicação desktop em Python que lê XMLs de Notas Fiscais Eletrônicas (NF-e modelo 55 e
NFC-e modelo 65), exibe um resumo por situação e **apura os impostos** (ICMS, ICMS-ST,
FCP, IPI, PIS, COFINS, Frete, Desconto, Total de Tributos e os campos da Reforma
Tributária **IBS/CBS**), exportando tudo para uma planilha Excel formatada.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Funcionalidades

- **Leitura recursiva** de pastas com arquivos `.xml` e `.zip` (extrai os XMLs internos).
- **Situações reconhecidas**: Autorizada, Rejeitada, Denegada, Cancelada, Sem protocolo,
  Inutilizada, Cancelamento, Evento CC-e, Evento e Inválida.
- **Apuração completa de impostos** agregada de todos os documentos:
  - Tradicionais: BC ICMS, ICMS, ICMS Desonerado, FCP, BC ICMS-ST, ICMS-ST, FCP-ST,
    FCP-ST Retido, Produtos, Frete, Seguro, Desconto, Imposto de Importação, IPI,
    IPI Devolvido, PIS, COFINS, Outras Despesas e Total de Tributos.
  - **Reforma Tributária (NT 2025.002)**: BC IBS/CBS, IBS UF, IBS Município, IBS Total,
    Crédito Presumido IBS, CBS, Crédito Presumido CBS, IBS/CBS Monofásico e suas
    retenções, além do Total NF (`vNFTot`).
- **Deduplicação** automática por chave de acesso (mantém o melhor status).
- **FCP no total** opcional.
- **Interface em abas**: Resumo (cartões + chips por situação + apuração recolhível) e
  Documentos (tabela com todas as colunas de impostos e scroll).
- **Exportação XLSX** com formatação profissional (cabeçalho azul, linhas alternadas,
  bordas, filtro, congelamento e moeda `R$ #,##0.00`) e seção de apuração por imposto.
- **Build nativo com Nuitka** (EXE único, leve e rápido, sem janela de console).

## Pré-requisitos

- Windows
- Python 3.10+ (para rodar via código-fonte)

## Como usar (código-fonte)

1. Instale as dependências:
   ```bat
   instalar.bat
   ```
2. Rode a aplicação:
   ```bat
   iniciar.bat
   ```
   Ou diretamente:
   ```bat
   python CalculadoraXml.py
   ```

## Como gerar o executável (EXE)

Recomendado — **Nuitka** (nativo, ~26 MB, inicialização rápida, sem console):

```bat
pip install "nuitka[onefile]"
criar_exe_nuitka.bat
```

Opcional — PyInstaller:

```bat
pip install pyinstaller openpyxl
pyinstaller --noconfirm --clean CalculadoraXml.spec
```

## Estrutura do projeto

```
Calculadora de XML FINAL/
├── CalculadoraXml.py        # Interface (CustomTkinter, abas, exportação XLSX)
├── nfe_parser.py            # Parser dos XMLs e agregação de impostos
├── CalculadoraXml.spec      # Configuração PyInstaller
├── requirements.txt         # Dependências
├── criar_exe.bat            # Build PyInstaller
├── criar_exe_nuitka.bat     # Build Nuitka (recomendado)
├── iniciar.bat              # Roda via Python
├── instalar.bat             # Instala dependências
├── xml.ico                  # Ícone do aplicativo
├── Exemplos/                # XMLs de exemplo para teste
├── contexto.md              # Documentação técnica do projeto
├── README.md
├── LICENSE
└── .gitignore
```

## Campos apurados (resumo)

| Grupo | Campos |
|-------|-------|
| ICMS | BC ICMS, ICMS, ICMS Desonerado, BC ICMS-ST, ICMS-ST, FCP, FCP-ST, FCP-ST Retido |
| Outros | Produtos, Frete, Seguro, Desconto, Imp. Importação, IPI, IPI Devolvido, PIS, COFINS, Outras, Total Tributos |
| Reforma Tributária | BC IBS/CBS, IBS UF, IBS Município, IBS Total, Crédito Presumido IBS, CBS, Crédito Presumido CBS, IBS/CBS Monofásico e retenções, Total NF |

## Como atualizar o projeto

1. Faça as alterações desejadas nos arquivos.
2. (Opcional) Regenere o EXE com `criar_exe_nuitka.bat`.
3. Versione e envie ao GitHub:
   ```bat
   git add .
   git commit -m "Descrição da alteração"
   git push
   ```

## Licença

Este projeto está licenciado sob a Licença MIT — veja o arquivo [LICENSE](LICENSE).
