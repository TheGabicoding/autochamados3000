# 🤖 Autochamados3000

Automação inteligente para alimentar planilhas de patrimônio e abrir chamados no sistema Gerbit de forma rápida e prática.

---

## 📋 O que é?

O **Autochamados3000** é um programa que automatiza dois processos principais:

1. **Gerar Planilhas (CSV)** - Organiza dados de equipamentos (marca, série, data) em planilhas prontas para usar
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
3. Clique em **"Gerar CSV"**
4. Clique em **"Copiar Planilha"**
5. O arquivo será salvo na pasta **`planilhas`** e os dados copiar para cola

#### **Para Abrir Chamados:**
1. Selecione o tipo de equipamento
2. Cole os dados das colunas da sua planilha (Produto e Série)
3. Clique em **"Abrir Chamados"**
4. Faça login no site da Gerbit, com usuário e senha
5. Aguarde e os chamados serão abertos automaticamente

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
│   └── gerador_planilha.py
├── planilhas/  (criada automaticamente)
├── logs/  (criada automaticamente)
└── README.md
```

---

## 📝 Saiba Mais

- **Logs:** Todo processo é registrado em `logs/automacao.log`
- **Planilhas geradas:** Ficam salvas em `planilhas/`
- **Dúvidas?** Clique no botão **"?"** dentro do programa para ver instruções

---

## ⚠️ Requisitos

- Windows 7 ou superior
- Navegador Chrome instalado
- Acesso ao site Gerbit

---

**Desenvolvido por TheGabicoding** 🚀
