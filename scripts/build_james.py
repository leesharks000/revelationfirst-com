#!/usr/bin/env python3
"""Render unfolding/james/derivation.json into unfolding/james/index.html.

The page carries the whole derivation as static HTML between the BUILD markers,
so a reader without JavaScript (and a machine fetcher) gets the seed, rules,
emissions, knot, coverage, measures, residue and slate. The script on the page
only replays the emissions; it no longer loads the data.

    python3 scripts/build_james.py          # write
    python3 scripts/build_james.py --check  # exit 1 if the page is out of date
"""
import html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / 'unfolding/james/derivation.json'
PAGE = ROOT / 'unfolding/james/index.html'
BEGIN, END = '<!-- BUILD:derivation -->', '<!-- /BUILD:derivation -->'
SUB_BEGIN, SUB_END = '<!-- BUILD:sub -->', '<!-- /BUILD:sub -->'

NUM = {2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight',
       9: 'Nine', 10: 'Ten', 11: 'Eleven', 12: 'Twelve', 13: 'Thirteen'}


def e(s):
    return html.escape(str(s), quote=True)


def render(D):
    els, rules, ems = D['seed']['elements'], D['rules'], D['emissions']
    rule = {r['id']: r for r in rules}
    fams = D.get('rule_families', {})
    nexp = len(fams.get('expand', {}).get('rules', []))
    nmatch = sum(len(m['matches']) for m in ems)
    anchors = D['coverage']['lexical_anchors']
    uq = sum(1 for a in anchors if 'unique' in a['status'])
    out = []
    w = out.append

    st = D.get('status')
    if st:
        w('<div class="working"><div class="lbl">WORKING SURFACE</div>'
          f'{e(st["note"])} <a href="{e(st["frozen_v1_0"])}">Frozen v1.0</a> · working since {e(st["working_since"])}.'
          '<ul>' + ''.join(f'<li>{e(c)}</li>' for c in st['changes_since_v1_0']) + '</ul></div>')

    w('<h2>The seed — Revelation 2:8–11</h2>')
    w(f'<div class="stage"><div class="lbl">INPUT · {len(els)} TYPED ELEMENTS · FOUR VERSES</div>')
    w('<div class="seedtext">' + ' … '.join(
        f'<span class="se" title="{e(x["gloss"])}">{e(x["quote"])}<span class="sid">{e(x["id"])}</span></span>' for x in els) + '</div>')
    w('<div class="elemgrid">' + ''.join(
        f'<div class="elem"><span class="id">{e(x["id"])} · {e(x["name"])}</span> <span class="dim">({e(x["ref"])})</span><br>'
        f'<span class="gk">{e(x["greek"])}</span><br>{e(x["gloss"])}</div>' for x in els) + '</div>')
    if D['seed'].get('note'):
        w(f'<div class="note-s">{e(D["seed"]["note"])}</div>')
    w('</div>')

    w('<h2>The rules</h2>')
    w(f'<div class="stage"><div class="lbl">TRANSFORM M · {len(rules)} OPERATIONS · {len(fams)} FAMILIES</div>')
    w('<table class="rules">' + ''.join(
        f'<tr><td class="op">{e(r["id"])} {e(r["op"])}<br><span class="fam">{e(r.get("family", ""))}</span></td>'
        f'<td><span class="sig">{e(r["sig"])}</span><br>{e(r["gloss"])}</td></tr>' for r in rules) + '</table>')
    if fams:
        w('<div class="fams">' + ''.join(
            f'<div><span class="fam">{e(k)}</span> · {e(", ".join(v["rules"]))} — {e(v["operation"])}</div>' for k, v in fams.items()) + '</div>')
    w('</div>')

    w('<div class="runbar"><button class="runbtn" id="run" type="button">▶ &nbsp;APPLY M TO THE SEED</button></div>')
    w('<h2>The emissions</h2>')
    w('<div id="output">')
    for i, m in enumerate(ems):
        r = rule[m['rule']]
        w(f'<div class="em in" id="em{i}"><div class="head"><span class="op">{e(m["rule"])} {e(r["op"])}</span>'
          f'<span class="from">← {e(" + ".join(m["from"]))}</span></div><div class="prod">{e(m["produces"])}</div>')
        for x in m['matches']:
            w(f'<div class="match{" unique" if x.get("anchor") else ""}"><span class="ref">{e(x["ref"])}</span> '
              f'<span class="gk">{e(x["greek"])}</span><div class="q">“{e(x["quote"])}”</div><div class="note">{e(x["note"])}</div></div>')
        w('</div>')
    w('</div>')

    w('<h2>The arrow in the morphology</h2>')
    w('<div class="arrowbox"><div class="tag">REV 2:10 — THE PROMISE PERFORMED (FIRST-PERSON FUTURE)</div>'
      '<div class="gk">δώσω σοι τὸν στέφανον τῆς ζωῆς</div><div class="big">↓</div>'
      '<div class="tag">JAS 1:12 — THE PROMISE CITED (AORIST)</div>'
      '<div class="gk">τὸν στέφανον τῆς ζωῆς, ὃν ἐπηγγείλατο τοῖς ἀγαπῶσιν αὐτόν</div><div class="big">↓</div>'
      '<div class="tag">JAS 2:5 — THE RECEIPT CLAUSE AGAIN, ON THE KINGDOM</div>'
      '<div class="gk">τῆς βασιλείας ἧς ἐπηγγείλατο τοῖς ἀγαπῶσιν αὐτόν</div>'
      '<div class="txt">"I <i>will give</i> thee the crown of life" → "the crown of life <i>which he promised</i>." A promise made, then a promise cited. '
      'The only two occurrences of the phrase in the canon, and the grammar carries the direction: performance, then receipt. '
      'James uses the receipt clause twice, the second time in the verse that holds Smyrna\'s poverty and riches.</div></div>')

    k = D.get('knot')
    if k:
        w(f'<h2>The knot — {e(k["ref"])}</h2>')
        w(f'<div class="stage"><div class="lbl">SIX VERSES · {NUM.get(len(k["items"]), len(k["items"])).upper()} SEED ELEMENTS</div><p class="kn">{e(k["note"])}</p>')
        w('<table class="anchors">' + ''.join(
            f'<tr><td class="a">{e(x["seed"])}</td><td class="gk2">Rev {e(x["rev"])}</td><td class="gk2">Jas {e(x["jas"])}</td></tr>' for x in k['items']) + '</table></div>')

    w('<h2>Coverage</h2>')
    w('<div class="stage"><div class="lbl">DERIVED PERICOPES</div><div class="chips">' +
      ''.join(f'<span class="chip">Jas {e(p)}</span>' for p in D['coverage']['derived_pericopes']) + '</div>')
    w('<div class="lbl" style="margin-top:12px">LEXICAL ANCHORS</div><table class="anchors">' + ''.join(
        f'<tr><td class="a">{e(a["anchor"])}</td><td class="{"u" if "unique" in a["status"] else ""}">{e(a["status"])}</td>'
        f'<td class="loc">{e(a["loci"])}</td></tr>' for a in anchors) + '</table>')
    w(f'<div class="stats">emissions: {len(ems)} · matches: {nmatch} · derived pericopes: {len(D["coverage"]["derived_pericopes"])} · '
      f'lexical anchors: {len(anchors)} ({uq} unique-in-canon) · residue pericopes: {len(D["residue"]["items"])}</div></div>')

    ms = D.get('measures')
    if ms:
        w('<h2>Measures</h2><div class="stage"><div class="lbl">SIX MEASURES FOR A DERIVATION BETWEEN TWO TEXTS</div><table class="anchors">' + ''.join(
            f'<tr><td class="a">{e(key)}</td><td>{e(val)}</td></tr>' for key, val in ms.items() if key != 'note') + '</table></div>')

    w('<h2>The residue — falsification surface</h2>')
    w('<div class="falsif"><div class="lbl">NOT DERIVED FROM THIS SEED · DISPLAYED PER WORKSTREAM 4</div>' + ''.join(
        f'<div class="res"><span class="ref">Jas {e(r["ref"].replace("Jas ", ""))}</span><span>{e(r["topic"])} — {e(r["note"])}</span>'
        f'<span class="cls">{e(r["class"].upper())}</span></div>' for r in D['residue']['items']) +
      '<div class="txt">Pericopes underivable through any plausible rule weigh against the case. A demonstrated reverse dependency of either unique anchor — James prior, Revelation citing — breaks it.</div></div>')

    w('<h2>The seven-letter slate</h2>')
    w('<p class="kn">The rough mapping across all seven, graded by evidence hardness — offered for ruling, not settled canon. This page executes the Smyrna row.</p>')
    w('<div class="stage" style="overflow-x:auto"><table class="slate"><tr><td class="g"><b>Letter</b></td><td><b>Epistle</b></td><td><b>Heteronym</b></td><td class="g"><b>Grade</b></td><td class="ev"><b>Evidence</b></td></tr>' + ''.join(
        '<tr' + (' class="this"' if r['letter'] == 'Smyrna' else '') + '>' +
        f'<td class="g">{e(r["letter"])}<br><span class="dim">{e(r["ref"])}</span></td>'
        f'<td>{e(r["epistle"])}</td><td>{e(r["heteronym"])}</td><td class="g">{e(r["grade"])}</td><td class="ev">{e(r["evidence"])}</td></tr>' for r in D['slate']['rows']) +
      '</table></div>')

    sub = (f'The executable granular case. {NUM.get(len(els), len(els))} seed elements from four verses. '
           f'{NUM.get(len(rules), len(rules))} rules, {NUM.get(nexp, nexp).lower()} of them one operation. Apply M, and the structural skeleton of the Epistle of James emerges — verse-matched, anchored, residue included.')
    return '\n'.join(out), sub


def splice(page, begin, end, body):
    pat = re.compile(re.escape(begin) + r'.*?' + re.escape(end), re.S)
    if not pat.search(page):
        sys.exit(f'markers {begin} not found in {PAGE}')
    return pat.sub(lambda _: f'{begin}\n{body}\n{end}', page)


def main():
    D = json.loads(DATA.read_text(encoding='utf-8'))
    body, sub = render(D)
    page = PAGE.read_text(encoding='utf-8')
    new = splice(splice(page, BEGIN, END, body), SUB_BEGIN, SUB_END, sub)
    if '--check' in sys.argv:
        print('up to date' if new == page else 'OUT OF DATE')
        sys.exit(0 if new == page else 1)
    PAGE.write_text(new, encoding='utf-8')
    print(f'wrote {PAGE.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
