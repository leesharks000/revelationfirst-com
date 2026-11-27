# Relation lemmas: three levels above the lemma. KIN (one derivational family), FIELD (one Louw-Nida subdomain), OPP (opposed families).
# Data: MACULA Greek, Nestle 1904 (Clear-Bible/macula-greek, CC BY 4.0, (c) Biblica): lemma, class, Louw-Nida codes per word.
import csv,re,collections,unicodedata as U,itertools
TSV='/tmp/fetch/macula/macula-greek/Nestle1904/tsv/macula-greek-Nestle1904.tsv'
def norm(t):
    t=U.normalize('NFD',t); return ''.join(c for c in t if not U.combining(c)).lower().replace('ς','σ')
BK={'MAT':'MT','MRK':'MR','LUK':'LU','JHN':'JOH','ACT':'AC','ROM':'RO','1CO':'1CO','2CO':'2CO','GAL':'GA','EPH':'EPH','PHP':'PHP','COL':'COL','1TH':'1TH','2TH':'2TH','1TI':'1TI','2TI':'2TI','TIT':'TIT','PHM':'PHM','HEB':'HEB','JAS':'JAS','1PE':'1PE','2PE':'2PE','1JN':'1JO','2JN':'2JO','3JN':'3JO','JUD':'JUDE','REV':'RE'}
V=collections.defaultdict(list); LN=collections.defaultdict(set); CLS={}
for r in csv.DictReader(open(TSV,encoding='utf-8'),delimiter='\t'):
    m=re.match(r'(\w+) (\d+):(\d+)',r['ref'])
    if not m: continue
    b=BK[m.group(1)]; k=(int(m.group(2)),int(m.group(3))); l=norm(r['lemma'])
    if r['class'] in('noun','verb','adj','adv'):
        V[(b,k)].append(l); CLS[l]=r['class']
        for d in r['domain'].split(): LN[l].add(d)
LEM=sorted(CLS)
PRE=['αντι','απο','ανα','δια','εισ','εκ','εξ','εν','εμ','εγ','επι','κατα','καθ','κατ','μετα','μεθ','μετ','παρα','παρ','περι','προσ','προ','συν','συμ','συγ','συλ','συ','υπερ','υπο','υπ','απ','αν','επ','αφ','εφ']
SUF=['ημοσυνη','οσυνη','ημων','ικοσ','ισμοσ','ιζομαι','ιζω','αζω','ευω','υνω','αινω','εομαι','αομαι','οομαι','ομαι','εω','αω','οω','μι','ωσισ','ησισ','σισ','μοσ','μα','τησ','τηρ','τωρ','τοσ','ινοσ','ειοσ','οτησ','ευσ','εια','ια','οσ','ον','ησ','ισ','υσ','η','α','ω']
def stem(l):
    for x in SUF:
        if l.endswith(x) and len(l)-len(x)>=3: return l[:-len(x)]
    return l
ST={l:stem(l) for l in LEM}
TOK=collections.Counter(l for v in V.values() for l in v)
byst=collections.defaultdict(set)
for l,s in ST.items(): byst[s].add(l)
stfreq={s:sum(TOK[l] for l in ls) for s,ls in byst.items()}
def dom3(l): return {d[:3] for d in LN[l]}
def sdom(s): return set().union(*[dom3(x) for x in byst[s]]) if s in byst else set()
FAM={}; NEG={}
def strip_i(s): return s[:-1] if s.endswith('ι') and len(s)>4 else s
for l in LEM:
    s=ST[l]; r={s}; neg=False
    # shorter stem that is a prefix of this one (ειρην in ειρηνικ), guarded by a shared domain
    for n in range(len(s)-1,3,-1):
        if s[:n] in byst and (sdom(s[:n])&dom3(l)): r.add(s[:n]); break
    for p in PRE:
        if s.startswith(p) and len(s)-len(p)>=3 and s[len(p):] in byst and (sdom(s[len(p):])&dom3(l) or len(s)-len(p)>=5): r.add(s[len(p):])
    for p in ('αν','α'):
        t=s[len(p):]
        if s.startswith(p) and len(t)>=3 and t in byst and (sdom(t)&dom3(l)): r.add(t); neg=True; break
    if not neg:
        for i in range(4,len(s)-2):
            a,b_=s[:i],s[i:]
            a2=a[:-1] if a[-1] in 'οι' else a
            for bb in {b_, b_+'ι' if False else b_}:
                if a2 in byst and len(a2)>=4 and bb in byst and (len(bb)>=4 or stfreq[bb]>=50): r|={a2,bb}
        # compounds whose second part lost its vowel to the ending (ειρηνοποι-οσ)
        for x in ('ποιοσ','ποιεω','ποιια','ποιησισ','ποιητοσ'):
            if l.endswith(x) and len(l)-len(x)>=4:
                a=l[:-len(x)]; a2=a[:-1] if a[-1]=='ο' else a
                if a2 in byst: r|={a2,'ποι'}
    FAM[l]=r; NEG[l]=neg
# polarity: opposed families, by hand (the reader's table; roots as stemmed above)
OPP=[('ελε','σκληρ'),('ελε','ωμ'),('πρωτ','εσχατ'),('ευλογ','καταρ'),('δε','λυ'),('ανοιγ','κλει'),('ζω','θανατ'),('ζω','νεκρ'),('φωτ','σκοτ'),('πλουσι','πτωχ'),('πλουτ','πτωχ'),('ταπειν','υψ'),('αγαπ','μισ'),('πειν','χορτ'),('γυμν','ενδυ'),('γυμν','περιβαλ'),('γρηγορ','καθευδ'),('συναγ','σκορπ'),('ιασ','πληγ'),('θεραπ','πληγ'),('κριν','αφι'),('πιστ','διστ'),('πιστ','διακριν'),('δικαι','αμαρτ'),('ειρην','μαχαιρ'),('ειρην','πολεμ'),('σοφ','μωρ'),('μεγ','μικρ'),('χαρ','λυπ'),('κλαι','γελ'),('δουλ','ελευθερ'),('σπειρ','θεριζ'),('διδ','λαμβαν'),('ομολογ','αρν'),('κρυπτ','φανερ'),('κρυπτ','αποκαλυπτ'),('στεν','πλατ'),('καθαρ','ακαθαρτ'),('ολιγ','πολ')]
OPPS=collections.defaultdict(set)
for a,b in OPP: OPPS[a].add(b); OPPS[b].add(a)
def fams(l): return FAM.get(l,{l})
def sub(l): return LN.get(l,set())
if __name__=='__main__':
    print('lemmas',len(LEM),'stems',len(byst))
    for probe in ['ελε','ειρην','ποι','δικαι','πιστ','κριν','πλουτ','μακαρ','ακου','γαμ','σκανδαλ','ομ','ορκ']:
        print(probe,sorted(l for l in LEM if probe in FAM[l])[:22])
    for l in ['ειρηνοποιοσ','ανελεοσ','ελεημων','ελεοσ','ελεεω','ακροατησ','ακουω','ποιητησ','ποιεω','αδικια','απιστια','ελευθεροσ','ψευδοπροφητησ','επιορκεω','ομνυω']:
        print(' ',l,ST.get(l),sorted(FAM.get(l,[])),'neg' if NEG.get(l) else '',sorted(LN.get(l,[]))[:4])
