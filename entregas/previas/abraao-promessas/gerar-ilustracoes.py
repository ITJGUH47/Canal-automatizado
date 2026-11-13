"""Papiro Revela — A jornada de Abraão. Arte procedural original, sem serviços de IA ou voz.
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

def sheep(c,x,y,s=.8):
 c.line([(x-14*s,y+8*s),(x-14*s,y+28*s)],'#c3ac7b',3);c.line([(x+12*s,y+8*s),(x+12*s,y+28*s)],'#c3ac7b',3)
 c.ellipse((x-28*s,y-13*s,x+24*s,y+16*s),CREAM,INK,1)
 c.ellipse((x+12*s,y-20*s,x+35*s,y+2*s),'#b2966c',CREAM,1)

def sara(c,x,y,s=1):
 person(c,x,y,s,CREAM)
 c.poly([(x-18*s,y-64*s),(x-22*s,y-94*s),(x,y-104*s),(x+22*s,y-94*s),(x+20*s,y-62*s),(x+10*s,y-68*s),(x+8*s,y-90*s),(x-9*s,y-90*s),(x-10*s,y-65*s)],'#b48665',CREAM,2)

def info_card(c,y,head,sub,gold=False):
 c.rect((34,y,426,y+83),GOLD if gold else CREAM,'white',3)
 c.txt(52,y+12,head,23,maxw=353)
 c.txt(52,y+47,sub,17,TEAL,italic=True,maxw=353)

def star(c,x,y,r=5):
 c.line([(x-r,y),(x+r,y)],CREAM,2);c.line([(x,y-r),(x,y+r)],CREAM,2)

def art(i):
 c=Canvas(460,410,TEAL)
 if i==0:
  c.ellipse((99,27,361,289),GOLD);elder(c,230,249,1.45)
  c.txt(230,321,'ESCOLHAS · ENCONTROS · PROMESSAS',15,CREAM,anchor='ma')
 elif i==1:
  hills(c);elder(c,100,269,.85);person(c,354,269,.85,ORANGE)
  for x,y in [(52,302),(112,325),(171,290),(295,312),(357,324),(409,285)]:sheep(c,x,y,.7)
  c.txt(230,365,'REBANHOS E CONTENDA ENTRE PASTORES',13,CREAM,anchor='ma')
 elif i==2:
  hills(c);c.poly([(240,218),(314,187),(460,205),(460,410),(255,410)],'#6e9a66')
  c.poly([(332,208),(344,211),(322,295),(353,410),(325,410),(301,294)],'#a6c2b1')
  elder(c,101,306,.95);person(c,323,301,.95,ORANGE,True)
  c.txt(101,337,'ABRÃO',18,CREAM,anchor='ma');c.txt(323,337,'LÓ',18,CREAM,anchor='ma')
 elif i==3:
  hills(c);elder(c,92,281,1)
  c.rect((169,72,424,166),CREAM,'white',3)
  c.txt(295,86,'À SUA',22,TEAL,anchor='ma');c.txt(295,118,'DESCENDÊNCIA',24,anchor='ma')
  c.txt(230,352,'A PROMESSA DA TERRA É REAFIRMADA',14,CREAM,anchor='ma')
 elif i==4:
  hills(c);elder(c,175,281,1.05);person(c,282,281,1.05,ORANGE)
  # Abstract journey/rescue arrow, without invented battle choreography.
  c.line([(82,110),(315,110)],CREAM,6);c.poly([(315,98),(315,122),(336,110)],CREAM)
  c.txt(230,56,'ABRÃO RESGATA LÓ',23,CREAM,anchor='ma')
  c.txt(230,344,'DEPOIS DE LÓ SER LEVADO CATIVO',15,CREAM,anchor='ma')
 elif i==5:
  elder(c,92,246,.92);person(c,366,246,.92,CREAM)
  c.rect((147,223,313,235),'#b89a6c',CREAM,2)
  c.line([(160,235),(160,281)],'#b89a6c',6);c.line([(301,235),(301,281)],'#b89a6c',6)
  c.ellipse((164,181,239,220),'#d5a16a',CREAM,2)
  for x in [185,202,218]:c.line([(x,190),(x-7,204)],'#9b6d45',2)
  c.poly([(260,179),(292,179),(287,213),(265,213)],'#a66045',CREAM,2);c.ellipse((260,174,292,184),'#743d37',CREAM,2)
  c.txt(230,37,'MELQUISEDEQUE',28,CREAM,anchor='ma')
  c.txt(230,77,'REI DE SALÉM · SACERDOTE',15,GOLD,anchor='ma')
  c.txt(230,312,'PÃO · VINHO · BÊNÇÃO',20,CREAM,anchor='ma')
  c.txt(230,347,'ABRÃO LHE DEU O DÍZIMO DE TUDO',13,CREAM,anchor='ma')
 elif i==6:
  tent(c,334,257,.85);elder(c,143,281,1.3)
  c.rect((42,38,418,120),CREAM,'white',3);c.txt(230,54,'AINDA SEM FILHOS',27,anchor='ma')
  c.txt(230,340,'ABRÃO APRESENTA SUA PREOCUPAÇÃO',14,CREAM,anchor='ma')
 elif i==7:
  c.rect((0,0,460,410),'#263e3d')
  rng2=random.Random(1505)
  for _ in range(45):star(c,rng2.randint(18,441),rng2.randint(18,212),rng2.choice([2,3,4]))
  c.poly([(0,301),(96,265),(221,297),(346,268),(460,301),(460,410),(0,410)],'#637451')
  elder(c,230,319,1.2)
  c.txt(230,365,'ASSIM SERIA SUA DESCENDÊNCIA',17,CREAM,anchor='ma')
 elif i==8:
  info_card(c,38,'ABRÃO','o nome usado até aqui.')
  c.line([(230,139),(230,200)],CREAM,4);c.poly([(219,189),(241,189),(230,210)],CREAM)
  info_card(c,233,'ABRAÃO','pai de muitas nações.',True)
 elif i==9:
  hills(c);tent(c,313,273,1.38);sara(c,239,286,1.04)
  c.rect((31,36,429,120),CREAM,'white',3);c.txt(230,53,'SARA TERIA UM FILHO',25,anchor='ma')
  c.txt(230,346,'ELA OUVIU E RIU CONSIGO MESMA',15,CREAM,anchor='ma')
 elif i==10:
  for y,h,b in [(28,'GÊNESIS 13–14','separação, resgate e encontro.'),(140,'GÊNESIS 15','a promessa e as estrelas.'),(252,'GÊNESIS 17–18','novo nome e promessa a Sara.')]:info_card(c,y,h,b,y==252)
 else:
  c.ellipse((115,22,345,261),GOLD);elder(c,230,269,1.25)
  for j,t in enumerate(['INSTAGRAM','TIKTOK','YOUTUBE']):
   x=12+j*150;c.rect((x,328,x+137,368),CREAM,INK,2);c.txt(x+68,340,t,15,anchor='ma')
 return c.im

SCENES=[
 ('01-jornada','UMA JORNADA.','escolhas, encontros e promessas.','GÊNESIS 13–18','Antes de ser Abraão, sua jornada continuava.','Gancho e abertura; sem representar todos os acontecimentos como um único dia.'),
 ('02-rebanhos','NÃO CABIA\nTODO MUNDO.','os rebanhos eram numerosos.','GÊNESIS 13:5–7','Houve contenda entre seus pastores.','A terra não comportava que permanecessem juntos por seus muitos bens e rebanhos.'),
 ('03-escolha','LÓ ESCOLHEU\nPRIMEIRO.','a planície era bem regada.','GÊNESIS 13:8–11','Abrão ofereceu a escolha a Ló.','Abrão propõe separação; Ló escolhe a planície do Jordão. Não inferir seus motivos além do texto.'),
 ('04-terra','A PROMESSA\nDA TERRA.','depois da separação.','GÊNESIS 13:14–17','Deus reafirmou a promessa a Abrão.','Terra prometida à descendência após a separação. Sem representar Deus como pessoa.'),
 ('05-resgate','ABRÃO\nRESGATOU LÓ.','ele havia sido levado cativo.','GÊNESIS 14:12–16','Abrão reuniu seus homens e foi resgatá-lo.','Resgate após a captura de Ló durante guerra. Sem inventar cenas de batalha ou ferimentos.'),
 ('06-melquisedeque','UM ENCONTRO\nDIFERENTE.','Melquisedeque abençoou Abrão.','GÊNESIS 14:18–20','Rei de Salém e sacerdote do Deus Altíssimo.','Pão, vinho, bênção e dízimo. Não introduzir identificação teológica de Melquisedeque nem símbolos cristãos posteriores.'),
 ('07-sem-filhos','AINDA SEM\nFILHOS.','Abrão apresenta sua preocupação.','GÊNESIS 15:1–3','A promessa continuava em sua história.','Abrão afirma continuar sem filhos neste ponto do relato; não antecipar Ismael ou Isaque.'),
 ('08-estrelas','CONTE AS\nESTRELAS.','se puder contá-las.','GÊNESIS 15:5–6','Assim seria sua descendência.','Céu estrelado como imagem da promessa. O número desenhado de estrelas é ilustrativo.'),
 ('09-novo-nome','AGORA,\nABRAÃO.','pai de muitas nações.','GÊNESIS 17:5','Um novo nome ligado à promessa.','Mudança de nome só aqui; cenas anteriores usam Abrão.'),
 ('10-sara','SARA TERIA\nUM FILHO.','ela ouviu e riu consigo mesma.','GÊNESIS 18:9–15','Haveria algo difícil demais para o Senhor?','Sara idosa junto à tenda; sem retratar filho já nascido nem transformar seu riso em caricatura.'),
 ('11-capitulos','VÁRIOS\nCAPÍTULOS.','uma história que avança no tempo.','GÊNESIS 13–18','Esses acontecimentos não foram no mesmo dia.','Recapitulação explicita os saltos de tempo e capítulos do roteiro unido.'),
 ('12-encerramento','SEGUE O\nPAPIRO REVELA.','curiosidades bíblicas, direto do texto.','GÊNESIS 13–18','Instagram · TikTok · YouTube','Segue o Papiro Revela no Instagram, TikTok e YouTube. Curiosidades bíblicas, direto do texto.')]

rng=random.Random(11019)
noise=Image.new('L',(540,960));noise.putdata([rng.randrange(218,256) for _ in range(540*960)])
texture=noise.resize((1080,1920)).convert('RGB')
images=[];manifest=[]
for i,(name,title,sub,ref,caption,story) in enumerate(SCENES):
 c=Canvas(540,960,PAPER);c.im=Image.blend(c.im,texture,.055);c.d=ImageDraw.Draw(c.im)
 c.rect((34,42,40,49),ORANGE);c.txt(46,38,'PAPIRO REVELA',14)
 c.txt(506,40,'DOSSIÊ 009',11,TEAL,anchor='ra');c.line([(34,73),(506,73)],'#aca48f')
 c.txt(34,102,'CURIOSIDADES BÍBLICAS · GÊNESIS 13–18',11)
 for j,t in enumerate(title.split('\n')):c.txt(34,132+j*57,t,55,ORANGE if i in [0,11] else INK,maxw=472)
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
thumb=Image.new('RGB',(1440,1920),PAPER)
for i,im in enumerate(images):thumb.paste(im.resize((360,640),Image.Resampling.LANCZOS),((i%4)*360,(i//4)*640))
thumb.save(OUT/'00-painel-de-cenas.jpg',quality=93)
(OUT/'cenas.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(f'{len(images)} imagens 1080×1920 + painel gerados em {OUT}')
