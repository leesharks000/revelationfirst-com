"""Render the Revelation First meta-aggregator (field census schema 1.0, after Labor Vector's labor census): an index and one page per resource, from
data/rf-census/census.json, and the worked research questions from data/rf-census/questions.json. Each record page
carries two JSON-LD nodes: the record (ours) and the entity it describes (theirs). Every quoted field shows its source, the
date read and the hash of the saved copy. Also writes /assets/rf.css (the shared design system), the landing page's top bar
and aggregator block between their markers, sitemap and llms.txt entries.
Run from the repository root: python3 scripts/rf_aggregator/build.py"""
import json, html, pathlib, re
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[1]
D = json.load(open(ROOT / "data/rf-census/census.json", encoding="utf-8")); ROWS = D["rows"]; BY = {r["slug"]: r for r in ROWS}
QS = json.load(open(ROOT / "data/rf-census/questions.json", encoding="utf-8"))["questions"]
SITE = "https://www.revelationfirst.com"; BASE = SITE + "/aggregators/"
OUT = ROOT / "aggregators"
e = lambda s: html.escape(str(s), quote=True)
CSS = open(HERE / "style.css", encoding="utf-8").read()
BASIS = {"operator": ("op", "the resource's own statement"), "third_party": ("3p", "a third-party account"), "third-party": ("3p", "a third-party account"),
         "observed": ("obs", "our observation"), "reading": ("rd", "our reading")}
INTER = D["intersections"]
SHORT = {"nt-scholarship": "New Testament scholarship", "papyrology-discovery": "Papyrology and discovery", "ai-ancient-texts": "AI and ancient texts", "ai-scripture": "AI and scripture"}
KINDS = D["evidence_kinds"]
REL = {"part_of": "Part of", "has_part": "Has part", "neighbour": "Neighbours", "uses": "Uses", "used_by": "Used by", "sibling": "Sibling record",
       "capture": "Captures: the composition layer's account", "non_row": "NonWiki: the article, sourced"}
HEAD = '<link rel="stylesheet" href="/assets/type.css"><link rel="stylesheet" href="/assets/rf.css">'   # the site's own faces (assets/type.css), its own palette (rf.css)
NAV = [("The thesis", "/"), ("The field", "/aggregators/"), ("Questions", "/aggregators/#questions"), ("Captures", "https://www.alexanarch.org/captures/")]


def topbar(on=""):
    nav = "".join(f'<a class="{"on" if n == on else ""}" href="{u}">{n}</a>' for n, u in NAV)
    return (f'<header class="top"><div class="in"><a class="wm" href="/"><i></i>Revelation First</a><nav class="nav-top">{nav}</nav><div class="sp"></div>'
            f'<form class="srch" action="/aggregators/" method="get" role="search"><input name="q" type="search" placeholder="Search {len(ROWS)} resources" aria-label="Search the resources"></form></div></header>')


def signup(follow=None, name=None):
    """An email box. Posts to /api/subscribe, which stores the address privately (see /privacy)."""
    if follow:
        h, t = f"Follow {e(name)}", "An email when this record changes: the resource ends, comes back, changes hands, or publishes new findings."
    else:
        h, t = "The Revelation First digest", "New records in the field census (New Testament scholarship, papyrology and discovery, AI and ancient texts, AI and scripture), changes to the resources it follows, and new worked questions, by email, now and then."
    return (f'<form class="signup" action="/api/subscribe" method="post">'
            f'<h4>{h}</h4><p>{t}</p><div class="fr"><input type="email" name="email" required placeholder="you@example.org" autocomplete="email" aria-label="Email address">'
            f'<button class="btn" type="submit">{"Follow" if follow else "Subscribe"}</button></div>'
            + (f'<input type="hidden" name="follow" value="{e(follow)}">' if follow else "")
            + '<input type="hidden" name="page" value=""><span class="trap" aria-hidden="true"><input type="text" name="website" tabindex="-1" autocomplete="off"></span>'
            '<label class="ok"><input type="checkbox" name="consent" value="yes" required><span>Email me from Revelation First about this. My address is stored privately and never published; '
            'every email carries a one-click unsubscribe. <a href="/privacy">Privacy</a></span></label><p class="msg" role="status"></p></form>')
