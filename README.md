# 🤖 Autochamados3000

Automação inteligente para alimentar planilhas de patrimônio e abrir chamados no sistema Gerbit de forma rápida e prática.

---

## 📋 O que é?

O **Autochamados3000** é um programa que automatiza dois processos principais:

1. **Gerar Planilhas (CSV)** - Organiza dados de equipamentos (marca, série, data) em planilhas prontas para copiar e colar na planilha oficial (Drive)
2. **Abrir Chamados Automáticos** - Acessa o site Gerbit e abre chamados de manutenção sem você digitar tudo manualmente

Economiza tempo e reduz erros na entrada de dados! 💪

---

## 🔧 Bibliotecas Python Utilizadas

| Biblioteca | Função |
|-----------|--------|
| **tkinter** | Cria a interface gráfica (janelas e botões) |
| **selenium** | Controla o navegador para abrir chamados automaticamente |
| **csv** | Lê e escreve arquivos de planilhas |
| **logging** | Registra logs de cada processo para debug |
| **threading** | Roda a automação em segundo plano, sem travar a janela |
| **datetime** | Adiciona data/hora aos registros |
| **os** | Gerencia pastas e caminhos de arquivos |

---

## 💻 Como Usar

### 1️⃣ Download do Executável

1. Acesse a pasta **`main`** deste repositório
2. Abra a subpasta **`dist`**
3. Procure pelo arquivo `autochamados.exe`
4. Baixe o arquivo clicando nele e depois em "Download"

### 2️⃣ Executar o Programa

- Clique duas vezes no executável para iniciar
- Uma janela deve aparecer com as opções

### 3️⃣ Usando o Programa

#### **Para Gerar Planilhas:**
1. Selecione o tipo de equipamento: `Estabilizador`, `Monitor` ou `Fonte`
2. Cole os dados no formato:
   ```
   MARCA
   1-SERIE
   2-SERIE
   ```
3. Clique em **"Gerar CSV"** — os itens são adicionados com status `ABRIR CHAMADO` ao arquivo CSV correspondente (se o arquivo já existir, os novos itens são **acrescentados** ao final, nada é apagado)
4. Clique em **"Copiar Planilha"**
5. Cole os dados na sua planilha oficial (Drive). O arquivo CSV local em **`planilhas`** é só um rascunho de apoio, não é a fonte da verdade

#### **Para Abrir Chamados:**
1. Selecione o tipo de equipamento
2. Cole os dados das colunas da sua planilha (Produto e Série, separados por TAB)
3. Clique em **"Abrir Chamados"** e confirme a mensagem de aviso
4. Um navegador Chrome vai abrir — faça login no site da Gerbit, com usuário e senha
5. Depois de logado, **não é preciso fazer mais nada**: aguarde o programa preencher e criar os chamados automaticamente
6. Ao final, uma mensagem mostra quantos chamados foram abertos com sucesso (ex.: "8 de 10 chamados abertos com sucesso")

> ⚠️ Enquanto os chamados estão sendo abertos, **não clique, digite nem role dentro da janela do Chrome** que o programa abriu — isso pode atrapalhar o preenchimento. Fora essa janela, você pode usar o resto do computador normalmente: a interface do próprio Autochamados3000 continua respondendo (não trava mais) e dá pra minimizar ou usar outros programas sem problema.

---

## 🆕 Mudanças desta versão

- **A interface não trava mais.** A abertura de chamados agora roda em segundo plano (thread separada), então a janela do programa continua respondendo o tempo todo — inclusive dá pra abri-la e ver o andamento enquanto o processo acontece.
- **Barra de progresso.** Mostra em tempo real qual item está sendo processado (ex.: "Processando 3/12: APC 300W"), em vez de uma mensagem estática.
- **Resumo no final.** Em vez de só "Processo finalizado", agora aparece quantos chamados deram certo e quantos falharam.
- **Confirmação antes de abrir o navegador**, já que o processo agora espera até 3 minutos pelo seu login (antes era um tempo fixo de 12 segundos, que falhava se o login demorasse mais que isso).
- **Botões ficam desabilitados durante o processamento**, evitando cliques duplicados.
- **Validação de campos vazios** antes de gerar CSV ou abrir chamados.
- **Geração de CSV mais robusta:** números de série com hífen não são mais cortados por engano, e linhas que não puderem ser reconhecidas são avisadas na tela em vez de simplesmente desaparecerem.
- **Não sobrescreve mais o arquivo CSV** ao gerar novamente — os novos itens são acrescentados ao que já existia.
- **Logs mais detalhados**, com a mensagem de erro real quando algo falha (antes só dizia "Falhou", sem dizer o motivo) — e agora com rotação automática, mantendo um histórico dos últimos logs em vez de apagar tudo a cada execução.
- **Configuração centralizada** (`config.py`): todo o comportamento específico de cada tipo de equipamento (Estabilizador/Fonte/Monitor) ficou em um único lugar.

---

## 📁 Estrutura de Pastas

```
autochamados3000/
├── main/
│   ├── dist/
│   │   └── autochamados3000.exe  ← BAIXE DAQUI!
│   ├── main.py
│   ├── tela.py
│   ├── chamados.py
│   ├── gerador_planilha.py
│   └── config.py
├── planilhas/  (criada automaticamente, apenas rascunho)
├── logs/  (criada automaticamente)
└── README.md
```

---

## 📝 Saiba Mais

- **Logs:** Todo processo é registrado em `logs/automacao.log`
- **Planilhas geradas:** Ficam salvas em `planilhas/`, servem apenas para copiar e colar na planilha oficial (Drive) — não são atualizadas depois que os chamados são abertos
- **Dúvidas?** Clique no botão **"?"** dentro do programa para ver instruções

---

## ⚠️ Requisitos

- Windows 7 ou superior
- Navegador Chrome instalado
- Acesso ao site Gerbit

---

**Desenvolvido por TheGabicoding** 🚀