"""Build the portfolio site into the repo root (served by GitHub Pages from main).

Pages are markdown files in src/content/ with YAML front matter. The layout is the
evidence desk: a charcoal rail for navigation, the page in the middle, and an
evidence ledger on the right that says how well each claim is supported.

Markdown extras:
  [[label]]            a citation tag
  [[label|url]]        a citation tag that links
  {{figure:name}}      a generated SVG figure (see FIGURES)
  {{table:name}}       a generated table (see TABLES)

Project data is read from local working repos, set with environment variables:
  AC_SAR_REPO  (default ~/Documents/GitHub/ac-sar)

Run:  .venv/bin/python build.py && .venv/bin/python check.py
"""
import csv
import html
import json
import os
import re
import shutil

import markdown
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = HERE
SRC = os.path.join(HERE, "src")
AC_SAR = os.path.expanduser(os.environ.get("AC_SAR_REPO", "~/Documents/GitHub/ac-sar"))
SITE = {"name": "iamkani", "sub": "Data projects that say how sure they are", "github": "https://github.com/iamkani"}

FONTS = ("https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700"
         "&family=IBM+Plex+Sans+Condensed:wght@500;600;700"
         "&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap")
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
           "%3Cpath d='M8 20a8 8 0 0 1 8-8h26l16 16v8L42 52H16a8 8 0 0 1-8-8z' fill='%23f2c318' "
           "stroke='%231f2421' stroke-width='3' stroke-linejoin='round'/%3E"
           "%3Ccircle cx='20' cy='32' r='5' fill='%231f2421'/%3E%3C/svg%3E")


# ---- content -----------------------------------------------------------------
def load_pages():
    pages = []
    for name in sorted(os.listdir(os.path.join(SRC, "content"))):
        if not name.endswith(".md"):
            continue
        raw = open(os.path.join(SRC, "content", name), encoding="utf-8").read()
        _, fm, body = raw.split("---", 2)
        meta = yaml.safe_load(fm)
        meta["body_md"] = body
        pages.append(meta)
    return sorted(pages, key=lambda p: p.get("order", 50))


def url_for(slug):
    return "/" if not slug else f"/{slug}/"


# ---- generated figures and tables ---------------------------------------------
def nb_sar_graph():
    return json.load(open(os.path.join(AC_SAR, "output", "nb_sar_corpus.graph.json"), encoding="utf-8"))


def figure_top_species():
    g = nb_sar_graph()
    rows = sorted(((len(n["documents"]), n["name"]) for n in g["nodes"]
                   if n["type"] == "species" and len(n.get("documents", [])) >= 3),
                  key=lambda r: (-r[0], r[1].lower()))
    n_shared = sum(1 for n in g["nodes"] if n["type"] == "species" and len(n.get("documents", [])) >= 2)
    bar_h, gap, left, right, top = 18, 7, 190, 40, 8
    width = 640
    height = top + len(rows) * (bar_h + gap) + 26
    unit = (width - left - right) / max(r[0] for r in rows)
    out = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-labelledby="fig-sp-t" xmlns="http://www.w3.org/2000/svg">',
           '<title id="fig-sp-t">Species named in three or more of the 30 NB-SAR documents</title>']
    for i, (count, name) in enumerate(rows):
        y = top + i * (bar_h + gap)
        w = count * unit
        out.append(f'<text x="{left - 10}" y="{y + bar_h - 5}" text-anchor="end" font-family="IBM Plex Sans, sans-serif" '
                   f'font-size="13" fill="#16181a">{html.escape(name)}</text>')
        out.append(f'<rect x="{left}" y="{y}" width="{w:.1f}" height="{bar_h}" rx="3" fill="{"#16181a" if count >= 5 else "#6b716c"}"/>')
        out.append(f'<text x="{left + w + 6:.1f}" y="{y + bar_h - 5}" font-family="IBM Plex Mono, monospace" '
                   f'font-size="12" fill="#474c49">{count}</text>')
    axis_y = top + len(rows) * (bar_h + gap) + 14
    out.append(f'<text x="{left}" y="{axis_y}" font-family="IBM Plex Mono, monospace" font-size="11" fill="#6b716c" '
               f'letter-spacing="0.06em">DOCUMENTS THAT NAME THE SPECIES (OF 30)</text>')
    out.append("</svg>")
    caption = (f"Species named in three or more of the 30 documents; {n_shared} species appear in two or more. "
               "Counts come from the merged graph (exact names after normalisation), so a species written two "
               "different ways counts twice. Wide-ranging bats and birds tie the corpus together.")
    return f'<figure class="figure">{"".join(out)}<figcaption>{caption}</figcaption></figure>'