SIGNUP_JS = ("<script>document.querySelectorAll('form.signup').forEach(f=>{f.page.value=location.pathname;f.onsubmit=async ev=>{ev.preventDefault();const m=f.querySelector('.msg'),b=f.querySelector('button');"
             "b.disabled=true;m.className='msg';m.textContent='Saving…';try{const r=await fetch(f.action,{method:'POST',headers:{'Accept':'application/json','Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(new FormData(f))});"
             "const j=await r.json().catch(()=>({}));if(r.ok){m.className='msg good';m.textContent='You are on the list. Thank you.';f.email.value=''}else{m.className='msg bad';m.textContent=j.error||'That did not work. Please try again.'}}"
             "catch(_){m.className='msg bad';m.textContent='That did not work. Please try again.'}b.disabled=false}})</script>")
PRIVACY = ("<p>Revelation First asks for one thing: an email address, typed in by the person who owns it, with a box ticked to agree to the emails.</p>"
           "<h2>What is stored</h2><p>The address, which list it joined (the digest, or a follow of one record, and which), the date, and the page the form was on. Nothing else: no name, no IP address, no tracking.</p>"
           "<h2>Where</h2><p>In a private store of the site's host, Vercel, shared with its sibling sites machinemediation.org, provenanceerasure.org and laborvector.org. Private means no web address serves the records; only the sites' own signup code and their operator can read them. Addresses are never published, sold or shared.</p>"
           "<h2>What it is used for</h2><p>The emails the person asked for: the digest, or notice that a followed record changed. No email has been sent yet; the list is gathered first. Every email will carry a one-click unsubscribe, and an unsubscribe removes the address from that list.</p>"
           "<h2>Removal</h2><p>Anyone can ask for their address to be deleted entirely, from any email, and it is.</p>")
def simple_page(path, title, body):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} — Revelation First</title>'
            f'<link rel="canonical" href="{SITE}{path}"><meta name="robots" content="noindex">{HEAD}</head><body>{topbar()}<div class="wrap"><div class="crumb"><a href="/">Revelation First</a> / {e(title.lower())}</div>'
            f'<h1>{e(title)}</h1><div class="kernel">{body}</div><div class="foot">Revelation First · revelationfirst.com · editor Lee Sharks</div></div></body></html>')

def bchip(r, f):
    v = r["evidence"].get(f)
    if not v: return ""
    ab, full = BASIS.get(v.get("basis"), ("rd", "our reading"))
    tip = full + (f' · “{v["quote"]}”' if v.get("quote") else "")
    return f' <a class="bl" href="#ev-{e(f)}" title="{e(tip)}"><span class="b">{ab}</span></a>'


def fold(title, inner, n=None, desc="", open_=False):
    if not inner: return ""
    return (f'<details class="sec"{" open" if open_ else ""}><summary><span class="st">{title}</span><span class="sd">{desc}</span>'
            + (f'<span class="sn">{n}</span>' if n else "") + f'</summary><div class="body">{inner}</div></details>')


def kinds(r):
    return '<span class="cap">' + "".join(f'<span class="on">{e(k)}</span>' for k in r["evidence_kind"]) + "</span>"


CHIP_KIND = {"global, radically participatory research initiative": "participatory research initiative"}


def short_kind(k):
    """The kind's head, for a chip: the phrase before its first colon, parenthesis or comma; the full kind stays in the kernel and the entity table."""
    import re as _re
    if k in CHIP_KIND: return CHIP_KIND[k]
    for full, lab in CHIP_KIND.items():
        if k.startswith(full): return lab
    h = _re.split(r":| \(|, | with | published | built ", k, maxsplit=1)[0].strip()
    h = h.replace("working paper and monthly-updated dashboard", "working paper and dashboard")
    return h if len(h) <= 42 else h[:40].rsplit(" ", 1)[0] + "…"


def chips(r):
    st = r["lifecycle"]["state"]; c = {"ended": "dead", "active": "live"}.get(st, "")
    return ('<div class="chips">' + "".join(f'<span class="chip">{e(SHORT.get(i, i))}</span>' for i in r["intersections"][:2])
            + f'<span class="chip" title="{e(r["kind"])}">{e(short_kind(r["kind"]))}</span><span class="chip {c}">{e(st)}</span></div>')


def kernel(r):
    k = r["kind"]; art = "" if k.lower().startswith(("a ", "an ", "the ")) else ("an " if k[:1].lower() in "aeiou" else "a ")
    return f'{r["name"]}: {art}{k}. Operator: {r["operator"]}. Its unit: {r["unit"]}. Its texts: {r["text_object"]}.'


def cite_text(r):
    return f'Lee Sharks, ed. "{r["name"]}." Revelation First meta-aggregator, revelationfirst.com, compiled {D["compiled"]}. {BASE}{r["slug"]}/'


