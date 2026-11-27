import re,glob,json,collections,unicodedata as U
C='/home/claude/repos/alexanarch/data/corpora/'
def norm(t):
    t=U.normalize('NFD',t); return ''.join(c for c in t if not U.combining(c)).lower().replace('ς','σ')
def load(f):
    out=[]
    for l in open(f,encoding='utf-8'):
        if '\t' in l: r,t=l.rstrip('\n').split('\t',1); out.append((r,norm(t)))
    return out
MT={r.split(' ',1)[1]:t for r,t in load(C+'gnt-nestle1904/text/Matt.txt')}
J={w:load(C+f'josephus/text/{w}.txt') for w in ('AJ','BJ','Vita','CA')}
LX=[t for f in glob.glob(C+'lxx-swete/text/*.txt') for r,t in load(f)]
def span(s):
    out=[]
    for part in re.split(r';\s*',s):
        m=re.match(r'(\d+):(\d+)(?:-(\d+))?',part.strip()); c,a=int(m.group(1)),int(m.group(2)); z=int(m.group(3) or a)
        out+=[f'{c}:{v}' for v in range(a,z+1) if f'{c}:{v}' in MT]
    return out
ROWS=[
# names and offices
('2:16','AJ',['ηρωδ','παιδ','ανειλ|αναιρ|ανελ'],'N','Herod kills children'),
('2:22','AJ',['αρχελα','ιουδαια','βασιλ'],'N','Archelaus reigns in Judaea'),
('14:1','AJ',['ηρωδ','τετρ.?αρχ'],'N','Herod the tetrarch'),
('3:1-6; 14:2','AJ',['ιωαν','βαπτι'],'N','John the baptizer'),
('14:3-4','AJ',['ηρωδιαδ','αδελφ','γυνα|γαμ|γημ'],'N','Herodias, the brother\'s wife'),
('27:2; 27:11-14','AJ',['πε?ιλατ','ηγεμ'],'N','Pilate the governor'),
('26:3; 26:57','AJ',['καιαφ','αρχιερ'],'N','Caiaphas the high priest'),
('3:7; 16:1; 16:6; 16:11-12; 22:23; 22:34','BJ',['φαρισ','σαδδουκ'],'N','Pharisees and Sadducees'),
('4:13; 8:5; 11:23; 17:24','BJ',['καφαρν'],'N','Capernaum'),
('14:34','BJ',['γεννησαρ'],'N','Gennesar'),
('4:25','BJ',['δεκαπολ'],'N','Decapolis'),
('16:13','BJ',['καισαρε?ια','φιλιππ'],'N','Caesarea of Philip'),
('8:28','BJ',['γαδαρ'],'N','Gadara'),
# words and constructions
('27:6','BJ',['κορβ'],'W','the sacred treasure, korban'),
('17:24','AJ',['διδραχμ'],'W','the didrachm'),
('5:33-34','BJ',['ομνυ|ομοσ','επιορκ'],'W','swearing and false swearing (Essenes)'),
('22:7','BJ',['ενεπρησ|εμπιπρ|ενεπιμπρ|εμπρησ','πολ[ιε]'],'W','the city burned'),
('5:41; 27:32','AJ',['αγγαρ'],'W','pressed into service'),
('20:1-12','AJ',['μια[νσ]?\\b','ωρα','μισθ'],'W','one hour and the full wage (temple workmen)'),
('24:27-31','BJ',['ανατολ','δυσ[μεω]','τεσσαρ','ανεμ'],'W','east, west, the four winds (Jesus son of Ananias)'),
('24:24-26','BJ',['ψευδοπροφ','ερημ','σημει'],'W','false prophet, wilderness, signs'),
('24:15','AJ',['δανιηλ','ερημω'],'W','Daniel and the desolation'),
('23:35','BJ',['ζαχαρι','υιο','\\bβαρ[αειο]'],'W','Zechariah son of Bar-'),
('12:22-45','AJ',['δαιμον','σολομ'],'W','demons and Solomon'),
('3:1-4','Vita',['ερημ','τροφ','εσθητ|ενδυμ'],'W','wilderness, food, clothing (Bannus)'),
('10:9-10','BJ',['υποδημ','χιτων|εσθητ'],'W','sandals and garments on the road (Essenes)'),
('9:9-11; 10:3','BJ',['τελων'],'W','the tax collector'),
('27:38; 27:44','BJ',['ληστ','σταυρ'],'W','robbers crucified'),
('21:12-13','BJ',['ληστ','ιερ[οω]|ναο'],'W','robbers and the temple'),
('27:11-14','BJ',['ιησου','απεκρι'],'W','a Jesus who answers the governor nothing'),
('27:15-16','AJ',['δεσμ','απολυ|απελυ'],'W','prisoners released'),
('1:15-16','Vita',['ματθ|μαθθ','ιωση'],'W','Matth- and Joseph at the foot of a genealogy'),
('27:51','BJ',['καταπετασμ'],'W','the veil'),
('24:28','BJ',['αετ[οω]'],'W','eagles'),
('1:20; 2:12-13; 2:19; 2:22; 27:19','AJ',['οναρ'],'W','in a dream'),
('2:2; 2:9-10','BJ',['αστρ|αστηρ|αστερ','πολ[ιε]'],'W','a star standing over'),
('24:7','BJ',['λιμο[ισυν]|λιμω','σεισμ'],'W','famine and earthquake'),
('27:57-60','Vita',['σταυρ','καθαιρ|καθελ'],'R','a Joseph asks the ruler for the crucified'),
]
def has(t,keys): return all(re.search(k,t) for k in keys)
held=[];cov=set();covW=set();covN=set()
for m,w,keys,cl,note in ROWS:
    mk=span(m); mt=' '.join(MT[k] for k in mk); inM=has(mt,keys)
    U_=J[w]; hits=[]
    for i in range(len(U_)):
        t=' '.join(x[1] for x in U_[max(0,i-1):i+2])
        if has(t,keys): hits.append(U_[i][0])
    # collapse adjacent
    loci=[];last=-9
    idx={r:i for i,(r,_) in enumerate(U_)}
    for h in hits:
        if idx[h]-last>2: loci.append(h)
        last=idx[h]
    three=any(has(t,keys) for t in LX) if len(keys)>1 else None
    ok=inM and bool(hits)
    print(f"{'HELD' if ok else 'no  '} {cl} {m:38} {w:4} {note} | in Matthew {inM} | places in {w}: {len(loci)} {loci[:4]} | LXX one verse: {three}")
    if ok and cl!='R':
        held.append(m); cov|=set(mk); (covN if cl=='N' else covW).update(mk)
