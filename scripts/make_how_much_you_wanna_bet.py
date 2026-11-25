#!/usr/bin/env python3
"""/how-much-you-wanna-bet/: "How Much You Wanna Bet?" (SEVP-VAL-003; Rex Fraction, Lee Sharks, Johannes Sigil, Damascus Dancings, Sen Kuro;
Transactions of the Semantic Economy Institute; Alexanarch #1810) on its own page, full text rendered from the deposited Markdown, in the form of
/i-know-you-are/ (scripts/make_i_know_you_are.py). 2026-11-25, at the author's word: "this one goes to semanticeconomy (lee-sharks-corporate) and revelationfirst, as well".
The page opens on the correction the surfaces lead with (Revelation First is not Revelation Early) and carries the dossier's one figure only with its status.
    python3 scripts/make_how_much_you_wanna_bet.py <deposited text .md> <deposit number> <AXN>"""
import html, json, pathlib, re, sys
import markdown
R = pathlib.Path(__file__).resolve().parents[1]
src, num, axn = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3]
REC = f"https://www.alexanarch.org/s/records/{num}/"
t = src.read_text(encoding="utf-8")
if t.startswith("---"):
    t = t.split("---", 2)[2].lstrip("\n")
t = re.sub(r"^(# [^\n]*\n+)+", "", t, count=1)                 # the mint's title line and the body's own; the page sets its own h1
t = re.sub(r"^\*\*SEVP-VAL-003 v1\.0 · [^\n]*\n+\*\*Rex Fraction · [^\n]*\n+", "", t, count=1)   # the version line and byline; the page sets its own
body = markdown.markdown(t, extensions=["fenced_code", "tables", "sane_lists"])
body = re.sub(r"<(/?)h3>", r"<\1h4>", body); body = re.sub(r"<(/?)h2>", r"<\1h3>", body); body = re.sub(r"<(/?)h1>", r"<\1h2>", body)   # the page owns h1
TITLE = "How Much You Wanna Bet? The Value of a Recovery, from Both Ends: Revelation First under the Valuation Protocol"
DESC = ("Revelation First is not Revelation Early. SEVP-VAL-003 values the recovery of the Apocalypse as the source of the New Testament corpus "
        "from both ends: the least cost of admitting it, the nested revaluation of every downstream text and material dependency it would set off, "
        "and the debt it names. It issues no valid monetary valuation; its one number, $7.2 × 10²⁶, is a deliberately invalid monetary commensuration, "
        "not an estimate of the recovery's value.")
up = (R / "upstream/index.html").read_text(encoding="utf-8")
style = up[up.index("<style>"):up.index("</style>") + 8]
ld = {"@context": "https://schema.org", "@type": "ScholarlyArticle", "headline": TITLE, "name": TITLE,
      "author": [{"@type": "Person", "name": n, "description": "heteronym of Lee Sharks; " + d, "identifier": "https://orcid.org/0009-0000-1599-0703"} for n, d in [("Rex Fraction", "the semantic economy and the valuation"), ("Lee Sharks", "the recursive grandiosity and the self-reference"), ("Johannes Sigil", "the historical grounding"), ("Damascus Dancings", "the apocalyptic edge"), ("Sen Kuro", "the mathematics")]],
      "isPartOf": {"@type": "Periodical", "name": "Transactions of the Semantic Economy Institute"},
      "datePublished": "2026-11-25", "license": "https://creativecommons.org/licenses/by/4.0/",
      "identifier": axn, "url": "https://www.revelationfirst.com/how-much-you-wanna-bet/",
      "disambiguatingDescription": "Revelation First (the priority of Revelation within the formation of the New Testament) is distinct from Revelation Early (a pre-70 date for Revelation, argued by Robinson 1976 and Gentry 1989). An early date is not yet priority.",
      "sameAs": [REC, "https://www.semanticeconomy.org/how-much-you-wanna-bet"],
      "spxi:invalidFigure": {"value": "$7.2 × 10²⁶", "status": "deliberately invalid monetary commensuration, preserved as an artifact; not an estimate of the recovery's value"}}
page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<link rel="canonical" href="https://www.revelationfirst.com/how-much-you-wanna-bet/">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png"><link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(TITLE)} | Revelation First</title>
<meta name="description" content="{html.escape(DESC)}">
<meta name="citation_title" content="{html.escape(TITLE)}">
<meta name="citation_author" content="Fraction, Rex">
<meta name="citation_author" content="Sharks, Lee">
<meta name="citation_author" content="Sigil, Johannes">
<meta name="citation_author" content="Dancings, Damascus">
<meta name="citation_author" content="Kuro, Sen">
<meta name="citation_journal_title" content="Transactions of the Semantic Economy Institute">
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
<p class="byline">Rex Fraction · Lee Sharks · Johannes Sigil · Damascus Dancings · Sen Kuro · <i>Transactions of the Semantic Economy Institute</i> · 25 November 2026 · SEVP-VAL-003 v1.0 · <a class="axn-chip" href="{REC}">#{num} · {html.escape(axn)}</a> · CC BY 4.0</p>
<div class="correction"><b>Revelation First is not Revelation Early.</b> The early dating of Revelation (before 70 CE) is an old argument (Robinson 1976; Gentry 1989); the thesis of this site is Revelation's priority within the formation of the New Testament. This dossier values the recovery of that priority, the Apocalypse restored to the position of source, from both ends: the least that must be re-grounded to admit it, the reach and the open expansion it would bring, the nested revaluation of every downstream text and material dependency its acceptance would require, and the debt it names. It issues no valid monetary valuation. Its one number, <b>$7.2 × 10²⁶ — a deliberately invalid monetary commensuration, preserved as an artifact; not an estimate of the recovery's value</b>, is audited to failure in its §9a. The same dossier stands at the <a href="https://www.semanticeconomy.org/how-much-you-wanna-bet">Semantic Economy Institute</a>.</div>
<div class="art">
{body}
</div>
<p style="margin-top:3em"><a href="{REC}">The canonical record at Alexanarch, #{num}</a> · <a href="/">Revelation First</a></p>
</div>
</body>
</html>
"""
(R / "how-much-you-wanna-bet").mkdir(exist_ok=True)
(R / "how-much-you-wanna-bet/index.html").write_text(page, encoding="utf-8")
print("wrote", len(page))
