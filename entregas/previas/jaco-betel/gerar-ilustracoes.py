"""Papiro Revela: Jacó em Betel: original paper-card illustrations.
Python 3 + Pillow; outputs alongside this file. No voice/API calls.
"""
from pathlib import Path
from functools import lru_cache
import math,json,random,subprocess,sys
from PIL import Image,ImageDraw,ImageFont
OUT=Path(__file__).resolve().parent;S=2
PAPER='#e5dfcf';INK='#262822';TEAL='#236963';ORANGE='#e85c2e';GOLD='#efbd49';CREAM='#f8f2df';SKIN='#bd875e'
FONT=Path('/usr/share/fonts/truetype/dejavu')
@lru_cache(maxsize=150)
def font(size,italic=False):return ImageFont.truetype(str(FONT/('DejaVuSerif-Italic.ttf' if italic else 'DejaVuSansCondensed-Bold.ttf')),round(size*S))
class C:
 def __init__(self,w=540,h=960,bg=PAPER):self.im=Image.new('RGB',(w*S,h*S),bg);self.d=ImageDraw.Draw(self.im)
 def poly(self,p,f,o=None,w=2):
  pts=[(round(x*S),round(y*S)) for x,y in p];self.d.polygon(pts,f)
  if o:self.d.line(pts+[pts[0]],o,w*S,joint='curve')
 def line(self,p,f=INK,w=2):self.d.line([(round(x*S),round(y*S)) for x,y in p],f,round(w*S),joint='curve')
 def rect(self,b,f,o=None,w=2):self.d.rectangle(tuple(round(v*S) for v in b),f,o,w*S)
 def ellipse(self,b,f,o=None,w=2):self.d.ellipse(tuple(round(v*S) for v in b),f,o,w*S)
 def text(self,x,y,t,size=20,col=INK,italic=False,anchor='la',maxw=470):
  while self.d.textlength(t,font(size,italic))>maxw*S:size-=.5
  self.d.text((round(x*S),round(y*S)),t,font=font(size,italic),fill=col,anchor=anchor)

def ease(t):t=max(0,min(1,t));return t*t*(3-2*t)

def ik(shoulder,target,l1=45,l2=44,side=1):
 dx,dy=target[0]-shoulder[0],target[1]-shoulder[1];d=max(.1,min(math.hypot(dx,dy),l1+l2-.01));theta=math.atan2(dy,dx)
 alpha=math.acos(max(-1,min(1,(l1*l1+d*d-l2*l2)/(2*l1*d))))
 elbow=(shoulder[0]+l1*math.cos(theta+side*alpha),shoulder[1]+l1*math.sin(theta+side*alpha))
 wrist=(shoulder[0]+d*math.cos(theta),shoulder[1]+d*math.sin(theta))
 return elbow,wrist

