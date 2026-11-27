import re,json,collections
from rel import *
def sp(b,s):
    out=[]
    for part in re.split(r'[;,]\s*',s):
        m=re.match(r'(\d+):(\d+)(?:[-–](?:(\d+):)?(\d+))?',part.strip())
        if not m: continue
        c,a=int(m.group(1)),int(m.group(2)); c2=int(m.group(3)) if m.group(3) else c; z=int(m.group(4)) if m.group(4) else a
        out+=[(b,k) for (bb,k) in V if bb==b and (c,a)<=k<=(c2,z)]
    return out
vfl=collections.Counter(); 
for v,ls in V.items():
    for l in set(ls): vfl[l]+=1
keyl=collections.defaultdict(set)
for l in LEM:
    for f in FAM[l]: keyl[f].add(l)
ffreq={f:len({v for v,ls in V.items() if set(ls)&keyl[f]}) for f in keyl}
ROWS=[
('25:1',[('RE','18:23'),('RE','4:5'),('RE','19:7-9')],'virgins, lamps, the bridegroom'),
('25:2',[('1CO','4:10')],'foolish and wise'),
('25:3-4',[('RE','6:6'),('RE','4:5')],'lamps and oil'),
('25:5',[('1TH','5:6-7'),('2PE','2:3')],'slumbered and slept'),
('25:6',[('1TH','4:16-17'),('RE','18:23')],'go out to meet him'),
('25:7-8',[('1TH','5:19'),('RE','4:5'),('RE','6:6')],'the lamps going out'),
('25:14-15',[('RO','12:3-6'),('EPH','4:7'),('RE','2:23'),('RE','16:21')],'to each according to ability; talents'),
('25:16-18',[('1CO','9:19-22'),('RE','16:21'),('RE','6:15')],'gained; hid'),
('25:19',[('RO','14:12'),('HEB','13:17'),('1PE','4:5')],'the reckoning'),
('25:20-23',[('RE','2:10'),('RE','2:26'),('RE','3:4'),('HEB','12:2'),('RE','17:14')],'faithful over a few; the joy'),
('25:26',[('RO','12:11')],'slothful servant'),
('25:28-29',[('RE','3:11'),('RE','2:25')],'to the one who has'),
('25:30',[('JUDE','1:13'),('RE','22:15'),('RO','3:12'),('2PE','2:17')],'the useless servant into the outer darkness'),
('25:33',[('RE','10:2')],'right and left'),
('25:40; 25:45',[('1CO','8:12'),('1CO','15:9'),('HEB','2:11-12'),('EPH','3:8')],'the least of my brothers'),
('25:46',[('1JO','4:18'),('2PE','2:9'),('RO','2:7-8'),('JUDE','1:7')],'eternal punishment, eternal life'),
]
EXTRA=[('25:41',[('JUDE','1:7'),('RE','12:9')],'eternal fire; the devil and his angels'),('25:35-36; 25:43',[('HEB','13:2-3'),('JAS','1:27'),('JAS','2:15-16')],'stranger, naked, visited')]
def links(mv,sv):
    M={l for v in mv for l in V[v]}; S={l for v in sv for l in V[v]}; out=[]
    for a in M:
        for b in S:
            if a==b and vfl[a]<=400: out.append((vfl[a],a,b,'lemma'))
            elif a!=b:
                sh=[f for f in FAM[a]&FAM[b] if len(f)>=3 and ffreq.get(f,999)<=400]
                if sh: out.append((min(ffreq[f] for f in sh),a,b,'kin'))
    opp=[(a,b) for a in M for b in S if any(g in FAM[b] for f in FAM[a] for g in OPPS.get(f,()))]
    best={}
    for fr,a,b,k in sorted(out):
        if a not in best: best[a]=(fr,a,b,k)
    L_=sorted(best.values()); ok=bool((len(L_)>=2 and L_[0][0]<=100) or (L_ and L_[0][0]<=10) or (opp and L_))
    return ok,L_,opp
def run(R,label):
    held=set();n=0
    for m,srcs,note in R:
        mv=sp('MT',m); sv=[]
        for b,s in srcs: sv+=sp(b,s)
        ok,L_,opp=links(mv,sv); n+=ok
        print(f"{'HELD' if ok else 'no  '} {m:14} {note[:40]:40} | "+', '.join(f"{a}{'~'+b if k=='kin' else ''}({fr})" for fr,a,b,k in L_[:6])+(f' | opp {opp[:2]}' if opp else ''))
        if ok: held|={f'{v[1][0]}:{v[1][1]}' for v in mv}
    print(label,'held',n,'of',len(R)); return held
h=run(ROWS,'NEW ROWS'); print(); h2=run(EXTRA,'ADDED SOURCES for verses already reached')
MT=[f'{k[0]}:{k[1]}' for (b,k) in sorted(V) if b=='MT']
led=set()
for r in json.load(open('../map/rev-matthew-ledger.json'))['rows']:
    led|={f'{v[1][0]}:{v[1][1]}' for v in sp('MT',r['matt'])}
old=led|set(json.load(open('../layer/bh.json')))|set(json.load(open('../control/bj2.json')))|set(json.load(open('../scripture/matt_scripture_verses.json')))
c25=[k for k in MT if k.startswith('25:')]
print('\nchapter 25: before',sum(k in old for k in c25),'of',len(c25),'| after',sum(k in old|h for k in c25),f'({100*sum(k in old|h for k in c25)/len(c25):.0f}%)')
print('still unreached:',[k for k in c25 if k not in old|h])
T=len(MT); print(f'book: before {len(old)} ({100*len(old)/T:.1f}%) | after {len(old|h)} ({100*len(old|h)/T:.1f}%)')
json.dump(sorted(h),open('bp.json','w'))
