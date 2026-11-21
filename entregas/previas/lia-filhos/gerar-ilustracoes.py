"""Papiro Revela: Lia e seus primeiros filhos: original paper-card illustrations.
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

def info(c,y,head,sub,gold=False):
 c.rect((30,y,430,y+96),GOLD if gold else CREAM,'white',4)
 c.text(51,y+14,head,25,TEAL,maxw=355)
 c.text(51,y+54,sub,22,INK,italic=True,maxw=355)

def baby(c,x,y,s=1,color=CREAM):
 def q(points):return [(x+a*s,y+b*s) for a,b in points]
 c.poly(q([(-44,-4),(-22,-25),(26,-13),(45,10),(23,28),(-25,22)]),color,CREAM,2)
 c.ellipse((x-39*s,y-24*s,x-10*s,y+5*s),SKIN,CREAM,2)
 c.line(q([(-35,-14),(-13,-17)]),CREAM,4)
 c.line(q([(-29,-8),(-24,-7)]),INK,1)
 c.line(q([(-5,-10),(20,22)]),'#a99b83',2)
 c.line(q([(-7,14),(25,0)]),'#a99b83',2)

def mother(c,x=155,y=350,s=1.1,color=CREAM):
 actor(c,x,y,s,'leah',left=(4,-65),right=(32,-71),tilt=-3)
 baby(c,x+17*s,y-66*s,.85*s,color)

def action(c,i,t):
 p=ease(t)
 if i==0:
  house(c);actor(c,158,346,1.17,'leah',left=(-34,-42),right=(34,-42),tilt=-4)
  info(c,24,'LIA','o desejo de ser amada.')
 elif i==1:
  house(c);mother(c,126,345,1.1);actor(c,324,345,1.1,'jacob')
  label(c,126,372,'LIA');label(c,324,372,'JACÓ')
  c.text(230,64,'FILHOS DE LIA E JACÓ',21,CREAM,anchor='ma')
 elif i==2:
  landscape(c);info(c,25,'DEUS VIU SUA AFLIÇÃO','o relato volta o olhar para Lia.')
  mother(c,220,352,1.17)
 elif i==3:
  house(c);info(c,24,'RÚBEN','o primeiro filho.',True);mother(c,228,352,1.15)
 elif i==4:
  landscape(c);mother(c,125,350,1.1);actor(c,345,350,1.1,'jacob')
  info(c,24,'SUA ESPERANÇA','que o marido a amasse.')
 elif i==5:
  house(c);info(c,24,'SIMEÃO','Lia reconhece que Deus a ouviu.',True)
  mother(c,228,352,1.15,'#d8c38f')
 elif i==6:
  house(c);info(c,24,'LEVI','o desejo de união com o marido.',True)
  mother(c,228,352,1.15,'#b5c5b5')
 elif i==7:
  landscape(c)
  for y,head,sub in [(25,'RÚBEN','Deus viu sua aflição.'),(150,'SIMEÃO','Deus ouviu seu sofrimento.'),(275,'LEVI','Ela desejava o marido próximo.')]:info(c,y,head,sub)
 elif i==8:
  house(c);info(c,24,'JUDÁ','desta vez, louvaria ao Senhor.',True)
  mother(c,228,352,1.15,'#efbd49')
 elif i==9:
  landscape(c);actor(c,230,350,1.15,'leah',left=(-44,-106),right=(44,-106),tilt=-3)
  info(c,24,'O TEXTO REGISTRA LOUVOR','sem dizer que toda dor acabou.')
 elif i==10:
  landscape(c)
  for j,(head,sub) in enumerate([('RÚBEN','aflição e esperança.'),('SIMEÃO','Deus a ouviu.'),('LEVI','desejo de proximidade.'),('JUDÁ','louvor ao Senhor.')]):
   y=22+j*95;c.rect((30,y,430,y+80),GOLD if j==3 else CREAM,'white',3)
   c.text(48,y+8,head,24,TEAL);c.text(48,y+43,sub,21,INK,italic=True,maxw=360)
 else:
  house(c);mother(c,230,352,1.2,'#efbd49')
  c.text(230,61,'PALAVRAS QUE CONTAM UMA HISTÓRIA',15,CREAM,anchor='ma',maxw=405)

DATA=[('01-lia', 'LIA QUERIA\nSER AMADA.', 'suas palavras revelam essa esperança.', 'GÊNESIS 29:30–35', 'Os nomes acompanham sua história.'), ('02-familia', 'FILHOS DE\nLIA E JACÓ.', 'depois do casamento.', 'GÊNESIS 29:31–35', 'Rúben, Simeão, Levi e Judá eram filhos de Jacó.'), ('03-aflicao', 'DEUS VIU\nSUA AFLIÇÃO.', 'Lia era desprezada.', 'GÊNESIS 29:30–31', 'O texto diz que Deus abriu seu ventre.'), ('04-ruben', 'O PRIMEIRO:\nRÚBEN.', 'Deus havia visto sua aflição.', 'GÊNESIS 29:32', 'Lia expressou esperança de ser amada.'), ('05-esperanca', 'AGORA,\nELE ME AMARÁ.', 'a esperança expressa por Lia.', 'GÊNESIS 29:32', 'Era seu desejo, não uma garantia do relato.'), ('06-simeao', 'DEPOIS,\nSIMEÃO.', 'o Senhor havia ouvido seu sofrimento.', 'GÊNESIS 29:33', 'Lia reconheceu que Deus a ouviu.'), ('07-levi', 'O TERCEIRO:\nLEVI.', 'ela desejava o marido próximo.', 'GÊNESIS 29:34', 'Lia esperava que Jacó se unisse a ela.'), ('08-palavras', 'POR TRÁS\nDOS NOMES.', 'aflição, reconhecimento e esperança.', 'GÊNESIS 29:32–34', 'As palavras acompanham cada nascimento.'), ('09-juda', 'ENTÃO,\nNASCEU JUDÁ.', 'desta vez, louvaria ao Senhor.', 'GÊNESIS 29:35', 'Naquele nascimento, Lia expressou louvor.'), ('10-louvor', 'SUAS PALAVRAS\nMUDAM DE FOCO.', 'a explicação agora destaca o louvor.', 'GÊNESIS 29:35', 'O texto não afirma que toda a dor terminou.'), ('11-nomes', 'MAIS QUE\nUMA LISTA.', 'palavras que revelam o que Lia vivia.', 'GÊNESIS 29:32–35', 'São os quatro primeiros filhos de Lia.'), ('12-encerramento', 'SEGUE O\nPAPIRO REVELA.', 'Instagram, TikTok e YouTube.', 'GÊNESIS 29:30–35', 'Curiosidades bíblicas, direto do texto.')]

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
  im=frame(i,.65);im.save(OUT/(name+'.png'),compress_level=3);panel.paste(im.resize((360,640),Image.Resampling.LANCZOS),((i%4)*360,(i//4)*640))
  manifest.append({'file':name+'.png','reference':ref,'title':title.replace('\n',' '),'caption':cap,'size':[1080,1920]})
 panel.save(OUT/'00-painel-de-cenas.jpg',quality=93);(OUT/'cenas.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print('12 imagens e painel gerados.',flush=True)

if __name__=='__main__':images()
