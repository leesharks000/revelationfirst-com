import sys,re,json,math,collections,unicodedata as U
exec(open('../residue/r1.py').read().split("print('P1")[0])
N=nf
C=lambda b,k:{l for l,t,_ in NT[b][k] if t[:2] in('N-','A-','V-')}
vf=collections.Counter(l for b in books for k in NT[b] for l in L(b,k))
def sp(b,s):
    out=[]
    for part in re.split(r'[;,]\s*',s):
        m=re.match(r'(\d+):(\d+)(?:[-–](?:(\d+):)?(\d+))?',part.strip())
        if not m: continue
        c,a=int(m.group(1)),int(m.group(2)); c2=int(m.group(3)) if m.group(3) else c; z=int(m.group(4)) if m.group(4) else a
        out+=[k for k in NT[b] if (c,a)<=k<=(c2,z)]
    return sorted(set(out))
def align(mk,hooks,B):
    ks=sorted(NT[B]); matched=[]; nm=0
    for k in mk:
        M={l for l in C('MT',k) if vf[l]<=300}-hooks; best=None
        for j,kk in enumerate(ks):
            sh=M&C(B,kk)
            if len(sh)>=3 or (len(sh)>=2 and min(vf[l] for l in sh)<=30):
                sc=sum(math.log(8000/vf[l]) for l in sh)
                if not best or sc>best[0]: best=(sc,j)
        if best: nm+=1; matched+=[ks[i] for i in (best[1]-1,best[1],best[1]+1) if 0<=i<len(ks)]
    ok=nm>=max(1,math.ceil(len(mk)/2))
    return (set(matched) if ok else None), nm
def lem(B,ks): return set().union(*[C(B,k) for k in ks]) if ks else set()
ROWS=[]
for r in json.load(open('../map/rev-matthew-ledger.json'))['rows']:
    mk=sp('MT',r['matt']); S=lem('RE',sp('RE',r['rev'])); M=lem('MT',mk)
    hooks={N(l) for l in r.get('lemmas',[])}&M or {l for l in M&S if vf[l]<=150}
    ROWS.append(('Revelation',r['rev']+' -> '+r['matt'],mk,hooks,S,'relational' in r.get('standing','')))
src=open('../layer/bh.py').read(); BH=eval(src[src.index('ROWS=[')+5:src.index('EXTRA=')])
for m,eps,three,note in BH:
    mk=sp('MT',m); E=set()
    for b,s in eps: E|=lem(b,sp(b,s))
    M=lem('MT',mk); hooks={l for l in M&E if vf[l]<=400}
    if len(hooks)>=2 or (hooks and min(vf[l] for l in hooks)<=10): ROWS.append(('letters',m+' ~ '+note,mk,hooks,E,False))
res=[]
tot=collections.defaultdict(lambda: collections.Counter())
for srcn,name,mk,hooks,S,rel in ROWS:
    if not hooks or not mk: continue
    mr,nmr=align(mk,hooks,'MR'); lu,nlu=align(mk,hooks,'LU')
    T=tot[srcn]; T['rows']+=1
    M=lem('MT',mk); others={l for l in M if vf[l]<=300}-hooks
    d=dict(src=srcn,name=name,hooks=sorted(hooks),mr=bool(mr),lu=bool(lu))
    if mr:
        A=lem('MR',mr); T['mr_rows']+=1; T['mr_hook']+=len(hooks&A); T['mr_hookN']+=len(hooks); T['mr_oth']+=len(others&A); T['mr_othN']+=len(others)
        own={l for l in (S&A)-M if vf[l]<=150}; T['mr_own']+=len(own); d['mr_has']=sorted(hooks&A); d['mr_lacks']=sorted(hooks-A); d['mr_own']=sorted(own)
    if lu:
        A=lem('LU',lu); T['lu_rows']+=1; T['lu_hook']+=len(hooks&A); T['lu_hookN']+=len(hooks); T['lu_oth']+=len(others&A); T['lu_othN']+=len(others)
    if mr and lu:
        Am=lem('MR',mr); Al=lem('LU',lu); T['tri_rows']+=1; T['tri_hooks']+=len(hooks)
        T['all3']+=len(hooks&Am&Al); T['MM_notL']+=len((hooks&Am)-Al); T['ML_notM']+=len((hooks&Al)-Am); T['M_only']+=len(hooks-Am-Al)
        d['ML_notM']=sorted((hooks&Al)-Am); d['MM_notL']=sorted((hooks&Am)-Al)
        To=T; To['tri_oth']+=len(others); To['o_all3']+=len(others&Am&Al); To['o_MM']+=len((others&Am)-Al); To['o_ML']+=len((others&Al)-Am)
    res.append(d)
json.dump(res,open('bn.json','w'),ensure_ascii=False,indent=0)
def pr(n,T):
    f=lambda a,b:f'{T[a]}/{T[b]} = {100*T[a]/max(1,T[b]):.0f}%'
    print(f"\n{n}: rows {T['rows']} | with Marcan parallel {T['mr_rows']} | with Lucan {T['lu_rows']} | with both {T['tri_rows']}")
    print('  hooks kept: Mark',f('mr_hook','mr_hookN'),'| Luke',f('lu_hook','lu_hookN'))
    print('  other words kept: Mark',f('mr_oth','mr_othN'),'| Luke',f('lu_oth','lu_othN'))
    rm=(T['mr_hook']/max(1,T['mr_hookN']))/max(1e-9,T['mr_oth']/max(1,T['mr_othN'])); rl=(T['lu_hook']/max(1,T['lu_hookN']))/max(1e-9,T['lu_oth']/max(1,T['lu_othN']))
    print(f'  hook keeping over other keeping: Mark {rm:.2f} | Luke {rl:.2f}')
    print(f"  in passages all three have ({T['tri_hooks']} hooks): in all three {T['all3']} | Matthew+Mark against Luke {T['MM_notL']} | Matthew+Luke against Mark {T['ML_notM']} | Matthew alone {T['M_only']}")
    print(f"     other words there ({T['tri_oth']}): all three {T['o_all3']} | Matthew+Mark against Luke {T['o_MM']} | Matthew+Luke against Mark {T['o_ML']}")
    print(f"  source words in Mark's parallel and not in Matthew: {T['mr_own']} (hooks Matthew holds in those rows: {T['mr_hookN']})")
for n in ('Revelation','letters'): pr(n,tot[n])
ALL=collections.Counter()
for n in tot: ALL.update(tot[n])
pr('Revelation and letters together',ALL)
print('\nHooks Matthew and Luke hold where Mark lacks them (rows with all three):')
for d in res:
    if d.get('ML_notM'): print('  ',d['src'][:3],d['name'][:44],'|',d['ML_notM'],'| Mark has',d.get('mr_has'))
print('\nSource words Mark has and Matthew lacks:')
for d in res:
    if d.get('mr_own'): print('  ',d['src'][:3],d['name'][:44],'|',d['mr_own'])
