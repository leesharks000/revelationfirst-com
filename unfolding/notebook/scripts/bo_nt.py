import sys,re,json,random,collections,itertools,statistics as st
from rel import *
random.seed(1127)
# one family id per lemma: the shortest key it shares with another lemma, else its own stem
keyl=collections.defaultdict(set)
for l in LEM:
    for f in FAM[l]: keyl[f].add(l)
def fid(l):
    c=[f for f in FAM[l] if len(keyl[f])>1 and len(f)>=3]
    return min(c,key=lambda f:(len(f),f)) if c else ST[l]
FID={l:fid(l) for l in LEM}
VF=collections.defaultdict(list)   # verse -> family ids
for v,ls in V.items(): VF[v]=sorted({FID[l] for l in ls})
vff=collections.Counter(f for v in VF for f in VF[v])
order={}
for b in {v[0] for v in VF}:
    ks=sorted(k for (bb,k) in VF if bb==b)
    for i,k in enumerate(ks): order[(b,k)]=(i,ks)
def window(v):
    b,k=v; i,ks=order[v]; S=set()
    for j in (i-1,i,i+1):
        if 0<=j<len(ks): S|=set(VF[(b,ks[j])])
    return S
WIN={v:window(v) for v in VF}
occ=collections.defaultdict(set)
for v,S in WIN.items():
    for f in S:
        if vff[f]<=60: occ[f].add(v)
EP=[b for b in {v[0] for v in VF} if b not in('MT','MR','LU','JOH','AC','RE')]
SRC={'Revelation':{'RE'},'letters':set(EP)}
cache={}
def chapters(f,g):
    k=(f,g) if f<g else (g,f)
    if k not in cache: cache[k]=len({(v[0],v[1][0]) for v in occ[f]&occ[g] if v[0] not in('MR','LU')})
    return cache[k]
MTV=sorted(v for v in VF if v[0]=='MT')
def reach(mapping=None):
    out={n:{} for n in SRC}
    for v in MTV:
        F=[f for f in VF[v] if vff[f]<=60]
        if mapping: F=[mapping.get(f,f) for f in F]
        for n,books in SRC.items():
            best=None
            for f in F:
                if vff[f]<=8:
                    ws=[w for w in occ[f] if w[0] in books]
                    if ws: best=('single',f,ws[0]); break
            if not best:
                for f,g in itertools.combinations(F,2):
                    ws=[w for w in occ[f]&occ[g] if w[0] in books]
                    if ws and (chapters(f,g) if not mapping else len({(w[0],w[1][0]) for w in occ[f]&occ[g] if w[0] not in('MR','LU')})+1)<=6:
                        best=('pair',(f,g),ws[0]); break
            if best: out[n][v]=best
    return out
true=reach()
bins=lambda n:0 if n<=1 else 1 if n<=2 else 2 if n<=4 else 3 if n<=8 else 4 if n<=16 else 5 if n<=32 else 6
byb=collections.defaultdict(list)
for f,n in vff.items():
    if n<=60: byb[bins(n)].append(f)
nul={n:[] for n in SRC}; nulsets=[]
for r in range(20):
    mp={}
    for b,fs in byb.items():
        sh=fs[:]; random.shuffle(sh); mp.update(dict(zip(fs,sh)))
    R=reach(mp); nulsets.append(R)
    for n in SRC: nul[n].append(len(R[n]))
def sp(b,s):
    out=[]
    for part in re.split(r'[;,]\s*',s):
        m=re.match(r'(\d+):(\d+)(?:[-–](?:(\d+):)?(\d+))?',part.strip())
        if not m: continue
        c,a=int(m.group(1)),int(m.group(2)); c2=int(m.group(3)) if m.group(3) else c; z=int(m.group(4)) if m.group(4) else a
        out+=[(b,k) for (bb,k) in VF if bb==b and (c,a)<=k<=(c2,z)]
    return out
led=set()
for r in json.load(open('../map/rev-matthew-ledger.json'))['rows']: led|=set(sp('MT',r['matt']))
tov=lambda L_:{('MT',tuple(map(int,x.split(':')))) for x in L_}
let=tov(json.load(open('../layer/bh.json'))); jo=tov(json.load(open('../control/bj2.json')))
T=len(MTV); print('Matthew verses',T,'| ledger',len(led),'letters',len(let),'Josephus',len(jo),'| hand lists together',len(led|let|jo))
for n in SRC:
    t=set(true[n]); m=st.mean(nul[n]); kinds=collections.Counter(x[0] for x in true[n].values())
    print(f'{n:11} true {len(t)} ({100*len(t)/T:.1f}%) {dict(kinds)} | exchanged mean {m:.1f} (range {min(nul[n])}-{max(nul[n])}) | ratio {len(t)/max(m,.1):.2f} | above chance {len(t)-m:.0f}')
print('recall: ledger verses found from Revelation',len(set(true['Revelation'])&led),'of',len(led),f"({100*len(set(true['Revelation'])&led)/len(led):.0f}%)",'| letters verses found from the letters',len(set(true['letters'])&let),'of',len(let),f"({100*len(set(true['letters'])&let)/len(let):.0f}%)")
hand=led|let|jo; fin=set(true['Revelation'])|set(true['letters'])
new=fin-hand; nulnew=st.mean(len((set(R['Revelation'])|set(R['letters']))-hand) for R in nulsets)
print(f'new verses (finder, in no hand list): {len(new)} | exchanged mean {nulnew:.1f} | chance share {100*nulnew/max(1,len(new)):.0f}%')
print(f'hand lists {len(hand)} ({100*len(hand)/T:.1f}%) | with finder {len(hand|fin)} ({100*len(hand|fin)/T:.1f}%) | with chance share off {len(hand)+len(new)-nulnew:.0f} ({100*(len(hand)+len(new)-nulnew)/T:.1f}%)')
json.dump({f'{v[1][0]}:{v[1][1]}':{n:[true[n][v][0],list(true[n][v][1]) if isinstance(true[n][v][1],tuple) else true[n][v][1],f'{true[n][v][2][0]} {true[n][v][2][1][0]}:{true[n][v][2][1][1]}'] for n in SRC if v in true[n]} for v in sorted(fin)},open('bo_nt.json','w'),ensure_ascii=False,indent=0)
print('\nnew, by the rarest shared family (first 60):')
rows=[]
for v in new:
    for n in SRC:
        if v in true[n]:
            k,f,w=true[n][v]; fr=vff[f] if k=='single' else max(vff[f[0]],vff[f[1]]); rows.append((fr,v,n,k,f,w))
for fr,v,n,k,f,w in sorted(rows)[:60]: print(f'  Matt {v[1][0]}:{v[1][1]} <- {n[:3]} {w[0]} {w[1][0]}:{w[1][1]} | {k} {f}')