def actor(c,x,y,s=1,who='jacob',left=(-42,-64),right=(43,-64),fur=False,seated=False,tension=False,tilt=0):
 color={'jacob':TEAL,'disguise':ORANGE,'esau':ORANGE,'isaac':'#9da68c','rebecca':TEAL}[who]
 hair='#d4cbb3' if who=='isaac' else '#a35e34' if who=='esau' else '#4e3c2b'
 def q(p):return [(x+a*s,y+b*s) for a,b in p]
 # Bent legs for seated Isaac; feet planted independently of upper-body gestures.
 if seated:
  c.line(q([(-42,-137),(-42,-37),(30,-37)]),'#6a5840',5)
  c.line(q([(-42,-37),(-42,10)]),'#6a5840',5);c.line(q([(26,-37),(26,10)]),'#6a5840',5)
  c.poly(q([(-27,-45),(10,-38),(24,-13),(46,-9),(44,4),(6,4),(-10,-19),(-29,-18)]),'#7b735f',CREAM,2)
  c.line(q([(-35,-47),(-35,8)]),'#6a5840',5)
 else:
  for xx in [-12,12]:c.line(q([(xx,-29),(xx,8)]),'#7e5e42',8)
 c.poly(q([(-24,-125),(-31,-84),(-34,-27),(29,-27),(28,-86),(22,-125)]),color,CREAM,3)
 c.line(q([(-28,-68),(27,-68)]),'#b29461',4)
 c.poly(q([(-7,-130),(-7,-121),(9,-121),(9,-131)]),SKIN)
 # Head can rotate around its base, separately from torso and arms.
 hx,hy=x,y-151*s
 def headq(p):
  a=math.radians(tilt);return [(hx+s*(u*math.cos(a)-v*math.sin(a)),hy+s*(u*math.sin(a)+v*math.cos(a))) for u,v in p]
 c.poly(headq([(-19,-22),(-10,-33),(11,-32),(21,-18),(18,9),(7,20),(-9,17),(-20,4)]),SKIN,CREAM,2)
 if who=='rebecca':c.poly(headq([(-23,12),(-26,-29),(0,-44),(25,-28),(25,13),(16,20),(13,-19),(0,-28),(-15,-19),(-15,17)]),'#c39468',CREAM,2)
 else:
  c.poly(headq([(-21,-7),(-24,-25),(-10,-40),(12,-38),(23,-24),(20,-8),(10,-20),(-6,-24),(-17,-15)]),hair,CREAM,2)
  if who in ['isaac','esau']:c.poly(headq([(-17,1),(-8,-2),(1,2),(11,-2),(18,4),(12,23),(0,29),(-13,21)]),hair,CREAM,1)
 for ex in [-8,8]:
  if who=='isaac':c.line(headq([(ex-4,-5),(ex+3,-4)]),INK,1)
  else:
   pt=headq([(ex,-5)])[0];c.ellipse((pt[0]-1.6*s,pt[1]-1.6*s,pt[0]+1.6*s,pt[1]+1.6*s),INK)
  if tension:c.line(headq([(ex-4,-14),(ex+3,-11 if ex<0 else -16)]),INK,1)
 # Arms solved as shoulder→elbow→wrist chains, with visible joints.
 for sh,target,side in [((-23,-115),left,1),((23,-115),right,-1)]:
  elbow,wrist=ik(sh,target,side=side)
  c.line(q([sh,elbow]),CREAM,15);c.line(q([sh,elbow]),color,11)
  c.line(q([elbow,wrist]),CREAM,13);c.line(q([elbow,wrist]),SKIN,9)
  px,py=q([wrist])[0];c.ellipse((px-5*s,py-5*s,px+5*s,py+5*s),SKIN,CREAM,1)
  if fur:
   c.ellipse((px-7*s,py-6*s,px+7*s,py+6*s),'#a39272',CREAM,1)
   for k in [-3,0,3]:c.line([(px+k*s,py-5*s),(px+(k+2)*s,py+3*s)],'#6f6652',1)
 if fur:
  c.poly(q([(-11,-128),(12,-128),(13,-115),(-12,-115)]),'#a39272',CREAM,1)
  for xx in [-6,0,6]:c.line(q([(xx,-126),(xx+3,-117)]),'#6f6652',1)

def ground(c,night=False):
 c.rect((0,0,460,410),'#273d43' if night else TEAL)
 if night:
  for x,y in [(34,37),(99,66),(167,29),(242,59),(318,25),(415,76),(366,117)]:
   c.line([(x-3,y),(x+3,y)],CREAM,1);c.line([(x,y-3),(x,y+3)],CREAM,1)
 else:c.ellipse((357,30,416,89),GOLD)
 c.poly([(0,209),(81,171),(166,201),(282,160),(379,192),(460,166),(460,410),(0,410)],'#5f7770' if night else '#7f9673')
 c.poly([(0,306),(111,268),(253,299),(366,261),(460,298),(460,410),(0,410)],'#526b62' if night else '#9aab80')
 c.poly([(229,238),(247,239),(275,295),(239,348),(281,410),(231,410),(205,347),(253,294)],'#a5aa83' if night else '#d8c38f')

