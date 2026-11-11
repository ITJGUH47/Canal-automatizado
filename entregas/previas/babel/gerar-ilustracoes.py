"""Papiro Revela — Babel. Arte procedural original, sem serviços de IA ou voz.
Execute com Python 3 e Pillow: python gerar-ilustracoes.py
Fontes DejaVu/Bitstream instaladas no sistema; saídas junto deste script.
"""
from pathlib import Path
import random, json, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
OUT=Path(__file__).resolve().parent
F=Path('/usr/share/fonts/truetype/dejavu')
PAPER='#e5dfcf'; INK='#262822'; TEAL='#236963'; ORANGE='#e85c2e'; GOLD='#efbd49'; CREAM='#f8f2df'
S=2
class Canvas:
 def __init__(self,w,h,bg):
  self.im=Image.new('RGB',(w*S,h*S),bg);self.d=ImageDraw.Draw(self.im)
 def rect(self,b,fill,outline=None,width=1):self.d.rectangle(tuple(round(v*S) for v in b),fill,outline,width*S)
 def poly(self,pts,fill,outline=None,width=1):
  q=[(round(x*S),round(y*S)) for x,y in pts];self.d.polygon(q,fill)
  if outline:self.d.line(q+[q[0]],fill=outline,width=width*S,joint='curve')
 def line(self,pts,fill,width=1):self.d.line([(round(x*S),round(y*S)) for x,y in pts],fill,width*S,joint='curve')
 def ellipse(self,b,fill,outline=None,width=1):self.d.ellipse(tuple(round(v*S) for v in b),fill,outline,width*S)
 def txt(self,x,y,t,size=20,color=INK,italic=False,anchor='la',maxw=None):
  face=F/('DejaVuSerif-Italic.ttf' if italic else 'DejaVuSansCondensed-Bold.ttf')
  font=ImageFont.truetype(str(face),round(size*S))
  if maxw:
   while self.d.textlength(t,font)>maxw*S:
    size-=.5;font=ImageFont.truetype(str(face),round(size*S))
  self.d.text((round(x*S),round(y*S)),t,font=font,fill=color,anchor=anchor)

def person(c,x,y,s=1,color=ORANGE,arm=False):
 def p(points):return [(x+a*s,y+b*s) for a,b in points]
 c.line(p([(-8,0),(-8,20)]),'#78583d',max(1,round(8*s)));c.line(p([(8,0),(8,20)]),'#78583d',max(1,round(8*s)))
 c.poly(p([(-15,-57),(-22,0),(22,0),(15,-57)]),color,CREAM,max(1,round(2*s)))
 c.ellipse((x-14*s,y-91*s,x+14*s,y-60*s),'#bb875d',CREAM,max(1,round(2*s)))
 c.poly(p([(-15,-77),(-14,-91),(0,-98),(15,-88),(15,-76),(5,-85),(-7,-84)]),'#513d2c')
 c.line(p([(-16,-50),(-28,-13)]),'#bb875d',max(1,round(7*s)))
 c.line(p([(16,-50),(37,-75) if arm else (28,-13)]),'#bb875d',max(1,round(7*s)))

def tower(c,x=230,base=327,s=1):
 # Repeated brick courses, offset joints, perspective side and flat terraces.
 # Artistic stepped silhouette: Genesis gives no height or number of levels.
 for level in range(5):
  w=(246-level*38)*s;h=47*s;y=base-level*48*s;left=x-w/2
  c.poly([(left,y),(left+w,y),(left+w+24*s,y-13*s),(left+24*s,y-13*s)],'#e9ad70',CREAM,2)
  c.poly([(left+w,y),(left+w+24*s,y-13*s),(left+w+24*s,y-h-13*s),(left+w,y-h)],'#a84e31',CREAM,2)
  c.rect((left,y-h,left+w,y),ORANGE,CREAM,2)
  for j in range(1,4):c.line([(left,y-j*h/4),(left+w,y-j*h/4)],'#a94e31',1)
  for row in range(4):
   for xx in range(int(left+14+(row%2)*14*s),int(left+w),max(8,int(29*s))):c.line([(xx,y-row*h/4),(xx,y-(row+1)*h/4)],'#a94e31',1)
 # Incomplete top and small human figures suggest active construction.
 top=base-240*s
 for dx in [-24,22]:c.line([(x+dx*s,top+15*s),(x+dx*s,top-15*s)],'#c7a479',max(1,round(3*s)))
 c.line([(x-30*s,top-3*s),(x+32*s,top-3*s)],'#c7a479',max(1,round(3*s)))

