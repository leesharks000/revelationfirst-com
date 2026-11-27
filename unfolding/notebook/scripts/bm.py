import re,glob,unicodedata as U
C='/home/claude/repos/alexanarch/data/corpora/'
G2C=dict(zip('αβγδεζηθικλμνξοπρστυφχψω','ⲁⲃⲅⲇⲉⲍⲏⲑⲓⲕⲗⲙⲛⲝⲟⲡⲣⲥⲧⲩⲫⲭⲯⲱ'))
def cn(s):
    s=U.normalize('NFD',s); return ''.join(c for c in s if not U.combining(c) and c not in '⳿·[]()<>{}.,:;')
def gn(t):
    t=U.normalize('NFD',t); return ''.join(c for c in t if not U.combining(c)).lower().replace('ς','σ')
TH=[cn(l.split('\t',1)[1]) for l in open(C+'coptic-gnostic/text/thomas-gospel-cop.txt',encoding='utf-8') if '\t' in l]
RE={}
for l in open(C+'gnt-nestle1904/text/Rev.txt',encoding='utf-8'):
    if '\t' in l: r,t=l.rstrip('\n').split('\t',1); RE[r.split(' ',1)[1]]=gn(t)
GK=gn(re.sub(r'[\[\]\(\){}]','',' '.join(l.split('\t',1)[1] for l in open(C+'nh-greek-witnesses/text/gospel-of-thomas-greek.txt',encoding='utf-8') if '\t' in l)))
def k2c(k):  # 'g:παραδ' -> coptic substring; 't:ⲟⲛϩ' token; plain coptic substring
    if k.startswith('g:'): return ('sub',''.join(G2C[c] for c in k[2:]))
    if k.startswith('t:'): return ('tok',k[2:])
    return ('sub',k)
def th_find(keys,w=4):
    ks=[[k2c(a) for a in k.split('|')] for k in keys]; out=[]
    for i in range(len(TH)):
        seg=' '.join(TH[max(0,i-w):i+w+1]); toks=set(seg.split()); flat=seg.replace(' ','')
        if all(any((m=='tok' and v in toks) or (m=='sub' and v in flat) for m,v in alt) for alt in ks): out.append(i)
    loci=[];last=-99
    for i in out:
        if i-last>w: loci.append(i)
        last=i
    return loci
def rv(refs,keys):
    t=' '.join(RE[r] for r in refs if r in RE); return all(re.search(k,t) for k in keys)
