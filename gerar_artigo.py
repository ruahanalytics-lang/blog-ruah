from openai import OpenAI
import os
import json
import re
import math
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# KEYWORDS — adicione/remova à vontade
# ---------------------------------------------------------------------------
KEYWORDS = [
    "como automatizar o WhatsApp da sua empresa com n8n",
    "como criar um dashboard de vendas no Power BI do zero",
    "automação de planilhas Excel com Python para pequenas empresas",
    "como integrar o Google Sheets com outros sistemas automaticamente",
    "o que é n8n e como usar para automatizar processos",
    "como montar um relatório automático de vendas no Power BI",
    "automação de e-mail marketing com n8n passo a passo",
    "como conectar seu ERP ao Power BI para relatórios em tempo real",
    "ferramentas gratuitas de automação para MEI e pequenas empresas",
    "como criar alertas automáticos de estoque com n8n",
    "dashboard financeiro no Power BI para pequenas empresas",
    "como automatizar relatórios mensais e economizar horas de trabalho",
    "n8n vs Zapier vs Make qual a melhor ferramenta de automação",
    "como usar Python para analisar dados de vendas",
    "automação de processos financeiros para contadores e escritórios",
    "como criar um CRM simples com automação no n8n",
    "Power BI para clínicas médicas como monitorar indicadores",
    "como automatizar o envio de boletos e cobranças com n8n",
    "Business Intelligence para e-commerce indicadores essenciais",
    "como reduzir trabalho manual com automações simples no seu negócio",
]

AFILIADOS = {
    "n8n": "https://n8n.io/?via=ruahanalytics",
    "Make": "https://www.make.com/en/register?pc=ruahanalytics",
    "Power BI": "https://www.microsoft.com/pt-br/power-platform/products/power-bi",
    "Hostinger": "https://www.hostinger.com.br/",
}


def slug_from_title(titulo: str) -> str:
    s = titulo.lower()
    s = re.sub(r"[áàãâä]", "a", s)
    s = re.sub(r"[éèêë]", "e", s)
    s = re.sub(r"[íìîï]", "i", s)
    s = re.sub(r"[óòõôö]", "o", s)
    s = re.sub(r"[úùûü]", "u", s)
    s = re.sub(r"[ç]", "c", s)
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    return s[:80]


def tempo_leitura(texto: str) -> int:
    palavras = len(texto.split())
    return max(1, math.ceil(palavras / 200))


def proxima_keyword() -> str:
    log_path = Path("artigos_gerados.json")
    gerados = json.loads(log_path.read_text(encoding="utf-8")) if log_path.exists() else []
    usadas = {a["keyword"] for a in gerados}
    for kw in KEYWORDS:
        if kw not in usadas:
            return kw
    # Todas usadas — recomeça do início
    return KEYWORDS[len(gerados) % len(KEYWORDS)]


def gerar_artigo(keyword: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""Você é um redator especialista em automação de processos e Business Intelligence para empresas brasileiras.

Escreva um artigo de blog completo em português do Brasil sobre o tema: "{keyword}"

REQUISITOS:
- 1.500 a 2.000 palavras
- Linguagem clara, prática e profissional (tom: consultor experiente falando com dono de PME)
- Estrutura: introdução envolvente + subtítulos H2 e H3 + exemplos reais + conclusão
- Mencione naturalmente pelo menos UMA das ferramentas a seguir com seus links de afiliado:
  * n8n: {AFILIADOS['n8n']}
  * Make: {AFILIADOS['Make']}
  * Power BI: {AFILIADOS['Power BI']}
- NÃO mencione concorrentes diretos ou ferramentas pagas sem afiliado
- Termine com um parágrafo de conclusão motivador (NÃO inclua CTA — será adicionado automaticamente)

Retorne APENAS um JSON válido com esta estrutura (sem markdown, sem texto fora do JSON):
{{
  "titulo": "título SEO otimizado do artigo",
  "meta_description": "descrição de até 155 caracteres para o Google",
  "categoria": "uma categoria: Automação | Power BI | n8n | Python | BI",
  "conteudo_html": "todo o corpo do artigo em HTML semântico (use <h2>, <h3>, <p>, <ul>, <li>, <strong>, <a href=...>)"
}}"""

    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content.strip()
    return json.loads(raw)


def renderizar_html(artigo: dict, keyword: str) -> str:
    template = Path("template.html").read_text(encoding="utf-8")
    slug = slug_from_title(artigo["titulo"])
    data = datetime.now().strftime("%d/%m/%Y")
    minutos = tempo_leitura(artigo["conteudo_html"])

    html = template
    html = html.replace("{{titulo}}", artigo["titulo"])
    html = html.replace("{{meta_description}}", artigo["meta_description"])
    html = html.replace("{{slug}}", slug)
    html = html.replace("{{categoria}}", artigo["categoria"])
    html = html.replace("{{data_publicacao}}", data)
    html = html.replace("{{tempo_leitura}}", str(minutos))
    html = html.replace("{{conteudo}}", artigo["conteudo_html"])
    return html, slug


def atualizar_index(artigo: dict, slug: str):
    index_path = Path("index.html")
    index_html = index_path.read_text(encoding="utf-8")

    data = datetime.now().strftime("%d/%m/%Y")
    card = f"""
    <a href="artigos/{slug}.html" class="card">
      <div class="card-cat">{artigo['categoria']}</div>
      <h2>{artigo['titulo']}</h2>
      <p>{artigo['meta_description']}</p>
      <div class="card-meta">{data}</div>
      <span class="card-arrow">&#8594;</span>
    </a>"""

    index_html = index_html.replace(
        "<!-- ARTIGOS_PLACEHOLDER -->",
        card + "\n    <!-- ARTIGOS_PLACEHOLDER -->"
    )
    index_path.write_text(index_html, encoding="utf-8")


def registrar_artigo(keyword: str, titulo: str, slug: str):
    log_path = Path("artigos_gerados.json")
    gerados = json.loads(log_path.read_text(encoding="utf-8")) if log_path.exists() else []
    gerados.append({
        "keyword": keyword,
        "titulo": titulo,
        "slug": slug,
        "data": datetime.now().isoformat(),
    })
    log_path.write_text(json.dumps(gerados, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    keyword = proxima_keyword()
    print(f"[+] Gerando artigo: {keyword}")

    artigo = gerar_artigo(keyword)
    print(f"[+] Artigo gerado: {artigo['titulo']}")

    html, slug = renderizar_html(artigo, keyword)

    artigo_path = Path("artigos") / f"{slug}.html"
    artigo_path.write_text(html, encoding="utf-8")
    print(f"[+] Salvo em: {artigo_path}")

    atualizar_index(artigo, slug)
    print("[+] Index atualizado")

    registrar_artigo(keyword, artigo["titulo"], slug)
    print("[+] Log atualizado")
    print(f"\n[OK] Artigo publicado: artigos/{slug}.html")


if __name__ == "__main__":
    main()