def table_nb_sar_documents():
    path = os.path.join(AC_SAR, "data", "scoping", "atlantic_candidates.csv")
    rows = [r for r in csv.DictReader(open(path, encoding="utf-8")) if r["in_nb_sar"] == "True"]
    rows.sort(key=lambda r: r["title"].lower())
    kind = {"RECOVERY_STRATEGY": "Recovery strategy", "ACTION_PLAN": "Action plan", "MANAGEMENT_PLAN": "Management plan"}
    out = ['<div class="table-wrap"><table><thead><tr><th>Document</th><th>Type</th><th>Published</th><th>Atlantic scope</th></tr></thead><tbody>']
    for r in rows:
        t = html.escape(r["title"])
        title = f'<a href="{html.escape(r["html"])}">{t}</a>' if r["html"] else t
        types = " / ".join(kind.get(x, x) for x in r["types"].split(";") if x)
        scope = "in scope" if r["in_scope"] == "True" else "out of region"
        out.append(f"<tr><td>{title}</td><td>{types}</td><td>{r['published'][:4]}</td><td>{scope}</td></tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


FIGURES = {"top_species": figure_top_species}
TABLES = {"nb_sar_documents": table_nb_sar_documents}


# ---- rendering -------------------------------------------------------------------
TAG = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
BLOCK = re.compile(r"\{\{(figure|table):([a-z_]+)\}\}")


def render_body(md_text):
    blocks = {}

    def stash(m):
        key = f"BLOCK{len(blocks)}X"
        blocks[key] = (FIGURES if m.group(1) == "figure" else TABLES)[m.group(2)]()
        return f"\n\n{key}\n\n"

    md_text = BLOCK.sub(stash, md_text)
    md_text = TAG.sub(lambda m: (f'<a class="tag" href="{m.group(2)}">{html.escape(m.group(1))}</a>' if m.group(2)
                                 else f'<span class="tag">{html.escape(m.group(1))}</span>'), md_text)
    out = markdown.markdown(md_text, extensions=["tables", "attr_list", "md_in_html", "sane_lists"])
    out = out.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    for key, value in blocks.items():
        out = out.replace(f"<p>{key}</p>", value)
    return out


def render_ledger(page):
    parts = []
    if page.get("ev_kicker"):
        parts.append(f'<p class="ev-kicker">{html.escape(page["ev_kicker"])}</p>')
    if page.get("ev_title"):
        parts.append(f'<h2 class="ev-title">{html.escape(page["ev_title"])}</h2>')
    if page.get("ev_note"):
        parts.append(f'<p class="ev-note">{render_inline(page["ev_note"])}</p>')
    marks = {"ok": ("", "✓"), "caution": (" ledger-caution", "~"), "unverified": (" ledger-unverified", "!")}
    for group in page.get("ledger", []):
        cls, mark = marks[group["kind"]]
        parts.append(f'<section class="ledger{cls}"><div class="ledger-head"><span class="ledger-mark" aria-hidden="true">{mark}</span>'
                     f'{html.escape(group["head"])}</div>')
        if group.get("rows"):
            parts.append('<dl class="ledger-rows">')
            for k, v in group["rows"]:
                parts.append(f"<div><dt>{html.escape(k)}</dt><dd>{render_inline(v)}</dd></div>")
            parts.append("</dl>")
        if group.get("issues"):
            parts.append('<ul class="ledger-issues">')
            for it in group["issues"]:
                parts.append(f'<li>{render_inline(it["q"])}<span>{render_inline(it["note"])}</span></li>')
            parts.append("</ul>")
        parts.append("</section>")
    return "".join(parts)


def render_inline(text):
    text = TAG.sub(lambda m: f'<span class="tag">{html.escape(m.group(1))}</span>', html.escape(str(text), quote=False))
    return markdown.markdown(text).removeprefix("<p>").removesuffix("</p>")


def render_cards(page):
    if not page.get("cards"):
        return ""
    out = ['<div class="cards">']
    for c in page["cards"]:
        out.append(f'<a class="card" href="{c["href"]}"><p class="card-kind">{html.escape(c["kind"])}</p>'
                   f'<span class="card-title">{html.escape(c["title"])}</span>'
                   f'<span class="card-text">{html.escape(c["text"])}</span>'
                   f'<span class="card-foot">{html.escape(c["foot"])}</span></a>')
    out.append("</div>")
    return "".join(out)


def render_page(page, pages):
    nav = []
    for p in pages:
        current = ' aria-current="page"' if p["slug"] == page["slug"] else ""
        status = p.get("status", "")
        scls = " is-live" if status == "live" else ""
        badge = f'<span class="nav-status{scls}">{html.escape(status)}</span>' if status else ""
        nav.append(f'<li><a href="{url_for(p["slug"])}"{current}><span>{html.escape(p["nav"])}</span>{badge}</a></li>')
    title = f'{page["nav"]} · {SITE["name"]}' if page["slug"] else f'{SITE["name"]} · {SITE["sub"]}'
    body_cls = "body plain" if page.get("plain") else "body"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(page.get('description', page['lede']))}">