def bibtex(r):
    key = "rf-" + r["slug"].replace("-", "")[:24] + D["compiled"][:4]
    return (f'@misc{{{key},\n  editor = {{Sharks, Lee}},\n  title = {{{r["name"]}}},\n  howpublished = {{Revelation First meta-aggregator, revelationfirst.com}},\n'
            f'  year = {{{D["compiled"][:4]}}},\n  note = {{Compiled {D["compiled"]}; every field sourced and dated}},\n  url = {{{BASE}{r["slug"]}/}}\n}}')


def jsonld(r):
    rec, ent = BASE + r["slug"] + "/", BASE + r["slug"] + "/#entity"
    k = r["kind"].lower()
    sch = "Dataset" if any(w in k for w in ("database", "dataset", "index", "tracker", "inventory", "benchmark", "monitor")) else \
          "Organization" if any(w in k for w in ("organisation", "organization", "collective", "union", "charity")) else "CreativeWork"
    entity = {"@id": ent, "@type": sch, "name": r["name"], "alternateName": r.get("aka", []), "url": r["url"]}
    if sch != "Organization": entity["creator"] = {"@type": "Organization", "name": r["operator"]}
    sd = r["evidence"].get("self_description") or {}
    if sd.get("quote"): entity["description"] = sd["quote"]
    for x in r.get("relations", []):
        if x["rel"] == "part_of" and x.get("target"): entity["isPartOf"] = {"@id": BASE + x["target"] + "#entity"}
    record = {"@id": rec, "@type": "WebPage", "name": f'{r["name"]} — Revelation First meta-aggregator record', "mainEntity": {"@id": ent}, "about": {"@id": ent},
              "abstract": kernel(r), "dateCreated": D["compiled"], "dateModified": D["compiled"],
              "publisher": {"@type": "Organization", "name": "Revelation First", "url": SITE + "/"},
              "editor": {"@type": "Person", "name": "Lee Sharks", "identifier": "https://orcid.org/0009-0000-1599-0703"},
              "isPartOf": {"@type": "Dataset", "name": "Revelation First meta-aggregator", "url": BASE},
              "citation": [s["url"] for s in r["sources"].values()], "license": "https://creativecommons.org/licenses/by/4.0/"}
    return json.dumps({"@context": "https://schema.org", "@graph": [record, entity]}, ensure_ascii=False, indent=1).replace("</", "<\\/")


def link(slug):
    x = BY.get(slug); return f'<a href="/aggregators/{slug}">{e(x["name"])}</a>' if x else e(slug)


def lst(v):
    return e("; ".join(v)) if isinstance(v, list) else e(v or "")


