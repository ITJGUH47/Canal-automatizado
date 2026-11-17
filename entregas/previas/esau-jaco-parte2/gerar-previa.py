"""Papiro Revela: Genesis 27. Original paper-card art and articulated preview.
Python 3 + Pillow + FFmpeg; outputs alongside this file. No voice/API calls.
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

def meal(c,x,y,s=1):
 c.poly([(x-45*s,y),(x+45*s,y),(x+31*s,y+15*s),(x-33*s,y+15*s)],'#c2a170',CREAM,2)
 c.ellipse((x-23*s,y-13*s,x+24*s,y+2*s),'#9f7650',CREAM,2)
 c.poly([(x-19*s,y-8*s),(x-12*s,y-17*s),(x+9*s,y-16*s),(x+18*s,y-7*s)],'#b18b58')
 c.ellipse((x-43*s,y-10*s,x-20*s,y+1*s),'#dfbb7b',CREAM,1)

def room(c):
 c.rect((0,0,460,410),TEAL)
 c.poly([(12,65),(222,36),(449,67),(449,313),(13,313)],'#44776d')
 c.poly([(306,92),(405,92),(414,310),(298,310)],'#e2cd9d',CREAM,2)
 c.poly([(327,105),(384,105),(385,310),(323,310)],'#9f9b76')
 c.rect((0,312,460,410),'#74917b')
 c.poly([(48,336),(389,336),(424,387),(22,387)],'#c5af7d',CREAM,2)
 c.line([(17,315),(445,315)],'#dfd5ad',2)

def action(c,i,t):
 p=ease(t)
 if i==0:
  actor(c,111,321,1,'isaac',right=(58,-83),seated=True)
  actor(c,337,334,1.13,'esau',left=(-40,-71),right=(46,-78))
 elif i in [1,9]:
  actor(c,117,335,1.1,'rebecca',right=(64,-91-8*p))
  actor(c,324,337,1.12,'jacob',left=(-49,-76),right=(43,-65))
  if i==9:
   c.rect((197,83,432,130),CREAM,INK,1);c.text(315,93,'CASA DE LABÃO',16,TEAL,anchor='ma',maxw=217)
 elif i==2:
  for x,label,hairy in [(116,'ESAÚ',True),(340,'JACÓ',False)]:
   c.poly([(x-34,318),(x-28,139),(x+27,139),(x+33,318)],SKIN,CREAM,4)
   c.ellipse((x-31,111,x+31,168),SKIN,CREAM,3)
   if hairy:
    for yy in range(172,305,19):
     for xx in [-17,0,17]:c.line([(x+xx,yy),(x+xx+5,yy-8)],'#865537',2)
   c.text(x,345,label,23,CREAM,anchor='ma')
 elif i==3:
  actor(c,232,339,1.38,'disguise',left=(-49,-72),right=(48,-78),fur=True)
  c.text(230,53,'ROUPAS DE ESAÚ · PELES NAS MÃOS',14,CREAM,anchor='ma',maxw=425)
 elif i in [4,5,6]:
  actor(c,125,325,1,'isaac',right=(73+21*p,-90),left=(-40,-70),seated=True,tilt=-2+3*p)
  jx=300+(32*(1-p) if i==4 else 0)
  actor(c,jx,330,1,'disguise',left=(-81,-95),right=(-28,-88),fur=True,tilt=-2)
  if i==4:meal(c,jx-52,247,1)
  if i==6:
   # Raise Isaac's hand toward the other character, without divine visual effects.
   pass
 elif i in [7,8]:
  actor(c,125,325,1,'isaac',right=(58,-86),seated=True,tilt=2*math.sin(t*math.pi) if i==8 else 0,tension=i==8)
  actor(c,334-24*p,333,1.12,'esau',left=(-68,-93),right=(-25,-81),tension=i==8)
  meal(c,284-24*p,240,1)
 elif i==10:
  for yy,title,sub in [(67,'GÊNESIS 25','Primogenitura'),(228,'GÊNESIS 27','Bênção de Isaque')]:
   c.rect((30,yy,430,yy+111),CREAM,'white',4);c.text(53,yy+15,title,26,TEAL);c.text(53,yy+57,sub,25,INK,italic=True)
 else:
  actor(c,132,328,1.1,'isaac',right=(60,-88),seated=True)
  actor(c,333,331,1.12,'jacob')

DATA=[
 ('01-pedido','A BÊNÇÃO\\nDE ISAQUE.','um novo episódio da família.','GÊNESIS 27:1–4','Isaque chamou Esaú e fez um pedido.'),
 ('02-plano','REBECA\\nOUVIU.','ela orientou Jacó.','GÊNESIS 27:5–10','O plano é uma ação dos personagens.'),
 ('03-diferenca','MÃOS LISAS,\\nMÃOS PELUDAS.','a preocupação de Jacó.','GÊNESIS 27:11–12','Se o pai o tocasse, poderia descobrir.'),
 ('04-disfarce','ROUPAS\\nE PELES.','Jacó se prepara para entrar.','GÊNESIS 27:15–17','As mãos e o pescoço foram cobertos.'),
 ('05-refeicao','A COMIDA\\nCHEGOU.','Jacó afirmou ser Esaú.','GÊNESIS 27:18–20','Isaque estranhou a rapidez da volta.'),
 ('06-maos','A VOZ\\nE AS MÃOS.','Isaque pediu que se aproximasse.','GÊNESIS 27:21–23','A voz era de Jacó. As mãos, de Esaú.'),
 ('07-bencao','ELE O\\nABENÇOOU.','fartura e domínio na bênção.','GÊNESIS 27:27–29','Ainda assim, Isaque abençoou Jacó.'),
 ('08-esau','ESAÚ\\nCHEGOU.','depois que Jacó havia saído.','GÊNESIS 27:30–32','Esaú trouxe a comida da caça.'),
 ('09-descoberta','A DESCOBERTA.','Isaque estremeceu intensamente.','GÊNESIS 27:33–34','Esaú soltou um grito amargo.'),
 ('10-fuga','JACÓ DEVERIA\\nFUGIR.','Rebeca o orientou a procurar Labão.','GÊNESIS 27:41–45','O relato menciona o plano de Esaú.'),
 ('11-episodios','DOIS\\nEPISÓDIOS.','primogenitura e bênção.','GÊNESIS 25; 27','Cenas diferentes na mesma história.'),
 ('12-encerramento','SEGUE O\\nPAPIRO REVELA.','Instagram, TikTok e YouTube.','GÊNESIS 27:1–45','Curiosidades bíblicas, direto do texto.')]
# Keep actual line breaks in the title strings, not literal backslash+n.
DATA=[(n,t.replace(chr(92)+'n','\n'),sub,ref,cap) for n,t,sub,ref,cap in DATA]

@lru_cache(maxsize=1)
def paper():
 c=C();r=random.Random(2701);noise=Image.new('L',(540,960));noise.putdata([r.randrange(218,256) for _ in range(540*960)])
 return Image.blend(c.im,noise.resize((1080,1920)).convert('RGB'),.055)

@lru_cache(maxsize=20)
def layout(i):
 _,title,sub,ref,cap=DATA[i];c=C();c.im=paper().copy();c.d=ImageDraw.Draw(c.im)
 c.rect((34,42,40,49),ORANGE);c.text(46,38,'PAPIRO REVELA',14);c.text(506,40,'PARTE 2 · ESTUDO VISUAL',10,TEAL,anchor='ra',maxw=240)
 c.line([(34,73),(506,73)],'#ada38d',1);c.text(34,102,'CURIOSIDADES BÍBLICAS · GÊNESIS 27',11)
 for j,line in enumerate(title.split('\n')):c.text(34,132+j*57,line,55,ORANGE if i in [0,11] else INK,maxw=472)
 c.text(34,260,sub,22,TEAL,italic=True,maxw=472)
 c.rect((43,340,506,753),'#a49b83')
 c.rect((48,758,335,794),INK);c.rect((45,755,332,790),GOLD if i%2 else ORANGE,INK,2);c.text(57,764,ref,16,maxw=263)
 c.text(270,801,'Interpretação artística · prévia sem áudio.',12,TEAL,italic=True,anchor='ma')
 c.rect((33,834,510,882),INK);c.rect((29,830,506,878),CREAM);c.text(267,841,cap,22,anchor='ma',maxw=455)
 c.text(34,916,ref,10,'#716951');c.text(506,916,'PYTHON · MOVIMENTOS ARTICULADOS',9,TEAL,anchor='ra',maxw=250)
 return c.im

def frame(i,t):
 c=C();c.im=layout(i).copy();c.d=ImageDraw.Draw(c.im)
 art=C(460,410,TEAL);room(art);action(art,i,t)
 card=art.im.rotate(1.2 if i%2==0 else -1.2,Image.Resampling.BICUBIC,expand=False,fillcolor=TEAL)
 c.im.paste(card,(39*S,331*S));c.d=ImageDraw.Draw(c.im);c.d.rectangle((39*S,331*S,499*S,741*S),outline=INK,width=4)
 return c.im

def images():
 manifest=[];panel=Image.new('RGB',(1440,1920),PAPER)
 for i,(name,title,sub,ref,cap) in enumerate(DATA):
  im=frame(i,.65);im.save(OUT/(name+'.png'),optimize=True);panel.paste(im.resize((360,640),Image.Resampling.LANCZOS),((i%4)*360,(i//4)*640))
  manifest.append({'file':name+'.png','reference':ref,'title':title.replace('\n',' '),'caption':cap,'size':[1080,1920]})
 panel.save(OUT/'00-painel-de-cenas.jpg',quality=93);(OUT/'cenas.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print('12 imagens e painel gerados.',flush=True)

def video():
 ids=[4,5,7];fps=30;length=4;frames=fps*length
 cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r',str(fps),'-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','19','-threads','2','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'previa-movimentos-sem-audio-1080p.mp4')]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 try:
  for index in ids:
   for f in range(frames):
    im=frame(index,f/(frames-1));fade=min(1,f/6,(frames-1-f)/6)
    if fade<1:im=Image.blend(Image.new('RGB',im.size,PAPER),im,max(0,fade))
    proc.stdin.write(im.tobytes())
   print('Trecho de movimento pronto:',DATA[index][0],flush=True)
 finally:proc.stdin.close()
 assert proc.wait()==0
 print('Prévia de 12 segundos sem áudio gerada.',flush=True)
if __name__=='__main__':
 if '--video-only' not in sys.argv:images()
 if '--images-only' not in sys.argv:video()