<meta name="theme-color" content="#1f2421">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="desk">
  <nav class="rail" aria-label="Site">
    <div class="rail-inner">
      <a class="brand" href="/"><span class="brand-tag">IK</span><span><span class="brand-name">{SITE['name']}</span>
        <span class="brand-sub" style="display:block">{html.escape(SITE['sub'])}</span></span></a>
      <p class="rail-label">Pages</p>
      <ul class="nav">{''.join(nav)}</ul>
      <div class="rail-foot">
        <a href="{SITE['github']}">GitHub</a><br>
        Evidence first: every claim says how it was checked.
      </div>
    </div>
  </nav>
  <main class="doc" id="main">
    <div class="doc-inner">
      <header class="page-head">
        <p class="kicker">{html.escape(page['kicker'])}</p>
        <h1>{html.escape(page['title'])}</h1>
        <p class="lede">{render_inline(page['lede'])}</p>
      </header>
      {render_cards(page)}
      <div class="{body_cls}">{render_body(page['body_md'])}</div>
    </div>
  </main>
  <aside class="evidence" aria-label="Evidence">
    <div class="evidence-inner">{render_ledger(page)}</div>
  </aside>
</div>
</body>
</html>
"""


def main():
    pages = load_pages()
    # Only generated paths are removed: index.html, assets/ and one folder per page.
    for page in pages:
        target = os.path.join(OUT, page["slug"]) if page["slug"] else os.path.join(OUT, "index.html")
        if page["slug"] and os.path.isdir(target):
            shutil.rmtree(target)
        elif not page["slug"] and os.path.exists(target):
            os.remove(target)
    shutil.rmtree(os.path.join(OUT, "assets"), ignore_errors=True)
    os.makedirs(os.path.join(OUT, "assets"))
    shutil.copy(os.path.join(SRC, "style.css"), os.path.join(OUT, "assets", "style.css"))
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    for page in pages:
        d = os.path.join(OUT, page["slug"]) if page["slug"] else OUT
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(render_page(page, pages))
    print(f"built {len(pages)} pages into the repo root")


if __name__ == "__main__":
    main()
