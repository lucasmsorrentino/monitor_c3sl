# 🕵️ Monitor C3SL - Intelligent Web Scraper

Um robô em Python que monitora atualizações no site do [C3SL (Centro de Computação Científica e Software Livre)](https://www.c3sl.ufpr.br/). 

Este projeto utiliza **Hashing (MD5)** para detectar alterações no *conteúdo interno* das páginas e as notificações são enviadas instantaneamente via **Telegram**.

## 🚀 Funcionalidades

- **Monitoramento Profundo (Deep Scan):** Entra em cada link, extrai o texto e compara com a versão anterior.
- **Detecção de Mudanças:** Identifica novos posts E edições em posts antigos.
- **Arquitetura Modular:** Código separado em camadas (Database, Scraper, Automation, Notifications).
- **Persistência de Dados:** Usa SQLite para manter histórico entre execuções.
- **Notificações em Tempo Real:** Integração com a API do Bot do Telegram.
- **Resiliência:** Tratamento de erros de conexão e verificação agendada.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.12+
- **Raspagem:** `requests`, `beautifulsoup4`
- **Agendamento:** `schedule`
- **Banco de Dados:** `sqlite3` (Nativo)
- **Variáveis de Ambiente:** `python-dotenv`

## 📂 Estrutura do Projeto

```text
monitor_c3sl/
│
├── database/               # Módulo de Persistência
│   ├── __init__.py         # (Arquivo vazio, indica que é um pacote Python)
│   └── manager.py          # Classe que gerencia o SQLite
│
├── scraper/                # Módulo de Raspagem
│   ├── __init__.py         # (Arquivo vazio)
│   └── c3sl.py             # Classe que acessa o site
│
├── automation/             # Módulo de Automação
│   ├── __init__.py         # (Arquivo vazio)
│   └── scheduler.py        # Classe que gerencia o agendamento
│
├── data/                   # Pasta para guardar o arquivo do banco de dados
│   └── .gitkeep            # (Opcional, só para garantir que a pasta exista)
│
├── notifications/
│   └── telegram_sender.py
│
├── main.py                 # Ponto de entrada (executa o programa)
├── .env                    # variáveis do ambiente
├── LICENSE                 # Licença de uso
├── .gitignore              
└── requirements.txt        # Lista de bibliotecas necessárias
```

## ▶️ Como Usar (Instalação e Configuração)

Siga estes passos para rodar o projeto na sua máquina local:

### 1. Preparação do Ambiente
Certifique-se de ter o Python instalado. Clone o repositório e entre na pasta:

```bash
git clone https://github.com/lucasmsorrentino/monitor_c3sl.git
cd monitor_c3sl
```

### 2. Criar e Ativar o Ambiente Virtual
É recomendado usar um ambiente virtual para não misturar dependências.

**No Windows (Git Bash/PowerShell):**
```bash
python -m venv .venv
source .venv/Scripts/activate
```

**No Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as Dependências
Com o ambiente ativado, instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

### 4. Configuração das Variáveis de Ambiente (Segurança)
O projeto não funciona sem as credenciais do Telegram. 

1. Crie um arquivo chamado `.env` na raiz do projeto (mesmo local do `main.py`).
2. Adicione o seguinte conteúdo, substituindo pelos seus dados:

```ini
TELEGRAM_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
TELEGRAM_CHAT_ID=987654321
```

> **Como conseguir:**
> * **Token:** Fale com o `@BotFather` no Telegram e crie um novo bot.
> * **Chat ID:** Fale com o `@userinfobot` no Telegram.

### 5. Executar o Monitor
Agora basta rodar o script principal:

```bash
python main.py
```

O bot iniciará o agendamento.
- Por padrão, ele verifica atualizações duas vezes por dia.
- Para testes, você pode alterar o intervalo no arquivo `automation/scheduler.py`.

## 🤝 Contribuição

Sinta-se à vontade para abrir Issues ou enviar Pull Requests. Sugestões de melhoria na lógica de raspagem ou novos canais de notificação (Discord, Slack) são bem-vindas!

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
