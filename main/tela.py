import tkinter as tk
from tkinter import messagebox, ttk
import os
import sys
import logging
import queue
import threading

from config import obter_pasta_logs

TEXTO_AJUDA = (
    "Instruções:\n\n"
    "Para gerar CSV:\n"
    "Cole no formato:\n"
    "MARCA\n"
    "1-SERIE\n"
    "2-SERIE\n\n"
    "Para abrir chamados:\n"
    "Cole as colunas direto da planilha (Produto e Série, separadas por TAB).\n\n"
    "Um navegador Chrome vai abrir - faça login manualmente no Gerbit quando solicitado.\n"
    "Evite efetuar cliques no navegador enquanto os chamados estão sendo abertos."
)


def iniciar_tela(funcao_csv, funcao_chamado):
    janela = tk.Tk()
    janela.title("Autochamados3000")
    janela.geometry("620x700")

    texto_para_area_transferencia = tk.StringVar(value="")
    botoes = []

    def mostrar_ajuda():
        messagebox.showinfo("Ajuda", TEXTO_AJUDA)

    def definir_botoes_ativos(ativo):
        estado = tk.NORMAL if ativo else tk.DISABLED
        for botao in botoes:
            botao.config(state=estado)

    # --- Topo ---
    frame_topo = tk.Frame(janela)
    frame_topo.pack(pady=10)

    tk.Label(frame_topo, text="Selecione o tipo:").pack(side=tk.LEFT, padx=5)
    botao_ajuda = tk.Button(frame_topo, text="?", command=mostrar_ajuda, width=2)
    botao_ajuda.pack(side=tk.LEFT)

    variavel_opcao = tk.StringVar(janela, value="Fonte")

    frame_opcoes = tk.Frame(janela)
    frame_opcoes.pack()
    for texto, valor in [("Estabilizador", "Estabilizador"), ("Monitor", "Monitor"), ("Fonte", "Fonte")]:
        tk.Radiobutton(frame_opcoes, text=texto, variable=variavel_opcao, value=valor).pack(side=tk.LEFT, padx=8)

    tk.Label(janela, text="Cole o texto aqui:").pack(pady=(15, 5))

    caixa_texto = tk.Text(janela, height=15, width=68)
    caixa_texto.pack()

    # --- Progresso ---
    frame_progresso = tk.Frame(janela)
    barra_progresso = ttk.Progressbar(frame_progresso, orient="horizontal", length=560, mode="determinate")
    barra_progresso.pack()

    rotulo_aviso = tk.Label(janela, text="", wraplength=580, justify=tk.LEFT)

    def obter_texto_entrada():
        return caixa_texto.get("1.0", tk.END).strip()

    # --- Ação: Gerar CSV ---
    def ao_clicar_csv():
        texto = obter_texto_entrada()
        if not texto:
            messagebox.showwarning("Aviso", "Cole os dados na caixa de texto antes de gerar o CSV.")
            return

        opcao = variavel_opcao.get()
        mensagem, texto_copiado = funcao_csv(texto, opcao)
        texto_para_area_transferencia.set(texto_copiado)

        if texto_copiado:
            caixa_texto.delete("1.0", tk.END)

        rotulo_aviso.config(text=mensagem)
        messagebox.showinfo("Processo Concluído", mensagem)

    # --- Ação: Copiar planilha ---
    def copiar_planilha():
        texto = texto_para_area_transferencia.get()
        if not texto:
            logging.error("Processo: Copiando planilha | Status: Falhou (nada tratado ainda)")
            messagebox.showerror("Erro", "Nenhum dado tratado para copiar. Gere o CSV primeiro.")
            return
        janela.clipboard_clear()
        janela.clipboard_append(texto)
        janela.update()
        logging.info("Processo: Copiando planilha | Status: Bem-sucedido")
        messagebox.showinfo("Copiado", "Dados copiados para a área de transferência!")

    # --- Ação: Abrir chamados (roda em thread separada para não travar a UI) ---
    def ao_clicar_chamado():
        texto = obter_texto_entrada()
        if not texto:
            messagebox.showwarning("Aviso", "Cole os dados (produto e série) antes de abrir os chamados.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "Um navegador Chrome vai abrir e você precisará fazer login manualmente no Gerbit.\n\n"
            "Depois de logado, o processo continua sozinho. Deseja continuar?"
        )
        if not confirmar:
            return

        opcao = variavel_opcao.get()

        definir_botoes_ativos(False)
        frame_progresso.pack(pady=(5, 0))
        barra_progresso["value"] = 0
        rotulo_aviso.config(text="Abrindo navegador... faça login quando a página carregar.")
        rotulo_aviso.pack(pady=5)

        fila = queue.Queue()

        def callback_progresso(indice, total, produto, sucesso):
            fila.put(("progresso", indice, total, produto, sucesso))

        def worker():
            mensagem = funcao_chamado(texto, opcao, callback_progresso)
            fila.put(("fim", mensagem))

        threading.Thread(target=worker, daemon=True).start()

        def processar_fila():
            try:
                while True:
                    item = fila.get_nowait()
                    if item[0] == "fim":
                        _, mensagem = item
                        definir_botoes_ativos(True)
                        frame_progresso.pack_forget()
                        rotulo_aviso.config(text=mensagem)
                        messagebox.showinfo("Processo Concluído", mensagem)
                        return
                    else:
                        _, indice, total, produto, sucesso = item
                        barra_progresso["maximum"] = total
                        barra_progresso["value"] = indice + (0 if sucesso is None else 1)
                        rotulo_aviso.config(text=f"Processando {indice + 1}/{total}: {produto}")
            except queue.Empty:
                pass
            janela.after(150, processar_fila)

        processar_fila()

    # --- Ação: Abrir log ---
    def abrir_log():
        caminho_log = os.path.join(obter_pasta_logs(), "automacao.log")
        try:
            os.startfile(caminho_log)
        except Exception:
            messagebox.showerror("Erro", "O arquivo automacao.log ainda não existe.")

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=15)

    botao_csv = tk.Button(frame_botoes, text="Gerar CSV", command=ao_clicar_csv, width=14)
    botao_csv.pack(side=tk.LEFT, padx=8)

    botao_copiar = tk.Button(frame_botoes, text="Copiar Planilha", command=copiar_planilha, width=14)
    botao_copiar.pack(side=tk.LEFT, padx=8)

    botao_chamado = tk.Button(frame_botoes, text="Abrir Chamados", command=ao_clicar_chamado, width=14)
    botao_chamado.pack(side=tk.LEFT, padx=8)

    botao_log = tk.Button(frame_botoes, text="Abrir Logs", command=abrir_log, width=12)
    botao_log.pack(side=tk.LEFT, padx=8)

    botoes.extend([botao_csv, botao_copiar, botao_chamado, botao_log])

    rotulo_aviso.pack(pady=5)

    janela.mainloop()