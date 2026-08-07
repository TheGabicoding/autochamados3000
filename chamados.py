from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
                if len(partes) > 1:
                    serie = partes[1].strip()
                else:
                    serie = ""
            else:
                produto = linha.strip()
                serie = ""
                
            produto_upper = produto.upper()
            if "S/N" in produto_upper:
                pos_sn = produto_upper.find("S/N")
                if not serie:
                    serie = produto[pos_sn + 3:].strip()
                produto = produto[:pos_sn].strip()
            elif "W" in produto_upper and not serie:
                pos_w = produto_upper.rfind("W") + 1
                if pos_w < len(produto):
                    serie = produto[pos_w:].strip()
                    produto = produto[:pos_w].strip()
                    
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
    
    for indice, (produto, serie) in enumerate(lista_produtos):
        
        logging.info("Processo: Alterando caixa para incidentes | Status: Em andamento")
        try:
            campo_tipo = WebDriverWait(navegador, 10).until(
                EC.presence_of_element_located((By.NAME, "type"))
            )
            
            try:
                selecao = Select(campo_tipo)
                selecao.select_by_value("1")
            except Exception:
                try:
                    selecao = Select(campo_tipo)
                    selecao.select_by_visible_text("Incidente")
                except Exception:
                    navegador.execute_script("arguments[0].value = '1'; arguments[0].dispatchEvent(new Event('change'));", campo_tipo)
                    
            logging.info("Processo: Alterando caixa para incidentes | Status: Bem-sucedido")
        except Exception as erro:
            logging.error("Processo: Alterando caixa para incidentes | Status: Falhou")
            
        time.sleep(5)
        
        logging.info("Processo: Adicionando titulo | Status: Em andamento")
        try:
            nome_completo = tipo_produto + " " + produto
            
            try:
                campo_titulo = WebDriverWait(navegador, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@name='name']"))
                )
            except Exception:
                campo_titulo = navegador.find_element(By.ID, "name")
                
            campo_titulo.clear()
            campo_titulo.send_keys(nome_completo)
            logging.info("Processo: Adicionando titulo | Status: Bem-sucedido")
        except Exception as erro:
            logging.error("Processo: Adicionando titulo | Status: Falhou")
            
        time.sleep(2)
        
        logging.info("Processo: Adicionando descricao | Status: Em andamento")
        try:
            iframe = WebDriverWait(navegador, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".tox-tinymce iframe"))
            )
            navegador.switch_to.frame(iframe)
            
            corpo_texto = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.ID, "tinymce"))
            )
            corpo_texto.click()
            corpo_texto.clear()
            corpo_texto.send_keys("S/N " + serie)
            
            navegador.switch_to.default_content()
            logging.info("Processo: Adicionando descricao (Iframe) | Status: Bem-sucedido")
        except Exception as erro_iframe:
            navegador.switch_to.default_content()
            try:
                script = "tinymce.activeEditor.setContent('S/N " + serie + "');"
                navegador.execute_script(script)
                logging.info("Processo: Adicionando descricao (JS) | Status: Bem-sucedido")
            except Exception as erro_js:
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
        
        if indice < len(lista_produtos) - 1:
            logging.info("Processo: Clicando em Criar chamado no menu | Status: Em andamento")
            try:
                botao_menu_lateral = WebDriverWait(navegador, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Criar chamado')]"))
                )
                botao_menu_lateral.click()
                logging.info("Processo: Clicando em Criar chamado no menu | Status: Bem-sucedido")
            except Exception:
                logging.error("Processo: Clicando em Criar chamado no menu | Status: Falhou. Recarregando via URL.")
                navegador.get("http://suporte.gerbit.com.br/front/ticket.form.php")
            
            time.sleep(5)
        
    logging.info("Processo: Finalizando chamados | Status: Bem-sucedido")
    return "Processo de chamados finalizado!"