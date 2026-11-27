#!/usr/bin/env python3
"""/unfolding/matthew/: "How to Write Matthew from Revelation: The Generative Grammar of the First Gospel" (Lee Sharks, Grammata:
Journal of Operative Philology; EA-REVFIRST-MATTHEW-01) on its own page inside the unfoldings, full text rendered from the versioned
Markdown kept beside the page, head and chrome in the form of /literary-genealogy/. 2026-11-27, at the author's word: "lets version
and install in the unfoldings on revfirst". The page states which version it carries and which version the Alexanarch record carries.
    python3 scripts/make_how_to_write_matthew.py <versioned text .md> <version> <deposit number> <deposited version>"""
import html, json, pathlib, re, sys
import markdown
R = pathlib.Path(__file__).resolve().parents[1]
src, ver, num, depver = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
REC = f"https://www.alexanarch.org/s/records/{num}/"
URL = "https://www.revelationfirst.com/unfolding/matthew/"
t = src.read_text(encoding="utf-8")
t = re.sub(r"^# [^\n]*\n+", "", t, count=1)                      # the title line; the page sets its own h1
body = markdown.markdown(t, extensions=["fenced_code", "tables", "sane_lists"])
body = re.sub(r"<(/?)h3>", r"<\1h4>", body); body = re.sub(r"<(/?)h2>", r"<\1h3>", body); body = re.sub(r"<(/?)h1>", r"<\1h2>", body)   # the page owns h1
body = body.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")   # wide tables scroll inside the column
TITLE = "How to Write Matthew from Revelation: The Generative Grammar of the First Gospel"
DESC = ("A paper by Lee Sharks (Grammata: Journal of Operative Philology). What a writer holding the Apocalypse would have to do to get a "
        "Gospel, answered by doing it: a ledger of 158 relations with their moves reaching 305 of Matthew's 1,067 verses (28.6 per cent), "
        "one passage produced blind from the rule, and beside that derivation a map of named pairs with the letters, Josephus and the "
        "Septuagint. The reconstructed sources of the Gospels are set beside an architecture of extant texts. No hypothetical source is supposed.")
SAME = (f'The record at Alexanarch, <a href="{REC}">#{num}</a>, carries the same version, reissued in place.' if ver == depver else
        f'The record at Alexanarch, <a href="{REC}">#{num}</a>, carries {html.escape(depver)}; {html.escape(ver)} has not been deposited there.')
up = (R / "upstream/index.html").read_text(encoding="utf-8")
style = up[up.index("<style>"):up.index("</style>") + 8]
ld = {"@context": "https://schema.org", "@type": "ScholarlyArticle", "headline": TITLE, "name": TITLE,
      "author": [{"@type": "Person", "name": "Lee Sharks", "identifier": "https://orcid.org/0009-0000-1599-0703"}],
      "isPartOf": {"@type": "Periodical", "name": "Grammata: Journal of Operative Philology"},
      "datePublished": "2026-11-27", "dateModified": "2026-11-27", "version": ver,
      "license": "https://creativecommons.org/licenses/by/4.0/", "url": URL,
      "isBasedOn": REC,
      "disambiguatingDescription": "Revelation First (the priority of Revelation within the formation of the New Testament) is distinct from Revelation Early (a pre-70 date for Revelation). The paper states that it does not prove which book was written first; it gives a procedure and its measured reach, and keeps a derivation (28.6 per cent of Matthew's verses) apart from a source map (61.8 to 64.9 per cent)."}
page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<link rel="canonical" href="{URL}">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png"><link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(TITLE)} | Revelation First</title>
<meta name="description" content="{html.escape(DESC)}">
<meta name="citation_title" content="{html.escape(TITLE)}">
<meta name="citation_author" content="Sharks, Lee">
<meta name="citation_journal_title" content="Grammata: Journal of Operative Philology">
<meta name="citation_publication_date" content="2026/11/27">
<link rel="stylesheet" href="/assets/msp-tokens.css">
<link rel="stylesheet" href="/assets/type.css">
{style}
<style>.art h2{{margin-top:2.2em}} .art h3{{margin-top:1.8em}} .art h4{{margin-top:1.4em}} .art blockquote{{border-left:3px solid var(--gold);margin:1em 0;padding:.2em 1em}} .art p,.art li{{max-width:76ch}} .art img{{max-width:100%;height:auto}} .tw{{overflow-x:auto;margin:12px 0}} .art table{{border-collapse:collapse;font-size:.92em;min-width:60%}} .art th{{font-family:var(--msp-mono);font-size:10.5px;text-align:left;color:#5c5e53;border-bottom:1px solid var(--rule);padding:4px 8px;letter-spacing:.05em}} .art td{{border-bottom:1px solid var(--rule);padding:6px 8px;vertical-align:top}} .byline{{font-family:var(--msp-mono);font-size:12px;color:#5c5e53;margin:6px 0 2px}} .correction{{border:1px solid var(--rule);background:var(--panel);border-radius:6px;padding:12px 16px;margin:18px 0}}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<div class="wrap">
<div class="nav"><a href="/">Revelation First</a><a href="/unfolding/">The Algorithmic Kernel</a><a href="/upstream/">The Upstream Unfoldings</a><a href="/works-cited/">Works cited</a><a href="{REC}">#{num} · the deposit ({html.escape(depver)})</a></div>
<h1>{html.escape(TITLE)}</h1>
<p class="byline">Lee Sharks · <em>Grammata: Journal of Operative Philology</em> · EA-REVFIRST-MATTHEW-01 · {html.escape(ver)} · 27 November 2026 · CC BY 4.0</p>
<div class="correction"><b>Which version this is.</b> This page carries {html.escape(ver)} of the paper. {SAME} The text of this page as Markdown: <a href="/unfolding/matthew/{html.escape(src.name)}">{html.escape(src.name)}</a>. The working notebook behind it: <a href="/unfolding/notebook/UNFOLDING-MAP-current.md">The Unfolding Map</a>. <b>Revelation First is not Revelation Early</b>: the paper does not argue a date, and says that taken alone it does not show which book was written first.</div>
<div class="art">
{body}
</div>
<p style="margin-top:3em"><a href="{REC}">The record at Alexanarch, #{num} ({html.escape(depver)})</a> · <a href="/unfolding/">The Algorithmic Kernel</a> · <a href="/">Revelation First</a></p>
</div>
</body>
</html>
"""
out = R / "unfolding/matthew/index.html"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(page, encoding="utf-8")
print("wrote", len(page))