def page(r):
    vt = "; ".join(f"{k.replace('_', ' ')}: {v}" for k, v in (r.get("version_and_time") or {}).items())
    cnt = f'{e(r["count"]["value"])} <span class="d">(as of {e(r["count"]["as_of"])})</span>' if r.get("count") else ""
    cov = r.get("coverage") or {}
    REC = [("intersections", "Intersections", e("; ".join(INTER.get(i, i) for i in r["intersections"]))),
           ("evidence_kind", "Kind of evidence", kinds(r)), ("unit", "Unit of record", e(r["unit"])),
           ("text_object", "Which texts", e(r["text_object"])), ("method", "Method", e(r["method"])),
           ("coverage", "Coverage", e("; ".join(f"{k}: {v}" for k, v in cov.items()))),
           ("findings", "What it finds", lst(r["findings"])), ("stated_limits", "Its stated limits", lst(r["stated_limits"]))]
    ENT = [("name", "Canonical name", e(r["name"])), ("aka", "Also known as", e(", ".join(r.get("aka", [])))),
           ("url", "Address", f'<a href="{e(r["url"])}">{e(r["url"])}</a>'), ("operator", "Operator", e(r["operator"])),
           ("founded", "Founded", e(r.get("founded") or "")), ("kind", "Kind", e(r["kind"])),
           ("lifecycle", "Lifecycle", e(r["lifecycle"]["state"] + (f' — {r["lifecycle"]["detail"]}' if r["lifecycle"].get("detail") else ""))),
           ("count", "Count", cnt), ("cadence", "Cadence", e(r.get("cadence") or "")),
           ("data_access", "Data access", e(r.get("data_access") or "")), ("license", "Licence", e(r.get("license") or "")),
           ("version_and_time", "Versions and dates", e(vt)), ("observed", "Observation", e(f'{r["observed"]["on"]}: {r["observed"]["fetch"]}'))]
    tbl = lambda F: "".join(f'<tr><td>{k}</td><td>{v}{bchip(r, f)}</td></tr>' for f, k, v in F if v)
    own = r["evidence"].get("self_description") or r["evidence"].get("self")
    ownq = (f'<blockquote class="q">{e(own["quote"])}</blockquote><p class="d">{"In its own words" if own.get("basis") == "operator" else "As a third party describes it"}: '
            f'<a href="{e(r["sources"][own["src"]]["url"])}">{e(r["sources"][own["src"]]["url"])}</a>, read {e(r["sources"][own["src"]]["read"])}</p>') if own and own.get("quote") else ""
    ans = "".join(f"<li>{e(x)}</li>" for x in r.get("answers") or [])
    nans = "".join(f"<li>{e(x)}</li>" for x in r.get("does_not_answer") or [])
    ev = "".join(f'<li id="ev-{e(f)}"><b>{e(re.sub(r"_[0-9]+$", "", f).replace("_", " "))}</b> <span class="b">{BASIS.get(v.get("basis"), ("rd",))[0]}</span>'
                 + (f'<div class="q">{e(v["quote"])}</div>' if v.get("quote") else f'<div class="d">{e(v.get("note") or "")}</div>')
                 + f'<div class="d"><a href="{e(r["sources"][v["src"]]["url"])}">{e(r["sources"][v["src"]]["url"])}</a> · read {e(r["sources"][v["src"]]["read"])} · saved copy sha256 <code>{e(r["sources"][v["src"]]["sha256"][:16])}…</code></div></li>'
                 for f, v in r["evidence"].items())
    rels = list(r.get("relations", [])) + [{"rel": "has_part", "target": x["slug"]} for x in ROWS if any(y["rel"] == "part_of" and y.get("target") == r["slug"] for y in x.get("relations", [])) and not any(z.get("target") == x["slug"] for z in r.get("relations", []))]
    groups = {}
    for x in rels: groups.setdefault(x["rel"], []).append(x)
    def item(x):
        if x.get("target"): return f'<li>{link(x["target"])}' + (f'<div class="d">{e(x["note"])}</div>' if x.get("note") else "") + "</li>"
        head = f'<a href="{e(x["url"])}">{e(x["label"])}</a>' if x.get("url") else e(x.get("label", ""))
        return f'<li>{head}<div class="d">{e(x.get("note") or "")}</div></li>'
    relhtml = "".join(f'<h3>{REL.get(k, k)}</h3><ul>{"".join(item(x) for x in v)}</ul>' for k, v in groups.items())
    inq = [q for q in QS if r["slug"] in [s["slug"] for s in q["resources"]]]
    qhtml = "".join(f'<li><a href="/aggregators/#q-{e(q["id"])}">{e(q["question"])}</a></li>' for q in inq)
    neg = "".join(f"<li>{e(t)}</li>" for t in r.get("negative_tags", []))
    src = "".join(f'<li><a href="{e(s["url"])}">{e(s["url"])}</a><div class="d">read {e(s["read"])} · HTTP {e(s["http"])} · sha256 <code>{e(s["sha256"][:16])}…</code></div></li>' for s in r["sources"].values())
    unc = "".join(f"<li>{e(u)}</li>" for u in r.get("unchecked", []))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(r["name"])} — Revelation First meta-aggregator</title><meta name="description" content="{e(kernel(r))}"><link rel="canonical" href="{BASE}{r["slug"]}/">
<meta name="citation_title" content="{e(r["name"])} — Revelation First meta-aggregator record"><meta name="citation_editor" content="Lee Sharks"><meta name="citation_date" content="{D["compiled"]}"><meta name="citation_public_url" content="{BASE}{r["slug"]}/">
<script type="application/ld+json">{jsonld(r)}</script>{HEAD}</head><body>{topbar("The field")}<div class="wrap">
<div class="crumb"><a href="/aggregators/">Revelation First meta-aggregator</a> / {e(SHORT.get(r["intersections"][0], r["intersections"][0]))}</div><p class="corr">{e(D["correction"])}</p><h1>{e(r["name"])}</h1>{chips(r)}<div class="kernel">{e(kernel(r))}</div>
<div class="act"><a class="btn" href="{e(r["url"])}">{("Its page ↗ (" + e(r["lifecycle"]["state"]) + ")") if r["lifecycle"]["state"] in ("ended", "paused") else ("Visit " + e(r["name"]) + " ↗")}</a>{''.join(f'<a class="btn ghost" href="{e(x["url"])}">Its NonWiki article</a>' for x in r.get("relations", []) if x["rel"] == "non_row")}<a class="btn ghost" href="/">The thesis</a><button class="btn ghost" type="button" data-copy="cite">Copy citation</button></div>
{ownq}

