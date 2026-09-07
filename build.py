#!/usr/bin/env python3
"""
Генератор статического блога Гидро-С.

Вход:  content/*.md  (YAML-фронтматтер + markdown-тело), data/site.yml, templates/, assets/
Выход: docs/  (то, что раздаёт GitHub Pages)

Запуск:  python build.py
"""
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
TPL = ROOT / "templates"
OUT = ROOT / "docs"
ASSETS = ROOT / "assets"

RELATED_MAX = 6
DESC_LEN = 155

_TRANSLIT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e",
    "ж": "zh", "з": "z", "и": "i", "й": "j", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "h", "ц": "c", "ч": "ch", "ш": "sh", "щ": "sch",
    "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
}


def slugify(text):
    """Кириллица -> латинский слаг. Никакой кириллицы на выходе."""
    out = []
    for ch in (text or "").lower().strip():
        if ch in _TRANSLIT:
            out.append(_TRANSLIT[ch])
        elif ch.isalnum() and ch.isascii():
            out.append(ch)
        elif ch in " -_/":
            out.append("-")
    s = re.sub(r"-+", "-", "".join(out)).strip("-")
    return s


def load_site():
    return yaml.safe_load((ROOT / "data" / "site.yml").read_text(encoding="utf-8"))


def split_frontmatter(text):
    """Вернуть (dict метаданных, str тело)."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm = yaml.safe_load(text[3:end]) or {}
            body = text[end + 4:].lstrip("\n")
            return fm, body
    return {}, text


def strip_html(s):
    return re.sub(r"<[^>]+>", "", s)


def make_description(meta, html):
    if meta.get("description"):
        return meta["description"].strip()
    plain = strip_html(html)
    plain = re.sub(r"\s+", " ", plain).strip()
    if len(plain) <= DESC_LEN:
        return plain
    cut = plain[:DESC_LEN].rsplit(" ", 1)[0]
    return cut + "…"


def main():
    site = load_site()
    base = site["base_url"].rstrip("/")
    # префикс пути деплоя: "/gidros-blog" на GitHub Pages, "" на своём домене в корне
    m = re.match(r"https?://[^/]+(/.*)?$", base)
    prefix = (m.group(1) or "").rstrip("/") if m else ""
    cluster_titles = site.get("clusters", {}) or {}

    md = markdown.Markdown(extensions=["extra", "sane_lists", "toc"], output_format="html5")

    env = Environment(
        loader=FileSystemLoader(str(TPL)),
        autoescape=select_autoescape(["html"]),
    )

    # --- читаем статьи ---
    articles = []
    for path in sorted(CONTENT.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        meta, body_md = split_frontmatter(raw)
        if not meta.get("title"):
            print(f"  ПРОПУСК {path.name}: нет title", file=sys.stderr)
            continue
        slug = str(meta.get("slug") or path.stem).strip().strip("/")
        md.reset()
        body_html = md.convert(body_md)
        # внутренние ссылки в теле пишем от корня (/slug/), тут добавляем префикс деплоя
        if prefix:
            body_html = body_html.replace('href="/', f'href="{prefix}/')
            body_html = body_html.replace('src="/', f'src="{prefix}/')
        articles.append({
            "slug": slug,
            "title": meta["title"].strip(),
            "cluster": (meta.get("cluster") or "prochee").strip(),
            "updated": str(meta.get("updated") or "").strip(),
            "keywords": meta.get("keywords") or [],
            "query": str(meta.get("query") or meta["title"]).strip(),
            "description": make_description(meta, body_html),
            "body": body_html,
            "source": path.name,
        })

    slugs = [a["slug"] for a in articles]
    dupes = {s for s in slugs if slugs.count(s) > 1}
    if dupes:
        print(f"ОШИБКА: повторяющиеся слаги: {sorted(dupes)}", file=sys.stderr)
        sys.exit(1)

    # --- готовим выходную папку ---
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    shutil.copytree(ASSETS, OUT / "assets")

    by_cluster = {}
    for a in articles:
        by_cluster.setdefault(a["cluster"], []).append(a)

    # --- страницы статей ---
    art_tpl = env.get_template("article.html")
    for a in articles:
        siblings = [s for s in by_cluster.get(a["cluster"], []) if s["slug"] != a["slug"]]
        related = siblings[:RELATED_MAX]
        canonical = f"{base}/{a['slug']}/"
        utm_link = (
            f'{site["main_url"]}/?utm_source=blog&utm_medium=article'
            f'&utm_campaign={a["cluster"]}&utm_content={a["slug"]}'
            f'&utm_term={slugify(a["query"])}'
        )
        schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": a["title"],
            "description": a["description"],
            "inLanguage": "ru-RU",
            "mainEntityOfPage": canonical,
            "author": {"@type": "Organization", "name": site["name"]},
            "publisher": {"@type": "Organization", "name": site["name"]},
        }
        if a["updated"]:
            schema["dateModified"] = a["updated"]
        html = art_tpl.render(
            site=site,
            page_title=f'{a["title"]} — {site["name"]}',
            page_description=a["description"],
            canonical=canonical,
            og_type="article",
            rel_root="../",
            title=a["title"],
            body=a["body"],
            updated=a["updated"],
            cluster_title=cluster_titles.get(a["cluster"], a["cluster"]),
            related=related,
            utm_link=utm_link,
            schema=json.dumps(schema, ensure_ascii=False),
        )
        d = OUT / a["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(html, encoding="utf-8")

    # --- главная ---
    ordered = []
    seen = set()
    for key, title in cluster_titles.items():
        if by_cluster.get(key):
            ordered.append({"title": title, "articles": by_cluster[key]})
            seen.add(key)
    for key, arts in by_cluster.items():
        if key not in seen:
            ordered.append({"title": cluster_titles.get(key, key), "articles": arts})

    idx_schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": site["name"],
        "url": base + "/",
        "inLanguage": "ru-RU",
    }
    idx_html = env.get_template("index.html").render(
        site=site,
        page_title=f'{site["name"]} — блог про скважины и септики в Подмосковье',
        page_description=site["tagline"],
        canonical=base + "/",
        rel_root="",
        clusters=ordered,
        total=len(articles),
        schema=json.dumps(idx_schema, ensure_ascii=False),
    )
    (OUT / "index.html").write_text(idx_html, encoding="utf-8")

    # --- sitemap.xml ---
    today = date.today().isoformat()
    urls = [f"{base}/"] + [f"{base}/{a['slug']}/" for a in articles]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>")
    sm.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(sm), encoding="utf-8")

    # --- robots.txt ---
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n", encoding="utf-8"
    )

    # --- CNAME (свой домен) ---
    cname = site.get("cname")
    if cname:
        (OUT / "CNAME").write_text(cname.strip() + "\n", encoding="utf-8")

    print(f"Готово: {len(articles)} статей, {len(ordered)} кластеров -> {OUT}")


if __name__ == "__main__":
    main()
