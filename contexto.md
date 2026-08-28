# Calculadora de NF-e / NFC-e - Contexto do Projeto

## Visão Geral

Aplicação desktop em Python que analisa XMLs de notas fiscais eletrônicas (NF-e e NFC-e),
exibe resumo por situação, **apura os impostos** (ICMS, ICMS-ST, FCP, IPI, PIS, COFINS, etc.)
e exporta tudo para planilha Excel formatada.

**Localização:** `C:\Users\User\Desktop\PYTHONS\Calculadora de Xml`
**EXE:** `dist\CalculadoraXml.exe`
**Ícone:** `xml.ico`

## Estrutura de Arquivos

```
Calculadora de Xml/
├── CalculadoraXml.py      # Interface principal (CustomTkinter, dark mode)
├── nfe_parser.py           # Parser XML para NF-e/NFC-e
├── CalculadoraXml.spec     # Configuração PyInstaller
├── requirements.txt        # Dependências
├── criar_exe.bat           # Script para gerar o EXE
├── iniciar.bat             # Script para rodar direto pelo Python
├── instalar.bat            # Script para instalar dependências
├── xml.ico                 # Ícone do executável
├── icone_128.png           # Ícone para o cabeçalho da interface
├── icone_64.png            # Ícone alternativo
├── icone_receipt.png       # Ícone alternativo
├── icone.ico               # Ícone antigo (substituído por xml.ico)
├── Exemplos/               # XMLs de exemplo para teste
│   ├── NFCe_Autorizada.xml
│   ├── NFCe_Inutilizada.xml
│   ├── NFE_Autorizada.xml
│   ├── NFE_Cancelada.xml
│   └── NFE_CartaCorrecao.xml
└── dist/
    └── CalculadoraXml.exe  # Executável final
```

## Dependências (requirements.txt)

```
customtkinter>=5.2.0
Pillow>=10.0.0
openpyxl>=3.1.0
```

Dependência de build (opcional, para gerar o EXE com Nuitka): `nuitka[onefile]`.

## Funcionalidades

### Interface (CalculadoraXml.py)

- **Tema:** Dark mode com CustomTkinter (verde como accent)
- **Layout:** Cabeçalho (ícone `xml.ico`) + Card de pasta + **Abas** (Resumo / Documentos) + Rodapé
- **Janela:** 980x680, mínima 820x560
- **Aba "Resumo":** Cartões de resumo, Resumo por Situação (chips), Apuração de Impostos (seção recolhível com scroll)
- **Aba "Documentos":** Checkboxes (mostrar impostos na tabela / exportar impostos) + Tabela Treeview com scroll horizontal e vertical

#### Componentes da Interface
1. **Cabeçalho** - Título + ícone (usa o mesmo `xml.ico` do executável)
2. **Card de Pasta** - Campo de texto, botões (Selecionar, Analisar, Limpar), checkboxes (Ignorar duplicados, Considerar FCP)
3. **Aba "Resumo"** (rolável):
   - **Cartões de Resumo** - Total Autorizadas, Documentos, NF-e, NFC-e, Canceladas, Total Tributos (soma de vTotTrib)
   - **Resumo por Situação** - Chips coloridos com quantidade e valor por status
   - **Apuração de Impostos** - Seção **recolhível** (clique no título para expandir/retrair) com scroll contendo chips de total por imposto: BC ICMS, ICMS, ICMS Deson., FCP, BC ICMS ST, ICMS ST, FCP ST, FCP ST Ret, Produtos, Frete, Seguro, Desconto, Imp. Import., IPI, IPI Devol., PIS, COFINS, Outras, Total Tributos, e os campos da Reforma Tributária (IBS/CBS): BC IBS/CBS, IBS UF, IBS Mun, IBS Total, Cred Pres IBS, CBS, Cred Pres CBS, IBS Mono, CBS Mono, retenções monofásicas e vNFTot
4. **Aba "Documentos"**:
   - Checkbox **Mostrar colunas de impostos na tabela** (toggle das colunas de impostos)
   - Checkbox **Exportar impostos na planilha** (formato antigo sem impostos quando desmarcado)
   - **Tabela** - Treeview com colunas: Modelo, Número, Série, Emissão, Emitente, Valor, Situação, Arquivo + todas as colunas de impostos (toggle), com scroll horizontal e vertical
5. **Rodapé** - Barra de progresso, status, botão Exportar XLSX

