"""Papiro Revela: Rebeca. Cenas narrativas originais por geometria Python/Pillow.
Python 3 + Pillow + fontes DejaVu. Execute neste arquivo; saídas ao lado.
"""
from pathlib import Path
import math,json
from PIL import Image,ImageDraw,ImageFont
OUT=Path(__file__).resolve().parent;S=2
INK='#342e27';TEAL='#28675f';ORANGE='#d96a3b';GOLD='#e9bc57';CREAM='#f7edce';SKIN='#b77c54'
FONT=Path('/usr/share/fonts/truetype/dejavu')
class C:
 def __init__(self):self.im=Image.new('RGB',(1080,1920),'#ead9b4');self.d=ImageDraw.Draw(self.im)
 def poly(self,p,f,o=INK,w=2):
  q=[(round(x*S),round(y*S)) for x,y in p];self.d.polygon(q,f)
  if o:self.d.line(q+[q[0]],o,w*S,joint='curve')
 def line(self,p,f=INK,w=2):self.d.line([(round(x*S),round(y*S)) for x,y in p],f,w*S,joint='curve')
 def rect(self,b,f,o=None,w=2):self.d.rectangle(tuple(round(v*S) for v in b),f,o,w*S)
 def ellipse(self,b,f,o=INK,w=2):self.d.ellipse(tuple(round(v*S) for v in b),f,o,w*S)
 def text(self,x,y,t,size=24,color=INK,anchor='la',maxw=480,stroke=0):
  font=ImageFont.truetype(str(FONT/'DejaVuSansCondensed-Bold.ttf'),size*S)
  while self.d.textlength(t,font)>maxw*S:size-=1;font=ImageFont.truetype(str(FONT/'DejaVuSansCondensed-Bold.ttf'),size*S)
  self.d.text((x*S,y*S),t,font=font,fill=color,anchor=anchor,stroke_width=stroke*S,stroke_fill=INK)

def scene(c,night=False):
 # Full-frame landscape, with a consistent city, path and evening sky.
 top=(53,85,81) if night else (229,156,92);bottom=(207,188,143) if night else (248,224,167)
 for y in range(480):
  p=y/480;col=tuple(round(a+(b-a)*p) for a,b in zip(top,bottom));c.line([(0,y),(540,y)],col,1)
 c.ellipse((389,137,471,219),'#f6d986',None)
 c.poly([(0,395),(90,356),(177,389),(265,352),(364,391),(447,345),(540,387),(540,960),(0,960)],'#bca275',None)
 for j,(x,w,h) in enumerate([(16,44,57),(62,35,74),(100,43,51),(144,37,65),(183,40,45)]):
  c.rect((x,376-h,x+w,376),'#b88758',INK,1);c.rect((x+13,354,x+24,376),'#71533c');c.rect((x+9,332,x+15,341),'#71533c')
 c.poly([(0,464),(153,426),(280,460),(425,429),(540,464),(540,960),(0,960)],'#d6bb88',None)
 c.poly([(250,439),(279,440),(320,553),(248,695),(367,960),(177,960),(173,683),(278,545)],'#ead4a5',None)
 for x,y in [(52,571),(454,529),(94,757),(477,733)]:
  c.line([(x,y),(x-5,y-17),(x,y),(x+9,y-14)],'#8b9363',2)

def spring(c,x,y,s=1):
 def q(p):return [(x+a*s,y+b*s) for a,b in p]
 c.poly(q([(-90,-5),(-50,-44),(62,-44),(100,0),(60,45),(-56,45)]),'#887456')
 c.poly(q([(-68,0),(-43,-22),(48,-22),(73,0),(42,28),(-43,28)]),'#8bb5ab')
 c.line(q([(-39,3),(35,3)]),'#d0e6cf',2)
 for j in range(4):
  yy=-60-j*18;c.poly(q([(-45-j*4,yy),(42+j*4,yy),(47+j*4,yy+15),(-50-j*4,yy+15)]),'#c6ad83')

