import os
import re
from PyPDF2 import PdfReader
import shutil

# Caminho para a pasta na sua área de trabalho
pasta_origem = 'C:\\Users\\ryane\\OneDrive\\Área de Trabalho\\teste'
pasta_destino = 'C:\\Users\\ryane\\OneDrive\\Área de Trabalho\\pdf_modificado'


# Função para ler e extrair informações específicas do PDF
def extrair_informacoes(caminho_pdf):
    try:
        leitor = PdfReader(caminho_pdf)
        texto = ''
        for pagina in leitor.pages:
            texto += pagina.extract_text() + '\n'

        # Exibir o texto extraído para depuração
        print("Texto extraído do PDF:")
        print(texto)
        
        # Ajustar regex para capturar o texto antes do marcador
        descricao_pagamento_match = re.search(r'([^\n\r]*)\s*Descrição do Pagamento:', texto)
        data_transacao_match = re.search(r'Data da Transação:\s*(\d{2}/\d{2}/\d{4})', texto)
        pix_match = re.search(r'([^\n\r]*)\s*Valor:', texto)
        data_pagamento_match = re.search(r'Data do Pagamento:\s*(\d{2}/\d{2}/\d{4})', texto)
        hora_pagamento_match = re.search(r'Hora do Pagamento:\s*(\d{2}/\d{2}/\d{4})', texto)


        if descricao_pagamento_match and data_transacao_match:
            # Capturar descrição do pagamento
            data_transacao = data_transacao_match.group(1)
            descricao_pagamento = descricao_pagamento_match.group(1).strip()
            
            # Limitar a descrição para as três últimas palavras
            palavras = descricao_pagamento.split()
            if len(palavras) >= 2:
                descricao_pagamento_limitada = ' '.join(palavras[-3:])
                descricao_pagamento_limitada = corrigir_texto_grudado(descricao_pagamento_limitada)
                descricao_pagamento_limitada = remover_palavras_indesejadas(descricao_pagamento_limitada)

            else:
                descricao_pagamento_limitada = descricao_pagamento
            
            # Converter data para o formato desejado
            data_formatada = re.sub(r'(\d{2})/(\d{2})/(\d{4})', r'\1.\2.\3', data_transacao)
            return descricao_pagamento_limitada, data_formatada
        
        elif pix_match and data_transacao_match:
            # Capturar Descição do pix
            descricao_pagamento = pix_match.group(1).strip()
            data_transacao = data_transacao_match.group(1)
            
            # Converter data para o formato desejado
            data_formatada = re.sub(r'(\d{2})/(\d{2})/(\d{4})', r'\1.\2.\3', data_transacao)
            return pix, data_formatada
        
        elif descricao_pagamento_match and data_pagamento_match :
            # Capturar descrição do pagamento
            data_transacao = data_pagamento_match.group(1)
            descricao_pagamento = descricao_pagamento_match.group(1).strip()
            
            # Limitar a descrição para as três últimas palavras
            palavras = descricao_pagamento.split()
            if len(palavras) >= 2:
                descricao_pagamento_limitada = ' '.join(palavras[-3:])
                descricao_pagamento_limitada = corrigir_texto_grudado(descricao_pagamento_limitada)
                descricao_pagamento_limitada = remover_palavras_indesejadas(descricao_pagamento_limitada)

            else:
                descricao_pagamento_limitada = descricao_pagamento
                
            # Converter data para o formato desejado
            data_formatada = re.sub(r'(\d{2})/(\d{2})/(\d{4})', r'\1.\2.\3', data_transacao)
            return descricao_pagamento_limitada, data_formatada
        
        elif hora_pagamento_match:
            # Capturar descrição do pagamento
            data_transacao = hora_pagamento_match.group(1)
            descricao_pagamento = descricao_pagamento_match.group(1).strip()
            
            # Limitar a descrição para as três últimas palavras
            palavras = descricao_pagamento.split()
            if len(palavras) >= 2:
                descricao_pagamento_limitada = ' '.join(palavras[-3:])
                descricao_pagamento_limitada = corrigir_texto_grudado(descricao_pagamento_limitada)
                descricao_pagamento_limitada = remover_palavras_indesejadas(descricao_pagamento_limitada)

            else:
                descricao_pagamento_limitada = descricao_pagamento
                
            # Converter data para o formato desejado
            data_formatada = re.sub(r'(\d{2})/(\d{2})/(\d{4})', r'\1.\2.\3', data_transacao)
            return descricao_pagamento_limitada, data_formatada
            

    except Exception as e:
        print(f'Erro ao ler o PDF {caminho_pdf}: {e}')
        return None, None
    
# Função para corrigir texto com palavras grudadas
def corrigir_texto_grudado(texto):
    # Adiciona um espaço antes de palavras específicas que parecem estar coladas
    texto_corrigido = re.sub(r'([a-z])([A-Z])', r'\1 \2', texto)
    return texto_corrigido

def remover_palavras_indesejadas(texto):
    # Lista de palavras indesejadas que você quer remover
    palavras_indesejadas = ['Eletrônica','Autenticação',":"]
    
    for palavra in palavras_indesejadas:
        # Remove todas as ocorrências da palavra indesejada
        texto = texto.replace(palavra, '').strip()
    
    return texto

# Função para remover caracteres inválidos para nomes de arquivos
def limpar_nome_arquivo(nome):
    return re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', nome)

# Percorrer os arquivos na pasta de origem
for nome_arquivo in os.listdir(pasta_origem):
    caminho_arquivo = os.path.join(pasta_origem, nome_arquivo)
    if os.path.isfile(caminho_arquivo) and nome_arquivo.lower().endswith('.pdf'):
        print(f'Lendo o arquivo: {nome_arquivo}')
        descricao_pagamento, data_formatada = extrair_informacoes(caminho_arquivo)
        if descricao_pagamento and data_formatada:
            descricao_pagamento = limpar_nome_arquivo(descricao_pagamento)
            
            novo_nome_arquivo = f'{descricao_pagamento} {data_formatada}.pdf'
            novo_caminho_arquivo = os.path.join(pasta_origem, novo_nome_arquivo)
            
            if not os.path.exists(novo_caminho_arquivo):
                try:
                    if os.path.exists(caminho_arquivo):
                        os.rename(caminho_arquivo, novo_caminho_arquivo)
                        print(f'Arquivo renomeado para: {novo_nome_arquivo}')
                    else:
                        print(f'O arquivo original não foi encontrado: {caminho_arquivo}')
                except Exception as e:
                    print(f'Erro ao renomear o arquivo: {e}')
            
            # Movendo o arquivo para a pasta de destino após renomeá-lo
            caminho_destino_final = os.path.join(pasta_destino, novo_nome_arquivo)
            try:
                shutil.move(novo_caminho_arquivo, caminho_destino_final)
                print(f'Arquivo movido para: {caminho_destino_final}')
            except Exception as e:
                print(f'Erro ao mover o arquivo: {e}')
        else:
            print(f'Não foi possível processar o arquivo: {nome_arquivo}')