tot=len(MT); print('\nheld',len(held),'of',len(ROWS),'| verses',len(cov),'| names class',len(covN),'| words class',len(covW))
import sys; sys.path.insert(0,'../layer')
led=set()
for r in json.load(open('../map/rev-matthew-ledger.json'))['rows']:
    for part in re.split(r'[;,]\s*',r['matt']):
        mm=re.match(r'(\d+):(\d+)(?:[-–](?:(\d+):)?(\d+))?',part.strip())
        if not mm: continue
        c,a=int(mm.group(1)),int(mm.group(2)); c2=int(mm.group(3)) if mm.group(3) else c; z=int(mm.group(4)) if mm.group(4) else a
        for k in MT:
            kc,kv=map(int,k.split(':'))
            if (c,a)<=(kc,kv)<=(c2,z): led.add(k)
let=set(json.load(open('../layer/bh.json')))
T=1067
print('ledger',len(led),'letters',len(let),'ledger∪letters',len(led|let))
for nm,c in (('Josephus all held',cov),('Josephus words class only',covW)):
    print(f'{nm}: {len(c)} verses | inside ledger {len(c&led)} | inside letters {len(c&let)} | new beyond both {len(c-led-let)} | total {len(led|let|c)} = {100*len(led|let|c)/T:.1f}%')
json.dump(sorted(cov),open('bj2.json','w'))
