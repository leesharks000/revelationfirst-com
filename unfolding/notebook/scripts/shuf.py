import random,sys,io,contextlib
from chap import *
src=open(sys.argv[1]).read(); R=eval(src[src.index('R=[')+2:src.index('run(R')])
rows=[r for r in R if r[1]]
true=[chkN(m,N_)[0] for m,N_,L_,J_,note in rows]
def strict(m,N_):
    ok,d=chkN(m,N_)
    if not ok: return False
    fr=[int(x) for x in re.findall(r'\((\d+)\)',d)]
    return bool((len(fr)>=2 and fr[0]<=20 and fr[1]<=60) or (fr and fr[0]<=6))
trueS=[strict(m,N_) for m,N_,L_,J_,note in rows]
random.seed(1127); sh=[];shS=[]
for _ in range(60):
    idx=list(range(len(rows)))
    while True:
        random.shuffle(idx)
        if all(i!=j for i,j in enumerate(idx)): break
    sh.append(sum(chkN(rows[i][0],rows[j][1])[0] for i,j in enumerate(idx))); shS.append(sum(strict(rows[i][0],rows[j][1]) for i,j in enumerate(idx)))
import statistics as st
n=len(rows); print(f'rows with a New Testament source: {n}')
print(f'rule as sealed: true {sum(true)} ({100*sum(true)/n:.0f}%) | sources shuffled among rows: mean {st.mean(sh):.1f} ({100*st.mean(sh)/n:.0f}%), range {min(sh)}-{max(sh)}')
print(f'stricter (two families, one in 20 verses or fewer and the other in 60 or fewer; or one in 6 or fewer): true {sum(trueS)} ({100*sum(trueS)/n:.0f}%) | shuffled mean {st.mean(shS):.1f} ({100*st.mean(shS)/n:.0f}%), range {min(shS)}-{max(shS)}')
vs=set(); vsS=set()
for (m,N_,L_,J_,note),t,ts in zip(rows,true,trueS):
    if t: vs|=set(mtv(m))
    if ts: vsS|=set(mtv(m))
print('verses in rows held by the New Testament source: as sealed',len(vs),'| stricter',len(vsS))
print('rows failing the stricter rule:',[m for (m,*_),t,ts in zip(rows,true,trueS) if t and not ts])
