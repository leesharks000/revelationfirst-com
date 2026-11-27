import sys,collections
sys.path.insert(0,'../residue')
exec(open('../residue/r1.py').read().split("print('P1")[0])
N=nf
def cont(b,ks): return {l for k in ks for l,t,_ in NT[b][k] if t[:2] in('N-','A-','V-')}
def rng(b,c,a,z): return [k for k in NT[b] if k[0]==c and a<=k[1]<=z]
vf=collections.Counter()
for b in books:
    if b=='RE': continue
    for k in NT[b]:
        for l in L(b,k): vf[l]+=1
LET={'Ephesus':rng('RE',2,1,7),'Smyrna':rng('RE',2,8,11),'Pergamum':rng('RE',2,12,17),'Thyatira':rng('RE',2,18,29),'Sardis':rng('RE',3,1,6),'Philadelphia':rng('RE',3,7,13),'Laodicea':rng('RE',3,14,22)}
INNER={'Eph':['EPH'],'Phil':['PHP'],'Cor':['1CO','2CO'],'Rom':['RO'],'Thess':['1TH','2TH'],'Gal':['GA'],'Col':['COL']}
OUTER={'John':['1JO','2JO','3JO'],'James':['JAS'],'Jude':['JUDE'],'Peter':['1PE','2PE'],'Persons':['1TI','2TI','TIT'],'Hebrews':['HEB'],'Paul':['EPH','PHP','1CO','2CO','RO','1TH','2TH','GA','COL']}
SI=dict(zip(LET,['Eph','Phil','Cor','Rom','Thess','Gal','Col'])); SO=dict(zip(LET,['John','James','Jude','Peter','Persons','Hebrews','Paul']))
def G(bs): return set().union(*[cont(b,NT[b].keys()) for b in bs]), sum(len(NT[b][k]) for b in bs for k in NT[b])
def table(groups,seal,name):
    gs={g:G(bs) for g,bs in groups.items()}; hit=0
    print('\n'+name)
    for s,ks in LET.items():
        rare={l for l in cont('RE',ks) if 0<vf[l]<=40}
        sc={g:(len(rare&S),1000*len(rare&S)/n) for g,(S,n) in gs.items()}
        order=sorted(sc,key=lambda g:-sc[g][1]); r=order.index(seal[s])+1; hit+=r<=2
        print(f'{s:13} rare {len(rare):3} | '+'  '.join(f'{g} {sc[g][0]}/{sc[g][1]:.1f}' for g in order)+f' | set: {seal[s]} rank {r}')
        print('      shared with set:',', '.join(sorted(rare&gs[seal[s]][0])))
    print('first or second:',hit,'of 7')
table(INNER,SI,'BC1 inner'); table(OUTER,SO,'BC2 outer')
# BC3
print('\nBC3 inner x outer, shared NT-rare lemmas per 1000 words of the two together')
allf=collections.Counter()
for b in books:
    for k in NT[b]:
        for l in L(b,k): allf[l]+=1
ins=[s for s in LET if s!='Laodicea']; top=0
for s in ins:
    Si,ni=G(INNER[SI[s]]); row={}
    for t in ins:
        So,no=G(OUTER[SO[t]]); sh={l for l in Si&So if allf[l]<=40}; row[SO[t]]=(len(sh),1000*len(sh)/(ni*no)**.5)
    o=sorted(row,key=lambda g:-row[g][1]); top+=o[0]==SO[s]
    print(f'{SI[s]:6}','  '.join(f'{g} {row[g][0]}/{row[g][1]:.1f}' for g in o),'| own:',SO[s],'rank',o.index(SO[s])+1)
print('own-slot highest:',top,'of 6')
def W(b,c,a,z,w=0): 
    S=set()
    for k in rng(b,c,a,z): S|={l for l,t,_ in NT[b][k] if t[:2] in('N-','A-','V-')}
    return S
def tri(name,M,E,R):
    print('\n'+name); print(' M∩E∩R:',sorted(M&E&R)); print(' M∩R not E:',sorted((M&R)-E)); print(' M∩E not R:',sorted((M&E)-R)); print(' E∩R not M:',sorted((E&R)-M))
# BC4
fl=lambda S:{N('σάρξ'),N('αἷμα')}<=S and fam(S,'ἀποκαλύπτω','ἀποκάλυψις')
print('\nBC4 flesh+blood+reveal ±1:',fmt([(b,k) for b in books for k in NT[b] if fl(win(b,k,1)) and N('σάρξ') in L(b,k)]))
print(' flesh+blood one verse:',fmt(has(lambda S:{N('σάρξ'),N('αἷμα')}<=S)))
print(' key all:',fmt(has(lambda S:N('κλείς') in S)),'| key+hades ±1:',fmt([(b,k) for b in books for k in NT[b] if N('κλείς') in L(b,k) and N('ᾅδης') in win(b,k,1)]))
tri('BC4 Matt 16:17-19 | Gal 1:15-16+2:9 | Rev 1:18+3:7-12',W('MT',16,17,19),W('GA',1,15,16)|W('GA',2,9,9),W('RE',1,18,18)|W('RE',3,7,12))
tri('BC5 Matt 5:33-37 | Jas 5:12 | Rev 10:5-6',W('MT',5,33,37),W('JAS',5,12,12),W('RE',10,5,6))
print('\nBC6 tribe+Benjamin:',fmt(has(lambda S:N('φυλή') in S and fam(S,'Βενιαμ'))),'| tribe+Judah:',fmt(has(lambda S:N('φυλή') in S and fam(S,'Ἰούδα'))))
tri('BC6 Matt 1:1-17 | Rom 1:3+11:1, Gal 3:16, Phil 3:5 | Rev 5:5, 7:4-8, 22:16',W('MT',1,1,17),W('RO',1,3,3)|W('RO',11,1,1)|W('GA',3,16,16)|W('PHP',3,5,5),W('RE',5,5,5)|W('RE',7,4,8)|W('RE',22,16,16))
tri('BC7 Matt 24:42-44 | 1 Thess 5:1-6 | Rev 3:2-3+16:15',W('MT',24,42,44),W('1TH',5,1,6),W('RE',3,2,3)|W('RE',16,15,15))
for b,c,v in [('MT',16,17),('MT',16,18),('MT',16,19),('GA',1,16),('GA',2,9),('RE',3,7),('RE',1,18),('RE',3,12),('PHP',3,5),('RE',7,8),('RE',7,5),('RO',1,3),('MT',1,1),('JAS',5,12),('RE',10,6)]: print(b,c,v,text(b,(c,v)))
