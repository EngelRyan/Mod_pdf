import os
import re
from PyPDF2 import PdfReader
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# Função para abrir o seletor de pastas
def selecionar_pasta_origem():
    pasta = filedialog.askdirectory(title="Selecione a pasta de origem")
    pasta_origem_entry.delete(0, tk.END)
    pasta_origem_entry.insert(0, pasta)

def selecionar_pasta_destino():
    pasta = filedialog.askdirectory(title="Selecione a pasta de destino")
    pasta_destino_entry.delete(0, tk.END)
    pasta_destino_entry.insert(0, pasta)

# Função para ler e extrair informações específicas do PDF
def extrair_informacoes(caminho_pdf):
    try:
        leitor = PdfReader(caminho_pdf)
        texto = ''
        for pagina in leitor.pages:
            texto += pagina.extract_text() + '\n'

        # Ajustar regex para capturar o texto
        descricao_pagamento_match = re.search(r'([^\n\r]*)\s*Descrição do Pagamento:', texto)
        data_transacao_match = re.search(r'Data da Transação:\s*(\d{2}/\d{2}/\d{4})', texto)
        pix_match = re.search(r'([^\n\r]*)\s*Valor:', texto)
        data_pagamento_match = re.search(r'Realizado em:\s*(\d{2}/\d{2}/\d{4})', texto)
        hora_pagamento_match = re.search(r'Hora do Pagamento:\s*(\d{2}/\d{2}/\d{4})', texto)

        # Verificações para evitar que acessos inválidos causem erros
        if descricao_pagamento_match and data_transacao_match:
            descricao_pagamento = descricao_pagamento_match.group(1).strip()
            data_transacao = data_transacao_match.group(1)
        
        elif pix_match and data_pagamento_match:
            descricao_pagamento = pix_match.group(1).strip()
            data_transacao = data_pagamento_match.group(1)

        elif descricao_pagamento_match and data_pagamento_match:
            descricao_pagamento = descricao_pagamento_match.group(1).strip()
            data_transacao = data_pagamento_match.group(1)

        elif hora_pagamento_match:
            descricao_pagamento = descricao_pagamento_match.group(1).strip() if descricao_pagamento_match else "Descrição indisponível"
            data_transacao = hora_pagamento_match.group(1)
            
        else:
            return None, None
            
        # Limitar a descrição para as três últimas palavras
        palavras = descricao_pagamento.split()
        if len(palavras) >= 2 and not pix_match:
            descricao_pagamento_limitada = ' '.join(palavras[-3:])
            descricao_pagamento_limitada = remover_palavras_indesejadas(descricao_pagamento_limitada)
        else:
            descricao_pagamento_limitada = descricao_pagamento
        
        # Converter data para o formato desejado
        data_formatada = re.sub(r'(\d{2})/(\d{2})/(\d{4})', r'\1.\2.\3', data_transacao)
        return descricao_pagamento_limitada, data_formatada

    except Exception as e:
        return None, None
    
def remover_palavras_indesejadas(texto):
    # Lista de palavras indesejadas que você quer remover
    palavras_indesejadas = ['Eletrônica','Autenticação',":"]
    
    for palavra in palavras_indesejadas:
        # Remove todas as ocorrências da palavra indesejada
        texto = texto.replace(palavra, '').strip()
    
    return texto

# Função principal para renomear e mover os arquivos
def renomear_mover_arquivos():
    pasta_origem = pasta_origem_entry.get()
    pasta_destino = pasta_destino_entry.get()

    if not pasta_origem or not pasta_destino:
        messagebox.showwarning("Erro", "Por favor, selecione as pastas de origem e destino.")
        return

    arquivos_processados = 0

    for nome_arquivo in os.listdir(pasta_origem):
        caminho_arquivo = os.path.join(pasta_origem, nome_arquivo)
        if os.path.isfile(caminho_arquivo) and nome_arquivo.lower().endswith('.pdf'):
            descricao_pagamento, data_formatada = extrair_informacoes(caminho_arquivo)
            if descricao_pagamento and data_formatada:
                novo_nome_arquivo = f'{descricao_pagamento} {data_formatada}.pdf'
                novo_caminho_arquivo = os.path.join(pasta_origem, novo_nome_arquivo)

                # Adicionar sufixo numérico se o arquivo já existir
                contador = 1
                while os.path.exists(novo_caminho_arquivo):
                    novo_nome_arquivo = f'{descricao_pagamento} {data_formatada}_{contador}.pdf'
                    novo_caminho_arquivo = os.path.join(pasta_origem, novo_nome_arquivo)
                    contador += 1

                os.rename(caminho_arquivo, novo_caminho_arquivo)
                caminho_destino_final = os.path.join(pasta_destino, novo_nome_arquivo)
                shutil.move(novo_caminho_arquivo, caminho_destino_final)
                arquivos_processados += 1
                print(f'Arquivo movido para: {caminho_destino_final}')
            else:
                # Exibir mensagem informando que o arquivo não pôde ser processado
                messagebox.showinfo("Aviso", f"Não foi possível processar o arquivo: {nome_arquivo}")
    
    # Exibir mensagem final com o número de arquivos processados
    messagebox.showinfo("Concluído", f"Renomeação concluída! {arquivos_processados} arquivos foram processados com sucesso.")

# Criação da interface gráfica
root = tk.Tk()
root.title("Renomeador de PDFs")

# Layout
tk.Label(root, text="Pasta de origem:").grid(row=0, column=0, padx=10, pady=10)
pasta_origem_entry = tk.Entry(root, width=50)
pasta_origem_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Selecionar", command=selecionar_pasta_origem).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Pasta de destino:").grid(row=1, column=0, padx=10, pady=10)
pasta_destino_entry = tk.Entry(root, width=50)
pasta_destino_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Selecionar", command=selecionar_pasta_destino).grid(row=1, column=2, padx=10, pady=10)

tk.Button(root, text="Renomear e Mover", command=renomear_mover_arquivos).grid(row=2, column=1, padx=10, pady=20)

root.mainloop()
