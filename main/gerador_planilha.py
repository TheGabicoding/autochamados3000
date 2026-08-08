import csv
import logging
from datetime import datetime

from config import EQUIPAMENTOS, STATUS_PENDENTE, caminho_planilha


def _parse_texto(texto):
    """
    Converte o texto colado pelo usuario em uma lista de tuplas (marca, serie).

    Formato esperado:
        MARCA
        1-SERIE
        2-SERIE

    Retorna (dados, avisos) onde 'avisos' descreve linhas que foram
    ignoradas, para que o usuario saiba exatamente o que aconteceu
    (em vez de itens sumirem silenciosamente da planilha).
    """
    dados = []
    avisos = []
    marca_atual = None

    for numero, linha_bruta in enumerate(texto.split("\n"), start=1):
        linha = linha_bruta.strip()
        if not linha:
            continue

        # Remove prefixos tipo "[algo]: " que às vezes vêm de sistemas colados.
        if "]" in linha and ":" in linha:
            linha = linha.split(":", 1)[-1].strip()

        # maxsplit=1: preserva hifens que fazem parte do proprio numero de serie.
        partes = linha.split("-", 1)
        primeira_parte = partes[0].strip()

        if primeira_parte.isdigit():
            serie = partes[1].strip() if len(partes) > 1 else ""

            if marca_atual is None:
                avisos.append(f"Linha {numero}: número de série sem marca definida antes — ignorada.")
                continue
            if not serie:
                avisos.append(f"Linha {numero}: número de série vazio — ignorada.")
                continue

            dados.append((marca_atual, serie))
        else:
            marca_atual = linha

    return dados, avisos


def gerar_csv(texto, opcao):
    """
    Gera/atualiza o CSV do tipo de equipamento indicado a partir do texto colado.

    Retorna (mensagem, texto_para_copiar).
    """
    logging.info("Processo: Gerando CSV (%s) | Status: Em andamento", opcao)

    if opcao not in EQUIPAMENTOS:
        logging.error("Processo: Gerando CSV | Status: Falhou | Tipo desconhecido: %s", opcao)
        return f"Tipo de equipamento desconhecido: {opcao}", ""

    if not texto or not texto.strip():
        logging.warning("Processo: Gerando CSV | Status: Cancelado | Motivo: texto vazio")
        return "Cole os dados na caixa de texto antes de gerar o CSV.", ""

    dados, avisos = _parse_texto(texto)

    if not dados:
        logging.warning("Processo: Gerando CSV | Status: Nenhum dado reconhecido")
        return "Nenhum item reconhecido no texto colado. Confira o formato (veja o botão '?').", ""

    config = EQUIPAMENTOS[opcao]
    hoje = datetime.now().strftime("%d/%m/%Y")
    caminho_final = caminho_planilha(opcao)

    linhas_planilha = [
        config["montar_linha"](marca, serie, hoje, STATUS_PENDENTE)
        for marca, serie in dados
    ]

    try:
        arquivo_existe = _arquivo_tem_conteudo(caminho_final)

        # Se o arquivo ja existe, adiciona as novas linhas ao final em vez de
        # sobrescrever o que ja estava la (evita perder trabalho anterior).
        modo = "a" if arquivo_existe else "w"
        with open(caminho_final, mode=modo, newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            if not arquivo_existe:
                escritor.writerow(config["cabecalho"])
            escritor.writerows(linhas_planilha)

        texto_para_copiar = "\n".join("\t".join(linha) for linha in linhas_planilha)

        logging.info("Processo: Gerando CSV (%s) | Status: Bem-sucedido | %d linha(s)",
                     opcao, len(linhas_planilha))

        mensagem = f"{len(linhas_planilha)} item(ns) adicionados à planilha de {opcao.lower()}."
        if avisos:
            mensagem += f"\n\n{len(avisos)} linha(s) ignoradas:\n" + "\n".join(avisos)

        return mensagem, texto_para_copiar

    except OSError as erro:
        logging.error("Processo: Gerando CSV (%s) | Status: Falhou | Erro: %s", opcao, erro)
        return f"Erro ao gravar o arquivo CSV: {erro}", ""


def _arquivo_tem_conteudo(caminho):
    try:
        with open(caminho, "r", encoding="utf-8-sig") as arquivo:
            return arquivo.readline() != ""
    except FileNotFoundError:
        return False