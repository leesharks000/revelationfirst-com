# checker for chapter batches: New Testament (lemma and family), Septuagint (stems), Josephus (named words)
import re,json,glob,collections,unicodedata as U
from rel import *
C='/home/claude/repos/alexanarch/data/corpora/'
def gn(t):
    t=U.normalize('NFD',t); return ''.join(c for c in t if not U.combining(c)).lower().replace('ς','σ')
def load(f): return [(l.split('\t',1)[0],gn(l.rstrip('\n').split('\t',1)[1])) for l in open(f,encoding='utf-8') if '\t' in l]
MTN={r.split(' ',1)[1]:t for r,t in load(C+'gnt-nestle1904/text/Matt.txt')}
stem5=lambda t:{w[:5] for w in re.findall(r'[α-ω]+',t) if len(w)>=5}
sf=collections.Counter()
for f in glob.glob(C+'gnt-nestle1904/text/*.txt'):
    for r,t in load(f):
        for s in stem5(t): sf[s]+=1
LXX={}
for f in glob.glob(C+'lxx-swete/text/*.txt'):
    for r,t in load(f): LXX[r]=t
JOS={w:load(C+f'josephus/text/{w}.txt') for w in ('AJ','BJ','Vita','CA')}
def rng(s):
    out=[]
    for part in re.split(r';\s*',s):
        m=re.match(r'(\d+):(\d+)(?:-(?:(\d+):)?(\d+))?',part.strip()); c,a=int(m.group(1)),int(m.group(2)); c2=int(m.group(3)) if m.group(3) else c; z=int(m.group(4)) if m.group(4) else a
        out.append(((c,a),(c2,z)))
    return out
def mtv(s): return [k for k in MTN if any(lo<=tuple(map(int,k.split(':')))<=hi for lo,hi in rng(s))]
def sp(b,s): return [(bb,k) for (bb,k) in V if bb==b and any(lo<=k<=hi for lo,hi in rng(s))]
vfl=collections.Counter()
for v,ls in V.items():
    for l in set(ls): vfl[l]+=1
keyl=collections.defaultdict(set)
for l in LEM:
    for f in FAM[l]: keyl[f].add(l)
ffreq={f:len({v for v,ls in V.items() if set(ls)&keyl[f]}) for f in keyl}
def chkN(m,srcs):
    mv=sp('MT',m); sv=[]
    for b,s in srcs: sv+=sp(b,s)
    M={l for v in mv for l in V[v]}; S={l for v in sv for l in V[v]}; best={}
    for a in M:
        for b in S:
            fr=None
            if a==b and vfl[a]<=400: fr=(vfl[a],a,'')
            elif a!=b:
                sh=[f for f in FAM[a]&FAM[b] if len(f)>=3 and ffreq.get(f,999)<=400]
                if sh: fr=(min(ffreq[f] for f in sh),a,'~'+b)
            if fr and (a not in best or fr<best[a]): best[a]=fr
    L_=sorted(best.values()); opp=any(g in FAM[b] for a in M for f in FAM[a] for g in OPPS.get(f,()) for b in S)
    ok=bool((len(L_)>=2 and L_[0][0]<=100) or (L_ and L_[0][0]<=10) or (opp and L_))
    return ok,', '.join(f'{a}{b}({fr})' for fr,a,b in L_[:5])
def chkL(m,srcs):
    M=set().union(*[stem5(MTN[k]) for k in mtv(m)]); S=set(); miss=[]
    for book,ref in srcs:
        got=False
        for r,t in LXX.items():
            bn,cv=r.rsplit(' ',1)
            try: key=tuple(map(int,cv.split(':')))
            except ValueError: continue
            if len(key)==2 and gn(book) in gn(bn) and any(lo<=key<=hi for lo,hi in rng(ref)): S|=stem5(t); got=True
        if not got: miss.append(book+' '+ref)
    sh=sorted(M&S,key=lambda s:sf[s]); ok=bool((len(sh)>=2 and sf[sh[0]]<=60) or (sh and sf[sh[0]]<=8))
    return ok,', '.join(f'{s}({sf[s]})' for s in sh[:5])+(f' [not found in the seat: {miss}]' if miss else '')
def chkJ(m,spec):
    w,keys=spec; mt=' '.join(MTN[k] for k in mtv(m))
    if not all(re.search(k,mt) for k in keys): return False,'not all in Matthew'
    U_=JOS[w]; hits=[U_[i][0] for i in range(len(U_)) if all(re.search(k,' '.join(x[1] for x in U_[max(0,i-1):i+2])) for k in keys)]
    return bool(hits),f'{w}: {len(hits)} sections, first {hits[:2]}'
def run(ROWS,reached_file,out_file,chapters):
    old=set(json.load(open(reached_file))); held=set(); n=0; tot=0
    for m,N_,L_,J_,note in ROWS:
        if not (N_ or L_ or J_): print(f'--   {m:22} {note} (left unmapped)'); continue
        tot+=1; parts=[]; ok=False
        if N_: o,d=chkN(m,N_); ok|=o; parts.append(('NT+' if o else 'NT-')+' '+d)
        if L_: o,d=chkL(m,L_); ok|=o; parts.append(('LXX+' if o else 'LXX-')+' '+d)
        if J_: o,d=chkJ(m,J_); ok|=o; parts.append(('Jos+' if o else 'Jos-')+' '+d)
        n+=ok; print(f"{'HELD' if ok else 'no  '} {m:22} {note[:34]:34} | "+' | '.join(parts))
        if ok: held|=set(mtv(m))
    print(f'\nrows held {n} of {tot} ({100*n/tot:.0f}%)')
    allk=list(MTN)
    b=sum(1 for k in allk if int(k.split(":")[0]) in chapters and k in old); a=sum(1 for k in allk if int(k.split(":")[0]) in chapters and k in old|held); t=sum(1 for k in allk if int(k.split(":")[0]) in chapters)
    print(f'these chapters: {b} -> {a} of {t} ({100*a/t:.0f}%)')
    for c in chapters:
        ck=[k for k in allk if int(k.split(':')[0])==c]; un=[k.split(':')[1] for k in ck if k not in old|held]
        print(f'  ch {c}: {sum(k in old for k in ck)} -> {sum(k in old|held for k in ck)} of {len(ck)} | still unreached: {",".join(un)}')
    T=1067; print(f'book: {len(old)} -> {len(old|held)} ({100*len(old|held)/T:.1f}%)')
    json.dump(sorted(old|held),open(out_file,'w'))
