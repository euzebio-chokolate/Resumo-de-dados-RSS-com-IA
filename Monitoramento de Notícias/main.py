import feedparser
import requests
from bs4 import BeautifulSoup
import urllib.parse

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


#Cole o link dentro dessa variável
RSS_URL = "https://www.google.com.br/alerts/feeds/xxxxxxxx/xxxxxxxxxx"


def limpar_link(url):

    if "google.com/url" in url:

        parsed = urllib.parse.urlparse(url)
        query = urllib.parse.parse_qs(parsed.query)

        if "url" in query:
            return query["url"][0]

    return url


def limpar_html(texto):

    return BeautifulSoup(texto, "html.parser").get_text()


def pegar_links():

    feed = feedparser.parse(RSS_URL)

    noticias = []

    for entry in feed.entries:

        titulo_limpo = limpar_html(entry.title)

        noticias.append({
            "titulo": titulo_limpo,
            "link": entry.link,
            "data": entry.published if "published" in entry else "não consta"
        })

    return noticias


def extrair_texto(url):

    try:

        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")

        texto = ""

        for p in soup.find_all("p"):
            texto += p.get_text() + "\n"

        return texto

    except Exception as e:
        print("Erro ao baixar:", e)
        return ""


def analisar_noticia(titulo, texto):

    prompt = f"""
Você é um Analista de Monitoramento de Mídia.

Analise a notícia abaixo e retorne EXATAMENTE neste formato:

Tema:
Resumo:
Risco: (Baixo, Médio ou Alto)
Ação:

Considere risco alto se houver:
denúncia, morte, negligência, investigação, polícia, MP, protesto.

Título: {titulo}

Texto:
{texto[:1000]}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


def gerar_painel(analises):

    texto = "\n".join(analises)

    prompt = f"""
Com base nas análises abaixo, gere:

1) Volume total de notícias
2) Principais temas
3) Quantidade de riscos altos
4) 3 pontos de atenção

{texto}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


def gerar_pdf(painel, tabela):

    doc = SimpleDocTemplate("relatorio_profissional.pdf")

    styles = getSampleStyleSheet()

    elementos = []

    #Título
    elementos.append(Paragraph("RELATÓRIO DE MONITORAMENTO DE MÍDIA", styles["Title"]))
    elementos.append(Spacer(1, 20))

    elementos.append(Paragraph("PAINEL EXECUTIVO", styles["Heading2"]))
    elementos.append(Spacer(1, 10))

    for linha in painel.split("\n"):
        elementos.append(Paragraph(linha, styles["Normal"]))

    elementos.append(Spacer(1, 20))

    elementos.append(Paragraph("TABELA DE INCIDENTES", styles["Heading2"]))
    elementos.append(Spacer(1, 10))

    for item in tabela:

        elementos.append(Paragraph(f"<b>Data:</b> {item['data']}", styles["Normal"]))
        elementos.append(Paragraph(f"<b>Título:</b> {item['titulo']}", styles["Normal"]))
        elementos.append(Paragraph(f"<b>Link:</b> {item['link']}", styles["Normal"]))

        for linha in item["analise"].split("\n"):
            elementos.append(Paragraph(linha, styles["Normal"]))

        elementos.append(Spacer(1, 15))

    doc.build(elementos)


def main():

    noticias = pegar_links()

    analises = []
    tabela = []

    for n in noticias[:5]:

        print("\nProcessando:", n["titulo"])

        link_limpo = limpar_link(n["link"])

        print("Link real:", link_limpo)

        texto = extrair_texto(link_limpo)

        print("Tamanho texto:", len(texto))

        if len(texto) < 200:
            print("Ignorado (texto muito pequeno)\n")
            continue

        print("Gerando análise...\n")

        analise = analisar_noticia(n["titulo"], texto)

        analises.append(analise)

        tabela.append({
            "data": n["data"],
            "titulo": n["titulo"],
            "link": link_limpo,
            "analise": analise
        })

    if not analises:
        print("Nenhuma notícia válida encontrada")
        return

    print("Gerando painel executivo...\n")

    painel = gerar_painel(analises)

    #Gerar PDF
    gerar_pdf(painel, tabela)

    print("\nPDF gerado: relatorio_profissional.pdf")


if __name__ == "__main__":
    main()