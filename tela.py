import tkinter as tk
from tkinter import messagebox

def iniciar_tela(funcao_comando):
    janela = tk.Tk()
    janela.title("Gerador de Planilhas CSV")
    janela.geometry("500x550")

    def mostrar_ajuda():
        texto_ajuda = "Instrucoes:\n\n"
        texto_ajuda += "1. Selecione o tipo de equipamento (Estabilizador, Monitor ou Fonte).\n"
        texto_ajuda += "2. Cole o texto copiado na caixa em branco.\n"
        texto_ajuda += "3. Clique em 'Gerar CSV'.\n\n"
        texto_ajuda += "O texto deve seguir este padrao:\n\n"
        texto_ajuda += "MARCA E MODELO\n"
        texto_ajuda += "1- NUMERO_DE_SERIE\n"
        texto_ajuda += "2- NUMERO_DE_SERIE\n\n"
        texto_ajuda += "Exemplo pratico:\n"
        texto_ajuda += "KRONNUS 200W\n"
        texto_ajuda += "1- 718211\n"
        texto_ajuda += "2- 752550\n"
        texto_ajuda += "COMTAC 250W\n"
        texto_ajuda += "1- N0091210x5867"
        
        messagebox.showinfo("Ajuda - Como usar", texto_ajuda)

    frame_topo = tk.Frame(janela)
    frame_topo.pack(pady=10)

    rotulo_opcao = tk.Label(frame_topo, text="O que voce quer cadastrar?")
    rotulo_opcao.pack(side=tk.LEFT, padx=5)

    botao_ajuda = tk.Button(frame_topo, text="Ajuda", command=mostrar_ajuda)
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

    caixa_texto = tk.Text(janela, height=15, width=50)
    caixa_texto.pack()

    def ao_clicar():
        texto = caixa_texto.get("1.0", tk.END)
        opcao = variavel_opcao.get()
        mensagem = funcao_comando(texto, opcao)
        rotulo_aviso.config(text=mensagem)

    botao = tk.Button(janela, text="Gerar CSV", command=ao_clicar)
    botao.pack(pady=10)

    rotulo_aviso = tk.Label(janela, text="")
    rotulo_aviso.pack(pady=5)

    janela.mainloop()