ROWS=[
('Prol.','the living Jesus; written words; not taste death',['t:ⲟⲛϩ','ⲥϩⲁⲓ'],['1:18','1:19'],['ζων','γραψον']),
('2','reign, and rest',['ⲣⲣⲟ','t:ⲧⲏⲣ'],['3:21','20:6','14:13'],['βασιλευσ','αναπαησονται']),
('3','know yourselves; you are poverty',['ϩⲏⲕⲉ','ⲥⲟⲩⲱⲛ'],['2:9','3:17'],['πτωχ','οιδα']),
('4','first and last',['ϣⲟⲣⲡ','ϩⲁⲉ'],['1:17','22:13'],['πρωτοσ','εσχατοσ']),
('8,21,24,63,65,96','whoever has ears, let him hear',['ⲙⲁⲁϫⲉ','ⲥⲱⲧⲙ'],['2:7','13:9'],['ουσ','ακουσατω']),
('10','fire cast on the world',['ⲕⲱϩⲧ','g:κοσμοσ','ⲛⲟⲩϫⲉ'],['8:5','8:7'],['πυρ','εβαλεν|εβληθη','γην']),
('16','fire, sword, war on the earth',['ⲥⲏϥⲉ','g:πολεμοσ','ⲕⲱϩⲧ'],['6:4','19:11','13:10'],['μαχαιρα','πολεμ']),
('11','this heaven will pass away; the dead do not live',['t:ⲡⲉ','g:παραγε','ⲙⲟⲟⲩⲧ'],['21:1','20:5'],['ουρανοσ','απηλθ|παρηλθ','νεκρων']),
('111','heaven and earth rolled up in your presence',['ϭⲱⲗ','ⲙⲧⲟ','t:ⲕⲁϩ'],['6:14','20:11'],['ελισσομενον','προσωπου','ουρανοσ']),
('13','the bubbling spring; words not to be told',['g:πηγη','ⲥⲱ'],['21:6','22:17','10:4'],['πηγησ','μη αυτα γραψησ']),
('18','beginning and end',['g:αρχη','ϩⲁⲏ'],['21:6','22:13'],['αρχη','τελοσ']),
('19','trees in paradise whose leaves do not fall',['g:παραδ','ϣⲏⲛ','ϭⲱⲃⲉ'],['2:7','22:2'],['παραδεισω','ξυλον','φυλλα']),
('21','the thief, watching, and the garments',['ϫⲓⲟⲩⲉ','ⲣⲟⲉⲓⲥ','ϣⲧⲏⲛ'],['16:15','3:3'],['κλεπτησ','γρηγορ','ιματια']),
('21','the sickle in his hand, the fruit ripe',['ⲁⲥϩ','ϭⲓϫ','g:καρποσ'],['14:14','14:15','14:18'],['δρεπανον','χειρι','θερισ|σταφυλ']),
('23','one from a thousand, two from ten thousand, standing',['t:ϣⲟ','ⲧⲃⲁ','ⲱϩⲉ'],['5:11','7:4','14:1'],['μυριαδ','χιλιαδ','εστοσ|εστηκ']),
('28','I stood in the midst; drunk; blind',['ⲙⲏⲧⲉ','g:κοσμοσ','ⲧⲁϩⲉ|ϯϩⲉ','ⲃⲗⲗⲉ'],['5:6','1:13','17:6','3:17'],['εν μεσω','εστηκοσ','μεθυ','τυφλοσ']),
('32','a city on a high mountain',['g:πολισ','ⲧⲟⲟⲩ','ϫⲟⲥⲉ'],['21:10'],['οροσ','υψηλον','πολιν']),
('37','undress without shame',['ϣⲓⲡⲉ','ϣⲧⲏⲛ'],['3:18','16:15'],['αισχυνη|ασχημοσυνη','ιματια']),
('39','the keys taken and hidden; not entering',['ϣⲟϣⲧ','g:γνωσισ'],['3:7','1:18'],['κλει[νσ]']),
('51','the rest of the dead and the new world',['g:αναπαυσισ','ⲙⲟⲟⲩⲧ','g:κοσμοσ','ⲃⲣⲣⲉ'],['14:13','21:1','21:5'],['νεκροι','αναπαησονται','καιν']),
('52','twenty-four prophets; the living and the dead',['ϫⲟⲩⲧⲁϥⲧⲉ','g:προφητησ'],['4:4','11:16','11:18'],['εικοσι τεσσαρ','προφητ']),
('56,80','the world a corpse',['g:πτωμα','g:κοσμοσ'],['11:8','11:9'],['πτωμα']),
('60','a lamb to be killed and eaten',['ϩⲓⲉⲓⲃ','ⲙⲟⲟⲩⲧ'],['5:6','5:12'],['αρνιον','εσφαγμεν']),
('61','on the bed; eating from the table; given of my father',['ϭⲗⲟϭ','g:τραπεζα','ⲉⲓⲱⲧ'],['2:22','3:20','2:28'],['κλινην','δειπνησω','πατροσ']),
('62','mysteries for the worthy',['g:μυστηριον','ⲙⲡϣⲁ'],['10:7','3:4','5:2'],['μυστηριον','αξιο']),
('64','the supper; buyers and merchants shut out',['g:διπνον','ⲉϣⲟⲧ|ⲉϣⲱⲧ'],['19:9','18:11','13:17'],['δειπνον','εμποροι','αγορασαι']),
('75','many at the door; the bridal chamber',['t:ⲣⲟ','g:νυμφ|ϣⲉⲗⲉⲉⲧ'],['3:20','19:7','21:2'],['θυραν','νυμφ|γαμοσ']),
('76','the merchant, the cargo, the pearl',['ⲉϣⲱⲧ','g:φορτιον','g:μαργαρ'],['18:11','18:12'],['εμποροι','γομον','μαργαριτ']),
('77','I am the all; from me the all came, to me it reached',['ⲁⲛⲟⲕ','t:ⲧⲏⲣ','ⲟⲩⲟⲉⲓⲛ'],['1:8','22:13','22:16'],['εγω ειμι|εγω το αλφα','αστηρ|αρχη']),
('83,84','images',['ϩⲓⲕⲱⲛ'],['13:14','13:15'],['εικον']),
('88','the angels and the prophets will come',['g:αγγελοσ','g:προφητησ'],['22:6','22:9'],['αγγελον','προφητων']),
('93','what is holy, dogs, pearls',['ⲟⲩϩⲟⲟⲣ|ⲟⲩϩⲱⲣ','g:μαργαρ','ⲟⲩⲁⲁⲃ'],['22:15','21:21','22:11'],['κυνεσ','μαργαριτ','αγιοσ']),
('98','the sword that slays the mighty',['ⲥⲏϥⲉ','ϫⲱⲱⲣⲉ|ⲙⲉⲅⲓⲥⲧⲁⲛⲟⲥ'],['19:18','19:21'],['ισχυρων','ρομφαια']),
('104','the bridegroom leaves the bridal chamber',['g:νυμφιοσ','g:νυμφων'],['18:23'],['νυμφιου','νυμφησ']),
('108','whoever drinks from my mouth',['ⲧⲁⲡⲣⲟ','ⲥⲱ'],['3:16','22:17'],['στοματοσ','εμεσαι|λαβετω υδωρ']),
('114','made male',['ϩⲟⲟⲩⲧ','ⲥϩⲓⲙⲉ'],['12:5','14:4'],['αρσεν','γυναικων']),
]
held=0;unv=[]
for lg,note,tk,refs,rk in ROWS:
    loci=th_find(tk); r=rv(refs,rk); ok=bool(loci) and r; held+=ok
    miss=[k for k in tk if not th_find([k],0)] if not loci else []
    if not loci and miss: unv.append(lg)
    print(f"{'HELD' if ok else 'no  '} {lg:18} {note[:46]:46} | Thomas lines {loci[:4]} ({len(loci)}) | Rev {r} {','.join(refs)}"+(f" | not in the Coptic as I spelled: {miss}" if miss else ''))
