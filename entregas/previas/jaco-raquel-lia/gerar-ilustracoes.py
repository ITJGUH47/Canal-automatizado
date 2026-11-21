"""Papiro Revela: Jacó, Raquel e Lia: original paper-card illustrations.
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
 color={'jacob':TEAL,'disguise':ORANGE,'esau':ORANGE,'isaac':'#9da68c','rebecca':TEAL,'rachel':'#b86839','leah':'#756080','laban':'#9b906f'}[who]
 hair='#d4cbb3' if who in ['isaac','laban'] else '#a35e34' if who=='esau' else '#4e3c2b'
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
 if who in ['rebecca','rachel','leah']:c.poly(headq([(-23,12),(-26,-29),(0,-44),(25,-28),(25,13),(16,20),(13,-19),(0,-28),(-15,-19),(-15,17)]),('#e5bd7a' if who=='rachel' else '#b9a2ba' if who=='leah' else '#c39468'),CREAM,2)
 else:
  c.poly(headq([(-21,-7),(-24,-25),(-10,-40),(12,-38),(23,-24),(20,-8),(10,-20),(-6,-24),(-17,-15)]),hair,CREAM,2)
  if who in ['isaac','esau','laban']:c.poly(headq([(-17,1),(-8,-2),(1,2),(11,-2),(18,4),(12,23),(0,29),(-13,21)]),hair,CREAM,1)
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

def landscape(c,night=False):
 c.rect((0,0,460,410),'#273d43' if night else TEAL)
 if night:
  for x,y in [(42,40),(123,77),(315,43),(404,100)]:c.ellipse((x,y,x+3,y+3),CREAM)
 else:c.ellipse((369,31,414,76),GOLD)
 c.poly([(0,236),(89,183),(183,224),(284,175),(460,234),(460,410),(0,410)],'#5f7770' if night else '#809571')
 c.poly([(0,315),(122,278),(290,314),(460,277),(460,410),(0,410)],'#526b62' if night else '#a4ad80')

def house(c,night=False):
 landscape(c,night)
 c.poly([(26,285),(26,157),(137,105),(238,157),(238,285)],'#ad9b77',CREAM,2)
 c.rect((110,197,159,285),'#55493a',CREAM,2)
 c.line([(26,157),(238,157)],CREAM,2)

def label(c,x,y,text):c.text(x,y,text,16,CREAM,anchor='ma',maxw=175)

def well(c):
 c.poly([(42,286),(88,260),(158,273),(170,318),(130,343),(58,328)],'#a5a38f',CREAM,3)
 c.ellipse((44,265,163,302),'#444b42',CREAM,3)
 c.line([(53,301),(158,319)],CREAM,2)
 c.line([(103,285),(103,311)],GOLD,2)
 c.poly([(86,307),(120,307),(115,332),(91,332)],'#a97b4f',CREAM,2)

def sheep(c,x,y,s=1):
 c.ellipse((x-26*s,y-17*s,x+24*s,y+12*s),CREAM,INK,1)
 c.ellipse((x+13*s,y-20*s,x+36*s,y+4*s),'#625d4d',CREAM,1)
 for a in [-15,11]:c.line([(x+a*s,y+7*s),(x+a*s,y+23*s)],INK,3)

def info(c,y,head,sub,gold=False):
 c.rect((30,y,430,y+96),GOLD if gold else CREAM,'white',4)
 c.text(51,y+14,head,25,TEAL,maxw=355)
 c.text(51,y+54,sub,22,INK,italic=True,maxw=355)

def action(c,i,t):
 p=ease(t)
 if i==0:
  house(c);actor(c,146,345,1.13,'jacob',right=(56,-100),tilt=3)
  actor(c,320,345,1.13,'leah',left=(-34,-42),right=(34,-42))
  label(c,146,368,'JACÓ');label(c,320,368,'LIA')
 elif i==1:
  landscape(c);well(c);actor(c,241,311,.93,'jacob',left=(-61,-32),right=(35,-50))
  actor(c,356,312,.93,'rachel',left=(-34,-42),right=(34,-42));sheep(c,308,354,.75);sheep(c,391,360,.7)
  label(c,350,107,'RAQUEL')
 elif i==2:
  house(c);actor(c,148,349,1.15,'jacob',right=(58,-93));actor(c,322,349,1.15,'laban',left=(-58,-93))
  label(c,148,375,'JACÓ');label(c,322,375,'LABÃO')
 elif i==3:
  landscape(c);info(c,24,'SETE ANOS DE SERVIÇO','para se casar com Raquel.')
  actor(c,128,350,1.04,'jacob',right=(60,-85));actor(c,322,350,1.04,'rachel',left=(-34,-42),right=(34,-42))
 elif i==4:
  landscape(c);info(c,30,'7 ANOS','pareceram poucos dias.',True)
  actor(c,120+14*p,349,1.02,'jacob',right=(55,-100));c.line([(176,352),(191,203)],'#6c5338',6)
  sheep(c,284,306,1.05);sheep(c,366,349,.8)
  label(c,230,380,'PELO AMOR QUE SENTIA POR ELA')
 elif i==5:
  house(c)
  for x,who in [(85,'jacob'),(228,'laban'),(373,'leah')]:actor(c,x,290,.78,who)
  c.rect((32,291,425,309),'#b38750',CREAM,3)
  for x in [55,402]:c.line([(x,309),(x,373)],'#6c5338',8)
  for x in [94,226,353]:
   c.ellipse((x-22,283,x+22,294),CREAM);c.ellipse((x-12,277,x+13,290),'#b38750')
  label(c,230,65,'UMA FESTA DE CASAMENTO')
 elif i==6:
  house(c,True);actor(c,104,347,1,'laban',right=(55,-96))
  actor(c,235,347,1,'leah',left=(-34,-42),right=(34,-42));actor(c,365,347,1,'jacob',left=(-34,-42),right=(34,-42))
  label(c,230,62,'LABÃO LEVOU LIA ATÉ JACÓ')
 elif i==7:
  house(c);actor(c,137,349,1.15,'jacob',right=(62,-127),tension=True)
  actor(c,322,349,1.15,'laban',left=(-51,-75));label(c,230,68,'JACÓ CONFRONTOU LABÃO')
 elif i==8:
  landscape(c);info(c,26,'A EXPLICAÇÃO DE LABÃO','o costume daquele lugar.')
  actor(c,120,350,1.02,'leah');actor(c,337,350,1.02,'rachel')
  label(c,120,370,'MAIS VELHA');label(c,337,370,'MAIS NOVA')
  c.line([(191,262),(264,262)],CREAM,3);c.poly([(254,253),(270,262),(254,271)],CREAM)
 elif i==9:
  landscape(c);info(c,27,'COMPLETAR A SEMANA','de celebração de Lia.')
  for j in range(7):
   x=39+j*56;c.rect((x,185,x+46,244),GOLD,CREAM,2);c.text(x+23,193,str(j+1),26,INK,anchor='ma')
  c.line([(65,282),(395,282)],CREAM,3)
  label(c,230,325,'DEPOIS, O CASAMENTO COM RAQUEL')
 elif i==10:
  landscape(c);info(c,26,'PRIMEIRO: SETE ANOS','de trabalho por Raquel.')
  info(c,150,'DEPOIS DA SEMANA','Jacó também se casa com Raquel.',True)
  info(c,274,'MAIS SETE ANOS','de serviço assumido.')
 else:
  landscape(c);actor(c,92,343,.94,'leah');actor(c,230,343,1.06,'jacob');actor(c,366,343,.94,'rachel')
  label(c,230,56,'UMA NOVA ETAPA NA HISTÓRIA')

DATA=[('01-amanhecer', 'AO AMANHECER,\nERA LIA.', 'Jacó havia trabalhado por Raquel.', 'GÊNESIS 29:18–25', 'Pela manhã, Jacó descobriu o engano.'), ('02-poco', 'UM ENCONTRO\nNO POÇO.', 'Raquel chegou com o rebanho.', 'GÊNESIS 29:1–12', 'Jacó ajudou a dar água às ovelhas.'), ('03-labao', 'LABÃO\nO RECEBEU.', 'o irmão de sua mãe.', 'GÊNESIS 29:13–15', 'Jacó ficou na casa de seus parentes.'), ('04-proposta', 'SETE ANOS\nPOR RAQUEL.', 'essa foi a proposta de Jacó.', 'GÊNESIS 29:16–19', 'Ele se ofereceu para servir sete anos.'), ('05-trabalho', 'PARECERAM\nPOUCOS DIAS.', 'pelo amor que sentia por ela.', 'GÊNESIS 29:20', 'Jacó cumpriu os sete anos de serviço.'), ('06-festa', 'LABÃO FEZ\nUMA FESTA.', 'o prazo de trabalho havia terminado.', 'GÊNESIS 29:21–22', 'As pessoas do lugar foram reunidas.'), ('07-noite', 'MAS LEVOU\nLIA ATÉ ELE.', 'era a filha mais velha.', 'GÊNESIS 29:23–25', 'O relato situa a troca durante a noite.'), ('08-confronto', 'POR QUE\nME ENGANOU?', 'Jacó confrontou Labão.', 'GÊNESIS 29:25', 'Ele havia servido para se casar com Raquel.'), ('09-costume', 'A MAIS VELHA\nPRIMEIRO.', 'a justificativa apresentada por Labão.', 'GÊNESIS 29:26', 'Labão mencionou o costume daquele lugar.'), ('10-semana', 'UMA SEMANA\nDE CELEBRAÇÃO.', 'a condição apresentada por Labão.', 'GÊNESIS 29:27–28', 'Jacó completou a semana de Lia.'), ('11-cronologia', 'ELE NÃO ESPEROU\nOUTROS SETE ANOS.', 'o casamento veio depois da semana.', 'GÊNESIS 29:27–30', 'Os outros sete anos eram de serviço.'), ('12-encerramento', 'SEGUE O\nPAPIRO REVELA.', 'Instagram, TikTok e YouTube.', 'GÊNESIS 29:1–30', 'Curiosidades bíblicas, direto do texto.')]

@lru_cache(maxsize=1)
def paper():
 c=C();r=random.Random(2701);noise=Image.new('L',(540,960));noise.putdata([r.randrange(218,256) for _ in range(540*960)])
 return Image.blend(c.im,noise.resize((1080,1920)).convert('RGB'),.055)

@lru_cache(maxsize=20)
def layout(i):
 _,title,sub,ref,cap=DATA[i];c=C();c.im=paper().copy();c.d=ImageDraw.Draw(c.im)
 c.rect((34,42,40,49),ORANGE);c.text(46,38,'PAPIRO REVELA',14);c.text(506,40,'ESTUDO VISUAL · GÊNESIS 29',10,TEAL,anchor='ra',maxw=240)
 c.line([(34,73),(506,73)],'#ada38d',1);c.text(34,102,'CURIOSIDADES BÍBLICAS · GÊNESIS 29',11)
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