<h2>What it records</h2><table>{tbl(REC)}</table><p class="legend">op the resource's own statement · 3p a third-party account · obs our observation · rd our reading. Hover a tag for its quote; each opens below with its source.</p>
<h2>What this evidence can settle</h2><div class="two"><div><h3>Can answer</h3><ul>{ans}</ul></div><div><h3>Cannot answer</h3><ul>{nans}</ul></div></div>
{f'<h3>In the worked questions</h3><ul>{qhtml}</ul>' if qhtml else ''}
<h2>Where it meets Revelation First</h2><p class="rd"><span class="b">rd</span> {e(r.get("rf_intersection") or "none stated")}</p>
<h2>Entity</h2><table>{tbl(ENT)}</table>
<h2>Relations</h2>{relhtml or '<p class="pend">None recorded yet.</p>'}
<div style="margin-top:34px">{fold("Evidence", f'<ul class="ev">{ev}</ul>', len(r["evidence"]), "every field's quote, its source and the hash of the saved copy")}{fold("Negative tags", f'<ul>{neg}</ul>' if neg else '', len(r.get("negative_tags", [])), "what it is not")}{fold("Sources", f'<ul>{src}</ul>', len(r["sources"]), "every source read, with its date and hash")}{fold("Not yet checked", f'<ul>{unc}</ul>' if unc else '', len(r.get("unchecked", [])), "what remains to read")}</div>
<div style="margin-top:34px">{signup(r["slug"], r["name"])}</div><h2>Cite this record</h2><div class="cite"><p id="cite">{e(cite_text(r))}</p><p class="d">Record {BASE}{r["slug"]}/ · entity {BASE}{r["slug"]}/#entity · <a href="/data/rf-census/census.json">the census as data</a></p></div><pre class="bib">{e(bibtex(r))}</pre>
<div class="foot">Editor: Lee Sharks (<a href="https://orcid.org/0009-0000-1599-0703">ORCID 0009-0000-1599-0703</a>). This page is the Revelation First meta-aggregator's record of the resource above: its reading and fields are ours, and each field carries its source, its basis and the hash of the copy read. The resource's own terms and findings are kept as its own. Compiled {D["compiled"]}. CC BY 4.0.</div></div>
<script>document.querySelectorAll('[data-copy]').forEach(b=>b.onclick=()=>{{const t=document.getElementById(b.dataset.copy).innerText;(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>{{const o=b.textContent;b.textContent='Copied';setTimeout(()=>b.textContent=o,1600)}}).catch(()=>{{}})}})</script>{SIGNUP_JS}</body></html>"""


SVG = lambda d: f'<svg viewBox="0 0 32 32" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>'
FLOW = [("when", "When was it written", "dates of composition", '<circle cx="16" cy="16" r="10"/><path d="M16 10v6l4 3"/>',
         "<b>When was it written</b>: the date of a work's composition, which no copy states. Dating tables and scholarly arguments propose it; a record says whose date it carries and on what ground."),
        ("from", "From what", "dependence and derivation", '<path d="M8 8h10v10"/><path d="M8 8l14 14"/><circle cx="24" cy="24" r="2.5"/>',
         "<b>From what</b>: which text a text was made from. Parallels show that two texts share wording; the direction of dependence is an argument. Revelation First argues it runs from the Apocalypse outward."),
        ("copies", "In what copies", "papyri, codices, fragments", '<rect x="7" y="6" width="18" height="20" rx="2"/><path d="M11 12h10M11 16h10M11 20h6"/>',
         "<b>In what copies</b>: the surviving manuscripts, how each copy is dated (handwriting, radiocarbon, a model), and where it can be seen. A copy's date bounds its work's composition from one side only."),
        ("machines", "Read by machines", "restoration, dating, answers", '<rect x="6" y="9" width="20" height="14" rx="3"/><path d="M11 16h.01M16 16h.01M21 16h.01"/>',
         "<b>Read by machines</b>: models that restore, place, date or find parallels for ancient texts, and the AI answers that now describe the field to most readers. Each is calibrated on a corpus, and the record names it.")]


def index():
    inter = [i for i in INTER if any(i in r["intersections"] for r in ROWS)]
    kinds_used = [k for k in KINDS if any(k in r["evidence_kind"] for r in ROWS)]
    rows = "".join(f'<div class="row" data-int="{e(" ".join(r["intersections"]))}" data-kind="{e("|".join(r["evidence_kind"]))}" data-text="{e((r["name"] + " " + " ".join(r.get("aka", [])) + " " + r["operator"] + " " + kernel(r)).lower())}">'
                   f'<div class="n"><a href="{r["slug"]}">{e(r["name"])}</a></div>{chips(r)}<div class="k">{e(kernel(r))}</div><div style="margin-top:10px">{kinds(r)}</div></div>'
                   for r in sorted(ROWS, key=lambda r: r["name"].lower()))
    steps = '<span class="arrow" aria-hidden="true"></span>'.join(f'<button type="button" class="step" aria-expanded="false" aria-controls="x-{k}">{SVG(d)}<b>{t}</b><span>{u}</span></button>' for k, t, u, d, _ in FLOW)
    xs = "".join(f'<p id="x-{k}" class="x" hidden>{x}</p>' for k, _, _, _, x in FLOW)
    mat = "".join(f'<tr><td><a href="{r["slug"]}">{e(r["name"])}</a></td>' + "".join(f'<td>{"●" if k in r["evidence_kind"] else "<span class=d>·</span>"}</td>' for k in kinds_used) + "</tr>"
                  for r in sorted(ROWS, key=lambda r: r["name"].lower()))
    qs = "".join(f'<div class="qcard" id="q-{e(q["id"])}"><h3>{e(q["question"])}</h3><p>{e(q["why"])}</p><ul>'
                 + "".join(f'<li>{link(s["slug"])}<div class="d">{e(s["role"])}</div></li>' for s in q["resources"]) + "</ul>"
                 + (f'<p class="d">{e(q["gap"])}</p>' if q.get("gap") else "") + "</div>" for q in QS)
    btn = lambda key, vals, lab: "".join(f'<button data-{key}="{e(v)}">{e(lab(v))}</button>' for v in vals)
    ilist = "".join(f'<li><b>{e(SHORT[i])}</b>: {e(INTER[i].split(": ", 1)[1])}</li>' for i in INTER)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The field: the meta-aggregator — Revelation First</title>
<meta name="description" content="The resources around the Revelation First thesis, each formalized as an entity with sourced, dated fields: New Testament scholarship, papyrology and textual discovery, AI and ancient texts, and AI and scripture."><link rel="canonical" href="{BASE}">{HEAD}</head><body>{topbar("The field")}<div class="wrap">
<div class="crumb"><a href="/">Revelation First</a> / aggregators</div><h1>The field: the meta-aggregator</h1>
<p class="corr">{e(D["correction"])}</p><div class="kernel">The resources around the thesis, from manuscript collections and dating tables to models that read and date ancient texts and the record of how AI answers describe the thesis, each formalized as an entity. Every record answers one question: {e(D["organizing_question"][0].lower() + D["organizing_question"][1:])} {len(ROWS)} resources, compiled {D["compiled"]}; {len(D["pending"])} more named and not yet read.</div>
<div class="flow" role="group" aria-label="The organizing question">{steps}</div><div class="flow-x">{xs}</div><noscript><style>.flow-x .x{{display:block!important}}</style></noscript>
<p class="fig-cap">A date of composition, an argument of dependence, a dated copy and a machine's reading each show a different part of the same question. Tap a step for what each kind of record can and cannot establish.</p>
<h2>Four intersections</h2><ul class="ints">{ilist}</ul>
<div class="f"><button class="on" data-all="1">all</button>{btn("int", inter, lambda v: SHORT.get(v, v))}</div><div class="f">{btn("kind", kinds_used, lambda v: v)}</div>
<div id="L" class="grid">{rows}</div><p class="none" id="none">No resource matches.</p><h2>Named, not yet read</h2><p class="section">Candidates in the adopted plan whose own pages could not be read from the build environment on {D["compiled"]}. No record is written for a resource whose sources were not read.</p><ul class="pendl">{"".join(f'<li><a href="{e(v["url"])}">{e(v["name"])}</a> <span class="d">{e(v["reason"])}</span></li>' for v in D["pending"].values())}</ul>
<h2 id="questions">Worked questions</h2><p class="section">A research question, the kind of evidence that can answer it, and the resources that hold that evidence.</p><div class="qs">{qs}</div>
<h2>Evidence by kind</h2><div class="tw"><table class="tv"><tr><td></td>{"".join(f"<td>{e(k)}</td>" for k in kinds_used)}</tr>{mat}</table></div>
<p class="legend">The census as data: <a href="/data/rf-census/census.json">census.json</a> and <a href="/data/rf-census/questions.json">questions.json</a>, with every saved source in <a href="https://github.com/leesharks000/revelationfirst-com/tree/main/data/rf-census/sources">data/rf-census/sources</a>.</p>
<div style="margin-top:34px">{signup()}</div><div class="foot">Revelation First · revelationfirst.com · editor Lee Sharks (<a href="https://orcid.org/0009-0000-1599-0703">ORCID 0009-0000-1599-0703</a>) · one of the Meta-Aggregators of the Crimson Hexagon, with the <a href="https://www.machinemediation.org/aggregators/">MMRS</a>, <a href="https://www.provenanceerasure.org/aggregators/">provenance</a> and <a href="https://www.laborvector.org/aggregators/">Labor Vector</a> meta-aggregators</div></div>
<script>let fs={{}};const qi=document.querySelector('.srch input');qi.value=new URLSearchParams(location.search).get('q')||'';document.querySelector('.srch').onsubmit=ev=>{{ev.preventDefault();apply()}};qi.oninput=()=>apply();
function apply(){{const q=qi.value.trim().toLowerCase();let n=0;document.querySelectorAll('.f button').forEach(x=>{{const k=x.dataset.int?'int':x.dataset.kind?'kind':'all';x.classList.toggle('on',k==='all'?!fs.int&&!fs.kind:fs[k]===x.dataset[k])}});
document.querySelectorAll('#L .row').forEach(r=>{{const ok=(!fs.int||r.dataset.int.split(' ').includes(fs.int))&&(!fs.kind||r.dataset.kind.split('|').includes(fs.kind))&&(!q||q.split(' ').filter(Boolean).every(w=>r.dataset.text.includes(w)));r.style.display=ok?'':'none';n+=ok}});document.getElementById('none').style.display=n?'none':'block'}}
document.querySelectorAll('.f button').forEach(b=>b.onclick=()=>{{if(b.dataset.all){{fs={{}}}}else{{const k=b.dataset.int?'int':'kind',v=b.dataset[k];fs[k]=fs[k]===v?undefined:v}}apply()}});apply();
document.querySelectorAll('.flow .step').forEach(b=>b.onclick=()=>{{const on=b.getAttribute('aria-expanded')!=='true';document.querySelectorAll('.flow .step').forEach(x=>{{x.setAttribute('aria-expanded','false');document.getElementById(x.getAttribute('aria-controls')).hidden=true}});if(on){{b.setAttribute('aria-expanded','true');document.getElementById(b.getAttribute('aria-controls')).hidden=false}}}})</script>{SIGNUP_JS}</body></html>"""