print('held',held,'of',len(ROWS),'| missed on a word not found at all (my spelling or my memory):',unv)
print('\nBM2 Greek fragments:')
for nm,p in (('ο ζων of Jesus','ιησουσ ο ζων'),('πρωτοι εσχατοι','πρωτοι.{0,12}εσχατοι'),('εστην εν μεσω','εστην εν μεσω'),('city, mountain, high','πολισ.{0,60}ορουσ.{0,12}υψηλ'),('not ashamed','αισχυν'),('keys','κλειδ'),('poverty','πτωχεια'),('reign and rest','βασιλευσ.{0,40}αναπαησ')):
    m=re.search(p,GK); print(' ',nm,':',bool(m),m.group(0)[:70] if m else '')
NT={}
for f in glob.glob(C+'gnt-nestle1904/text/*.txt'):
    for l in open(f,encoding='utf-8'):
        if '\t' in l: r,t=l.rstrip('\n').split('\t',1); NT[r]=gn(t)
print('\nBM3 Matt 5:14:',NT['Matt 5:14']); print('    Matt 13:45-46:',NT['Matt 13:45'],NT['Matt 13:46']); print('    Rev 21:10:',RE['21:10'][:110]); print('    Rev 18:11-12:',RE['18:11'],RE['18:12'][:60])
print('    paradise in NT:',[r for r,t in NT.items() if 'παραδεισ' in t])
print('BM4 twenty-four in NT:',[r for r,t in NT.items() if 'εικοσι τεσσαρ' in t or 'εικοσιτεσσαρ' in t])
flat=[t.replace(' ','') for t in TH]
print('BM5 ear+hear lines:',len(th_find(['ⲙⲁⲁϫⲉ','ⲥⲱⲧⲙ'],1)),'| Thomas 24-count check ϫⲟⲩⲧⲁϥⲧⲉ:',sum('ϫⲟⲩⲧⲁϥⲧⲉ' in t for t in flat))
