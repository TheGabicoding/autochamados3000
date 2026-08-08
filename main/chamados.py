import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL_ABERTURA_CHAMADO = "http://suporte.gerbit.com.br/front/ticket.form.php"

# Tempo generoso para o PRIMEIRO chamado, porque o usuario ainda precisa
# fazer login manualmente. Substitui o antigo "time.sleep(12)" fixo, que
# falhava sempre que o login demorava mais que isso.
TIMEOUT_PRIMEIRO_CHAMADO = 180
TIMEOUT_PADRAO = 10


def _parse_texto(texto):
    """Converte o texto colado (produto + serie, separados por TAB) em lista de tuplas."""
    lista_produtos = []
    for linha_bruta in texto.split("\n"):
        linha = linha_bruta.strip()
        if not linha:
            continue

        if "\t" in linha:
            partes = linha.split("\t")
            produto = partes[0].strip()
            serie = partes[1].strip() if len(partes) > 1 else ""
        else:
            produto = linha
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

    return lista_produtos


def _selecionar_tipo_incidente(navegador, timeout):
    campo_tipo = WebDriverWait(navegador, timeout).until(
        EC.presence_of_element_located((By.NAME, "type"))
    )
    try:
        Select(campo_tipo).select_by_value("1")
    except Exception:
        try:
            Select(campo_tipo).select_by_visible_text("Incidente")
        except Exception:
            navegador.execute_script(
                "arguments[0].value = '1'; arguments[0].dispatchEvent(new Event('change'));",
                campo_tipo,
            )


def _preencher_titulo(navegador, titulo):
    try:
        campo_titulo = WebDriverWait(navegador, 2).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='name']"))
        )
    except Exception:
        campo_titulo = navegador.find_element(By.ID, "name")

    campo_titulo.clear()
    campo_titulo.send_keys(titulo)


def _preencher_descricao(navegador, descricao):
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
        corpo_texto.send_keys(descricao)
        navegador.switch_to.default_content()
    except Exception:
        navegador.switch_to.default_content()
        script = f"tinymce.activeEditor.setContent({descricao!r});"
        navegador.execute_script(script)


def _clicar_adicionar(navegador):
    navegador.find_element(By.NAME, "add").click()


def _ir_para_novo_chamado(navegador):
    try:
        botao_menu_lateral = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Criar chamado')]"))
        )
        botao_menu_lateral.click()
    except Exception:
        logging.warning("Menu 'Criar chamado' não encontrado, recarregando via URL.")
        navegador.get(URL_ABERTURA_CHAMADO)


def abrir_chamados(texto, tipo_produto, callback_progresso=None):
    """
    Abre um chamado no Gerbit para cada item do texto colado.

    callback_progresso(indice, total, produto, sucesso_ou_none), se fornecido,
    é chamado antes (sucesso_ou_none=None) e depois (True/False) de cada
    item, para permitir feedback de progresso na interface.

    Retorna uma mensagem-resumo (ex.: "8 de 10 chamados abertos com sucesso").
    """
    logging.info("Processo: Organizando texto | Status: Em andamento")

    if not texto or not texto.strip():
        return "Cole os dados (produto e série) antes de abrir os chamados."

    try:
        lista_produtos = _parse_texto(texto)
        logging.info("Processo: Organizando texto | Status: Bem-sucedido | %d item(ns)", len(lista_produtos))
    except Exception as erro:
        logging.error("Processo: Organizando texto | Status: Falhou | Erro: %s", erro)
        return f"Erro ao organizar texto: {erro}"

    if not lista_produtos:
        return "Nenhum item reconhecido no texto colado."

    total = len(lista_produtos)
    sucessos = 0

    try:
        navegador = webdriver.Chrome()
        navegador.get(URL_ABERTURA_CHAMADO)
        logging.info("Processo: Abrindo navegador | Status: Bem-sucedido")
    except Exception as erro:
        logging.error("Processo: Abrindo navegador | Status: Falhou | Erro: %s", erro)
        return f"Erro ao abrir o navegador: {erro}"

    try:
        for indice, (produto, serie) in enumerate(lista_produtos):
            if callback_progresso:
                callback_progresso(indice, total, produto, None)

            timeout = TIMEOUT_PRIMEIRO_CHAMADO if indice == 0 else TIMEOUT_PADRAO
            item_ok = True

            try:
                _selecionar_tipo_incidente(navegador, timeout)
            except Exception as erro:
                logging.error("Item %d/%d (%s): falha ao selecionar tipo incidente | Erro: %s",
                              indice + 1, total, produto, erro)
                item_ok = False

            time.sleep(0.3)

            try:
                _preencher_titulo(navegador, f"{tipo_produto} {produto}")
            except Exception as erro:
                logging.error("Item %d/%d (%s): falha ao preencher título | Erro: %s",
                              indice + 1, total, produto, erro)
                item_ok = False

            time.sleep(0.2)

            try:
                _preencher_descricao(navegador, f"S/N {serie}")
            except Exception as erro:
                logging.error("Item %d/%d (%s): falha ao preencher descrição | Erro: %s",
                              indice + 1, total, produto, erro)
                item_ok = False

            time.sleep(0.2)

            try:
                _clicar_adicionar(navegador)
            except Exception as erro:
                logging.error("Item %d/%d (%s): falha ao clicar em adicionar | Erro: %s",
                              indice + 1, total, produto, erro)
                item_ok = False

            time.sleep(2)

            if item_ok:
                sucessos += 1
                logging.info("Item %d/%d (%s): chamado aberto com sucesso.", indice + 1, total, produto)

            if callback_progresso:
                callback_progresso(indice, total, produto, item_ok)

            if indice < total - 1:
                _ir_para_novo_chamado(navegador)
                time.sleep(2)

    finally:
        try:
            navegador.quit()
        except Exception:
            pass

    logging.info("Processo: Finalizando chamados | Status: Concluído | %d/%d sucesso(s)", sucessos, total)

    if sucessos == total:
        return f"{sucessos} de {total} chamados abertos com sucesso!"
    return (f"{sucessos} de {total} chamados abertos com sucesso. "
            f"{total - sucessos} falharam — veja 'Abrir Logs' para detalhes.")