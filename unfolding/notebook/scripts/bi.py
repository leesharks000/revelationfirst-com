import re,glob,collections,itertools,random,unicodedata as U,statistics as st
C='/home/claude/repos/alexanarch/data/corpora/'
def norm(t):
    t=U.normalize('NFD',t); return ''.join(c for c in t if not U.combining(c)).lower().replace('ς','σ')
def stems(t): return {w[:5] for w in re.findall(r'[α-ω]+',norm(t)) if len(w)>=5}
def words(d):
    out=[]
    for f in sorted(glob.glob(C+d+'/text/*.txt')):
        for l in open(f,encoding='utf-8'):
            if l.startswith('['): continue
            if '\t' in l: l=l.split('\t',1)[1]
            out+=re.findall(r'[α-ω]+',norm(l))
    return out
def pieces(ws,n=100): return [{w[:5] for w in ws[i:i+n] if len(w)>=5} for i in range(0,len(ws)-n+1,n)]
MT={}
for l in open(C+'gnt-nestle1904/text/Matt.txt',encoding='utf-8'):
    if '\t' in l: r,t=l.rstrip('\n').split('\t',1); MT[r]=stems(t)
freq=collections.Counter()
for f in glob.glob(C+'gnt-nestle1904/text/*.txt'):
    for l in open(f,encoding='utf-8'):
        if '\t' in l:
            for s in stems(l.split('\t',1)[1]): freq[s]+=1
rare={s for s,c in freq.items() if c<=60}
iL=collections.defaultdict(set)
i=0
for f in glob.glob(C+'lxx-swete/text/*.txt'):
    for l in open(f,encoding='utf-8'):
        if '\t' in l:
            for s in stems(l.split('\t',1)[1]): iL[s].add(i)
            i+=1
VP={r:[p for p in itertools.combinations(sorted(ss&rare),2) if not (iL[p[0]]&iL[p[1]])] for r,ss in MT.items()}
def rate(ps):
    ix=collections.defaultdict(set)
    for j,s in enumerate(ps):
        for x in s: ix[x].add(j)
    return sum(any(ix[a]&ix[b] for a,b in prs) for prs in VP.values())
random.seed(1127)
SRC={'Philo':'philo','Josephus (in the system)':'josephus','Epictetus':'epictetus-dissertationes-schenkl-1916','Maximus of Tyre':'maximus-tyrius','Strabo':'strabo','Diodorus':'diodorus-bibliotheca'}
T=len(MT); res={}
for n,d in SRC.items():
    P=pieces(words(d)); k=180
    draws=[rate(random.sample(P,k)) for _ in range(20)] if len(P)>k else [rate(P)]
    res[n]=(st.mean(draws),min(draws),max(draws),len(P),rate(P))
    print(f'{n:26} pieces {len(P):5} | at 18,000 words: mean {st.mean(draws):6.1f} verses ({100*st.mean(draws)/T:.1f}%), range {min(draws)}-{max(draws)} | whole corpus {res[n][4]} ({100*res[n][4]/T:.1f}%)')
for c in ('Maximus of Tyre','Epictetus','Strabo','Diodorus','Josephus (in the system)'): print(f'Philo / {c}: {res["Philo"][0]/res[c][0]:.2f}')
print('verses with any candidate pair:',sum(bool(v) for v in VP.values()),'of',T)