def stone(c,x,y,standing=False):
 pts=[(-38,7),(-25,-10),(9,-14),(32,-1),(38,18),(18,27),(-26,25)] if not standing else [(-22,110),(-28,30),(-9,0),(17,3),(31,104),(17,114)]
 c.poly([(x+a,y+b) for a,b in pts],'#9b9e8c',CREAM,3)
 if standing:c.line([(x-11,y+14),(x-13,y+96)],'#c7c9b3',2)

def sleeping(c):
 stone(c,127,316)
 c.poly([(148,298),(176,281),(281,295),(327,312),(322,340),(173,340),(147,327)],TEAL,CREAM,3)
 c.poly([(318,313),(347,315),(353,327),(322,328)],'#78583d',CREAM,2)
 c.ellipse((104,267,150,312),SKIN,CREAM,2)
 c.poly([(104,292),(102,273),(112,257),(136,258),(148,272),(146,281),(128,277),(114,282)],'#4e3c2b',CREAM,2)
 c.line([(116,291),(123,292)],INK,1)
 c.line([(164,305),(195,319),(223,311)],SKIN,8)

def angel(c,x,y,s=.7,down=False):
 def q(p):return [(x+a*s,y+b*s) for a,b in p]
 # Plain light-robed messengers; no wings or halos asserted by this passage.
 c.line(q([(-7,-2),(-12,14)]),CREAM,5);c.line(q([(7,-2),(14,8)]),CREAM,5)
 c.poly(q([(-12,-45),(-17,0),(17,0),(12,-45)]),CREAM,'#b6c6bd',1)
 c.ellipse((x-11*s,y-69*s,x+11*s,y-47*s),'#d6bb92',CREAM,1)
 c.line(q([(-12,-38),(-24,-25 if down else -47)]),CREAM,4)
 c.line(q([(12,-38),(25,-47 if down else -25)]),CREAM,4)

def dream(c,p):
 ground(c,True)
 # Schematic inclined stair/ladder; not an exact claimed ancient design.
 c.poly([(108,355),(144,364),(355,49),(319,40)],'#b7ad82',CREAM,2)
 for j in range(11):
  t=j/10;x=108+211*t;y=355-315*t;c.line([(x,y),(x+36,y+9)],CREAM,4)
 for t,down in [(.16,False),(.39,True),(.63,False),(.84,True)]:
  t=t+(.022*math.sin(math.pi*p*2))*(-1 if down else 1)
  angel(c,125+211*t,350-315*t,.64,down)
 c.ellipse((288,22,353,57),'#bac8b8',None);c.ellipse((325,24,389,60),'#bac8b8',None)
 c.text(230,378,'UMA CENA DO SONHO',14,CREAM,anchor='ma')

def oiljar(c,x,y,s=.8,angle=60):
 def q(p):
  a=math.radians(angle);return [(x+s*(u*math.cos(a)-v*math.sin(a)),y+s*(u*math.sin(a)+v*math.cos(a))) for u,v in p]
 c.poly(q([(-7,-34),(8,-34),(6,-22),(17,-8),(14,12),(-12,12),(-17,-8),(-5,-22)]),'#b68151',CREAM,2)
 c.line(q([(-7,-34),(8,-34)]),GOLD,2)

def info(c,y,head,sub,gold=False):
 c.rect((30,y,430,y+96),GOLD if gold else CREAM,'white',4)
 c.text(51,y+14,head,25,TEAL,maxw=355)
 c.text(51,y+54,sub,22,INK,italic=True,maxw=355)