def book(c):
 c.poly([(55,85),(135,66),(230,86),(325,66),(405,85),(405,303),(325,284),(230,306),(135,284),(55,303)],CREAM,'white',5)
 c.line([(230,86),(230,306)],'#ac9c7e',3)
 for y in [113,143,173,203,233,263]:
  c.line([(76,y),(137,y-12),(207,y+2)],'#c9bca0',2);c.line([(253,y+2),(324,y-12),(384,y)],'#c9bca0',2)
 c.rect((128,171,333,234),GOLD,INK,2);c.txt(230,183,'GÊNESIS 11',25,anchor='ma')

SCENES=[
 ('01-por-que-babel','POR QUE\nUMA TORRE?','o motivo aparece no próprio relato.','GÊNESIS 11:4','Uma cidade, uma torre e um propósito.','Gancho: uma torre com o topo nos céus; o que os construtores queriam?'),
 ('02-sinar','UMA SÓ\nLÍNGUA.','o povo encontra uma planície.','GÊNESIS 11:1–2','Eles decidem morar em Sinar.','A humanidade fala uma só língua e se estabelece numa planície em Sinar.'),
 ('03-tijolos','TIJOLOS\nE BETUME.','os materiais citados em Gênesis.','GÊNESIS 11:3','Tijolos no lugar de pedras.','Fabricam tijolos e usam betume como argamassa.'),
 ('04-proposito','FAZER UM\nNOME.','e evitar a dispersão pela terra.','GÊNESIS 11:4','O próprio povo explica seu objetivo.','Construir cidade e torre, tornar o nome famoso e evitar que fossem espalhados.'),
 ('05-linguas','SEM SE\nENTENDER.','o trabalho deixa de avançar.','GÊNESIS 11:7–8','A construção da cidade parou.','O Senhor confunde sua língua; deixam de se entender. Sem representação humana de Deus.'),
 ('06-dispersao','O POVO SE\nESPALHOU.','justamente o que queria evitar.','GÊNESIS 11:8–9','Do mesmo lugar, para outros caminhos.','O povo é espalhado pela terra; torre permanece em pé na ilustração.'),
 ('07-detalhe','A TORRE FOI\nDESTRUÍDA?','Gênesis não afirma isso.','GÊNESIS 11:1–9','O relato fala da dispersão do povo.','Detalhe final: o texto não diz que a torre foi destruída; sem inventar desfecho.'),
 ('08-encerramento','SEGUE O\nPAPIRO REVELA.','curiosidades bíblicas, direto do texto.','GÊNESIS 11:1–9','Instagram · TikTok · YouTube','Segue o Papiro Revela no Instagram, TikTok e YouTube. Curiosidades bíblicas, direto do texto.')]

def art(i):
 c=Canvas(460,410,TEAL)
 if i in [0,3]:
  c.ellipse((101,30,359,288),GOLD);tower(c,225,327,.92)
  if i==0:
   for x,y in [(40,326),(372,338)]:
    c.rect((x,y-48,x+48,y),CREAM,INK,2);c.rect((x+17,y-23,x+29,y),INK)
  else:
   for x,col in [(80,ORANGE),(377,GOLD)]:person(c,x,350,.65,col,True)
  c.txt(230,374,'CIDADE + TORRE' if i==0 else 'FAMA · EVITAR A DISPERSÃO',17,CREAM,anchor='ma',maxw=420)
 elif i==1:
  c.ellipse((320,34,389,103),GOLD)
  c.poly([(0,205),(92,168),(214,199),(332,165),(460,191),(460,410),(0,410)],'#8a9b63')
  c.poly([(205,200),(233,201),(261,250),(211,298),(251,410),(179,410),(159,297),(217,248)],'#a6c2b1')
  for x,y in [(302,224),(340,241),(380,224)]:c.rect((x,y-27,x+30,y),CREAM,INK,1)
  for x,col in [(70,ORANGE),(122,GOLD),(340,CREAM)]:person(c,x,345,.8,col)
  c.txt(230,370,'PLANÍCIE NA TERRA DE SINAR',16,CREAM,anchor='ma')
 elif i==2:
  c.ellipse((91,45,361,315),GOLD)
  for x,y in [(67,257),(128,207),(59,156)]:
   c.poly([(x,y),(x+143,y-15),(x+143,y+37),(x,y+52)],ORANGE,CREAM,3)
   c.poly([(x,y),(x+35,y-24),(x+178,y-39),(x+143,y-15)],'#eaa16d',CREAM,3)
   c.poly([(x+143,y-15),(x+178,y-39),(x+178,y+13),(x+143,y+37)],'#b85432',CREAM,3)
  c.poly([(324,174),(372,174),(363,212),(386,253),(380,298),(309,298),(302,253),(332,210)],'#625542',CREAM,3)
  c.ellipse((319,168,378,185),INK,CREAM,3)
  c.txt(230,354,'TIJOLOS + BETUME',21,CREAM,anchor='ma')
 elif i==4:
  tower(c,237,264,.55)
  person(c,100,346,1,CREAM);person(c,353,346,1,ORANGE)
  for x in [48,288]:
   c.rect((x,113,x+123,194),CREAM,INK,2);c.poly([(x+36,194),(x+55,215),(x+59,194)],CREAM)
  c.poly([(82,173),(108,131),(134,173)],TEAL)
  c.rect((327,132,368,173),ORANGE)
  c.txt(230,380,'A LÍNGUA FOI CONFUNDIDA',17,CREAM,anchor='ma')
 elif i==5:
  c.ellipse((159,22,307,170),GOLD);tower(c,230,179,.49)
  c.poly([(0,267),(125,234),(231,254),(345,224),(460,265),(460,410),(0,410)],'#83925e')
  for pts in [[(224,255),(144,300),(59,410)],[(236,255),(298,304),(408,410)]]:c.line(pts,CREAM,19)
  for x,y,s,col in [(98,351,.52,ORANGE),(63,374,.57,CREAM),(352,359,.52,GOLD),(386,384,.57,CREAM)]:person(c,x,y,s,col)
 elif i==6:
  book(c);c.txt(230,351,'O QUE O TEXTO DIZ?',21,CREAM,anchor='ma')
 else:
  c.ellipse((120,41,340,261),GOLD);tower(c,228,278,.77)
  for j,t in enumerate(['INSTAGRAM','TIKTOK','YOUTUBE']):
   x=12+j*150;c.rect((x,328,x+137,373),CREAM,INK,2);c.txt(x+68,341,t,15,anchor='ma')
 return c.im

