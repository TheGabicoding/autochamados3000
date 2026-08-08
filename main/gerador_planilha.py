import os
import csv
import logging
import sys
from datetime import datetime

def gerar_csv(texto, opcao):
    logging.info("Processo: Iniciando criacao de CSV | Status: Em andamento")
    try:
        linhas = texto.split('\n')
        dados = []
        marca_atual = ""
        
        data_hoje = datetime.now()
        hoje = data_hoje.strftime("%d/%m/%Y")
        
        for linha in linhas:
            linha = linha.strip()
            
            if linha == "":
                continue
                
            if "]" in linha:
                if ":" in linha:
                    partes_linha = linha.split(":")
                    linha = partes_linha[-1]
                    linha = linha.strip()
                    
            partes = linha.split("-")
            primeira_parte = partes[0]
            primeira_parte = primeira_parte.strip()
            
            if primeira_parte.isdigit():
                serie = ""
                tamanho = len(partes)
                if tamanho > 1:
                    serie = partes[1]
                    serie = serie.strip()
                    
                if opcao == "Estabilizador":
                    linha_planilha = [marca_atual, serie, "", hoje, "", "CHAMADO ABERTO"]
                    dados.append(linha_planilha)
                if opcao == "Fonte":
                    linha_planilha = [marca_atual, serie, "", hoje, "", "CHAMADO ABERTO"]
                    dados.append(linha_planilha)
                if opcao == "Monitor":
                    linha_planilha = [marca_atual, serie, "", "CHAMADO ABERTO", "", hoje, ""]
                    dados.append(linha_planilha)
            else:
                marca_atual = linha
                
        logging.info("Processo: Organizando texto | Status: Bem-sucedido")

        nome_arquivo = ""
        cabecalho = []
        
        if opcao == "Estabilizador":
            nome_arquivo = "estabilizador.csv"
            cabecalho = ["ESTABILIZADOR MARCA", "Nº DE SERIE", "ENVIO DO CHAMADO", "DATA DE ABERTURA", "LOCAL DA RETIRADA", "STATUS"]
        if opcao == "Fonte":
            nome_arquivo = "fontes.csv"
            cabecalho = ["FONTE MARCA", "Nº DE SERIE", "ENVIO DO CHAMADO", "DATA DE ABERTURA", "LOCAL DA RETIRADA", "STATUS"]
        if opcao == "Monitor":
            nome_arquivo = "monitores.csv"
            cabecalho = ["DESCRIÇÃO", "PATRIMÔNIO Nº", "LOCAL DA RETIRADA", "STATUS", "ENVIO DO CHAMADO", "DATA DE ABERTURA", "LOCAL"]

        if getattr(sys, 'frozen', False):
            pasta_raiz = os.path.dirname(sys.executable)
        else:
            caminho_atual = os.path.abspath(__file__)
            pasta_atual = os.path.dirname(caminho_atual)
            pasta_raiz = os.path.dirname(pasta_atual)
            
        pasta_planilhas = os.path.join(pasta_raiz, "planilhas")

        if not os.path.exists(pasta_planilhas):
            os.makedirs(pasta_planilhas)

        caminho_final = os.path.join(pasta_planilhas, nome_arquivo)

        arquivo = open(caminho_final, mode='w', newline='', encoding='utf-8-sig')
        escritor = csv.writer(arquivo, delimiter=';')
        escritor.writerow(cabecalho)
        
        texto_para_copiar = ""
        for linha_dado in dados:
            escritor.writerow(linha_dado)
            
            linha_texto = "\t".join(linha_dado)
            texto_para_copiar = texto_para_copiar + linha_texto + "\n"
            
        arquivo.close()
        
        logging.info("Processo: Criando arquivo CSV | Status: Bem-sucedido")
        
        mensagem = "Dados tratados com sucesso"
        return mensagem, texto_para_copiar
        
    except Exception:
        logging.error("Processo: Criando arquivo CSV | Status: Falhou")
        return "Erro ao gerar arquivo.", ""