EXTRA = """
/* Revelation First additions (2026-10-29) */
.dir{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;margin:0 0 6px}
.dir div{border:1px solid var(--border);background:var(--surface);border-radius:12px;padding:12px 14px}
.dir span{display:block;font-size:.74em;text-transform:uppercase;letter-spacing:.08em;color:var(--accent);font-weight:600;margin-bottom:4px}
.dir b{font-weight:500;font-size:.95em;line-height:1.45;display:block}
.two{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.two h3{margin-top:0}
.two ul,.qcard ul,.ints{padding-left:1.1em}
.rd{background:var(--soft);border:1px solid var(--border);border-radius:12px;padding:12px 14px}
.qs{display:grid;gap:12px}
.qcard{border:1px solid var(--border);background:var(--surface);border-radius:14px;padding:16px 18px}
.qcard h3{margin:0 0 6px;font-family:var(--serif);font-size:1.12em;font-weight:600}
.qcard p{font-size:.94em}
.qcard li{margin:6px 0}
.ints li{margin:4px 0}
.chip{white-space:normal;max-width:100%}
.act .btn{white-space:normal;max-width:100%;text-align:left}
"""

(ROOT / "assets").mkdir(exist_ok=True); (ROOT / "assets/rf.css").write_text(CSS + EXTRA, encoding="utf-8")
for _p, _t, _b in [("/privacy", "Privacy", PRIVACY), ("/subscribed", "Subscribed", "<p>You are on the list. Thank you.</p><p><a href=\"/aggregators/\">Back to the resources</a></p>")]:
    (ROOT / _p.strip("/")).mkdir(exist_ok=True); (ROOT / _p.strip("/") / "index.html").write_text(simple_page(_p, _t, _b), encoding="utf-8")