def trough(c,x,y,s=1):
 def q(p):return [(x+a*s,y+b*s) for a,b in p]
 c.poly(q([(-105,-13),(95,-13),(110,8),(-90,8)]),'#d6c399')
 c.poly(q([(-90,8),(110,8),(106,49),(-86,49)]),'#aa9670')
 c.poly(q([(-90,-8),(84,-8),(96,3),(-79,3)]),'#80aba1',INK,1)

def jar(c,x,y,s=1,tilt=0):
 def q(p):
  a=math.radians(tilt);return [(x+s*(u*math.cos(a)-v*math.sin(a)),y+s*(u*math.sin(a)+v*math.cos(a))) for u,v in p]
 c.poly(q([(10,-34),(29,-31),(37,-17),(30,-2),(16,0),(19,-9),(27,-10),(29,-19),(22,-25),(12,-25)]),'#a35e3f')
 c.poly(q([(-12,-51),(11,-51),(8,-37),(21,-22),(23,3),(13,20),(-13,20),(-23,3),(-21,-22),(-9,-37)]),'#bd7049')
 c.line(q([(-17,-17),(17,-17)]),'#e4aa78',3)
 c.poly(q([(-13,-54),(12,-54),(14,-48),(-14,-48)]),'#daa075')

def human(c,x,y,s=1,who='rebecca',pose='stand'):
 def q(p):return [(x+a*s,y+b*s) for a,b in p]
 robe=TEAL if who=='rebecca' else '#c5904c'
 # Feet and tunic, full articulated sleeves rather than stick figures.
 c.line(q([(-13,-24),(-13,5)]),SKIN,max(1,round(12*s)));c.line(q([(13,-24),(13,5)]),SKIN,max(1,round(12*s)))
 c.poly(q([(-20,-9),(-23,13),(-5,13),(-4,-10)]),'#79543a')
 c.poly(q([(6,-9),(6,13),(26,13),(22,-10)]),'#79543a')
 c.poly(q([(-24,-155),(-34,-111),(-39,-18),(36,-18),(30,-111),(21,-155)]),robe)
 c.poly(q([(-7,-153),(-12,-24),(2,-18),(8,-149)]),'#3a8376' if who=='rebecca' else '#d7aa68',None)
 c.line(q([(-34,-66),(32,-66)]),'#8e6845',4)
 c.poly(q([(-10,-161),(-10,-148),(13,-148),(13,-162)]),SKIN)
 c.ellipse((x-24*s,y-211*s,x+24*s,y-156*s),SKIN)
 if who=='rebecca':
  c.poly(q([(-26,-167),(-31,-212),(-4,-231),(26,-217),(29,-163),(18,-153),(15,-198),(5,-211),(-17,-204),(-16,-164)]),'#dca273')
 else:
  c.poly(q([(-28,-197),(-26,-216),(-11,-228),(20,-223),(29,-207),(21,-197),(6,-207),(-17,-202)]),'#e6d2aa')
  c.poly(q([(-20,-176),(-9,-181),(1,-176),(13,-181),(21,-174),(15,-153),(1,-144),(-13,-153)]),'#62503c')
 for ex in [-10,10]:c.ellipse((x+(ex-2)*s,y-190*s,x+(ex+2)*s,y-186*s),INK,None)
 c.line(q([(-15,-197),(-6,-198)]),INK,1);c.line(q([(7,-198),(15,-197)]),INK,1)
 c.line(q([(0,-186),(-2,-177),(3,-177)]),'#805238',1)
 c.line(q([(-6,-170),(0,-168),(7,-170)]),'#75472e',1)
 if pose=='pray':
  arms=[[(-25,-145),(-40,-115),(-12,-87),(0,-100)],[(24,-145),(38,-114),(13,-87),(0,-100)]]
 elif pose=='shoulder':
  arms=[[(-24,-143),(-38,-113),(-25,-83)],[(23,-142),(44,-162),(35,-193)]]
 elif pose=='offer':
  arms=[[(-23,-140),(-38,-109),(-6,-90)],[(24,-140),(53,-121),(70,-133)]]
 elif pose=='pour':
  arms=[[(-24,-140),(-20,-105),(36,-104)],[(23,-141),(51,-122),(56,-100)]]
 elif pose=='fill':
  arms=[[(-24,-140),(-25,-85),(20,-34)],[(24,-141),(47,-77),(48,-19)]]
 elif pose=='run':
  arms=[[(-24,-141),(-47,-117),(-28,-99)],[(23,-143),(42,-164),(49,-181)]]
 else:arms=[[(-25,-144),(-39,-112),(-33,-80)],[(25,-144),(39,-112),(33,-80)]]
 for pts in arms:
  c.line(q(pts),INK,max(2,round(13*s)));c.line(q(pts),robe,max(2,round(10*s)))
  a,b=pts[-1];c.ellipse((x+(a-5)*s,y+(b-5)*s,x+(a+5)*s,y+(b+5)*s),SKIN,INK,1)
 if pose=='shoulder':jar(c,x+39*s,y-179*s,.70*s,-12)
 elif pose=='offer' and who=='rebecca':jar(c,x+59*s,y-130*s,.65*s,-45)
 elif pose=='pour':jar(c,x+57*s,y-103*s,.8*s,62)
 elif pose=='fill':jar(c,x+48*s,y-16*s,.7*s,0)
 elif pose=='run':jar(c,x+46*s,y-176*s,.68*s,-13)

