import sys,json,math,re,collections
exec(open('../residue/r1.py').read().split("print('P1")[0])
N=nf
C=lambda b,k:{l for l,t,_ in NT[b][k] if t[:2] in('N-','A-','V-')}
def windows(bs):
    W=[]
    for b in bs:
        ks=sorted(NT[b])
        for i,k in enumerate(ks):
            S=set()
            for j in (i-1,i,i+1):
                if 0<=j<len(ks): S|=C(b,ks[j])
            W.append((b,k,S))
    return W
EP=[b for b in books if b not in('MT','MR','LU','JOH','AC','RE')]
SRC={'letters':windows(EP),'Revelation':windows(['RE']),'Acts':windows(['AC'])}
def reach(W,theta=0.01):
    Nw=len(W); p=collections.Counter()
    for _,_,S in W:
        for l in S: p[l]+=1
    out={}
    for k in sorted(NT['MT']):
        M=C('MT',k); m=len(M); best=None
        Mi=[l for l in M if l in p]
        if len(Mi)<2: out[k]=None; continue
        for b,kk,S in W:
            sh=sorted((l for l in Mi if l in S),key=lambda l:p[l])
            if len(sh)<2: continue
            lp=math.log(Nw)
            for i,l in enumerate(sh):
                lp+=math.log(p[l]/Nw)
                if i>=1:
                    e=lp+math.log(math.comb(m,i+1))
                    if best is None or e<best[0]: best=(e,b,kk,sh[:i+1])
        out[k]=best if best and best[0]<math.log(theta) else None
    return out
R={n:reach(W) for n,W in SRC.items()}
R5={n:reach(W,0.05) for n,W in SRC.items()}
exec(open('bd.py').read().split("rows=json.load")[0].split("def span")[1].join(["def span",""]) if False else "")
def span(b,s):
    out=[]
    for part in re.split(r'[;,]\s*',s):
        m=re.match(r'(\d+):(\d+)(?:[-–](?:(\d+):)?(\d+))?',part.strip())
        if not m: continue
        c,a=int(m.group(1)),int(m.group(2)); c2=int(m.group(3)) if m.group(3) else c; z=int(m.group(4)) if m.group(4) else a
        out+=[k for k in NT[b] if (c,a)<=k<=(c2,z)]
    return out
rows=json.load(open('../map/rev-matthew-ledger.json'))['rows']
led=set()
for r in rows: led|=set(span('MT',r['matt']))
T=len(NT['MT']); print('Matthew verses',T,'ledger',len(led))
wc={n:sum(len(NT[b][k]) for b in bs for k in NT[b]) for n,bs in (('letters',EP),('Revelation',['RE']),('Acts',['AC']))}
for th,RR in (('0.01',R),('0.05',R5)):
    print('\ntheta',th)
    for n in SRC:
        h={k for k,v in RR[n].items() if v}
        print(f' {n:10} windows {len(SRC[n]):5} words {wc[n]:6} reaches {len(h):4} ({100*len(h)/T:.1f}%) per 1000 words {1000*len(h)/wc[n]:.1f} | inside ledger {len(h&led)} ({100*len(h&led)/max(1,len(h)):.0f}%)')
    L_={k for k,v in RR['letters'].items() if v}; RV={k for k,v in RR['Revelation'].items() if v}; A={k for k,v in RR['Acts'].items() if v}
    print(f' ledger recall by instrument: {len(RV&led)}/{len(led)} = {100*len(RV&led)/len(led):.0f}% | Rev-instrument verses outside ledger {len(RV-led)}')
    print(f' letters ∪ ledger = {len(L_|led)} ({100*len(L_|led)/T:.1f}%) | letters only (standalone) {len(L_-led)} | letters∪ledger∪RevInstr {len(L_|led|RV)} ({100*len(L_|led|RV)/T:.1f}%)')
    print(f' letters not also reached by Acts: {len(L_-A)} | Acts only {len(A-L_)}')
L_={k:v for k,v in R['letters'].items() if v}
for k in [(16,17),(5,34),(10,2),(17,25),(16,23),(26,70),(17,5),(19,28),(23,35),(26,41),(24,43)]:
    v=R5['letters'][k]; print('calib',k,v and (v[1],v[2],v[3],round(math.exp(v[0]),4)))
cnt=collections.Counter(v[1] for v in L_.values()); w1={b:sum(len(NT[b][k]) for k in NT[b]) for b in EP}
print('\nby letter (verses, per 1000 words):',', '.join(f'{b} {n} ({1000*n/w1[b]:.1f})' for b,n in sorted(cnt.items(),key=lambda x:-1000*x[1]/w1[x[0]])))
bych=collections.Counter(k[0] for k in L_); print('by Matthew chapter:',dict(sorted(bych.items())))
print('\nstandalone (outside ledger), strongest 45:')
for k,v in sorted(((k,v) for k,v in L_.items() if k not in led),key=lambda x:x[1][0])[:45]: print(f'  {k[0]}:{k[1]} | {v[1]} {v[2][0]}:{v[2][1]} | {"+".join(v[3])} | E={math.exp(v[0]):.1e}')
json.dump({f'{k[0]}:{k[1]}':[v[1],f'{v[2][0]}:{v[2][1]}',v[3],math.exp(v[0])] for k,v in L_.items()},open('bg.json','w'),ensure_ascii=False,indent=0)
P=json.load(open('../philo/matt-philo-pairs.json'))
ph={tuple(map(int,k.split(':'))) for k,v in P.items() if v[0]}; jo={tuple(map(int,k.split(':'))) for k,v in P.items() if v[1]}
print(f'\nPhilo pair file: verses with a Philo pair {len(ph)} ({100*len(ph)/T:.0f}%), with a Josephus pair {len(jo)} ({100*len(jo)/T:.0f}%)')
print(f' union ledger ∪ letters ∪ Philo-pairs = {len(led|set(L_)|ph)} ({100*len(led|set(L_)|ph)/T:.1f}%)')
