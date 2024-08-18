# PDF Renamer
Este projeto é um script em Python que automatiza o processo de renomeação de arquivos PDF baseando-se em informações extraídas de seu conteúdo. É útil para organizar comprovantes de pagamentos, recibos e outros documentos que seguem um padrão de formatação, como datas e descrições de transações.

## Funcionalidades
Leitura e extração de informações específicas de arquivos PDF.

Renomeação dos arquivos PDF com base na descrição do pagamento e data da transação.

Limpeza de palavras indesejadas e caracteres inválidos nos nomes dos arquivos.

Movimentação dos arquivos renomeados para uma pasta de destino específica.

## Tecnologias Utilizadas
Python 3.x

PyPDF2 - Biblioteca usada para leitura e extração de textos de arquivos PDF.

Regex (re) - Para captura e processamento de informações específicas nos textos.

OS e Shutil - Para manipulação de arquivos e diretórios.

## Como Usar

### Instale as dependências:

Antes de executar o script, instale as bibliotecas necessárias com o seguinte comando:
```bash
pip install PyPDF2
```
### Edite o código:

Defina os caminhos para as pastas de origem e destino nos parâmetros pasta_origem e pasta_destino. Certifique-se de que os arquivos PDF estejam na pasta de origem.
```bash
pasta_origem = 'Caminho da pasta de origem'
pasta_destino = 'Caminho da pasta de destino'
```
### Execute o script:

Para rodar o script, utilize o seguinte comando no terminal:
```bash
python script.py
```

O script irá processar todos os arquivos PDF na pasta de origem, renomeá-los com base nas informações extraídas, e movê-los para a pasta de destino.

## Exemplo de Renomeação
O script captura a descrição do pagamento e a data de transação. Por exemplo:

PDF Original: comprovante.pdf

PDF Renomeado: Pix 12.08.2023.pdf

Observações
O script está preparado para lidar com diferentes padrões de formato de texto nos PDFs. Certifique-se de ajustar as expressões regulares de acordo com o formato específico dos seus documentos.

A função remover_palavras_indesejadas permite excluir palavras que você não deseja incluir no nome dos arquivos.