def bowed(c,x,y,s=1):
 def q(p):return [(x+a*s,y+b*s) for a,b in p]
 c.line(q([(-14,-18),(-14,9)]),SKIN,12);c.line(q([(14,-18),(14,9)]),SKIN,12)
 c.poly(q([(-25,4),(-25,17),(-4,17),(-4,4)]),'#79543a')
 c.poly(q([(5,4),(5,17),(27,17),(25,4)]),'#79543a')
 c.poly(q([(-34,-20),(-27,-103),(4,-147),(37,-137),(53,-106),(19,-83),(31,-20)]),'#c5904c')
 c.poly(q([(-11,-24),(-9,-92),(17,-131),(25,-122),(7,-87),(4,-24)]),'#d7aa68',None)
 c.ellipse((x+26*s,y-161*s,x+73*s,y-110*s),SKIN)
 c.poly(q([(25,-145),(25,-167),(44,-178),(76,-162),(75,-150),(52,-157),(35,-144)]),'#e6d2aa')
 c.poly(q([(36,-128),(48,-129),(56,-120),(70,-121),(65,-98),(49,-97),(38,-108)]),'#62503c')
 c.ellipse((x+53*s,y-142*s,x+58*s,y-138*s),INK,None)
 c.line(q([(-18,-107),(-30,-76),(18,-63),(31,-79)]),INK,15);c.line(q([(-18,-107),(-30,-76),(18,-63),(31,-79)]),'#c5904c',11)
 c.line(q([(33,-108),(46,-82),(31,-79)]),INK,15);c.line(q([(33,-108),(46,-82),(31,-79)]),'#c5904c',11)
 c.ellipse((x+23*s,y-85*s,x+37*s,y-72*s),SKIN)

