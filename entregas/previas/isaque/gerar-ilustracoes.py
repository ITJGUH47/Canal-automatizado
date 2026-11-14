"""Papiro Revela — Isaque. Arte procedural original, sem serviços de IA ou voz.
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

def sara(c,x,y,s=1,baby=False):
 def q(pts):return [(x+a*s,y+b*s) for a,b in pts]
 c.line(q([(-10,0),(-10,20)]),'#78583d',max(1,round(8*s)));c.line(q([(10,0),(10,20)]),'#78583d',max(1,round(8*s)))
 c.poly(q([(-18,-62),(-26,0),(26,0),(18,-62)]),CREAM,CREAM,2)
 c.ellipse((x-16*s,y-99*s,x+16*s,y-63*s),'#bb875d',CREAM,2)
 c.poly(q([(-19,-63),(-23,-100),(0,-112),(23,-100),(20,-62),(11,-69),(10,-94),(-10,-94),(-10,-68)]),'#b48665',CREAM,2)
 c.line(q([(-9,-77),(-4,-75)]),'#76573e',1);c.line(q([(5,-75),(10,-77)]),'#76573e',1)
 c.line(q([(-5,-70),(0,-68),(5,-70)]),'#76573e',1)
 if baby:
  # Wrapped infant rests across both forearms; face visible above the cloth.
  c.line(q([(-17,-52),(-29,-32),(6,-24)]),'#bb875d',max(1,round(9*s)))
  c.line(q([(17,-52),(33,-29),(-7,-20)]),'#bb875d',max(1,round(9*s)))
  c.poly(q([(-28,-47),(-7,-60),(24,-42),(30,-25),(13,-16),(-13,-25)]),'#e3c895',TEAL,2)
  c.ellipse((x-31*s,y-59*s,x-7*s,y-36*s),'#bb875d',CREAM,2)
  c.line(q([(-7,-50),(15,-27),(-8,-28)]),'#ad9364',2)
  c.line(q([(-24,-47),(-20,-46)]),'#76573e',1)
 else:
  c.line(q([(-18,-53),(-28,-17)]),'#bb875d',max(1,round(7*s)));c.line(q([(18,-53),(28,-17)]),'#bb875d',max(1,round(7*s)))

def info(c,y,head,sub,gold=False):
 c.rect((33,y,427,y+95),GOLD if gold else CREAM,'white',3)
 c.txt(53,y+14,head,25,maxw=350)
 c.txt(53,y+54,sub,18,TEAL,italic=True,maxw=350)

def art(i):
 c=Canvas(460,410,TEAL)
 if i==0:
  c.ellipse((108,26,352,270),GOLD);sara(c,230,276,1.55,True)
  c.txt(230,350,'SARA DÁ À LUZ ISAQUE',20,CREAM,anchor='ma')
 elif i==1:
  hills(c);tent(c,302,281,1.25);sara(c,192,286,1.05)
  c.rect((35,33,425,120),CREAM,'white',3);c.txt(230,52,'ANTES DO NASCIMENTO',24,anchor='ma')
  c.txt(230,348,'SARA OUVIU A PROMESSA',18,CREAM,anchor='ma')
 elif i==2:
  info(c,40,'O NOME JÁ FOI ANUNCIADO','antes do nascimento.')
  c.line([(230,154),(230,202)],CREAM,4);c.poly([(219,191),(241,191),(230,213)],CREAM)
  c.rect((56,239,404,333),GOLD,'white',4);c.txt(230,251,'ISAQUE',51,anchor='ma')
 elif i==3:
  c.rect((48,43,412,158),CREAM,'white',4);c.txt(230,58,'ISAQUE',57,anchor='ma')
  c.txt(230,187,'ligado ao verbo hebraico',21,CREAM,italic=True,anchor='ma')
  c.rect((95,239,365,339),GOLD,'white',4);c.txt(230,248,'RIR',62,anchor='ma')
 elif i==4:
  c.ellipse((80,20,380,320),GOLD)
  c.rect((56,57,312,295),CREAM,'white',4);c.txt(184,73,'ABRAÃO',24,anchor='ma')
  c.txt(184,121,'100',89,ORANGE,anchor='ma');c.txt(184,242,'ANOS',26,anchor='ma')
  elder(c,362,283,1.05);c.txt(230,348,'QUANDO ISAQUE NASCEU',19,CREAM,anchor='ma')
 elif i==5:
  sara(c,105,281,1.3,True)
  c.rect((185,73,426,253),CREAM,'white',3)
  c.txt(306,91,'SARA',27,anchor='ma');c.txt(306,135,'CELEBRA',27,ORANGE,anchor='ma')
  c.txt(306,182,'o nascimento.',20,TEAL,italic=True,anchor='ma')
  c.txt(230,334,'QUEM SOUBESSE RIRIA COM ELA',16,CREAM,anchor='ma')
 elif i==6:
  info(c,40,'ANTES','Sara ouve a promessa.')
  c.line([(230,153),(230,206)],CREAM,4);c.poly([(219,195),(241,195),(230,217)],CREAM)
  info(c,244,'DEPOIS','Sara celebra o nascimento.',True)
 elif i==7:
  hills(c);tent(c,359,276,.8);sara(c,204,290,1.5,True)
  c.txt(230,352,'UM FILHO NA VELHICE',20,CREAM,anchor='ma')
 else:
  c.ellipse((112,20,348,256),GOLD);sara(c,230,278,1.55,True)
  for j,t in enumerate(['INSTAGRAM','TIKTOK','YOUTUBE']):
   x=12+j*150;c.rect((x,328,x+137,368),CREAM,INK,2);c.txt(x+68,340,t,15,anchor='ma')
 return c.im

SCENES=[
 ('01-nascimento','ISAQUE\nNASCEU.','uma história marcada pelo riso.','GÊNESIS 21:1–3','Sara deu à luz no tempo anunciado.','Nascimento do filho de Sara e Abraão; criança envolta em tecido, sem antecipar cenas posteriores.'),
 ('02-promessa','ANTES, UMA\nPROMESSA.','Sara ouviu e riu consigo mesma.','GÊNESIS 18:9–15','O riso também aparece antes do nascimento.','Retorno ao episódio do anúncio; Sara sem criança, sem representação humana de Deus.'),
 ('03-nome-anunciado','O NOME VEIO\nANTES.','ele já havia sido anunciado.','GÊNESIS 17:19','Deus já havia indicado o nome Isaque.','Nome anunciado a Abraão antes do nascimento; não inventar que foi escolhido só ao nascer.'),
 ('04-significado','ISAQUE\nE O RISO.','o nome e sua relação com rir.','GÊNESIS 17:19; 21:6','Um nome ligado ao verbo hebraico rir.','O nome Yitsḥaq é relacionado à raiz hebraica do riso; não apresentar rir como uma tradução literal completa do nome.'),
 ('05-cem-anos','100 ANOS.','a idade de Abraão nesse momento.','GÊNESIS 21:5','Abraão tinha cem anos quando Isaque nasceu.','Distinguir dos 75 anos na saída de Harã do episódio anterior.'),
 ('06-sara-celebra','MOTIVO\nDE RISO.','Sara celebra o nascimento.','GÊNESIS 21:6','Todos os que soubessem ririam com ela.','Adaptação em linguagem atual das palavras de Sara, sem inventar pessoas rindo na cena.'),
 ('07-dois-momentos','DOIS\nMOMENTOS.','o riso atravessa o relato.','GÊNESIS 18:12; 21:6','Antes, a promessa. Depois, o nascimento.','Comparação temporal; sem atribuir ao primeiro riso uma interpretação psicológica adicional.'),
 ('08-filho-na-velhice','UM FILHO NA\nVELHICE.','a pergunta de Sara.','GÊNESIS 21:7','Sara recorda o nascimento na velhice.','Sara pergunta quem diria que amamentaria filhos; imagem mostra apenas o filho referido, sem nudez ou ação de amamentação.'),
 ('09-encerramento','SEGUE O\nPAPIRO REVELA.','curiosidades bíblicas, direto do texto.','GÊNESIS 17–18; 21','Instagram · TikTok · YouTube','Segue o Papiro Revela no Instagram, TikTok e YouTube. Curiosidades bíblicas, direto do texto.')]

rng=random.Random(11019)
noise=Image.new('L',(540,960));noise.putdata([rng.randrange(218,256) for _ in range(540*960)])
texture=noise.resize((1080,1920)).convert('RGB')
images=[];manifest=[]
for i,(name,title,sub,ref,caption,story) in enumerate(SCENES):
 c=Canvas(540,960,PAPER);c.im=Image.blend(c.im,texture,.055);c.d=ImageDraw.Draw(c.im)
 c.rect((34,42,40,49),ORANGE);c.txt(46,38,'PAPIRO REVELA',14)
 c.txt(506,40,'DOSSIÊ 010',11,TEAL,anchor='ra');c.line([(34,73),(506,73)],'#aca48f')
 c.txt(34,102,'CURIOSIDADES BÍBLICAS · GÊNESIS 21',11)
 for j,t in enumerate(title.split('\n')):c.txt(34,132+j*57,t,55,ORANGE if i in [0,8] else INK,maxw=472)
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
 c.rect((0,955,(i+1)*540/len(SCENES),960),ORANGE)
 path=OUT/(name+'.png');c.im.save(path,optimize=True);images.append(c.im)
 manifest.append({'file':path.name,'size':[1080,1920],'title':title.replace('\n',' '),'reference':ref,'script_excerpt':story})
thumb=Image.new('RGB',(1080,1920),PAPER)
for i,im in enumerate(images):thumb.paste(im.resize((360,640),Image.Resampling.LANCZOS),((i%3)*360,(i//3)*640))
thumb.save(OUT/'00-painel-de-cenas.jpg',quality=93)
(OUT/'cenas.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(f'{len(images)} imagens 1080×1920 + painel gerados em {OUT}')