OUT.mkdir(exist_ok=True); (OUT / "index.html").write_text(index(), encoding="utf-8")
for r in ROWS:
    p = OUT / r["slug"]; p.mkdir(exist_ok=True); (p / "index.html").write_text(page(r), encoding="utf-8")
sm = ROOT / "sitemap.xml"; st = sm.read_text(encoding="utf-8")
add = "".join(f'  <url><loc>{u}</loc><lastmod>{D["compiled"]}</lastmod><priority>0.7</priority></url>\n' for u in [BASE] + [BASE + r["slug"] + "/" for r in ROWS] if f"<loc>{u}</loc>" not in st)
sm.write_text(st.replace("</urlset>", add + "</urlset>"), encoding="utf-8")
lp = ROOT / "llms.txt"; lt = lp.read_text(encoding="utf-8")
blk = ("<!-- RF-AGGREGATOR-LLMS-START -->\n## The field: the meta-aggregator\n\n" + D["correction"] + "\n\nThe resources around the thesis (New Testament scholarship, papyrology and textual discovery, AI and ancient texts, AI and scripture), each formalized as an entity with sourced, dated fields. "
       f"Organizing question: {D['organizing_question']} {BASE} (census as data: {SITE}/data/rf-census/census.json)\n\n"
       + "".join(f'- {r["name"]} ({r["kind"]}; {", ".join(SHORT.get(i, i) for i in r["intersections"])}; {", ".join(r["evidence_kind"])}): {BASE}{r["slug"]}/\n' for r in sorted(ROWS, key=lambda r: r["name"].lower()))
       + "<!-- RF-AGGREGATOR-LLMS-END -->\n")