#### Checkboxes
- **Ignorar XMLs duplicados** (padrão: ligado) - Remove XMLs com mesma chave de acesso, mantendo o de melhor status
- **Considerar FCP no total** (padrão: desligado) - Quando marcado, soma vFCP + vFCPST + vFCPSTRet ao total
- **Mostrar colunas de impostos na tabela** (padrão: ligado) - Exibe/oculta as colunas de impostos (ICMS, ICMS-ST, FCP, IPI, PIS, COFINS, IBS, CBS, etc.) na tabela de documentos
- **Exportar impostos na planilha** (padrão: ligado) - Quando marcado, a planilha inclui todas as colunas de impostos e a seção APURACAO DE IMPOSTOS; quando desmarcado, exporta apenas o formato antigo (Modelo, Numero, Serie, Emissao, Emitente, Valor, Situacao, Chave + RESUMO POR SITUACAO + TOTAL)

#### Análise
- Varredura recursiva em subpastas
- Suporte a arquivos `.xml` e `.zip` (extrai XMLs dentro do ZIP)
- Barra de progresso com nome do arquivo atual
- Análise em thread separada (não trava a interface)

#### Exportação XLSX
- Formato Excel (.xlsx) via openpyxl
- **Sem coluna de diretório/arquivo** do XML
- Colunas: Modelo, Numero, Serie, Emissao, Emitente, Valor (R$), Situacao, Chave
- **Mais uma coluna para cada imposto** do `TRIBUTOS` (ICMS, ICMS-ST, FCP, IPI, PIS, COFINS, Frete, Desconto, Total Tributos, etc.)
- Seção **RESUMO POR SITUACAO** abaixo dos dados
- Seção **APURACAO DE IMPOSTOS** com o total de cada imposto
- Total geral (TOTAL AUTORIZADAS) ao final

