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
        pix_match = re.search(r'([^\n\r]*)\s*Valor:', texto)
        data_transacao_match = re.search(r'Realizado em:\s*(\d{2}/\d{2}/\d{4})', texto)

        if pix_match and data_transacao_match:
            # Capturar Descição do pix
            pix = pix_match.group(1).strip()
            data_transacao = data_transacao_match.group(1)
            
            # Converter data para o formato desejado
            data_formatada = re.sub(r'(\d{2})/(\d{2})/(\d{4})', r'\1.\2.\3', data_transacao)
            return pix, data_formatada
        else:
            print(f'Informações não encontradas no PDF: {caminho_pdf}')
            return None, None
    except Exception as e:
        print(f'Erro ao ler o PDF {caminho_pdf}: {e}')
        return None, None
    
# Função para remover caracteres inválidos para nomes de arquivos
def limpar_nome_arquivo(nome):
    return re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', nome)

# Percorrer os arquivos na pasta de origem
for nome_arquivo in os.listdir(pasta_origem):
    caminho_arquivo = os.path.join(pasta_origem, nome_arquivo)
    if os.path.isfile(caminho_arquivo) and nome_arquivo.lower().endswith('.pdf'):
        print(f'Lendo o arquivo: {nome_arquivo}')
        pix, data_formatada = extrair_informacoes(caminho_arquivo)
        if pix and data_formatada:
            pix = limpar_nome_arquivo(pix)
            
            novo_nome_arquivo = f'{pix} {data_formatada}.pdf'
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