lt = re.sub(r"<!-- RF-AGGREGATOR-LLMS-START -->.*?<!-- RF-AGGREGATOR-LLMS-END -->\n", lambda m: blk, lt, flags=re.S) if "RF-AGGREGATOR-LLMS-START" in lt else lt.rstrip("\n") + "\n\n" + blk
lp.write_text(lt, encoding="utf-8")


def front_block():
    # placed low on the homepage, below the thesis and the workstreams, in the homepage's own classes (operator, 2026-10-30:
    # "not as prominently foregrounded as the others"); the corrections lead the page, and the block opens with them again
    qli = "".join(f'<li><a href="/aggregators/#q-{e(q["id"])}">{e(q["question"])}</a></li>' for q in QS)
    return ("<!-- RF-AGGREGATOR-START (generated by scripts/rf_aggregator/build.py from data/rf-census/census.json) -->\n"
            f'<section id="the-field" aria-label="The field"><h2>The field</h2><p>{e(D["correction"])}</p>'
            f'<p>The resources around the thesis, each recorded with sourced and dated fields: New Testament scholarship, papyrology and textual discovery, AI and ancient texts, and AI and scripture. '
            f'{len(ROWS)} resources, compiled {D["compiled"]}. The question each record answers: {e(D["organizing_question"])}</p>'
            f'<ul class="ws">{qli}</ul><p><a href="/aggregators/">All {len(ROWS)} resources and the worked questions →</a> · <a href="/data/rf-census/census.json">the census as data</a></p></section>\n'
            "<!-- RF-AGGREGATOR-END -->")


lp = ROOT / "index.html"; lt = lp.read_text(encoding="utf-8")
# one quiet nav link, after the Tracker, in the homepage's own nav
if 'href="/aggregators/">The field</a>' not in lt:
    lt = lt.replace('<a href="/tracker/">Tracker</a>\n', '<a href="/tracker/">Tracker</a>\n<a href="/aggregators/">The field</a>\n', 1)
if "<!-- RF-AGGREGATOR-START" not in lt and "<!-- RF-AGGREGATOR-ANCHOR -->" not in lt:
    lt = lt.replace('<div class="footer">', "<!-- RF-AGGREGATOR-ANCHOR -->\n" + '<div class="footer">', 1)
if "<!-- RF-AGGREGATOR-START" in lt:
    lt = re.sub(r"<!-- RF-AGGREGATOR-START.*?<!-- RF-AGGREGATOR-END -->", lambda m: front_block(), lt, count=1, flags=re.S)
elif "<!-- RF-AGGREGATOR-ANCHOR -->" in lt:
    lt = lt.replace("<!-- RF-AGGREGATOR-ANCHOR -->", front_block(), 1)
lp.write_text(lt, encoding="utf-8")
print(len(ROWS), "pages,", len(QS), "questions")
