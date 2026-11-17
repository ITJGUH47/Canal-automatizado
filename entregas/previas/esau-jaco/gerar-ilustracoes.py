"""Papiro Revela: Esaú e Jacó. Cenas narrativas originais por geometria Python/Pillow.
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

def tent(c,x,y,s=1):
 def q(p):return [(x+a*s,y+b*s) for a,b in p]
 c.poly(q([(-90,0),(-48,-113),(3,-148),(42,-117),(94,0)]),'#b58b5c')
 c.poly(q([(3,-148),(42,-117),(94,0),(19,0)]),'#977047')
 c.poly(q([(3,-112),(-27,0),(19,0)]),'#4e4233')
 c.line(q([(-90,-2),(-110,25)]),INK,2);c.line(q([(93,-2),(108,25)]),INK,2)

def landscape(c,inside=False):
 if inside:
  c.rect((0,0,540,960),'#b18c62')
  c.poly([(0,0),(275,0),(170,742),(0,742)],'#c6a06f',None)
  c.poly([(285,0),(540,0),(540,742),(390,742)],'#92704f',None)
  c.line([(270,120),(270,739)],'#72583e',9)
  c.poly([(0,731),(540,731),(540,960),(0,960)],'#cfb17b',None)
  c.poly([(81,792),(459,792),(480,900),(62,900)],'#b45f43')
  return
 for y in range(490):
  p=y/490;col=tuple(round(a+(b-a)*p) for a,b in zip((225,161,103),(248,224,169)));c.line([(0,y),(540,y)],col,1)
 c.ellipse((386,145,463,222),'#f4d984',None)
 c.poly([(0,389),(113,331),(215,382),(324,342),(441,384),(540,349),(540,960),(0,960)],'#b29c72',None)
 c.poly([(0,485),(144,439),(278,480),(407,447),(540,477),(540,960),(0,960)],'#d5b986',None)
 c.poly([(316,432),(339,439),(296,599),(353,767),(487,960),(356,960),(244,771),(246,594)],'#ead4a5',None)
 tent(c,109,491,.78);tent(c,442,519,.57)
 for x,y in [(58,638),(462,687),(75,757)]:c.line([(x,y),(x-6,y-16),(x,y),(x+8,y-13)],'#7f8b5b',2)

def person(c,x,y,s=1,who='jacob',pose='stand'):
 def q(p):return [(x+a*s,y+b*s) for a,b in p]
 color={'jacob':TEAL,'esau':ORANGE,'isaac':'#466b79','rebecca':TEAL}[who]
 hair='#a85e35' if who=='esau' else '#493b2e'
 c.line(q([(-14,-25),(-14,6)]),SKIN,max(1,round(13*s)));c.line(q([(14,-25),(14,6)]),SKIN,max(1,round(13*s)))
 c.poly(q([(-26,2),(-26,15),(-5,15),(-4,2)]),'#79543a');c.poly(q([(4,2),(5,15),(29,15),(26,2)]),'#79543a')
 c.poly(q([(-25,-151),(-35,-113),(-39,-22),(36,-22),(30,-113),(22,-151)]),color)
 c.poly(q([(-9,-145),(-15,-28),(0,-22),(7,-145)]),'#46847a' if who in ['jacob','rebecca'] else '#dd9360' if who=='esau' else '#688a97',None)
 c.line(q([(-35,-65),(33,-65)]),'#866442',5)
 c.poly(q([(-10,-162),(-10,-148),(12,-148),(12,-162)]),SKIN)
 c.ellipse((x-25*s,y-211*s,x+25*s,y-157*s),SKIN)
 if who=='rebecca':
  c.poly(q([(-27,-165),(-31,-216),(-3,-232),(26,-219),(30,-164),(17,-155),(14,-201),(4,-212),(-16,-205),(-16,-163)]),'#d39a70')
 else:
  c.poly(q([(-27,-190),(-30,-211),(-12,-231),(15,-227),(28,-211),(24,-190),(12,-201),(-5,-207),(-17,-199)]),hair)
  if who in ['esau','isaac']:
   c.poly(q([(-19,-176),(-10,-180),(0,-176),(11,-180),(20,-173),(14,-154),(0,-146),(-14,-155)]),hair)
 for ex in [-10,10]:c.ellipse((x+(ex-2)*s,y-191*s,x+(ex+2)*s,y-187*s),INK,None)
 c.line(q([(-16,-199),(-7,-200)]),INK,1);c.line(q([(7,-200),(16,-199)]),INK,1)
 c.line(q([(0,-187),(-2,-177),(3,-177)]),'#805238',1)
 c.line(q([(-7,-170),(0,-169),(7,-170)]),'#75472e',1)
 if pose=='pray':arms=[[(-25,-143),(-38,-113),(-11,-89),(0,-99)],[(25,-143),(38,-113),(12,-89),(0,-99)]]
 elif pose=='ask':arms=[[(-25,-143),(-42,-110),(-20,-90)],[(25,-143),(49,-126),(66,-132)]]
 elif pose=='oath':arms=[[(-25,-143),(-38,-109),(-30,-82)],[(25,-143),(46,-160),(46,-197)]]
 elif pose=='give':arms=[[(-25,-143),(-30,-108),(17,-102)],[(25,-143),(49,-119),(66,-113)]]
 elif pose=='cook':arms=[[(-25,-143),(-36,-106),(-10,-82)],[(25,-143),(48,-113),(68,-117)]]
 elif pose=='tired':arms=[[(-25,-143),(-41,-111),(-34,-82)],[(25,-143),(38,-104),(26,-81)]]
 else:arms=[[(-25,-143),(-39,-111),(-33,-82)],[(25,-143),(39,-111),(33,-82)]]
 for pts in arms:
  c.line(q(pts),INK,max(2,round(14*s)));c.line(q(pts),color,max(2,round(10*s)))
  a,b=pts[-1];c.ellipse((x+(a-5)*s,y+(b-5)*s,x+(a+5)*s,y+(b+5)*s),SKIN,INK,1)
 if who=='esau':
  # Small forearm hatching recalls the textual description without caricature.
  for u,v in [(-37,-107),(-36,-99),(34,-104),(31,-94)]:c.line(q([(u-2,v),(u+2,v-4)]),hair,1)
  # Hunting gear is a contextual artistic prop; no animal kill is depicted.
  c.line(q([(-46,-159),(-59,-185),(-62,-221)]),'#805d3d',3)
 if pose=='cook':c.line(q([(60,-139),(88,-70)]),'#785238',4)

def pot(c,x,y,s=1):
 def q(p):return [(x+a*s,y+b*s) for a,b in p]
 c.line(q([(-35,20),(43,44)]),'#715139',8);c.line(q([(-34,45),(40,20)]),'#715139',8)
 c.poly(q([(-12,25),(-18,8),(-5,14),(4,-2),(12,15),(20,9),(16,28)]),'#dd9852',None)
 c.poly(q([(-55,-53),(55,-53),(47,-8),(30,13),(-29,13),(-47,-9)]),'#6f5844')
 c.ellipse((x-57*s,y-65*s,x+57*s,y-40*s),'#bd6743')
 for a,b in [(-35,-54),(-17,-49),(2,-54),(25,-49),(39,-55)]:c.ellipse((x+(a-3)*s,y+(b-2)*s,x+(a+3)*s,y+(b+2)*s),'#875139',None)
 for dx in [-23,18]:c.line(q([(dx,-76),(dx-5,-91),(dx+3,-105)]),'#f0dfbc',2)

def bowl(c,x,y,s=1):
 def q(p):return [(x+a*s,y+b*s) for a,b in p]
 c.poly(q([(-43,-9),(43,-9),(30,20),(-27,20)]),'#b57d50')
 c.ellipse((x-44*s,y-20*s,x+44*s,y+1*s),'#bd6743')
 for a,b in [(-29,-10),(-15,-13),(0,-8),(16,-13),(28,-8)]:c.ellipse((x+(a-3)*s,y+(b-2)*s,x+(a+3)*s,y+(b+2)*s),'#875139',None)

def bread(c,x,y,s=1):
 c.ellipse((x-49*s,y-18*s,x+49*s,y+18*s),'#d7a066')
 for dx in [-23,0,23]:c.line([(x+dx*s,y-9*s),(x+(dx-8)*s,y+8*s)],'#96673e',2)

def twins(c):
 # Swaddled newborns, with one small hand touching the other's heel.
 c.poly([(90,555),(433,555),(455,725),(67,725)],'#c6a278')
 for x,cloth,skin in [(178,'#ddb58b','#bc8058'),(340,'#b7c8af',SKIN)]:
  c.poly([(x-46,614),(x-35,566),(x+26,568),(x+45,611),(x+37,687),(x-23,706),(x-47,666)],cloth)
  c.ellipse((x-30,555,x+26,613),skin)
  c.line([(x-15,590),(x-8,591)],INK,1);c.line([(x+6,591),(x+13,590)],INK,1)
  c.line([(x-27,626),(x+26,655),(x-16,674)],'#8f987c',2)
 # Esaú's heel extends to the right; Jacó's hand reaches it.
 c.poly([(208,671),(236,670),(244,680),(233,689),(208,686)],'#bc8058')
 c.line([(306,643),(284,673),(244,680)],SKIN,12)
 c.ellipse((235,672,251,688),SKIN)
 c.text(178,739,'ESAÚ',18,INK,'ma');c.text(340,739,'JACÓ',18,INK,'ma')

DATA=[
 ('01-panela','UMA CONDIÇÃO.','GÊNESIS 25:29–31',['ESAÚ VOLTOU CANSADO.','JACÓ TINHA UM COZIDO.'],'Abertura antecipa o encontro junto à panela; depois retorna ao início da história.'),
 ('02-oracao','ANTES DOS GÊMEOS.','GÊNESIS 25:21–23',['ISAQUE OROU.','REBECA ENGRAVIDOU.'],'Rebeca e Isaque na tenda, antes do nascimento; sem imagem humana de Deus ou luta literal de bebês.'),
 ('03-nascimento','DOIS IRMÃOS.','GÊNESIS 25:24–26',['JACÓ NASCEU SEGURANDO','O CALCANHAR DE ESAÚ.'],'Dois recém-nascidos envoltos em tecido, sem parto explícito; gesto do calcanhar interpretado visualmente.'),
 ('04-irmaos','ELES CRESCERAM.','GÊNESIS 25:27',['ESAÚ, HOMEM DO CAMPO.','JACÓ HABITAVA EM TENDAS.'],'Esaú e Jacó adultos, aparência consistente nas cenas posteriores. Sem morte de animais.'),
 ('05-pedido','A COMIDA VERMELHA.','GÊNESIS 25:29–30',['ESAÚ PEDIU UM POUCO','DAQUELE COZIDO.'],'Pedido junto à panela; não retratar Esaú como comprovadamente moribundo.'),
 ('06-primogenitura','O QUE ESTAVA EM JOGO?','GÊNESIS 25:31–34',['PRIMOGENITURA: O DIREITO','DO FILHO MAIS VELHO.'],'Explicação geral de posição familiar e herança. Não atribuir automaticamente a regra posterior de porção dobrada ao contrato narrado aqui.'),
 ('07-negociacao','A CONDIÇÃO DE JACÓ.','GÊNESIS 25:31–32',['JACÓ PEDIU','A PRIMOGENITURA.'],'Negociação entre irmãos. A frase sobre estar a ponto de morrer é declaração de Esaú, não diagnóstico do narrador.'),
 ('08-juramento','O JURAMENTO.','GÊNESIS 25:33',['ESAÚ JUROU','E VENDEU SEU DIREITO.'],'Gesto de mão erguida é interpretação artística; não implica contrato escrito ou gesto ritual especificado pelo texto.'),
 ('09-pao-lentilhas','PÃO E LENTILHAS.','GÊNESIS 25:34',['JACÓ LHE DEU PÃO','E COZIDO DE LENTILHAS.'],'Plano de comida e mãos; sem acrescentar carne ou quantidade de porções.'),
 ('10-partida','ELE FOI EMBORA.','GÊNESIS 25:34',['ELE COMEU, BEBEU,','LEVANTOU-SE E PARTIU.'],'Partida após a refeição, sem afirmar arrependimento, satisfação ou outros pensamentos não informados.'),
 ('11-capitulos','NÃO CONFUNDA AS CENAS.','GÊNESIS 25; 27',['A PRIMOGENITURA É UMA CENA.','A BÊNÇÃO VEM DEPOIS.'],'Distinção entre os episódios; não antecipar o disfarce de Jacó nem dizer que os temas não possuem relação.'),
 ('12-encerramento','PAPIRO REVELA','GÊNESIS 25:19–34',['SEGUE O PAPIRO REVELA.','INSTAGRAM · TIKTOK · YOUTUBE'],'Encerramento do canal com os irmãos e os elementos principais do episódio.')]

images=[];manifest=[]
for i,(name,label,ref,caption,note) in enumerate(DATA):
 c=C();landscape(c,inside=i in [1,2])
 if i in [0,4,6,7,11]:
  person(c,150,728,1.4,'jacob','cook' if i==0 else 'ask' if i==6 else 'give')
  person(c,383,728,1.4,'esau','oath' if i==7 else 'tired' if i in [0,4] else 'ask')
  pot(c,280,727,.8)
 elif i==1:
  person(c,150,745,1.4,'isaac','pray');person(c,384,745,1.4,'rebecca')
  c.rect((70,272,470,373),CREAM,INK,2);c.text(270,291,'DOIS FILHOS,',26,INK,'ma');c.text(270,328,'DUAS NAÇÕES.',26,INK,'ma')
 elif i==2:twins(c)
 elif i==3:
  person(c,145,741,1.5,'jacob');person(c,391,741,1.5,'esau')
  c.text(145,784,'JACÓ',20,INK,'ma');c.text(391,784,'ESAÚ',20,INK,'ma')
 elif i==5:
  person(c,395,754,1.3,'esau')
  c.rect((30,313,315,634),CREAM,INK,2)
  c.text(173,337,'PRIMEIRO',30,TEAL,'ma');c.text(173,376,'FILHO',38,TEAL,'ma')
  c.line([(58,441),(286,441)],'#b6a37f',2)
  c.text(173,468,'POSIÇÃO NA',23,INK,'ma');c.text(173,501,'FAMÍLIA',27,INK,'ma');c.text(173,557,'E HERANÇA',26,ORANGE,'ma')
 elif i==8:
  c.poly([(45,579),(488,579),(509,739),(28,739)],'#b08b5c')
  bowl(c,306,643,1.5);bread(c,133,665,1.15);pot(c,394,499,.64)
  c.line([(54,518),(133,574),(208,597)],TEAL,35);c.line([(208,597),(245,606)],SKIN,18)
 elif i==9:
  person(c,131,741,1.32,'jacob');person(c,395,617,1.0,'esau')
  bowl(c,273,744,.7);pot(c,241,678,.72)
 elif i==10:
  person(c,113,753,1.1,'jacob');person(c,426,753,1.1,'esau')
  for y,head,body in [(235,'GÊNESIS 25','PRIMOGENITURA'),(378,'GÊNESIS 27','BÊNÇÃO DE ISAQUE')]:
   c.rect((55,y,485,y+113),CREAM,INK,2);c.text(270,y+14,head,26,TEAL,'ma');c.text(270,y+58,body,29,INK,'ma')
 c.rect((24,31,245,69),TEAL);c.text(36,40,'PAPIRO REVELA',17,CREAM,maxw=198)
 c.text(30,92,label,27,INK,maxw=480)
 c.rect((20,823,520,912),'#ead9b4')
 for k,t in enumerate(caption):c.text(270,832+k*33,t,28,INK,'ma',maxw=468)
 c.text(29,931,ref,11,INK,maxw=310);c.text(511,931,f'PRÉVIA {i+1:02}',10,TEAL,'ra',maxw=130)
 path=OUT/(name+'.png');c.im.save(path,optimize=True);images.append(c.im)
 manifest.append({'file':path.name,'size':[1080,1920],'shot':label,'reference':ref,'caption':caption,'description':note})
panel=Image.new('RGB',(1440,1920),'#ead9b4')
for i,im in enumerate(images):panel.paste(im.resize((360,640),Image.Resampling.LANCZOS),((i%4)*360,(i//4)*640))
panel.save(OUT/'00-painel-de-cenas.jpg',quality=93)
(OUT/'cenas.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(f'{len(images)} imagens narrativas 1080×1920 e painel gerados.',flush=True)