def camel(c,x,y,s=.8,kneel=False,drink=False,flip=False):
 def q(p):return [(x+(-a if flip else a)*s,y+b*s) for a,b in p]
 coat='#ba8a52';shadow='#90643d'
 # Dromedary silhouette: long neck, hump, four legs and broad feet.
 for k,lx in enumerate([-40,-24,25,41]):
  pts=[(lx,-12),(lx+5,26),(lx+18,36),(lx-7,36)] if kneel else [(lx,-12),(lx+4,50),(lx+15,55),(lx-7,55)]
  c.poly(q(pts),shadow if k%2 else coat,INK,1)
 c.poly(q([(-61,-21),(-61,-52),(-38,-66),(-25,-64),(-10,-99),(5,-108),(20,-96),(31,-65),(54,-61),(66,-31),(45,-13),(-35,-11)]),coat)
 neck=[(41,-49),(55,-68),(69,-59),(82,-20),(103,-8),(101,7),(80,9),(67,-9),(56,-29)] if drink else [(42,-53),(51,-82),(62,-121),(78,-127),(87,-108),(79,-94),(73,-64),(69,-33)]
 c.poly(q(neck),coat)
 head=[(80,-10),(105,-12),(119,-2),(114,9),(92,12),(80,4)] if drink else [(67,-129),(91,-133),(110,-123),(107,-111),(83,-108),(71,-115)]
 c.poly(q(head),coat)
 if not drink:
  c.poly(q([(73,-130),(68,-145),(78,-140),(82,-131)]),coat,INK,1)
  c.ellipse((x+88*s,y-125*s,x+92*s,y-121*s),INK,None)
  c.line(q([(92,-112),(105,-115)]),INK,1)
 c.line(q([(-59,-49),(-75,-24),(-73,-12)]),shadow,2)
 c.poly(q([(-37,-57),(33,-57),(38,-28),(-34,-28)]),'#9b6e44',INK,1)
 c.poly(q([(-28,-61),(23,-61),(25,-47),(-29,-47)]),'#ddbd83',INK,1)

def ten(c):
 # Two separated rows of five: exactly ten legible silhouettes, no implied crowd.
 for row,y in enumerate([626,748]):
  for j in range(5):camel(c,42+j*99,y,.48,kneel=True)

DATA=[
 ('01-dez-camelos','DEZ CAMELOS.','GÊNESIS 24:10–11',['DEZ CAMELOS','CHEGARAM À FONTE.'],'Plano aberto: caravana e cidade ao entardecer. Duas filas de cinco camelos.'),
 ('02-oracao','UMA ORAÇÃO.','GÊNESIS 24:12–14',['ANTES DO ENCONTRO,','O SERVO OROU.'],'Servo junto à fonte em oração; sem representação humana de Deus.'),
 ('03-rebeca-chega','REBECA CHEGA.','GÊNESIS 24:15',['ANTES DE TERMINAR,','REBECA APARECEU.'],'Rebeca com cântaro no ombro, aproximando-se da fonte.'),
 ('04-enche-cantaro','JUNTO À FONTE.','GÊNESIS 24:16',['ELA DESCEU À FONTE','E ENCHEU O CÂNTARO.'],'Rebeca junto aos degraus e à água; sem roldana ou balde moderno.'),
 ('05-agua-ao-servo','UM POUCO DE ÁGUA.','GÊNESIS 24:17–18',['O VIAJANTE PEDIU.','REBECA LHE DEU ÁGUA.'],'Encontro em plano médio, Rebeca oferecendo água com o cântaro.'),
 ('06-oferta-camelos','TAMBÉM AOS CAMELOS.','GÊNESIS 24:19',['TAMBÉM TIRAREI ÁGUA','PARA OS TEUS CAMELOS.'],'Oferta de Rebeca adaptada em linguagem atual; não é citação literal.'),
 ('07-bebedouro','ÁGUA NO BEBEDOURO.','GÊNESIS 24:20',['ELA ESVAZIOU O CÂNTARO','NO BEBEDOURO.'],'Cântaro inclinado e água caindo no bebedouro; um camelo em primeiro plano representa parte do grupo.'),
 ('08-volta-fonte','DE NOVO À FONTE.','GÊNESIS 24:20',['E CORREU DE NOVO','PARA TIRAR ÁGUA.'],'Rebeca em deslocamento de volta à fonte. Sem sugerir contagem de viagens ou litros.'),
 ('09-observa','EM SILÊNCIO.','GÊNESIS 24:21',['O SERVO OBSERVAVA','EM SILÊNCIO.'],'Servo em primeiro plano observa Rebeca e o bebedouro ao fundo.'),
 ('10-familia','DE QUEM ÉS FILHA?','GÊNESIS 24:23–25',['REBECA ERA','DA FAMÍLIA DE ABRAÃO.'],'Conversa depois de os camelos beberem. Sem afirmar parentesco ou identidade do servo não nomeados no trecho.'),
 ('11-adoracao','O SERVO ADOROU.','GÊNESIS 24:26–27',['ELE SE INCLINOU','E ADOROU AO SENHOR.'],'Servo inclinado em reverência; a composição usa o personagem em postura de oração com inclinação.'),
 ('12-encerramento','PAPIRO REVELA','GÊNESIS 24:1–27',['SEGUE O PAPIRO REVELA.','INSTAGRAM · TIKTOK · YOUTUBE'],'Recapitulação dos dez camelos e encerramento das três redes.')]