def action(c,i,t):
 p=ease(t)
 if i==0:
  ground(c,True);actor(c,182+32*p,338,1.1,'jacob',left=(-34,-42),right=(34,-42))
  c.text(230,56,'RUMO A HARÃ',19,CREAM,anchor='ma')
 elif i==1:ground(c,True);sleeping(c)
 elif i==2:dream(c,p)
 elif i==3:
  ground(c,True);info(c,42,'O DEUS DE ABRAÃO','e de Isaque.')
  actor(c,228,346,1.05,'jacob',left=(-34,-42),right=(34,-42),tilt=-2)
  c.text(230,378,'A PROMESSA ALCANÇA JACÓ',15,CREAM,anchor='ma')
 elif i==4:
  ground(c);actor(c,109,339,1,'jacob',left=(-34,-42),right=(57,-90))
  info(c,33,'À SUA DESCENDÊNCIA','a promessa da terra.')
  for k in range(36):
   x=190+(k%9)*26;y=256+(k//9)*22;c.ellipse((x-2,y-2,x+2,y+2),CREAM)
  c.text(292,364,'COMO O PÓ DA TERRA',15,CREAM,anchor='ma')
 elif i==5:
  ground(c)
  for y,h,s in [(32,'PRESENÇA','Deus estaria com ele.'),(151,'PROTEÇÃO','Por onde ele fosse.'),(270,'RETORNO','Àquela terra.')]:info(c,y,h,s,y==270)
 elif i==6:
  ground(c,True);stone(c,285,332);actor(c,162,342,1.15,'jacob',left=(-34,-42),right=(51,-83),tilt=-3)
  c.text(230,69,'CASA DE DEUS',24,CREAM,anchor='ma');c.text(230,105,'PORTA DOS CÉUS',21,CREAM,anchor='ma')
 elif i==7:
  ground(c);stone(c,253,213,True)
  actor(c,146,338,1,'jacob',left=(-34,-42),right=(82,-95),tilt=-1)
 elif i==8:
  ground(c);stone(c,253,213,True)
  actor(c,146,338,1,'jacob',left=(-34,-42),right=(81,-108),tilt=-2)
  oiljar(c,238,226,.8,60+2*math.sin(p*math.pi));c.line([(262,212),(260,222),(261,243)],GOLD,2)
 elif i==9:
  ground(c);info(c,32,'ANTES: LUZ','o nome anterior da cidade.')
  c.line([(230,150),(230,209)],CREAM,4);c.poly([(218,199),(242,199),(230,218)],CREAM)
  info(c,249,'BETEL','nome ligado a casa de Deus.',True)
 elif i==10:
  ground(c)
  for y,h,s in [(33,'UM VOTO DE JACÓ','proteção na jornada.'),(152,'ALIMENTO E ROUPA','necessidades mencionadas.'),(271,'RETORNO EM PAZ','à casa de seu pai.')]:info(c,y,h,s,y==271)
 else:
  ground(c);stone(c,283,213,True);actor(c,143,339,1.06,'jacob',left=(-34,-42),right=(34,-42))
  c.text(230,54,'UMA PEDRA, UM SONHO, UMA PROMESSA',13,CREAM,anchor='ma',maxw=420)

DATA=[
 ('01-caminho','O SOL\\nSE PÔS.','Jacó parou durante a jornada.','GÊNESIS 28:10–11','Ele estava a caminho de Harã.'),
 ('02-pedra','UMA PEDRA.','um apoio para a cabeça.','GÊNESIS 28:11','Jacó se deitou naquele lugar.'),
 ('03-sonho','ENTÃO,\\nSONHOU.','a escada ligava a terra ao céu.','GÊNESIS 28:12','Anjos subiam e desciam por ela.'),
 ('04-promessa','UMA NOVA\\nGERAÇÃO.','a promessa alcançava Jacó.','GÊNESIS 28:13','O Senhor se apresentou a Jacó.'),
 ('05-descendencia','TERRA E\\nDESCENDÊNCIA.','numerosa como o pó da terra.','GÊNESIS 28:13–14','Todas as famílias seriam abençoadas.'),
 ('06-jornada','NA SUA\\nJORNADA.','presença, proteção e retorno.','GÊNESIS 28:15','Deus prometeu estar com Jacó.'),
 ('07-despertar','ELE\\nDESPERTOU.','reconheceu algo que não sabia.','GÊNESIS 28:16–17','O Senhor estava naquele lugar.'),
 ('08-coluna','A PEDRA\\nFOI ERGUIDA.','na manhã seguinte.','GÊNESIS 28:18','Jacó colocou a pedra como coluna.'),
 ('09-azeite','AZEITE\\nSOBRE ELA.','um marco naquela jornada.','GÊNESIS 28:18','Ele derramou azeite sobre a pedra.'),
 ('10-betel','ANTES,\\nERA LUZ.','Jacó chamou o lugar de Betel.','GÊNESIS 28:19','Betel é ligado à expressão casa de Deus.'),
 ('11-voto','UM VOTO.','o relato registra suas palavras.','GÊNESIS 28:20–22','Jacó mencionou o retorno em paz.'),
 ('12-encerramento','SEGUE O\\nPAPIRO REVELA.','Instagram, TikTok e YouTube.','GÊNESIS 28:10–22','Curiosidades bíblicas, direto do texto.')]
DATA=[(n,t.replace(chr(92)+'n','\n'),sub,ref,cap) for n,t,sub,ref,cap in DATA]

@lru_cache(maxsize=1)
def paper():
 c=C();r=random.Random(2701);noise=Image.new('L',(540,960));noise.putdata([r.randrange(218,256) for _ in range(540*960)])
 return Image.blend(c.im,noise.resize((1080,1920)).convert('RGB'),.055)

@lru_cache(maxsize=20)
def layout(i):
 _,title,sub,ref,cap=DATA[i];c=C();c.im=paper().copy();c.d=ImageDraw.Draw(c.im)
 c.rect((34,42,40,49),ORANGE);c.text(46,38,'PAPIRO REVELA',14);c.text(506,40,'ESTUDO VISUAL · BETEL',10,TEAL,anchor='ra',maxw=240)
 c.line([(34,73),(506,73)],'#ada38d',1);c.text(34,102,'CURIOSIDADES BÍBLICAS · GÊNESIS 28',11)
 for j,line in enumerate(title.split('\n')):c.text(34,132+j*57,line,55,ORANGE if i in [0,11] else INK,maxw=472)
 c.text(34,260,sub,22,TEAL,italic=True,maxw=472)
 c.rect((43,340,506,753),'#a49b83')
 c.rect((48,758,335,794),INK);c.rect((45,755,332,790),GOLD if i%2 else ORANGE,INK,2);c.text(57,764,ref,16,maxw=263)
 c.text(270,801,'Interpretação artística do relato.',12,TEAL,italic=True,anchor='ma')
 c.rect((33,834,510,882),INK);c.rect((29,830,506,878),CREAM);c.text(267,841,cap,22,anchor='ma',maxw=455)
 c.text(34,916,ref,10,'#716951');c.text(506,916,'PRÉVIA VISUAL · POR SCRIPT',9,TEAL,anchor='ra',maxw=250)
 return c.im

def frame(i,t):
 c=C();c.im=layout(i).copy();c.d=ImageDraw.Draw(c.im)
 art=C(460,410,TEAL);action(art,i,t)
 card=art.im.rotate(1.2 if i%2==0 else -1.2,Image.Resampling.BICUBIC,expand=False,fillcolor=TEAL)
 c.im.paste(card,(39*S,331*S));c.d=ImageDraw.Draw(c.im);c.d.rectangle((39*S,331*S,499*S,741*S),outline=INK,width=4)
 return c.im

def images():
 manifest=[];panel=Image.new('RGB',(1440,1920),PAPER)
 for i,(name,title,sub,ref,cap) in enumerate(DATA):
  im=frame(i,.65);im.save(OUT/(name+'.png'),optimize=True);panel.paste(im.resize((360,640),Image.Resampling.LANCZOS),((i%4)*360,(i//4)*640))
  manifest.append({'file':name+'.png','reference':ref,'title':title.replace('\n',' '),'caption':cap,'size':[1080,1920]})
 panel.save(OUT/'00-painel-de-cenas.jpg',quality=93);(OUT/'cenas.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print('12 imagens e painel gerados.',flush=True)

if __name__=='__main__':images()
