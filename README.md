# Monitoramento de Notícias (Google Alerts + IA Local)

Este projeto coleta notícias automaticamente a partir do Google Alerts (RSS), extrai o conteúdo, analisa com uma IA local e gera um relatório profissional em PDF.

---

# Funcionalidades

- Coleta automática de notícias via RSS (Google Alerts)
- Limpeza de links do Google
- Extração de conteúdo das páginas
- Análise automática com IA local (Ollama)
- Classificação de risco (Baixo, Médio, Alto)
- Exportação em PDF formatado

---

# Tecnologias utilizadas

- Python 3.14.4
  ## Bibliotecas
- feedparser
- requests
- beautifulsoup4
- reportlab
  ## IA 
- Ollama (IA local)

---

# Instalar IA local (Ollama)

## 1. Baixar o Ollama

Acesse:
https://ollama.com/download

Instale normalmente.

---

## 2. Baixar o modelo de IA

No terminal:

```bash
ollama run phi3
```
Isso vai baixar o modelo (~3.7GB)

---

# Instalar dependências Python

```bash
pip install feedparser requests beautifulsoup4 reportlab
```
Caso der Erro:
```bash
python -m pip install feedparser requests beautifulsoup4 reportlab
```
# Configurar RSS do Google Alerts
- Acesse: https://www.google.com/alerts
- Crie um alerta normal
### exemplo:
```bash
(Emprego OR Desemprego OR Trabalho OR "Mercado de Trabalho" OR Jovem OR "Jovem Aprendiz" OR Juventude OR "Primeiro Emprego" OR Estágio OR Vagas OR Contratação OR Sine) (Acre OR "Rio Branco")
```
- Copie o link RSS e cole no código
```python
#Cole o link dentro dessa variável
RSS_URL = "https://www.google.com.br/alerts/feeds/xxxxxxxx/xxxxxxxxxx"
```

# Como rodar o projeto:
```bash
python main.py
```
- O PDF é gerado e enviado para a pasta do projeto
