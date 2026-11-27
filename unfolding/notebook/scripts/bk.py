import sys,re,json,random,collections,statistics as st
from rel import *
sys.path.insert(0,'../layer')
src=open('../layer/bh.py').read(); ROWS=eval(src[src.index('ROWS=[')+5:src.index('EXTRA=')])
def sp(b,s):
    out=[]
    for part in re.split(r'[;,]\s*',s):
        m=re.match(r'(\d+):(\d+)(?:[-–](?:(\d+):)?(\d+))?',part.strip())
        if not m: continue
        c,a=int(m.group(1)),int(m.group(2)); c2=int(m.group(3)) if m.group(3) else c; z=int(m.group(4)) if m.group(4) else a
        out+=[(b,k) for (bb,k) in V if bb==b and (c,a)<=k<=(c2,z)]
    return out
def lem(vs): return {l for v in vs for l in V[v]}
vfl=collections.Counter(); vff=collections.Counter(); vfs=collections.Counter()
for v,ls in V.items():
    for l in set(ls): vfl[l]+=1
    for f in set().union(*[fams(l) for l in ls]) if ls else (): vff[f]+=1
    for d in set().union(*[sub(l) for l in ls]) if ls else (): vfs[d]+=1
def links(M,E):
    L0={l for l in M&E if vfl[l]<=100}
    fM=collections.defaultdict(set); fE=collections.defaultdict(set)
    for l in M:
        for f in fams(l): fM[f].add(l)
    for l in E:
        for f in fams(l): fE[f].add(l)
    KIN={f for f in set(fM)&set(fE) if vff[f]<=150 and len(f)>=3 and not (fM[f]&fE[f]) }
    kinl=set().union(*[fM[f]|fE[f] for f in KIN]) if KIN else set()
    sM=collections.defaultdict(set); sE=collections.defaultdict(set)
    for l in M-L0-kinl:
        for d in sub(l): sM[d].add(l)
    for l in E-L0-kinl:
        for d in sub(l): sE[d].add(l)
    FIELD={d for d in set(sM)&set(sE) if vfs[d]<=150 and not (sM[d]&sE[d])}
    OPPL=set()
    for f in fM:
        for g in OPPS.get(f,()):
            if g in fE: OPPL.add((f,g))
        if f in fE and len(f)>=3:
            if {NEG[x] for x in fM[f]}!={NEG[x] for x in fE[f]} or (any(NEG[x] for x in fM[f])!=any(NEG[x] for x in fE[f])): OPPL.add((f,'not-'+f))
    return L0,KIN,FIELD,OPPL
P=[]
for m,eps,three,note in ROWS:
    Mv=sp('MT',m); Ev=[]
    for b,s in eps: Ev+=sp(b,s)
    P.append((m,note,lem(Mv),lem(Ev)))
print('BK1')
for m,note,M,E in P:
    if m in('5:7','5:9','7:21-27'):
        a,b,c,d=links(M,E); print(' ',m,note,'| lemma',sorted(a),'| KIN',sorted(b),'| FIELD',sorted(c),'| OPP',sorted(d))
tot=[sum(len(x) for x in col) for col in zip(*[links(M,E) for _,_,M,E in P])]
random.seed(1127); sh=[]
for _ in range(200):
    idx=list(range(len(P)))
    while True:
        random.shuffle(idx)
        if all(i!=j for i,j in enumerate(idx)): break
    sh.append([sum(len(x) for x in col) for col in zip(*[links(P[i][2],P[j][3]) for i,j in enumerate(idx)])])
mean=[st.mean(c) for c in zip(*sh)]
print('\nBK2 links over the 52 pairs: level | true | shuffled mean | ratio')
for n,t,m_ in zip(('same lemma','KIN alone','FIELD alone','OPP'),tot,mean): print(f'  {n:12} {t:5} {m_:7.1f} {t/max(m_,.01):6.1f}')
held=sum(1 for _,_,M,E in P if (lambda a,b,c,d: len(a)+len(b)>=2 or (a and min(vfl[x] for x in a)<=10) or (len(a)+len(b)+len(d)>=2))(*links(M,E)))
print('pairs joined at lemma or KIN or OPP by two links (or one rare lemma):',held,'of',len(P))
rows=json.load(open('../map/rev-matthew-ledger.json'))['rows']
turn=[r for r in rows if re.search(r'OPPOS|TURN|turn|REVERS|INVERT',r.get('move','')+' '+r.get('standing',''))]
print('\nBK3 ledger rows with an opposing or turning move:',len(turn))
hit=0
for r in turn:
    a,b,c,d=links(lem(sp('RE',r['rev'])),lem(sp('MT',r['matt'])))
    hit+=bool(d); print(' ',r['rev'],'->',r['matt'],'|',r['move'][:40],'| OPP',sorted(d)[:3],'| KIN',sorted(b)[:4])
print('OPP link found in',hit,'of',len(turn))
allr=[links(lem(sp('RE',r['rev'])),lem(sp('MT',r['matt']))) for r in rows]
print('whole ledger: rows with a KIN link beyond shared lemmas',sum(bool(x[1]) for x in allr),'| with an OPP link',sum(bool(x[3]) for x in allr),'of',len(rows))
