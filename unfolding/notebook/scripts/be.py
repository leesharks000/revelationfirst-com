import sys,json,math,re,collections,itertools
src=open('bd.py').read(); exec(src.split("rows=json.load")[0])
ALLW={}
occ=collections.defaultdict(set)
for b in books:
    ks=sorted(NT[b])
    for i,k in enumerate(ks):
        S=set()
        for j in (i-1,i,i+1):
            if 0<=j<len(ks): S|=C(b,ks[j])
        for l in S:
            if ok(l): occ[l].add((b,k))
cache={}
def chapters(p):
    if p not in cache:
        a,b_=p; cache[p]={(b,k[0]) for b,k in occ[a]&occ[b_] if b not in('MR','LU')}
    return cache[p]
def strict(S,mch):
    S={l for l in S if ok(l)}; out=[]
    for b,k,E in WINS:
        sh=S&E
        if len(sh)<2: continue
        for p in itertools.combinations(sorted(sh),2):
            ch=chapters(p)
            if len(ch)<=3: out.append((len(ch),-w(p[0])-w(p[1]),b,k,p,E))
    if not out: return None
    out.sort(); return out[0],sorted({(o[2],o[3][0],o[4]) for o in out})
rows=json.load(open('../map/rev-matthew-ledger.json'))['rows']
res=[];reached=set()
for r in rows:
    mk=span('MT',r['matt']); rk=span('RE',r['rev']); reached|=set(mk)
    M=set().union(*[C('MT',k) for k in mk]); R=set().union(*[C('RE',k) for k in rk])
    s=strict(M,None)
    if s:
        (n,_,b,k,p,E),allp=s; Mo={l for l in M if ok(l)}; Ro={l for l in R if ok(l)}
        res.append(dict(rev=r['rev'],matt=r['matt'],rel='relational' in r.get('standing',''),par=f'{b} {k[0]}:{k[1]}',pair=p,n=n,a=sorted((Mo&Ro)-E),b=sorted((Mo&E)-Ro),c=sorted((E&Ro)-Mo),t=sorted(Mo&E&Ro),others=[f'{x[0]} {x[1]} {"+".join(x[2])}' for x in allp][:6]))
print('rows with strict parallel',len(res),'of',len(rows),'| relational among them',sum(d['rel'] for d in res))
J=[d for d in res if d['a'] and d['b']]; CH=[d for d in res if not d['a'] and d['t']]; NO=[d for d in res if not d['a'] and not d['t']]
print('joined',len(J),'chain not excluded',len(CH),'no rare word shared with Revelation',len(NO),'other',len(res)-len(J)-len(CH)-len(NO))
for tag,X in (('JOINED',J),('CHAIN NOT EXCLUDED',CH),('NO REV WORD',NO),('OTHER',[d for d in res if d not in J+CH+NO])):
    print('\n'+tag)
    for d in X: print(' ',d['rev'],'->',d['matt'],'|',d['par'],'+'.join(d['pair']),f"({d['n']} ch)",'| a',d['a'][:6],'| b',d['b'][:6],'| c',d['c'][:4],'| t',d['t'][:4])
hit={}
for k in NT['MT']:
    s=strict(C('MT',k),None); hit[k]=s
rc=[bool(hit[k]) for k in NT['MT'] if k in reached]; un=[bool(hit[k]) for k in NT['MT'] if k not in reached]
print(f'\nBE3 reached {sum(rc)}/{len(rc)} = {100*sum(rc)/len(rc):.1f}% | unreached {sum(un)}/{len(un)} = {100*sum(un)/len(un):.1f}% | ratio {sum(rc)/len(rc)/(sum(un)/len(un)):.2f}')
for k in [(16,17),(5,34),(5,37),(24,43),(1,1)]:
    print('BE4',k,hit[k] and (hit[k][0][2],hit[k][0][3],hit[k][0][4],hit[k][0][0]))
cnt=collections.Counter(hit[k][0][2] for k in NT['MT'] if hit[k]); wc={b:sum(len(NT[b][k]) for k in NT[b]) for b in EP}
print('verse-level strict parallels by letter (count, per 1000 words):',', '.join(f'{b} {n} ({1000*n/wc[b]:.1f})' for b,n in sorted(cnt.items(),key=lambda x:-1000*x[1]/wc[x[0]])))
un_list=[(k,hit[k][0][2],hit[k][0][3],hit[k][0][4]) for k in sorted(NT['MT']) if hit[k] and k not in reached]
print('unreached verses with strict parallel:',len(un_list)); print('; '.join(f'{k[0]}:{k[1]} {b} {v[0]}:{v[1]} {"+".join(p)}' for k,b,v,p in un_list))
json.dump([{**d,'pair':list(d['pair'])} for d in res],open('be.json','w'),ensure_ascii=False,indent=0)
