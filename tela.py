import tkinter as tk
from tkinter import messagebox
import os

def iniciar_tela(funcao_csv, funcao_chamado):
    janela = tk.Tk()
    janela.title("Automação")
    janela.geometry("600x650")

    def mostrar_ajuda():
        texto_ajuda = "Instrucoes:\n\n"
        texto_ajuda += "Para CSV: Cole no formato MARCA e MODELO, e depois 1- SERIE.\n\n"
        texto_ajuda += "Para Chamados: Cole as colunas direto da planilha (Produto e Serie).\n"
        messagebox.showinfo("Ajuda", texto_ajuda)

    frame_topo = tk.Frame(janela)
    frame_topo.pack(pady=10)

    rotulo_opcao = tk.Label(frame_topo, text="Selecione o tipo:")
    rotulo_opcao.pack(side=tk.LEFT, padx=5)

    botao_ajuda = tk.Button(frame_topo, text="?", command=mostrar_ajuda)
    botao_ajuda.pack(side=tk.LEFT)

    variavel_opcao = tk.StringVar(janela)
    variavel_opcao.set("Fonte")

    radio1 = tk.Radiobutton(janela, text="Estabilizador", variable=variavel_opcao, value="Estabilizador")
    radio1.pack()

    radio2 = tk.Radiobutton(janela, text="Monitor", variable=variavel_opcao, value="Monitor")
    radio2.pack()

    radio3 = tk.Radiobutton(janela, text="Fonte", variable=variavel_opcao, value="Fonte")
    radio3.pack()

    rotulo_texto = tk.Label(janela, text="Cole o texto aqui:")
    rotulo_texto.pack(pady=5)

    caixa_texto = tk.Text(janela, height=15, width=60)
    caixa_texto.pack()

    def ao_clicar_csv():
        texto = caixa_texto.get("1.0", tk.END)
        opcao = variavel_opcao.get()
        mensagem = funcao_csv(texto, opcao)
        rotulo_aviso.config(text=mensagem)
        messagebox.showinfo("Processo Concluido", mensagem)
        
    def ao_clicar_chamado():
        texto = caixa_texto.get("1.0", tk.END)
        opcao = variavel_opcao.get()
        rotulo_aviso.config(text="Abrindo chamados... Nao mexa no mouse.")
        janela.update()
        mensagem = funcao_chamado(texto, opcao)
        rotulo_aviso.config(text=mensagem)
        messagebox.showinfo("Processo Concluido", mensagem)

    def abrir_log():
        try:
            os.startfile("automacao.log")
        except Exception:
            messagebox.showerror("Erro", "O arquivo automacao.log ainda nao existe.")

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    botao_csv = tk.Button(frame_botoes, text="Gerar CSV", command=ao_clicar_csv)
    botao_csv.pack(side=tk.LEFT, padx=10)

    botao_chamado = tk.Button(frame_botoes, text="Abrir Chamados no Site", command=ao_clicar_chamado)
    botao_chamado.pack(side=tk.LEFT, padx=10)

    botao_log = tk.Button(frame_botoes, text="Abrir Logs", command=abrir_log)
    botao_log.pack(side=tk.LEFT, padx=10)

    rotulo_aviso = tk.Label(janela, text="")
    rotulo_aviso.pack(pady=5)

    janela.mainloop()