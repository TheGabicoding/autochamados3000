import os
from datetime import datetime
import csv
import logging

def gerar_csv(texto, opcao):
    logging.info("Processo: Iniciando criacao de CSV | Status: Em andamento")
    
    try:
        linhas = texto.split('\n')
        dados = []
        marca_atual = ""
        hoje = datetime.now().strftime("%d/%m/%Y")
        
        for linha in linhas:
            linha = linha.strip()
            
            if linha == "":
                continue
                
            if "]" in linha and ":" in linha:
                linha = linha.split(":")[-1].strip()
                
            partes = linha.split("-", 1)
            
            if partes[0].strip().isdigit():
                serie = ""
                if len(partes) > 1:
                    serie = partes[1].strip()
                    
                if opcao == "Estabilizador":
                    linha_planilha = [marca_atual, serie, "", hoje, "", "CHAMADO ABERTO"]
                elif opcao == "Fonte":
                    linha_planilha = [marca_atual, serie, "", hoje, "", "CHAMADO ABERTO"]
                elif opcao == "Monitor":
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
        elif opcao == "Fonte":
            nome_arquivo = "fontes.csv"
            cabecalho = ["FONTE MARCA", "Nº DE SERIE", "ENVIO DO CHAMADO", "DATA DE ABERTURA", "LOCAL DA RETIRADA", "STATUS"]
        elif opcao == "Monitor":
            nome_arquivo = "monitores.csv"
            cabecalho = ["DESCRIÇÃO", "PATRIMÔNIO Nº", "LOCAL DA RETIRADA", "STATUS", "ENVIO DO CHAMADO", "DATA DE ABERTURA", "LOCAL"]

        pasta_do_codigo = os.path.dirname(os.path.abspath(__file__))
        caminho_final = os.path.join(pasta_do_codigo, nome_arquivo)

        arquivo = open(caminho_final, mode='w', newline='', encoding='utf-8-sig')
        escritor = csv.writer(arquivo, delimiter=';')
        escritor.writerow(cabecalho)
        
        for linha_dado in dados:
            escritor.writerow(linha_dado)
            
        arquivo.close()
        
        logging.info("Processo: Criando arquivo CSV | Status: Bem-sucedido")
        
        return "Arquivo " + nome_arquivo + " gerado com sucesso!"
        
    except Exception as erro:
        logging.error("Processo: Criando arquivo CSV | Status: Falhou")
        return "Erro ao gerar arquivo."