rng=random.Random(11019)
noise=Image.new('L',(540,960));noise.putdata([rng.randrange(218,256) for _ in range(540*960)])
texture=noise.resize((1080,1920)).convert('RGB')
images=[];manifest=[]
for i,(name,title,sub,ref,caption,story) in enumerate(SCENES):
 c=Canvas(540,960,PAPER);c.im=Image.blend(c.im,texture,.055);c.d=ImageDraw.Draw(c.im)
 c.rect((34,42,40,49),ORANGE);c.txt(46,38,'PAPIRO REVELA',14)
 c.txt(506,40,'DOSSIÊ 007',11,TEAL,anchor='ra');c.line([(34,73),(506,73)],'#aca48f')
 c.txt(34,102,'CURIOSIDADES BÍBLICAS · GÊNESIS 11',11)
 for j,t in enumerate(title.split('\n')):c.txt(34,132+j*57,t,55,ORANGE if i in [0,7] else INK,maxw=472)
 c.txt(34,260,sub,23,TEAL,italic=True,maxw=472)
 c.rect((44,340,506,752),'#a49b83')
 # Same slightly angled illustration cards as the existing Enoch video.
 card=art(i).rotate(1.5 if i%2==0 else -1.5,resample=Image.Resampling.BICUBIC,expand=False,fillcolor=TEAL)
 c.im.paste(card,(39*S,331*S));c.d=ImageDraw.Draw(c.im)
 c.d.rectangle((39*S,331*S,499*S,741*S),outline=INK,width=2*S)
 c.rect((48,726,278,761),INK);c.rect((46,723,275,757),GOLD if i%2 else ORANGE,INK,2);c.txt(58,731,ref,17,maxw=206)
 if i in [0,3,4,5]:c.txt(270,780,'Torre: interpretação artística.',12,TEAL,italic=True,anchor='ma')
 c.rect((33,834,510,882),INK);c.rect((29,830,506,878),CREAM)
 c.txt(267,841,caption,22,anchor='ma',maxw=455)
 c.txt(34,916,ref,10,'#716951');c.txt(506,916,'PRÉVIA VISUAL · POR SCRIPT',10,'#716951',anchor='ra')
 c.rect((0,955,(i+1)*540/8,960),ORANGE)
 path=OUT/(name+'.png');c.im.save(path,optimize=True);images.append(c.im)
 manifest.append({'file':path.name,'size':[1080,1920],'title':title.replace('\n',' '),'reference':ref,'script_excerpt':story})
thumb=Image.new('RGB',(1440,1280),PAPER)
for i,im in enumerate(images):thumb.paste(im.resize((360,640),Image.Resampling.LANCZOS),((i%4)*360,(i//4)*640))
thumb.save(OUT/'00-painel-de-cenas.jpg',quality=93)
(OUT/'cenas.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(f'{len(images)} imagens 1080×1920 + painel gerados em {OUT}')
