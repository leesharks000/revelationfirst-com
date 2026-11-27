import sys,json,re,collections
exec(open('../residue/r1.py').read().split("print('P1")[0])
N=nf
vf=collections.Counter(l for b in books for k in NT[b] for l in L(b,k))
def sp(b,s):
    out=[]
    for part in re.split(r'[;,]\s*',s):
        m=re.match(r'(\d+):(\d+)(?:[-–](?:(\d+):)?(\d+))?',part.strip())
        c,a=int(m.group(1)),int(m.group(2)); c2=int(m.group(3)) if m.group(3) else c; z=int(m.group(4)) if m.group(4) else a
        out+=[k for k in NT[b] if (c,a)<=k<=(c2,z)]
    return out
C=lambda b,ks:{l for k in ks for l,t,_ in NT[b][k] if t[:2] in('N-','A-','V-')}
# (matthew, [(book, span)], three-way with the Septuagint?, note)
ROWS=[
('5:3',[('JAS','2:5')],0,'the poor and the kingdom'),
('5:7',[('JAS','2:13')],0,'mercy to the merciful'),
('5:9',[('JAS','3:18')],0,'peacemakers'),
('5:10-12',[('1PE','3:14'),('1PE','4:13-14')],0,'blessed when reviled; rejoice'),
('5:16',[('1PE','2:12')],0,'good works seen, God glorified'),
('5:17',[('RO','13:8-10'),('GA','5:14')],0,'the law fulfilled'),
('5:33-37',[('JAS','5:12')],0,'the oath'),
('5:39-44',[('RO','12:14'),('RO','12:17-21')],0,'bless those who persecute; evil for evil'),
('6:13',[('2TI','4:18'),('2TH','3:2-3')],0,'deliver from the evil one'),
('6:19-20',[('JAS','5:2-3')],0,'moth, rust, treasure'),
('6:31-33',[('RO','14:17')],0,'eating and drinking; kingdom and righteousness'),
('7:1-2',[('RO','2:1-3')],0,'judging and being judged'),
('7:7-11',[('JAS','1:5'),('JAS','1:17')],0,'ask and it will be given'),
('7:16-20',[('JAS','3:12')],0,'figs and vines'),
('7:21-27',[('JAS','1:22-25'),('RO','2:13')],0,'hearers and doers'),
('10:10',[('1TI','5:18'),('1CO','9:14')],0,'the worker is worthy'),
('10:16',[('PHP','2:15'),('RO','16:19')],0,'innocent in the midst'),
('10:22; 24:13',[('JAS','5:11')],0,'endure to the end'),
('11:25-27',[('1CO','1:19-21'),('1CO','2:7-10')],1,'hidden from the wise, revealed'),
('13:33; 16:6; 16:11-12',[('GA','5:9'),('1CO','5:6-8')],0,'leaven and the whole lump'),
('15:14',[('RO','2:19')],0,'guide of the blind'),
('15:11; 15:17-20',[('RO','14:14'),('RO','14:20'),('1CO','6:13')],0,'what goes into the belly does not defile'),
('16:17',[('GA','1:15-16')],0,'not flesh and blood'),
('16:21; 17:23; 20:19',[('1CO','15:4')],0,'raised on the third day'),
('16:27',[('RO','2:6')],1,'to each according to works'),
('17:20; 21:21',[('1CO','13:2')],0,'faith to move mountains'),
('21:21-22',[('JAS','1:5-6')],0,'ask in faith, not doubting; the sea'),
('18:6-7',[('RO','14:13'),('1CO','8:13')],0,'the stumbling-block for a brother'),
('18:15-20',[('2CO','13:1'),('1CO','5:3-5')],1,'two or three witnesses; gathered in the name'),
('19:5-9',[('1CO','6:16'),('1CO','7:10-11'),('EPH','5:31')],1,'one flesh; not to separate'),
('19:18-19; 22:37-40',[('RO','13:8-10'),('GA','5:14')],1,'the commandments; love the neighbour'),
('21:42',[('1PE','2:6-8')],1,'the stone rejected'),
('22:44; 26:64',[('HEB','1:13'),('1CO','15:25'),('RO','8:34')],1,'at the right hand; enemies under the feet'),
('23:12',[('JAS','4:10'),('1PE','5:6')],0,'humbled and exalted'),
('23:31-37',[('1TH','2:15-16')],0,'killing the prophets; filling the measure'),
('24:8; 24:19',[('1TH','5:3')],0,'birth pangs; the one with child'),
('24:24',[('2TH','2:9-11')],0,'signs and wonders to deceive'),
('24:30-31',[('1TH','4:16-17')],0,'trumpet, clouds, gathering'),
('24:42-44',[('1TH','5:2-6')],0,'the thief'),
('25:24-26',[('2CO','9:6'),('GA','6:7-8')],0,'sowing and reaping'),
('25:35-44',[('RO','12:20')],1,'hungry, feed; thirsty, give drink'),
('26:26-28',[('1CO','11:23-25')],0,'the supper'),
('26:38-45',[('1TH','5:6-10')],0,'watch and sleep'),
('27:51',[('HEB','10:19-20'),('HEB','6:19'),('HEB','9:3')],0,'the veil'),
('27:52-53',[('1CO','15:20')],0,'those who have fallen asleep raised'),
('28:18',[('COL','1:16'),('COL','1:20')],0,'authority in heaven and on earth'),
('28:19',[('1CO','1:13-15')],0,'baptized into the name'),
('13:39-40; 13:49; 24:3; 28:20',[('HEB','9:26')],0,'the consummation of the age'),
('1:1',[('RO','1:3'),('GA','3:16')],0,'son of David, son of Abraham'),
('3:9',[('RO','9:7-8')],0,'children of Abraham'),
('10:2-6',[('1CO','15:5-7'),('GA','2:7-9')],0,'the twelve, Cephas first; to the circumcision'),
('17:1-8',[('2PE','1:16-18')],0,'the mountain and the voice'),
]
EXTRA=[('16:23',[('RO','16:17-20')],0,'Satan and the stumbling-block'),('17:24-27',[('RO','13:6-7')],0,'tax'),('19:28',[('1CO','6:2-3')],0,'judging'),('23:34-35',[('HEB','11:4'),('HEB','12:24')],0,'Abel'),('14:28-31',[('JAS','1:6')],0,'doubt, wind, sea')]
def run(R,label):
    held=[];cov=set();cov3=set()
    for m,eps,three,note in R:
        mk=sp('MT',m); M=C('MT',mk); E=set()
        for b,s in eps: E|=C(b,sp(b,s))
        sh=sorted((l for l in M&E if vf[l]<=400),key=lambda l:vf[l])
        ok=(len(sh)>=2 and vf[sh[0]]<=100) or (sh and vf[sh[0]]<=10)
        print(f"{'HELD ' if ok else 'no   '}{m:28} {'+'.join(b+' '+s for b,s in eps):34} {'3way ' if three else '     '}{note} | {', '.join(f'{l}({vf[l]})' for l in sh[:7])}")
        if ok: held.append(m); cov|=set(mk); cov3|=set(mk) if not three else set()
    print(label,'held',len(held),'of',len(R),'| verses covered',len(cov),'| without three-way rows',len(cov3))
    return cov,cov3
cov,cov3=run(ROWS,'SEALED LIST'); print(); cx,cx3=run(EXTRA,'READ EARLIER (4.10, 4.12), not part of the sealed 52')
rows=json.load(open('../map/rev-matthew-ledger.json'))['rows']; led=set()
for r in rows: led|=set(sp('MT',r['matt']))
T=len(NT['MT'])
for nm,c in (('sealed list',cov),('sealed list without three-way',cov3),('sealed + read earlier',cov|cx)):
    print(f'{nm}: {len(c)} verses, inside ledger {len(c&led)} ({100*len(c&led)/max(1,len(c)):.0f}%), new {len(c-led)}; with ledger {len(c|led)} = {100*len(c|led)/T:.1f}%')
json.dump(sorted(f'{k[0]}:{k[1]}' for k in (cov|cx)),open('bh.json','w'))
