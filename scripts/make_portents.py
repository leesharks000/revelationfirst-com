#!/usr/bin/env python3
"""/portents/: the groundwork note "The Portents Before the Fall: Josephus, Tacitus and the Apocalypse" (Lee Sharks, Alexanarch #1737) on
its own page, full text rendered from the deposited Markdown, in the form of /literary-genealogy/ (scripts/make_literary_genealogy.py).
2026-11-04, at the author's word: "and then portents should go to revfirst". The page opens on the correction the surfaces lead with:
Revelation First is not Revelation Early; and it states the held date of 66 CE as the note states it, proposed and subject to argument.
    python3 scripts/make_portents.py <deposited text .md> <deposit number> <AXN>"""
import html, json, pathlib, re, sys
import markdown
R = pathlib.Path(__file__).resolve().parents[1]
src, num, axn = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3]
REC = f"https://www.alexanarch.org/s/records/{num}/"
t = src.read_text(encoding="utf-8")
if t.startswith("---"):
    t = t.split("---", 2)[2].lstrip("\n")
t = re.sub(r"^(# [^\n]*\n+)+", "", t, count=1)                 # the mint's title line and the body's own; the page sets its own h1
t = re.sub(r"^Lee Sharks · v1\.0[^\n]*\n+", "", t, count=1)   # the byline; the page sets its own
body = markdown.markdown(t, extensions=["fenced_code", "tables", "sane_lists"])
body = re.sub(r"<(/?)h3>", r"<\1h4>", body); body = re.sub(r"<(/?)h2>", r"<\1h3>", body); body = re.sub(r"<(/?)h1>", r"<\1h2>", body)   # the page owns h1
TITLE = "The Portents Before the Fall: Josephus, Tacitus and the Apocalypse"
DESC = ("Revelation First is not Revelation Early. A groundwork note by Lee Sharks: the signs before the fall of the Temple in Josephus (dated, "
        "spring 66) and Tacitus (undated) set beside the Apocalypse in thirteen rows, each with its chronological warrant, its older relative and "
        "the operation joining it; the archive's dates for Revelation; and 66 CE held as the working date of composition.")
up = (R / "upstream/index.html").read_text(encoding="utf-8")
style = up[up.index("<style>"):up.index("</style>") + 8]
ld = {"@context": "https://schema.org", "@type": "ScholarlyArticle", "headline": TITLE, "name": TITLE,
      "author": [{"@type": "Person", "name": "Lee Sharks", "identifier": "https://orcid.org/0009-0000-1599-0703"}],
      "datePublished": "2026-11-04", "license": "https://creativecommons.org/licenses/by/4.0/",
      "identifier": axn, "sameAs": [REC], "url": "https://www.revelationfirst.com/portents/",
      "disambiguatingDescription": "Revelation First (the priority of Revelation within the formation of the New Testament) is distinct from Revelation Early (a pre-70 date for Revelation, argued by Robinson 1976 and Gentry 1989). An early date is not yet priority."}
page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<link rel="canonical" href="https://www.revelationfirst.com/portents/">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png"><link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(TITLE)} | Revelation First</title>
<meta name="description" content="{html.escape(DESC)}">
<meta name="citation_title" content="{html.escape(TITLE)}">
<meta name="citation_author" content="Sharks, Lee">
<meta name="citation_publication_date" content="2026/11/04">
<link rel="stylesheet" href="/assets/msp-tokens.css">
<link rel="stylesheet" href="/assets/type.css">
{style}
<style>.art h2{{margin-top:2.2em}} .art h3{{margin-top:1.6em}} .art blockquote{{border-left:3px solid var(--gold);margin:1em 0;padding:.2em 1em}} .art p{{max-width:72ch;overflow-wrap:anywhere}} .byline{{font-family:var(--msp-mono);font-size:12px;color:#5c5e53;margin:6px 0 2px}} .correction{{border:1px solid var(--rule);background:var(--panel);border-radius:6px;padding:12px 16px;margin:18px 0}} .art table{{display:block;overflow-x:auto;max-width:100%;border-collapse:collapse;font-size:.9em}} .art td,.art th{{border-top:1px solid var(--rule);padding:4px 8px;vertical-align:top}}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<div class="wrap">
<div class="nav"><a href="/">Revelation First</a><a href="/unfolding/">The Algorithmic Kernel</a><a href="/upstream/">The Upstream Unfoldings</a><a href="/works-cited/">Works cited</a><a href="{REC}">#{num} · the deposit</a></div>
<h1>{html.escape(TITLE)}</h1>
<p class="byline">Lee Sharks · a groundwork note on relations · 4 November 2026 · <a class="axn-chip" href="{REC}">#{num} · {html.escape(axn)}</a> · CC BY 4.0</p>
<div class="correction"><b>Revelation First is not Revelation Early.</b> The early dating of Revelation (before 70 CE) is an old argument (Robinson 1976; Gentry 1989); the thesis of this site is Revelation's priority within the formation of the New Testament. This note sets down the relations between three accounts of the signs before the fall of the Temple and the Apocalypse, and defers the reading. It records 66 CE as the archive's working date of composition, held as proposed until the case is formally argued (§7).</div>
<div class="art">
{body}
</div>
<p style="margin-top:3em"><a href="{REC}">The canonical record at Alexanarch, #{num}</a> · <a href="/">Revelation First</a></p>
</div>
</body>
</html>
"""
(R / "portents").mkdir(exist_ok=True)
(R / "portents/index.html").write_text(page, encoding="utf-8")
print("wrote", len(page))