manifest=[];previews=[]
for i,(name,label,ref,caption,note) in enumerate(DATA):
 c=C();scene(c)
 if i in [0,11]:
  spring(c,427,475,.47);ten(c);human(c,266,498,.62,'servant')
 elif i in [1,10]:
  spring(c,370,580,.73)
  for j in range(3):camel(c,80+j*135,715,.63,kneel=True)
  if i==1:human(c,170,602,1.35,'servant','pray')
  else:
   bowed(c,191,642,1.3)
 elif i==2:
  spring(c,104,700,.75);human(c,333,738,1.65,'rebecca','shoulder')
 elif i==3:
  spring(c,257,714,1.12);human(c,153,720,1.1,'rebecca','fill')
 elif i in [4,5,9]:
  spring(c,460,497,.47)
  if i==5:camel(c,355,520,.65,kneel=True)
  human(c,145,727,1.42,'rebecca','offer' if i==4 else 'shoulder')
  human(c,383,727,1.42,'servant')
  if i==9:c.line([(359,559),(329,570),(310,562)],SKIN,11)
 elif i==6:
  human(c,146,635,1.32,'rebecca','pour');trough(c,289,673,1.21)
  camel(c,410,663,.9,kneel=False,drink=True,flip=True)
  c.line([(269,474),(281,556),(289,660)],'#acd4ca',7)
 elif i==7:
  trough(c,101,713,.6);spring(c,398,539,.66);human(c,268,737,1.65,'rebecca','run')
 elif i==8:
  trough(c,382,561,.72);human(c,287,536,.73,'rebecca','pour');camel(c,450,560,.48,kneel=True,drink=True,flip=True)
  human(c,131,770,1.85,'servant')
 # Minimal brand + small shot label; action, not a title card, fills the frame.
 c.rect((24,31,245,69),TEAL);c.text(36,40,'PAPIRO REVELA',17,CREAM,maxw=198)
 c.text(30,92,label,27,INK,maxw=480)
 # Caption band deliberately separated from action and platform UI margins.
 c.rect((20,823,520,912),'#ead9b4')
 for k,t in enumerate(caption):c.text(270,832+k*33,t,28,INK,'ma',maxw=468)
 c.text(29,931,ref,11,INK,maxw=310);c.text(511,931,f'PRÉVIA {i+1:02}',10,TEAL,'ra',maxw=130)
 path=OUT/(name+'.png');c.im.save(path,optimize=True);previews.append(c.im)
 manifest.append({'file':path.name,'size':[1080,1920],'shot':label,'reference':ref,'caption':caption,'description':note})
panel=Image.new('RGB',(1440,1920),'#ead9b4')
for i,im in enumerate(previews):panel.paste(im.resize((360,640),Image.Resampling.LANCZOS),((i%4)*360,(i//4)*640))
panel.save(OUT/'00-painel-de-cenas.jpg',quality=93)
(OUT/'cenas.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(f'{len(previews)} cenas narrativas 1080×1920 e painel gerados.',flush=True)
