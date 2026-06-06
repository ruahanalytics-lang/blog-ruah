import json
from datetime import datetime
from pathlib import Path


def gerar_sitemap():
    log_path = Path("artigos_gerados.json")
    gerados = json.loads(log_path.read_text(encoding="utf-8")) if log_path.exists() else []

    base = "https://blog.ruahanalytics.com"
    hoje = datetime.now().strftime("%Y-%m-%d")

    urls = [f"""  <url>
    <loc>{base}/</loc>
    <lastmod>{hoje}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>"""]

    for artigo in gerados:
        slug = artigo.get("slug", "")
        data = artigo.get("data", hoje)[:10]
        if slug:
            urls.append(f"""  <url>
    <loc>{base}/artigos/{slug}.html</loc>
    <lastmod>{data}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>""")

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""

    Path("sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"[OK] Sitemap gerado com {len(gerados) + 1} URLs")


if __name__ == "__main__":
    gerar_sitemap()
