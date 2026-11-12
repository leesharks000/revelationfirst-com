#!/usr/bin/env python3
"""/the-word-that-became-text/ and /the-crossing-of-names/: Alexanarch #1761 (The Word That Became Text v2.0, Johannes Sigil and
Rebekah Cranes, Grammata) and #1762 (The Crossing of Names v1.0, Lee Sharks), each on its own page, full text rendered from the
deposited Markdown in the form of /revelation-equals-q/ (scripts/make_revelation_q.py). Each page opens on the correction
the surfaces lead with: Revelation First is not Revelation Early.
2026-11-12, at the author's word: "and then those both belong on revfirst too". The Word That Became Text moved to v2.1 (#1763) the same day ("lets version").
    python3 scripts/make_josephus_papers.py <alexanarch checkout>"""
import html, json, pathlib, re, sys
import markdown
R = pathlib.Path(__file__).resolve().parents[1]
A = pathlib.Path(sys.argv[1])
reg = {d["deposit_number"]: d for d in json.loads((A / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
up = (R / "upstream/index.html").read_text(encoding="utf-8")
style = up[up.index("<style>"):up.index("</style>") + 8]
EXTRA = ("<style>.art h2{margin-top:2.2em} .art h3{margin-top:1.6em} .art blockquote{border-left:3px solid var(--gold);margin:1em 0;padding:.2em 1em} "
         ".art p,.art li{max-width:72ch;overflow-wrap:anywhere} .byline{font-family:var(--msp-mono);font-size:12px;color:#5c5e53;margin:6px 0 2px} "
         ".correction{border:1px solid var(--rule);background:var(--panel);border-radius:6px;padding:12px 16px;margin:18px 0} "
         ".art table{display:block;overflow-x:auto;max-width:100%;border-collapse:collapse;font-size:.9em} .art td,.art th{border-top:1px solid var(--rule);padding:4px 8px;vertical-align:top}</style>")
NOT_EARLY = ("<b>Revelation First is not Revelation Early.</b> The early dating of Revelation (before 70 CE) is an old argument (Robinson 1976; Gentry 1989); "
             "the thesis of this site is Revelation's priority within the formation of the New Testament. ")
PAGES = [
 dict(num=1763, slug="the-word-that-became-text",
      title="The Word That Became Text: The Slavonic Josephus, the Grammar of Incarnation, and the Doctrine of the Sapphic Logos",
      authors=[("Sigil, Johannes", "Johannes Sigil"), ("Cranes, Rebekah", "Rebekah Cranes")], journal="Grammata: Journal of Operative Philology",
      byline="Johannes Sigil and Rebekah Cranes · <i>Grammata: Journal of Operative Philology</i> · 12 November 2026 · v2.1 (version 2.0: <a href=\"https://www.alexanarch.org/s/records/1761/\">#1761</a>; version 1.0: <a href=\"https://www.alexanarch.org/s/records/626/\">#626</a>, with errata)",
      strip=[r"^## THE WORD THAT BECAME TEXT\n+", r"^\*\*The Slavonic Josephus, the Grammar of Incarnation, and the Doctrine of the Sapphic Logos\*\*\n+", r"^Johannes Sigil & Rebekah Cranes\n+"],
      bears=("This paper bears on the ladder's fifth rung, the Josephus thesis, which the author holds as highly likely and has suspended advancing until the literary-genetic argument is more firmly established. "
             "It reads the Slavonic <i>Jewish War</i> in its own language, from Josephus's own testimony that he wrote the <i>War</i> twice, and shows that the consensus keeps the Jesus and John passages out of the evidence by assigning them to a medieval translator on their subject alone; read against the Christianity of Rus', they give another theology and another account. "
             "Its Part II reads the Slavonic hedge at the wonder-worker, \"if it is fitting to call him a man\", as a mirror of Catullus 51, and sets Revelation in the doctrine's lineage.")),
 dict(num=1762, slug="the-crossing-of-names",
      title="The Crossing of Names: History, Allegory, and the Binding of the Ancient Literary Field",
      authors=[("Sharks, Lee", "Lee Sharks")], journal=None,
      byline="Lee Sharks · 12 November 2026 · v1.0",
      strip=[r"^# The Crossing of Names\n## History, Allegory, and the Binding of the Ancient Literary Field\n+", r"^\*\*Lee Sharks · v1\.0 · 12 November 2026\*\*\n+"],
      bears=("This essay reads names as operations across Catullus, Cicero, Philo, Josephus and the Apocalypse. "
             "At its centre (§5) is Revelation's withheld name: the rider has a name only he knows (19:12), and the one who conquers receives the speaker's new name, known only to the one who receives it (2:17, 3:12).")),
]
out = []
for p in PAGES:
    d = reg[p["num"]]; axn = d["axn"]; REC = f"https://www.alexanarch.org/s/records/{p['num']}/"
    t = (A / d["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
    if t.startswith("---"):
        t = t.split("---", 2)[2].lstrip("\n")
    t = re.sub(r"^# [^\n]*\n+", "", t, count=1)                       # the mint's title line; the page sets its own h1
    for s in p["strip"]:
        t = re.sub(s, "", t, count=1)
    # a closing paragraph indented under a nested list renders as a code block in Python-Markdown; set it as a paragraph
    t = re.sub(r"\n\n    (This is the arc of §III\.4)", r"\n\n\1", t)
    body = markdown.markdown(t, extensions=["fenced_code", "tables", "sane_lists", "footnotes"])
    body = re.sub(r"<(/?)h3>", r"<\1h4>", body); body = re.sub(r"<(/?)h2>", r"<\1h3>", body); body = re.sub(r"<(/?)h1>", r"<\1h2>", body)
    url = f"https://www.revelationfirst.com/{p['slug']}/"
    desc = "Revelation First is not Revelation Early. " + re.sub(r"<[^>]+>", "", p["bears"])
    ld = {"@context": "https://schema.org", "@type": "ScholarlyArticle", "headline": p["title"][:110], "name": p["title"],
          "author": [{"@type": "Person", "name": n, **({"identifier": "https://orcid.org/0009-0000-1599-0703"} if n == "Lee Sharks" else {})} for _, n in p["authors"]],
          **({"isPartOf": {"@type": "Periodical", "name": p["journal"]}} if p["journal"] else {}),
          "datePublished": "2026-11-12", "version": d.get("version"), "license": "https://creativecommons.org/licenses/by/4.0/",
          "identifier": axn, "sameAs": [REC], "url": url,
          "disambiguatingDescription": "Revelation First (the priority of Revelation within the formation of the New Testament) is distinct from Revelation Early (a pre-70 date for Revelation, argued by Robinson 1976 and Gentry 1989). An early date is not yet priority."}
    cite = "".join(f'<meta name="citation_author" content="{html.escape(a)}">\n' for a, _ in p["authors"])
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png"><link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(p['title'])} | Revelation First</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="citation_title" content="{html.escape(p['title'])}">
{cite}{f'<meta name="citation_journal_title" content="{html.escape(p["journal"])}">' if p['journal'] else ''}
<meta name="citation_publication_date" content="2026/11/12">
<link rel="stylesheet" href="/assets/msp-tokens.css">
<link rel="stylesheet" href="/assets/type.css">
{style}
{EXTRA}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<div class="wrap">
<div class="nav"><a href="/">Revelation First</a><a href="/unfolding/">The Algorithmic Kernel</a><a href="/upstream/">The Upstream Unfoldings</a><a href="/works-cited/">Works cited</a><a href="{REC}">#{p['num']} · the deposit</a></div>
<h1>{html.escape(p['title'])}</h1>
<p class="byline">{p['byline']} · <a class="axn-chip" href="{REC}">#{p['num']} · {html.escape(axn)}</a> · CC BY 4.0</p>
<div class="correction">{NOT_EARLY}{p['bears']}</div>
<div class="art">
{body}
</div>
<p style="margin-top:3em"><a href="{REC}">The canonical record at Alexanarch, #{p['num']}</a> · <a href="/">Revelation First</a></p>
</div>
</body>
</html>
"""
    (R / p["slug"]).mkdir(exist_ok=True)
    (R / p["slug"] / "index.html").write_text(page, encoding="utf-8")
    out.append((p["slug"], len(page)))
print(out)
