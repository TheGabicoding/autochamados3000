"""
Configuracao central do Autochamados3000.

"""

import os
import sys

# Status usado na coluna STATUS da planilha ao gerar o CSV. A planilha
# "oficial" fica no Drive (o CSV local é só um rascunho para copiar e
# colar), então o programa não tenta sincronizar status de volta para
# o arquivo local depois de abrir os chamados.
STATUS_PENDENTE = "ABRIR CHAMADO"


def _montar_linha_padrao(marca, serie, hoje, status):
    """Ordem de colunas usada por Estabilizador e Fonte."""
    return [marca, serie, "", hoje, "", status]


def _montar_linha_monitor(marca, serie, hoje, status):
    """Monta a linha do Monitor na ordem exata das colunas da planilha."""
    return [
        marca,       # DESCRIÇÃO
        serie,       # Nº DE SERIE
        "",          # PATRIMÔNIO Nº
        "",          # LOCAL DA RETIRADA
        status,      # STATUS
        "",          # ENVIO DO CHAMADO
        hoje,        # DATA DE ABERTURA
        "",          # LOCAL
    ]

EQUIPAMENTOS = {
    "Estabilizador": {
        "arquivo": "estabilizador.csv",
        "cabecalho": ["ESTABILIZADOR MARCA", "Nº DE SERIE", "ENVIO DO CHAMADO",
                      "DATA DE ABERTURA", "LOCAL DA RETIRADA", "STATUS"],
        "montar_linha": _montar_linha_padrao,
    },
    "Fonte": {
        "arquivo": "fontes.csv",
        "cabecalho": ["FONTE MARCA", "Nº DE SERIE", "ENVIO DO CHAMADO",
                      "DATA DE ABERTURA", "LOCAL DA RETIRADA", "STATUS"],
        "montar_linha": _montar_linha_padrao,
    },
    "Monitor": {
        "arquivo": "monitores.csv",
        "cabecalho": ["DESCRIÇÃO", "Nº DE SERIE", "PATRIMÔNIO Nº", "LOCAL DA RETIRADA",
                      "STATUS", "ENVIO DO CHAMADO", "DATA DE ABERTURA", "LOCAL"],
        "montar_linha": _montar_linha_monitor,
    },
}


def obter_pasta_raiz():
    """Retorna a pasta raiz do programa, tanto rodando via .py quanto via .exe (PyInstaller)."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(pasta_atual)


def obter_pasta_planilhas():
    pasta = os.path.join(obter_pasta_raiz(), "planilhas")
    os.makedirs(pasta, exist_ok=True)
    return pasta


def obter_pasta_logs():
    pasta = os.path.join(obter_pasta_raiz(), "logs")
    os.makedirs(pasta, exist_ok=True)
    return pasta


def caminho_planilha(opcao):
    config = EQUIPAMENTOS[opcao]
    return os.path.join(obter_pasta_planilhas(), config["arquivo"])