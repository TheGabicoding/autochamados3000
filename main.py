import logging
from tela import iniciar_tela
from gerador_planilha import gerar_csv
from chamados import abrir_chamados

logging.basicConfig(
    filename='automacao.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S'
)

iniciar_tela(gerar_csv, abrir_chamados)