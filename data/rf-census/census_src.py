"""The Revelation First field census, first batch (2026-10-30). Writes census.json.

Operator, 2026-10-30: revelationfirst.com takes the fleet's meta-aggregator function, less prominently foregrounded than on the other
sites, across New Testament scholarship, papyrology and textual discovery, AI and ancient texts, and AI and scripture ("adopted as
worded. lets build."). Organizing question: what evidence does each resource hold on when and from what the New Testament writings
were composed, and how do machines now read those texts?

Each row is written in rows/<slug>.py from the saved sources only (sources/, dated and hashed in sources/manifest.json, fetched with
the archive's own user agent). Every quoted value is checked verbatim (whitespace-normalised) against the saved text of its source.
Fields without a quote are readings. A resource's own terms and findings are kept as its own; where it meets the Revelation First
workstreams is stated separately, in rf_intersection, as the archive's reading.
"""
import json, pathlib, re
HERE = pathlib.Path(__file__).parent
MAN = json.load(open(HERE / "sources/manifest.json"))

INTERSECTIONS = {
    "nt-scholarship": "New Testament scholarship: dating, authorship and literary dependence",
    "papyrology-discovery": "Papyrology and textual discovery: manuscripts, editions, new finds and redatings",
    "ai-ancient-texts": "AI and ancient texts: machine reading, restoration and dating",
    "ai-scripture": "AI and scripture: how AI systems represent, cite and summarize sacred texts",
}
EVIDENCE_KINDS = ["manuscript images", "transcription or edition", "critical apparatus", "catalogue or metadata", "palaeographic dating",
                  "physical or radiocarbon dating", "machine reading, restoration or dating", "dating table", "dependence argument",
                  "bibliography or directory", "AI representation record", "community or policy resource"]


def Q(src, quote, basis="operator"):
    return {"src": src, "basis": basis, "quote": quote}


ROWS = []
def row(**r): ROWS.append(r)


ORDER = ["csntm", "oxyrhynchus-online", "bodmer-lab", "dss-digital-library", "early-christian-writings",
         "enoch-dss-dating", "ithaca", "aeneas", "vesuvius-challenge", "ai-and-faith", "capture-registry"]
for slug in ORDER:
    p = HERE / "rows" / f"{slug}.py"
    if p.exists():
        exec(compile(p.read_text(encoding="utf-8"), str(p), "exec"), {"row": row, "Q": Q})

# candidates named in the adopted plan whose own pages could not be read from the build environment on 2026-10-30;
# no row is written for a resource whose sources were not read
PENDING = {
    "intf-ntvmr": {"name": "INTF New Testament Virtual Manuscript Room (Münster)", "url": "https://ntvmr.uni-muenster.de/",
                   "reason": "connection refused from the build environment; the INTF home page was read and carries news only"},
    "codex-sinaiticus": {"name": "Codex Sinaiticus Project", "url": "https://www.codexsinaiticus.org/en/",
                         "reason": "connection refused; the British Library's page returned its post-cyber-attack notice"},
    "papyri-info": {"name": "papyri.info", "url": "https://papyri.info/", "reason": "served a bot-check page (Anubis) to the archive's user agent"},
    "ldab": {"name": "Leuven Database of Ancient Books", "url": "https://www.trismegistos.org/ldab/", "reason": "connection refused"},
    "trismegistos": {"name": "Trismegistos", "url": "https://www.trismegistos.org/", "reason": "HTTP 403 and connection refused"},
    "llm-religious-text-emory": {"name": "When Large Language Models Meet Religious Text (Emory thesis)", "url": "https://etd.library.emory.edu/concern/etds/j9602216f",
                                 "reason": "HTTP 405"},
    "nt-gateway": {"name": "The New Testament Gateway", "url": "https://www.ntgateway.com/",
                   "reason": "the domain now serves Logos's 'Lecture Hall' pages; the directory itself was not found there"},
}

# ---------------------------------------------------------------- write
def norm(s): return re.sub(r"\s+", " ", s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')).strip()
problems = []
REQ = ["slug", "name", "url", "operator", "intersections", "evidence_kind", "kind", "unit", "text_object", "method",
       "findings", "stated_limits", "answers", "does_not_answer", "rf_intersection", "lifecycle", "version_and_time", "negative_tags", "evidence"]
for r in ROWS:
    miss = [k for k in REQ if k not in r]
    if miss: problems.append((r.get("slug"), "missing fields", miss))
    for i in r.get("intersections") or []:
        if i not in INTERSECTIONS: problems.append((r["slug"], "unknown intersection", i))
    for k in r.get("evidence_kind") or []:
        if k not in EVIDENCE_KINDS: problems.append((r["slug"], "unknown evidence kind", k))
    srcs = {}
    for f, ev in r["evidence"].items():
        sid = ev["src"]
        if sid not in MAN:
            problems.append((r["slug"], f, "source not saved", sid)); continue
        srcs[sid] = {"url": MAN[sid]["url"], "read": MAN[sid]["fetched"][:10], "sha256": MAN[sid]["sha256"], "http": MAN[sid]["http"]}
        if ev.get("quote"):
            txt = norm((HERE / "sources" / f"{sid}.txt").read_text(encoding="utf-8"))
            if norm(ev["quote"]) not in txt:
                problems.append((r["slug"], f, sid, ev["quote"][:80]))
    r["sources"] = srcs
    r.setdefault("observed", {"on": "2026-10-30", "fetch": "read"})
unread = {k: {"url": v["url"], "http": v["http"], "fetched": v["fetched"]} for k, v in MAN.items() if v["http"] != "200" or v["text_chars"] < 300}
out = {"name": "Revelation First field census", "compiled": "2026-10-30", "schema_version": "1.0", "editor": "Lee Sharks",
       "schema_note": ("The fleet census core (slug, name, aka, url, operator, kind, unit, count, lifecycle, version_and_time, negative_tags, evidence, "
                       "relations, unchecked, sources), after Labor Vector's labor census, extended for the field around the Revelation First thesis: "
                       "intersections (one or more of four), evidence_kind, text_object (which texts), method, coverage, findings, stated_limits, "
                       "answers and does_not_answer (which questions of composition, dating and machine reading this kind of evidence can and cannot settle), "
                       "and rf_intersection (where it meets the Revelation First workstreams: the archive's reading, kept apart from the resource's own terms). "
                       "Every quote is verbatim from a saved source."),
       "organizing_question": ("What evidence does each resource hold on when and from what the New Testament writings were composed, "
                               "and how do machines now read those texts?"),
       "correction": ("Revelation First ≠ Revelation Early. The pre-70 date is the old argument (Robinson, 1976; Gentry, 1989); Revelation First "
                      "is the priority thesis: the rest of the New Testament unfolds from the Apocalypse."),
       "intersections": INTERSECTIONS, "evidence_kinds": EVIDENCE_KINDS, "pending": PENDING, "unread_sources": unread, "rows": ROWS}
json.dump(out, open(HERE / "census.json", "w"), ensure_ascii=False, indent=1)
print(len(ROWS), "rows;", sum(len(r["evidence"]) for r in ROWS), "evidence items;", len(problems), "problems")
for p in problems: print("  ", p)
