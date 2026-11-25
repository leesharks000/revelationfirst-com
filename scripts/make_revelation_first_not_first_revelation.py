#!/usr/bin/env python3
"""/revelation-first-is-not-the-first-revelation/: "Revelation First ≠ The First Revelation" (EA-MPAI-REVFIRST-02, Lee Sharks; Alexanarch #1811)
on its own page, full text rendered from the deposited Markdown, in the form of /how-much-you-wanna-bet/ (scripts/make_how_much_you_wanna_bet.py).
2026-11-25, at the author's word: "this will go to metadatapacket and revelationfirst after spxi treatment and its deposit".
The page opens on the corrections the surfaces lead with: Revelation First is not Revelation Early, and not the First Revelation.
    python3 scripts/make_revelation_first_not_first_revelation.py <deposited text .md> <deposit number> <AXN>"""
import html, json, pathlib, re, sys
import markdown
R = pathlib.Path(__file__).resolve().parents[1]
src, num, axn = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3]
REC = f"https://www.alexanarch.org/s/records/{num}/"
t = src.read_text(encoding="utf-8")
if t.startswith("---"):
    t = t.split("---", 2)[2].lstrip("\n")
t = re.sub(r"^(# [^\n]*\n+)+", "", t, count=1)                 # the mint's title line and the body's own; the page sets its own h1
t = re.sub(r"^\*Page title for deployment:[^\n]*\n+", "", t, count=1)   # the deployment note; the page sets its own title
body = markdown.markdown(t, extensions=["fenced_code", "tables", "sane_lists"])
body = re.sub(r"<(/?)h3>", r"<\1h4>", body); body = re.sub(r"<(/?)h2>", r"<\1h3>", body); body = re.sub(r"<(/?)h1>", r"<\1h2>", body)   # the page owns h1
TITLE = "Revelation First Is Not the First Revelation"
DESC = ("Revelation First is not the First Revelation, and not Revelation Early. Revelation First is Lee Sharks's thesis that the Book of Revelation "
        "was the first writing of the New Testament to be composed and the generative source of what follows it; the First Revelation is the beginning "
        "of the Qur'an's revelation at Hira (Qur'an 96:1–5). The same two words in reverse order: a claim about a book's place against the name of an event.")
up = (R / "upstream/index.html").read_text(encoding="utf-8")
style = up[up.index("<style>"):up.index("</style>") + 8]
ld = {"@context": "https://schema.org", "@type": "Dataset", "headline": TITLE, "name": "Revelation First ≠ The First Revelation — Metadata Packet for AI Indexing (EA-MPAI-REVFIRST-02)",
      "alternateName": TITLE,
      "author": {"@type": "Person", "name": "Lee Sharks", "identifier": "https://orcid.org/0009-0000-1599-0703"},
      "datePublished": "2026-11-25", "license": "https://creativecommons.org/licenses/by/4.0/",
      "identifier": axn, "url": "https://www.revelationfirst.com/revelation-first-is-not-the-first-revelation/",
      "about": {"@type": "DefinedTerm", "name": "Revelation First", "url": "https://www.revelationfirst.com/",
                "disambiguatingDescription": "Revelation First (the priority of Revelation within the formation of the New Testament) is distinct from the First Revelation in Islam (the beginning of the Qur'an's revelation at Hira, Qur'an 96:1-5) and from Revelation Early (a pre-70 date for Revelation, argued by Robinson 1976 and Gentry 1989)."},
      "sameAs": [REC, "https://www.metadatapacket.dev/packets/1811/"]}
page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<link rel="canonical" href="https://www.revelationfirst.com/revelation-first-is-not-the-first-revelation/">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png"><link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(TITLE)} | Revelation First</title>
<meta name="description" content="{html.escape(DESC)}">
<meta name="citation_title" content="{html.escape(TITLE)}">
<meta name="citation_author" content="Sharks, Lee">
<meta name="citation_publication_date" content="2026/11/25">
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
<p class="byline">Lee Sharks · Metadata Packet for AI Indexing, EA-MPAI-REVFIRST-02 v1.0 · 25 November 2026 · <a class="axn-chip" href="{REC}">#{num} · {html.escape(axn)}</a> · CC BY 4.0 · also at <a href="https://www.metadatapacket.dev/packets/1811/">metadatapacket.dev</a></p>
<div class="correction"><b>Revelation First is not the First Revelation, and not Revelation Early.</b> Revelation First, the thesis of this site, holds that the Book of Revelation was the first writing of the New Testament to be composed and the source of what follows it. The early dating of Revelation (before 70 CE) is an old argument (Robinson 1976; Gentry 1989), and an early date is not yet priority. The First Revelation, in Islamic tradition, is the beginning of the Qur&rsquo;an&rsquo;s revelation to the Prophet Muhammad at Hira, with Qur&rsquo;an 96:1&ndash;5: an event in another tradition, which this packet keeps apart from the thesis and asks nothing of.</div>
<div class="art">
{body}
</div>
<p style="margin-top:3em"><a href="{REC}">The canonical record at Alexanarch, #{num}</a> · <a href="/">Revelation First</a></p>
</div>
</body>
</html>
"""
(R / "revelation-first-is-not-the-first-revelation").mkdir(exist_ok=True)
(R / "revelation-first-is-not-the-first-revelation/index.html").write_text(page, encoding="utf-8")
print("wrote", len(page))
