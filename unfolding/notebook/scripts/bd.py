import sys,json,math,re,collections,unicodedata
exec(open('../residue/r1.py').read().split("print('P1")[0])
N=nf
C=lambda b,k:{l for l,t,_ in NT[b][k] if t[:2] in('N-','A-','V-')}
vf=collections.Counter()
for b in books:
    for k in NT[b]:
        for l in C(b,k): vf[l]+=1
ok=lambda l:vf[l]<=150; w=lambda l:math.log(8000/vf[l])
EP=[b for b in books if b not in('MT','MR','LU','JOH','AC','RE')]
WINS=[]
for b in EP:
    ks=sorted(NT[b])
    for i,k in enumerate(ks):
        S=set()
        for j in (i-1,i,i+1):
            if 0<=j<len(ks): S|=C(b,ks[j])
        WINS.append((b,k,{l for l in S if ok(l)}))
def best(S):
    S={l for l in S if ok(l)}; top=None
    for b,k,E in WINS:
        sh=S&E
        if len(sh)>=2 and min(vf[l] for l in sh)<=40:
            sc=sum(w(l) for l in sh)
            if not top or sc>top[0]: top=(sc,b,k,sh,E)
    return top
def span(b,s):
    out=[]
    for part in re.split(r'[;,]\s*',s):
        part=part.strip()
        m=re.match(r'(\d+):(\d+)(?:[-–](?:(\d+):)?(\d+))?',part)
        if not m:
            m2=re.match(r'(\d+)$',part)
            if m2 and out: out.append((out[-1][0],int(m2.group(1))))
            continue
        c,a=int(m.group(1)),int(m.group(2)); c2=int(m.group(3)) if m.group(3) else c; z=int(m.group(4)) if m.group(4) else a
        out+=[k for k in NT[b] if (c,a)<=k<=(c2,z)]
    return sorted(set(out))
rows=json.load(open('../map/rev-matthew-ledger.json'))['rows']
FOL=[N(x) for x in('Πέτρος','Σίμων','Ἰάκωβος','Ἰωάννης','Ἀνδρέας','Ἰούδας','Ζεβεδαῖος')]
res=[];reached=set();unp=0
for r in rows:
    mk=span('MT',r['matt']); rk=span('RE',r['rev'])
    if not mk or not rk: unp+=1; print('unparsed',r['rev'],r['matt']); continue
    reached|=set(mk)
    M=set().union(*[C('MT',k) for k in mk]); R=set().union(*[C('RE',k) for k in rk])
    rel='relational' in r.get('standing','')
    named=any(l in FOL for l in M)
    t=best(M)
    d=dict(rev=r['rev'],matt=r['matt'],rel=rel,named=named,par=None)
    if t:
        sc,b,k,sh,E=t; Mo={l for l in M if ok(l)}; Ro={l for l in R if ok(l)}
        d.update(par=f'{b} {k[0]}:{k[1]}',sc=round(sc,1),sh=sorted(sh),a=sorted((Mo&Ro)-E),b=sorted((Mo&E)-Ro),c=sorted((E&Ro)-Mo),t=sorted(Mo&E&Ro),book=b)
    res.append(d)
json.dump(res,open('bd.json','w'),ensure_ascii=False,indent=0)
def rep(name,X):
    P=[d for d in X if d['par']]
    J=[d for d in P if d['a'] and d['b']]; CH=[d for d in P if not d['a'] and d['t']]
    Eonly=[d for d in P if not d['a'] and not d['t']]; Ronly=[d for d in P if d['a'] and not d['b']]
    print(f'{name}: rows {len(X)}, with parallel {len(P)} ({100*len(P)/len(X):.0f}%), joined {len(J)} ({100*len(J)/max(1,len(P)):.0f}%), chain not excluded {len(CH)}, no word shared with Revelation by the rule {len(Eonly)}, epistle adds nothing past Revelation {len(Ronly)}')
    return P,J,CH
print('unparsed',unp)
P,J,CH=rep('all',res); rep('counted',[d for d in res if not d['rel']]); rep('relational',[d for d in res if d['rel']])
print('\nCHAIN NOT EXCLUDED');
for d in CH: print(' ',d['rev'],'->',d['matt'],'|',d['par'],'| t',d['t'],'| b',d['b'],'| c',d['c'])
print('\nJOINED, by weight');
for d in sorted(J,key=lambda d:-d['sc'])[:30]: print(' ',d['rev'],'->',d['matt'],'|',d['par'],d['sc'],'| a',d['a'][:6],'| b',d['b'][:8],'| c',d['c'][:5])
# BD5
cnt=collections.Counter(d['book'] for d in P); wc={b:sum(len(NT[b][k]) for k in NT[b]) for b in EP}
print('\nBD5 by letter:',', '.join(f'{b} {n} ({1000*n/wc[b]:.1f})' for b,n in sorted(cnt.items(),key=lambda x:-1000*x[1]/wc[x[0]])))
P7=('RO','1CO','2CO','GA','EPH','PHP','COL','1TH','2TH'); print(' Paul seven:',sum(cnt[b] for b in P7),'of',len(P))
# BD6
nm=[d for d in res if d['named']]; ot=[d for d in res if not d['named']]
print('BD6 named rows',len(nm),'with parallel',sum(1 for d in nm if d['par']),'| others',len(ot),sum(1 for d in ot if d['par']))
# BD2 verse level
hit={k:bool(best(C('MT',k))) for k in NT['MT']}
rc=[hit[k] for k in NT['MT'] if k in reached]; un=[hit[k] for k in NT['MT'] if k not in reached]
print(f'BD2 reached {sum(rc)}/{len(rc)} = {100*sum(rc)/len(rc):.1f}% | unreached {sum(un)}/{len(un)} = {100*sum(un)/len(un):.1f}% | ratio {sum(rc)/len(rc)/(sum(un)/len(un)):.2f}')
# control: same rule with Mark's verses? and length control: mean content lemmas
ml=lambda ks:sum(len({l for l in C('MT',k) if ok(l)}) for k in ks)/len(ks)
print(' mean rare lemmas per verse: reached',round(ml([k for k in NT['MT'] if k in reached]),2),'unreached',round(ml([k for k in NT['MT'] if k not in reached]),2))
# speech control: by chapter sets of discourse (5-7,10,13,18,23-25)
disc={5,6,7,10,13,18,23,24,25}
for nm_,f in (('discourse',lambda k:k[0] in disc),('narrative',lambda k:k[0] not in disc)):
    a=[hit[k] for k in NT['MT'] if f(k) and k in reached]; b=[hit[k] for k in NT['MT'] if f(k) and k not in reached]
    print(f' {nm_}: reached {sum(a)}/{len(a)} {100*sum(a)/len(a):.0f}% | unreached {sum(b)}/{len(b)} {100*sum(b)/len(b):.0f}%')
