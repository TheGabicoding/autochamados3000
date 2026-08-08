import logging
import os
from logging.handlers import RotatingFileHandler

from config import obter_pasta_logs
from tela import iniciar_tela
from gerador_planilha import gerar_csv
from chamados import abrir_chamados

caminho_log = os.path.join(obter_pasta_logs(), "automacao.log")

# RotatingFileHandler em vez de filemode='w': mantém um histórico (últimos
# arquivos .log.1, .log.2...) em vez de apagar tudo a cada execução, o que
# ajuda muito quando o usuário só percebe um problema dias depois.
handler = RotatingFileHandler(caminho_log, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", datefmt="%d/%m/%Y %H:%M:%S"))

logging.basicConfig(level=logging.INFO, handlers=[handler])

if __name__ == "__main__":
    iniciar_tela(gerar_csv, abrir_chamados)