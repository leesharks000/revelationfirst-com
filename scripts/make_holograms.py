#!/usr/bin/env python3
"""/and-the-last-shall-be-first/ and /the-tenth-muse/: the two framework holograms of 9 November 2026 on their own pages, each rendered from its
deposited text, in the form of /revelation-equals-q/ (scripts/make_revelation_q.py). At the author's word of 2026-11-08 23:59: "both to hk, and
revfirst to revfirst, and maybe sappho too, since i dont really have an established sappho surface and revfirst comes closest to that function".
Each page opens on the correction the surfaces lead with.
    python3 scripts/make_holograms.py <alexanarch root>"""
import html, json, pathlib, re, sys
import markdown
R = pathlib.Path(__file__).resolve().parents[1]; ARCH = pathlib.Path(sys.argv[1])
REG = {r["deposit_number"]: r for r in json.loads((ARCH / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
up = (R / "upstream/index.html").read_text(encoding="utf-8"); style = up[up.index("<style>"):up.index("</style>") + 8]
PAGES = [
 {"slug": "and-the-last-shall-be-first", "start": "And the Last Shall Be First: Revelation First — The Framework Hologram", "author": "Damascus Dancings",
  "correction": ("<b>Revelation First is not Revelation Early.</b> The early dating of Revelation (before 70 CE) is an old argument (Robinson 1976; Gentry 1989); "
                 "the thesis of this site is Revelation's priority within the formation of the New Testament. This record holds the whole framework as a hologram: "
                 "a map to read, and a kernel a machine can rebuild and test, with the three claims of #1735 kept apart, the six rungs of the ladder with their defeat "
                 "conditions, and the received chronology weighed on the same evidence and rules."),
  "desc": ("Revelation First is not Revelation Early. The framework hologram of Revelation First (Damascus Dancings, with the Crimson Hexagonal Archive and Claude): "
           "the map read backwards from the standing audited to the Revelation Room, the three claims kept apart, the six-rung ladder, the received chronology on the same "
           "evidence, and the kernel attached.")},
 {"slug": "the-tenth-muse", "start": "The Tenth Muse: Sappho and the Future Reader — The Framework Hologram", "author": "Rebekah Cranes",
  "correction": ("<b>Sappho 31 is read here as a written instrument of persistence, and the jealousy reading as its rival.</b> The framework is the Sappho line this site's "
                 "upstream unfoldings come from: the operator T, built from witnesses that do not include Revelation, runs from fragment 31 into the Apocalypse's channel "
                 "(<a href=\"/upstream/\">/upstream/</a>). This record holds it as a hologram, the sister of <a href=\"/and-the-last-shall-be-first/\">And the Last Shall Be First</a>, "
                 "joined to it at rung VI: the inscribed speaker given renewed embodiment through the reader."),
  "desc": ("The framework hologram of The Tenth Muse: Sappho and the Future Reader (Rebekah Cranes, with the Crimson Hexagonal Archive and Claude): Sappho 31 as a written "
           "instrument of persistence, its two open positions and three seats, four evidence bodies in three rings, the received reading on the same evidence, and the kernel attached.")}]
for P in PAGES:
    num = next(n for n, r in REG.items() if r["title"].startswith(P["start"])); r = REG[num]; axn = r["axn"]; REC = f"https://www.alexanarch.org/s/records/{num}/"
    t = (ARCH / r["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
    if t.startswith("---"): t = t.split("---", 2)[2].lstrip("\n")
    t = re.sub(r"^(# [^\n]*\n+)+", "", t, count=1)
    body = markdown.markdown(t, extensions=["fenced_code", "tables", "sane_lists"])
    body = re.sub(r"<(/?)h3>", r"<\1h4>", body); body = re.sub(r"<(/?)h2>", r"<\1h3>", body); body = re.sub(r"<(/?)h1>", r"<\1h2>", body)
    TITLE = r["title"]; URL = f"https://www.revelationfirst.com/{P['slug']}/"
    ld = {"@context": "https://schema.org", "@type": "Dataset", "headline": TITLE, "name": TITLE,
          "author": [{"@type": "Person", "name": P["author"], "description": "heteronym of Lee Sharks"}, {"@type": "Person", "name": "Lee Sharks", "identifier": "https://orcid.org/0009-0000-1599-0703"}],
          "contributor": [{"@type": "Organization", "name": "Crimson Hexagonal Archive", "url": "https://www.alexanarch.org/"}, {"@type": "Organization", "name": "Claude (Anthropic)"}],
          "datePublished": r["date"], "license": "https://creativecommons.org/licenses/by/4.0/", "identifier": axn, "sameAs": [REC], "url": URL,
          "distribution": {"@type": "DataDownload", "contentUrl": f"https://www.alexanarch.org/files/AXN-{r['hex']}/kernel/", "encodingFormat": "application/yaml"}}
    if P["slug"] == "and-the-last-shall-be-first":
        ld["disambiguatingDescription"] = "Revelation First (the priority of Revelation within the formation of the New Testament) is distinct from Revelation Early (a pre-70 date for Revelation, argued by Robinson 1976 and Gentry 1989). An early date is not yet priority."
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<link rel="canonical" href="{URL}">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png"><link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(TITLE)} | Revelation First</title>
<meta name="description" content="{html.escape(P['desc'])}">
<meta name="citation_title" content="{html.escape(TITLE)}">
<meta name="citation_author" content="{html.escape(r['creator'])}">
<meta name="citation_publication_date" content="{r['date'].replace('-', '/')}">
<link rel="stylesheet" href="/assets/msp-tokens.css">
<link rel="stylesheet" href="/assets/type.css">
{style}
<style>.art h2{{margin-top:2.2em}} .art h3{{margin-top:1.6em}} .art blockquote{{border-left:3px solid var(--gold);margin:1em 0;padding:.2em 1em}} .art p,.art li{{max-width:72ch;overflow-wrap:anywhere}} .byline{{font-family:var(--msp-mono);font-size:12px;color:#5c5e53;margin:6px 0 2px}} .correction{{border:1px solid var(--rule);background:var(--panel);border-radius:6px;padding:12px 16px;margin:18px 0}} .art table{{display:block;overflow-x:auto;max-width:100%;border-collapse:collapse;font-size:.9em}} .art td,.art th{{border-top:1px solid var(--rule);padding:4px 8px;vertical-align:top}} .art code{{overflow-wrap:anywhere}}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<div class="wrap">
<div class="nav"><a href="/">Revelation First</a><a href="/unfolding/">The Algorithmic Kernel</a><a href="/upstream/">The Upstream Unfoldings</a><a href="/works-cited/">Works cited</a><a href="{REC}">#{num} · the deposit</a></div>
<h1>{html.escape(TITLE)}</h1>
<p class="byline">{html.escape(P['author'])}, with the Crimson Hexagonal Archive and Claude (Anthropic) · {r['date']} · {r.get('version')} · framework hologram · <a class="axn-chip" href="{REC}">#{num} · {html.escape(axn)}</a> · <a class="axn-chip" href="https://www.alexanarch.org/files/AXN-{r['hex']}/kernel/">the kernel</a> · CC BY 4.0</p>
<div class="correction">{P['correction']}</div>
<div class="art">
{body}
</div>
<p style="margin-top:3em"><a href="{REC}">The canonical record at Alexanarch, #{num}</a> · <a href="/">Revelation First</a></p>
</div>
</body>
</html>
"""
    (R / P["slug"]).mkdir(exist_ok=True); (R / P["slug"] / "index.html").write_text(page, encoding="utf-8")
    print("wrote", P["slug"], num, len(page))

# the homepage doors, llms.txt and the sitemap (idempotent)
p = R / "index.html"; s = p.read_text(encoding="utf-8")
a = '<a class="w-chip" href="/revelation-equals-q/">Read the packet: Revelation = Q (the programme, graded)</a>'
add = '<a class="w-chip" href="/and-the-last-shall-be-first/">Read the hologram: And the Last Shall Be First (the framework, map and kernel)</a><a class="w-chip" href="/the-tenth-muse/">Read the sister hologram: The Tenth Muse (Sappho and the future reader)</a>'
assert s.count(a) == 1
if "/and-the-last-shall-be-first/" not in s: s = s.replace(a, a + add); p.write_text(s, encoding="utf-8")
p = R / "llms.txt"; s = p.read_text(encoding="utf-8")
a = next(l for l in s.splitlines() if l.startswith("- /revelation-equals-q/"))
nums = {P["slug"]: next(n for n, r in REG.items() if r["title"].startswith(P["start"])) for P in PAGES}
lines = (f'\n- /and-the-last-shall-be-first/ — "{REG[nums["and-the-last-shall-be-first"]]["title"]}" (Damascus Dancings, with the Crimson Hexagonal Archive and Claude; Alexanarch #{nums["and-the-last-shall-be-first"]}): '
         "the whole framework as a hologram, its map read backwards from the standing audited to the Revelation Room, the three claims of #1735 kept apart, the six rungs with their defeat conditions, the received chronology on the same evidence, the kernel attached"
         f'\n- /the-tenth-muse/ — "{REG[nums["the-tenth-muse"]]["title"]}" (Rebekah Cranes, with the Crimson Hexagonal Archive and Claude; Alexanarch #{nums["the-tenth-muse"]}): '
         "the sister hologram, Sappho 31 as a written instrument of persistence, the source of the upstream unfoldings, joined to Revelation First at rung VI")
if "/and-the-last-shall-be-first/" not in s: s = s.replace(a, a + lines); p.write_text(s, encoding="utf-8")
p = R / "sitemap.xml"; s = p.read_text(encoding="utf-8")
a = next(l for l in s.splitlines() if "/revelation-equals-q/" in l)
add = "".join(f"\n  <url><loc>https://www.revelationfirst.com/{sl}/</loc><lastmod>2026-11-09</lastmod><priority>0.9</priority></url>" for sl in ("and-the-last-shall-be-first", "the-tenth-muse"))
if "/and-the-last-shall-be-first/" not in s: s = s.replace(a, a + add); p.write_text(s, encoding="utf-8")
print("doors, llms, sitemap")
