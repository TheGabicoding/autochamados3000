from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import logging

def abrir_chamados(texto, tipo_produto):
    logging.info("Processo: Organizando texto | Status: Em andamento")
    
    try:
        linhas = texto.split('\n')
        lista_produtos = []
        
        for linha in linhas:
            linha = linha.strip()
            if linha == "":
                continue
            
            if "\t" in linha:
                partes = linha.split("\t")
                produto = partes[0].strip()
                serie = partes[1].strip()
            else:
                pos = linha.find("W")
                if pos != -1:
                    produto = linha[:pos+1].strip()
                    serie = linha[pos+1:].strip()
                else:
                    produto = linha
                    serie = ""
                    
            lista_produtos.append((produto, serie))
            
        logging.info("Processo: Organizando texto | Status: Bem-sucedido")
        
    except Exception as erro:
        logging.error("Processo: Organizando texto | Status: Falhou")
        return "Erro ao organizar texto."
        
    logging.info("Processo: Abrindo navegador | Status: Em andamento")
    
    try:
        navegador = webdriver.Chrome()
        navegador.get("http://suporte.gerbit.com.br/front/ticket.form.php")
        logging.info("Processo: Abrindo navegador | Status: Bem-sucedido")
    except Exception as erro:
        logging.error("Processo: Abrindo navegador | Status: Falhou")
        return "Erro ao abrir navegador."
        
    time.sleep(15)
    
    for produto, serie in lista_produtos:
        
        logging.info("Processo: Alterando caixa para incidentes | Status: Em andamento")
        try:
            campo_tipo = navegador.find_element(By.NAME, "type")
            selecao = Select(campo_tipo)
            selecao.select_by_visible_text("Incidente")
            logging.info("Processo: Alterando caixa para incidentes | Status: Bem-sucedido")
        except Exception as erro:
            logging.error("Processo: Alterando caixa para incidentes | Status: Falhou")
            
        time.sleep(5)
        
        logging.info("Processo: Adicionando titulo | Status: Em andamento")
        try:
            nome_completo = tipo_produto + " " + produto
            
            try:
                campo_titulo = navegador.find_element(By.XPATH, "//input[@name='name']")
            except Exception as erro:
                campo_titulo = navegador.find_element(By.ID, "name")
                
            campo_titulo.clear()
            campo_titulo.send_keys(nome_completo)
            logging.info("Processo: Adicionando titulo | Status: Bem-sucedido")
        except Exception as erro:
            logging.error("Processo: Adicionando titulo | Status: Falhou")
            
        time.sleep(2)
        
        logging.info("Processo: Adicionando descricao | Status: Em andamento")
        try:
            iframe = navegador.find_element(By.TAG_NAME, "iframe")
            navegador.switch_to.frame(iframe)
            corpo_texto = navegador.find_element(By.ID, "tinymce")
            corpo_texto.clear()
            corpo_texto.send_keys("S/N " + serie)
            navegador.switch_to.default_content()
            logging.info("Processo: Adicionando descricao | Status: Bem-sucedido")
        except Exception as erro1:
            try:
                campo_desc = navegador.find_element(By.XPATH, "//textarea[@name='content']")
                campo_desc.clear()
                campo_desc.send_keys("S/N " + serie)
                logging.info("Processo: Adicionando descricao | Status: Bem-sucedido")
            except Exception as erro2:
                logging.error("Processo: Adicionando descricao | Status: Falhou")
        
        time.sleep(2)
        
        logging.info("Processo: Clicando em adicionar | Status: Em andamento")
        try:
            botao_adicionar = navegador.find_element(By.NAME, "add")
            botao_adicionar.click()
            logging.info("Processo: Clicando em adicionar | Status: Bem-sucedido")
        except Exception as erro:
            logging.error("Processo: Clicando em adicionar | Status: Falhou")
        
        time.sleep(5)
        navegador.get("http://suporte.gerbit.com.br/front/ticket.form.php")
        time.sleep(3)
        
    logging.info("Processo: Finalizando chamados | Status: Bem-sucedido")
    return "Processo de chamados finalizado!"