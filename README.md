# Apurador de XML de NF-e / NFC-e

Programa para Windows que lê os XMLs das suas notas fiscais eletrônicas
(NF-e e NFC-e), mostra um resumo organizado e **calcula os impostos** de
cada documento (ICMS, ICMS-ST, FCP, IPI, PIS, COFINS, frete, desconto,
Total de Tributos e os novos IBS/CBS da Reforma Tributária). Tudo pode ser
exportado para uma planilha Excel pronta para uso.

Não precisa instalar nada nem ter conhecimento técnico: basta baixar o
programa, abrir e apontar para a pasta onde estão seus XMLs.

## Como baixar a versão pronta

1. Acesse a página de versões do projeto:
   **https://github.com/otofiles/apurador-xml/releases**
2. Na primeira versão (ex.: **v1.0.0**), clique no arquivo
   **`CalculadoraXml.exe`** para baixá-lo.
3. Salve o arquivo em qualquer pasta do seu computador (ex.: Área de
   Trabalho ou Documentos).

> O programa é um único arquivo (sem instalação). Funciona offline, sem
> internet.

## Tutorial de uso (para o usuário comum)

Siga estes passos:

1. **Abra o programa** — dê um duplo clique no `CalculadoraXml.exe` que
   você baixou. O aplicativo aparecerá em alguns segundos.
   - *Obs.:* o Windows pode mostrar um aviso de "editor desconhecido".
     Isso é normal em programas sem assinatura paga. Como o código é aberto,
     você pode usar com segurança. Clique em "Executar mesmo assim" /
     "Mais informações → Executar assim mesmo".

2. **Escolha a pasta das notas** — clique no botão **"Selecionar pasta"**
   e aponte para a pasta que contém seus arquivos XML.
   - A pasta pode conter subpastas e arquivos `.zip` (o programa abre os
     XMLs dentro dos zips automaticamente).

3. **Aguarde o processamento** — o programa lê todos os XMLs, remove
   duplicados e classifica cada nota por situação (Autorizada, Cancelada,
   Denegada, Rejeitada, Inutilizada, Carta de Correção etc.).

4. **Veja o resultado** — na aba **Resumo** você encontra:
   - Cartões com totais (Quantidade de documentos, Valor total, Total de
     impostos e Total de tributos);
   - Um “chip” para cada situação, com a contagem e o valor;
   - A **Apuração de Impostos**, com o valor somado de cada imposto de
     todos os documentos.

5. **Veja documento a documento** — na aba **Documentos** há uma tabela
   com cada nota e todas as colunas de impostos. Use a caixa
   **“Mostrar colunas de impostos na tabela”** se quiser ver essas colunas.

6. **Exporte para Excel** — clique em **“Exportar XLSX”**, escolha onde
   salvar e pronto. A planilha vem formatada (cabeçalho azul, valores em
   reais `R$`, filtros e congelamento) e já inclui a aba de apuração de
   impostos.
   - Se quiser a planilha no formato simples (apenas as colunas básicas),
     desmarque a opção **“Exportar colunas de impostos”** antes de exportar.

## Dicas e perguntas frequentes

- **Posso processar muitos arquivos de uma vez?** Sim. Quanto mais XMLs,
  mais tempo leva, mas o programa faz o trabalho em paralelo para ser rápido.
- **Ele altera meus XMLs?** Não. O programa apenas lê os arquivos; nada é
  modificado ou enviado para lugar nenhum.
- **O Windows diz que o arquivo é suspeito.** É só o aviso padrão de
  arquivos sem certificado. O projeto é de código aberto e pode ser
  inspecionado no repositório.
- **Funciona em outro Windows?** Sim, basta copiar o `CalculadoraXml.exe`
  para o outro computador.
- **E se eu só quiser a apuração de impostos?** Marque a opção de mostrar
  as colunas de impostos e exporte com a apuração — a planilha trará tudo
  consolidado.

## Licença

Este programa é disponibilizado sob a Licença MIT (veja `LICENSE`).
Você pode usá-lo livremente.
