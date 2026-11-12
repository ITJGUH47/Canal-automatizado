"""Papiro Revela — Abrão. Arte procedural original, sem serviços de IA ou voz.
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

def elder(c,x,y,s=1):
 person(c,x,y,s,GOLD)
 c.poly([(x-12*s,y-74*s),(x,y-48*s),(x+12*s,y-74*s),(x+8*s,y-64*s),(x-8*s,y-64*s)],'#e7ddc8')
 c.line([(x+37*s,y-81*s),(x+37*s,y+19*s)],'#d5b783',max(1,round(4*s)))

def hills(c):
 c.ellipse((332,33,392,93),GOLD)
 c.poly([(0,213),(107,172),(218,200),(326,157),(460,212),(460,410),(0,410)],'#879562')
 c.poly([(218,217),(243,217),(289,277),(237,326),(252,410),(188,410),(184,323),(253,275)],'#dbcca4')

def tent(c,x,y,s=1):
 c.poly([(x-68*s,y),(x,y-70*s),(x+68*s,y)],'#b89a6c',CREAM,2)
 c.poly([(x,y-70*s),(x+12*s,y),(x+68*s,y)],'#96754b',CREAM,2)
 c.poly([(x,y-48*s),(x-15*s,y),(x+12*s,y)],INK)

def stone(c,x,y,w,h):
 c.poly([(x,y+h),(x-4,y+5),(x+w*.3,y),(x+w-3,y+2),(x+w,y+h)],'#9a9b84',CREAM,2)

def art(i):
 c=Canvas(460,410,TEAL)
 if i==0:
  c.ellipse((95,25,365,295),GOLD)
  c.rect((102,63,358,289),CREAM,'white',4)
  c.txt(230,82,'ABRÃO',24,anchor='ma')
  c.line([(125,124),(335,124)],'#baac8f')
  c.txt(230,124,'75',108,ORANGE,anchor='ma')
  c.txt(230,247,'ANOS',24,anchor='ma')
  c.txt(230,330,'QUANDO SAIU DE HARÃ',19,CREAM,anchor='ma')
 elif i==1:
  hills(c);tent(c,92,235,.75);elder(c,306,310,1.1)
  c.txt(230,348,'UM CHAMADO PARA PARTIR',18,CREAM,anchor='ma')
 elif i==2:
  for y,head,body in [(42,'UMA GRANDE NAÇÃO','uma promessa para o futuro.'),(145,'UM NOME ENGRANDECIDO','a bênção de Deus.'),(248,'AS FAMÍLIAS DA TERRA','abençoadas por meio dele.')]:
   c.rect((28,y,432,y+86),GOLD if y==248 else CREAM,'white',3)
   c.txt(46,y+13,head,21,maxw=370)
   c.txt(46,y+46,body,18,TEAL,italic=True,maxw=370)
 elif i==3:
  c.rect((37,43,423,162),GOLD,'white',4);c.txt(230,55,'NESTE RELATO',16,anchor='ma');c.txt(230,87,'ABRÃO',46,anchor='ma')
  c.line([(230,177),(230,216)],CREAM,4);c.poly([(220,207),(240,207),(230,222)],CREAM)
  c.rect((37,237,423,336),CREAM,'white',4);c.txt(230,248,'MAIS ADIANTE · GÊNESIS 17:5',15,TEAL,anchor='ma');c.txt(230,277,'ABRAÃO',36,anchor='ma')
 elif i==4:
  c.ellipse((90,35,370,315),GOLD)
  elder(c,230,259,1.12);person(c,100,273,1.03,CREAM);person(c,360,273,1.03,ORANGE)
  # Sarai: simple head covering, without claims about historical appearance.
  c.poly([(81,194),(78,166),(99,158),(118,171),(120,199),(109,193),(106,175),(92,174),(92,195)],'#b48665',CREAM,2)
  for x,t in [(100,'SARAI'),(230,'ABRÃO'),(360,'LÓ')]:c.txt(x,312,t,22,CREAM,anchor='ma')
 elif i==5:
  # A route diagram, not a geographic map or reconstructed exact itinerary.
  c.line([(96,96),(178,96),(178,186),(293,186),(293,281),(369,281)],CREAM,9)
  c.ellipse((69,69,123,123),GOLD,CREAM,3);c.ellipse((342,254,396,308),ORANGE,CREAM,3)
  c.txt(96,36,'HARÃ',24,CREAM,anchor='ma');c.txt(345,317,'CANAÃ',24,CREAM,anchor='ma')
  elder(c,248,171,.64)
  c.txt(230,367,'TRAJETO ESQUEMÁTICO · SEM ESCALA',12,CREAM,anchor='ma')
 elif i==6:
  hills(c);tent(c,367,245,.55)
  for x,y,w,h in [(120,267,68,42),(192,267,72,42),(268,267,65,42),(134,225,81,40),(219,225,92,40),(150,196,65,28),(219,196,74,28)]:stone(c,x,y,w,h)
  elder(c,67,292,.8)
  c.txt(230,345,'UM ALTAR DURANTE A JORNADA',17,CREAM,anchor='ma')
 else:
  hills(c);elder(c,232,270,1.15)
  for j,t in enumerate(['INSTAGRAM','TIKTOK','YOUTUBE']):
   x=12+j*150;c.rect((x,328,x+137,368),CREAM,INK,2);c.txt(x+68,340,t,15,anchor='ma')
 return c.im

SCENES=[
 ('01-setenta-e-cinco','75 ANOS.','uma nova etapa na jornada.','GÊNESIS 12:4','Abrão tinha 75 anos quando saiu de Harã.','Idade de Abrão na saída de Harã; não sua idade na mudança de nome.'),
 ('02-chamado','UM CHAMADO.','deixar sua terra e partir.','GÊNESIS 12:1','Rumo à terra que Deus lhe mostraria.','Deixar terra, parentela e casa do pai. Sem representar Deus em forma humana.'),
 ('03-promessa','UMA PROMESSA.','uma bênção que alcança famílias.','GÊNESIS 12:2–3','Todas as famílias da terra.','Grande nação, nome engrandecido e bênção para as famílias da terra.'),
 ('04-nome','AINDA ERA\nABRÃO.','a mudança de nome vem depois.','GÊNESIS 12:4; 17:5','Abraão é o nome que aparece mais adiante.','Distinguir Abrão em Gênesis 12 e a mudança para Abraão em Gênesis 17:5.'),
 ('05-companhia','NÃO FOI\nSOZINHO.','Sarai e Ló foram com ele.','GÊNESIS 12:5','Sua esposa e seu sobrinho o acompanharam.','Sarai, Ló, bens e as pessoas adquiridas em Harã. Imagem enfatiza os três nomes, sem inventar o tamanho do grupo.'),
 ('06-canaa','RUMO A\nCANAÃ.','o destino indicado no relato.','GÊNESIS 12:5','O grupo seguiu para Canaã.','Diagrama narrativo Harã–Canaã, não mapa geográfico de itinerário exato.'),
 ('07-altar','UM ALTAR.','a jornada continuava.','GÊNESIS 12:7–9','Uma promessa à sua descendência.','Promessa da terra à descendência, construção de altar e continuação da jornada. Sem representar aparição divina, sacrifício ou fogo não citados aqui.'),
 ('08-encerramento','SEGUE O\nPAPIRO REVELA.','curiosidades bíblicas, direto do texto.','GÊNESIS 12:1–9','Instagram · TikTok · YouTube','Segue o Papiro Revela no Instagram, TikTok e YouTube. Curiosidades bíblicas, direto do texto.')]

rng=random.Random(11019)
noise=Image.new('L',(540,960));noise.putdata([rng.randrange(218,256) for _ in range(540*960)])
texture=noise.resize((1080,1920)).convert('RGB')
images=[];manifest=[]
for i,(name,title,sub,ref,caption,story) in enumerate(SCENES):
 c=Canvas(540,960,PAPER);c.im=Image.blend(c.im,texture,.055);c.d=ImageDraw.Draw(c.im)
 c.rect((34,42,40,49),ORANGE);c.txt(46,38,'PAPIRO REVELA',14)
 c.txt(506,40,'DOSSIÊ 008',11,TEAL,anchor='ra');c.line([(34,73),(506,73)],'#aca48f')
 c.txt(34,102,'CURIOSIDADES BÍBLICAS · GÊNESIS 12',11)
 for j,t in enumerate(title.split('\n')):c.txt(34,132+j*57,t,55,ORANGE if i in [0,7] else INK,maxw=472)
 c.txt(34,260,sub,23,TEAL,italic=True,maxw=472)
 c.rect((44,340,506,752),'#a49b83')
 # Same slightly angled illustration cards as the existing Enoch video.
 card=art(i).rotate(1.5 if i%2==0 else -1.5,resample=Image.Resampling.BICUBIC,expand=False,fillcolor=TEAL)
 c.im.paste(card,(39*S,331*S));c.d=ImageDraw.Draw(c.im)
 c.d.rectangle((39*S,331*S,499*S,741*S),outline=INK,width=2*S)
 c.rect((48,758,330,793),INK);c.rect((46,755,327,789),GOLD if i%2 else ORANGE,INK,2);c.txt(58,763,ref,17,maxw=258)
 c.txt(270,801,'Interpretação artística do relato.',12,TEAL,italic=True,anchor='ma')
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