#### Formatação da Planilha (estilo pythons-saurus)
- **Cabeçalho:** Azul escuro (#1F4E78), fonte branca bold, centralizado
- **Linhas alternadas:** Cinza (#F2F2F2) em linhas pares
- **Bordas:** Thin em todas as células
- **Colunas:** Auto-ajustadas (largura do maior conteúdo + 5)
- **Congelamento:** Primeira linha (freeze_panes = A2)
- **Filtro automático:** Aplicado em todas as colunas
- **Formato moeda:** `R$ #,##0.00` em colunas de valor e FCP (incluindo seção de resumo)

### Parser XML (nfe_parser.py)

#### Classe Documento
```python
class Documento:
    arquivo      # Caminho do arquivo XML
    chave        # Chave de acesso (44 dígitos)
    modelo       # 55=NF-e, 65=NFC-e
    modelo_nome  # "NF-e" ou "NFC-e"
    numero       # Número da nota
    serie        # Série da nota
    emissao      # Data de emissão (dhEmi ou dEmi)
    emitente     # Nome + CNPJ/CPF do emitente
    valor        # vNF (Decimal)
    vBC          # Base de cálculo do ICMS (Decimal)
    vICMS        # Valor do ICMS (Decimal)
    vICMSDeson   # Valor do ICMS desonerado (Decimal)
    vFCP         # Fundo de Combate à Pobreza (Decimal)
    vBCST        # Base de cálculo do ICMS-ST (Decimal)
    vST          # Valor do ICMS-ST (Decimal)
    vFCPST       # FCP-ST (Decimal)
    vFCPSTRet    # FCP-ST Retido (Decimal)
    vProd        # Valor total dos produtos (Decimal)
    vFrete       # Valor do frete (Decimal)
    vSeg         # Valor do seguro (Decimal)
    vDesc        # Valor do desconto (Decimal)
    vII          # Valor do Imposto de Importação (Decimal)
    vIPI         # Valor do IPI (Decimal)
    vIPIDevol    # Valor do IPI devolvido (Decimal)
    vPIS         # Valor do PIS (Decimal)
    vCOFINS      # Valor do COFINS (Decimal)
    vOutro       # Outras despesas acessórias (Decimal)
    vTotTrib     # Valor total dos tributos (Lei da transparência) (Decimal)
    vBCIBSCBS    # Base de cálculo total do IBS/CBS (Reforma Tributária)
    vIBSUF       # IBS Estadual (UF)
    vIBSMun      # IBS Municipal
    vIBS         # IBS Total
    vCredPresIBS # Crédito presumido do IBS
    vCBS         # CBS (Contribuição sobre Bens e Serviços)
    vCredPresCBS # Crédito presumido da CBS
    vIBSMono     # IBS Monofásico
    vCBSMono     # CBS Monofásico
    vIBSMonoReten # IBS Monofásico retido (retenção)
    vCBSMonoReten # CBS Monofásico retido (retenção)
    vIBSMonoRet  # IBS Monofásico retido
    vCBSMonoRet  # CBS Monofásico retido
    vNFTot       # Total geral da NF-e (vNFTot, Reforma Tributária)
    status       # Situação da nota
    erro         # Mensagem de erro (se XML inválido)
    evento_cancelamento  # True se é evento de cancelamento
    evento       # True se é evento/inutilização/CC-e
```

#### Status Possíveis
| Status | Cor | Descrição |
|--------|-----|-----------|
| Autorizada | #4caf50 (verde) | cStat=100 |
| Rejeitada | #ffa726 (laranja) | cStat diferente de 100/135/denegados |
| Denegada | #ffb74d (laranja claro) | cStat 110, 301, 302, 303 |
| Cancelada | #ef5350 (vermelho) | cStat=135 ou evento cancelamento |
| Sem protocolo | #90a4ae (cinza azulado) | Sem protNFe |
| Inutilizada | #ce93d8 (roxo) | cStat 135/136 em infInut |
| Cancelamento | #ef5350 (vermelho) | Evento de cancelamento |
| Evento CC-e | #4fc3f7 (azul claro) | Carta de correção (tpEvento=110110) |
| Evento | #80cbc4 (verde agua) | procEventoNFe genérico |
| Inválida | #ef5350 (vermelho) | XML não é NF-e/NFC-e |

#### Funções Principais
- `parse_arquivo_xml(dados, arquivo)` - Parse de bytes XML, retorna lista de Documento
- `escanear_arquivo_xml(arquivo)` - Lê arquivo ou ZIP
- `escanear_pasta(pasta, incluir_subpastas, on_progress)` - Varre pasta inteira
- `resumir(documentos, ignorar_duplicados, considerar_fcp)` - Gera resumo agregado

#### Lógica de Deduplicação
- Quando `ignorar_duplicados=True`, mantém apenas 1 XML por chave de acesso
- Se há duplicatas, mantém a de melhor status (Autorizada > Rejeitada > Denegada/Cancelada)

#### Lógica FCP
- Quando `considerar_fcp=True`, o total somado é: `vNF + vFCP + vFCPST + vFCPSTRet`
- Quando `considerar_fcp=False`, o total é apenas `vNF` (comportamento padrão)

## Geração do EXE

O build recomendado usa **Nuitka**, que compila para binário nativo (mais leve e com
inicialização muito mais rápida que o PyInstaller onefile):

```batch
pip install "nuitka[onefile]"
criar_exe_nuitka.bat
```

O comando Nuitka equivalente é:

```batch
python -m nuitka --onefile --assume-yes-for-downloads ^
  --windows-disable-console ^
  --enable-plugin=tk-inter ^
  --windows-icon-from-ico=xml.ico ^
  --include-data-files=xml.ico=xml.ico ^
  --output-filename=CalculadoraXml.exe --remove-output CalculadoraXml.py
```

O EXE resultante (`CalculadoraXml.exe`, ~26 MB) é um arquivo único e nativo.

Como alternativa (menos otimizado), mantém-se o empacotamento PyInstaller:

```batch
pip install pyinstaller openpyxl
pyinstaller --noconfirm --clean CalculadoraXml.spec
```

## Otimizações aplicadas

- **Import preguiçoso do `openpyxl`**: carregado apenas na exportação XLSX, reduzindo
  memória e tempo de inicialização.
- **Parsing paralelo**: `escanear_pasta` usa `ThreadPoolExecutor` para ler/decodificar
  vários XMLs simultaneamente (libera o GIL no parse em C), acelerando pastas grandes.
- **`_base_dir()` robusto** para ambos os empacotadores (PyInstaller `_MEIPASS` e
  Nuitka `sys.executable`), garantindo que `xml.ico` seja encontrado em runtime.

## Referências

- Estilo da planilha baseado no projeto `pythons-saurus` (`editor_excel.py` e `Sistema_XML_Excel.py`)
  localizado em `C:\Users\User\Meu Drive\TRABALHO - DRIVE\PYTHONS\pythons - saurus`
