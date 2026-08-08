import logging
import os
from tela import iniciar_tela
from gerador_planilha import gerar_csv
from chamados import abrir_chamados

pasta_atual = os.path.dirname(os.path.abspath(__file__))
pasta_raiz = os.path.dirname(pasta_atual)
pasta_logs = os.path.join(pasta_raiz, 'logs')

if not os.path.exists(pasta_logs):
    os.makedirs(pasta_logs)

caminho_log = os.path.join(pasta_logs, 'automacao.log')

logging.basicConfig(
    filename=caminho_log,
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S'
)

iniciar_tela(gerar_csv, abrir_chamados)