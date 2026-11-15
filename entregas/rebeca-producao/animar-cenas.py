"""Animate the approved procedural Rebekah artwork as separate original layers."""
from pathlib import Path
from functools import lru_cache
import json,math,subprocess,textwrap,sys
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
source=(ROOT/'entregas/previas/rebeca/gerar-ilustracoes.py').read_text()
ns={'__file__':str(ROOT/'entregas/previas/rebeca/gerar-ilustracoes.py')}
exec(compile(source[:source.index('manifest=[];previews=[]')],'<approved-art>','exec'),ns)
C=ns['C'];DATA=ns['DATA'];S=2
background=C();ns['scene'](background);BG=background.im
# Reuse exactly the approved shot composition; substitute cached animated layers.
a=source.index(' if i in [0,11]:',source.index('manifest=[];previews=[]'))
b=source.index(' # Minimal brand',a)
body=textwrap.dedent(source[a:b])
state={'p':0.,'seconds':0.,'visual':0}
@lru_cache(maxsize=180)
def sprite(kind,s,args,kwargs):
 c=C();c.im=Image.new('RGBA',(1080,1920));c.d=ImageDraw.Draw(c.im)
 ns[kind](c,240,480,s,*args,**dict(kwargs))
 box=c.im.getbbox();return c.im.crop(box),box

def layer(kind):
 def f(c,x,y,s=1,*args,**kwargs):
  p=state['p'];sec=state['seconds'];i=state['visual'];dx=dy=angle=0
  if kind=='human':
   who=args[0] if args else kwargs.get('who','rebecca')
   if who=='rebecca' and i==2:dx=80*(1-p);dy=2*math.sin(sec*8)
   elif who=='rebecca' and i==7:dx=-55+145*p;dy=-160*p+3*math.sin(sec*12);s=round(s*(1-.15*p)/.04)*.04
   elif who=='rebecca' and i in [3,4,5,6]:angle=.65*math.sin(sec*2);dy=.8*math.sin(sec*3)
   elif who=='servant' and i==8:angle=.5*math.sin(sec*1.5)
  elif kind=='camel':
   if i in [0,11]:dy=1.3*math.sin(sec*2+x*.08)
   elif kwargs.get('drink'):angle=.8*math.sin(sec*2.4)
  elif kind=='bowed':angle=1.8*math.sin(math.pi*p)
  im,box=sprite(kind,round(s,3),args,tuple(sorted(kwargs.items())))
  if angle:im=im.rotate(angle,Image.Resampling.BICUBIC,expand=False)
  c.im.paste(im,(round((x+dx)*S)+box[0]-480,round((y+dy)*S)+box[1]-960),im)
 return f
render_ns=ns.copy()
for name in ['human','camel','spring','trough','bowed']:render_ns[name]=layer(name)
# Ten animals retain the exact count while moving separately.
def ten(c):
 for row,y in enumerate([626,748]):
  for j in range(5):render_ns['camel'](c,42+j*99,y,.48,kneel=True)
render_ns['ten']=ten
exec('def draw_actors(i,c):\n'+textwrap.indent(body,' '),render_ns)
scenes=json.loads((Path(__file__).parent/'cenas-tempos.json').read_text());out=ROOT/'out/rebeca-clips';out.mkdir(exist_ok=True)
@lru_cache(maxsize=20)
def hud(visual,mode):
 c=C();c.im=Image.new('RGBA',(1080,1920));c.d=ImageDraw.Draw(c.im)
 _,label,ref,caption,_=DATA[visual]
 if mode=='recap':label='O DETALHE DO RELATO.';caption=['ELA OFERECEU ÁGUA','AOS DEZ CAMELOS.']
 c.rect((24,31,245,69),ns['TEAL']);c.text(36,40,'PAPIRO REVELA',17,ns['CREAM'],maxw=198)
 c.text(30,92,label,27,ns['INK'],maxw=480)
 c.rect((20,823,520,912),'#ead9b4')
 for k,t in enumerate(caption):c.text(270,832+k*33,t,28,ns['INK'],'ma',maxw=468)
 c.text(29,931,ref,11,ns['INK'],maxw=290);c.text(511,931,'VOZ: ELEVENLABS.IO',9,ns['TEAL'],'ra',maxw=180)
 return c.im

def frame(s,f):
 p=f/max(1,s['duration']-1);i=s['visual'];sec=f/30
 state.update(p=p,seconds=sec,visual=i)
 c=C();c.im=BG.copy();c.d=ImageDraw.Draw(c.im)
 render_ns['draw_actors'](i,c)
 # Animated ripples and water droplets reinforce the actual narrated action.
 if i in [3,6,8]:
  x,y=(257,714) if i==3 else (289,672) if i==6 else (382,561)
  radius=12+8*((sec*1.5)%1)
  c.ellipse((x-radius,y-4,x+radius,y+4),'#8bb5ab','#c6e1d7',1)
 if i==6:
  for j in range(5):
   y=490+((sec*85+j*36)%165);x=270+(y-474)*.10
   c.ellipse((x-2,y-3,x+2,y+3),'#d1ede3',None)
 # Slow camera push is applied only to the illustrated area, keeping text stable.
 zoom=1+.025*p
 if i==1 and p>.45:zoom=1.08+.025*p
 w=1080/zoom;h=1646/zoom;left=(1080-w)/2;top=(1646-h)*.55
 art=c.im.crop((round(left),round(top),round(left+w),round(top+h))).resize((1080,1646),Image.Resampling.BICUBIC)
 c.im.paste(art,(0,0));c.im.paste(hud(i,s['id']),(0,0),hud(i,s['id']));c.d=ImageDraw.Draw(c.im)
 total=sum(x['duration'] for x in scenes);progress=(s['start']+f)/total
 c.rect((0,956,540*progress,960),ns['ORANGE'])
 opacity=min(1,f/7,max(0,(s['duration']-1-f)/7))
 if opacity<1:c.im=Image.blend(Image.new('RGB',(1080,1920),'#ead9b4'),c.im,opacity)
 return c.im

if '--stills' in sys.argv:
 panel=Image.new('RGB',(1080,2000),'#ead9b4')
 for i,s in enumerate(scenes):
  im=frame(s,s['duration']//2);im.save(out/f'review-{i}.png');panel.paste(im.resize((270,480)),((i%4)*270,(i//4)*500))
 panel.save(ROOT/'out/rebeca-animacao-previa.jpg',quality=92);print('Painel de animação gerado.');raise SystemExit()
for i,s in enumerate(scenes):
 target=out/f'{i}.mp4'
 cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','pipe:0','-an','-frames:v',str(s['duration']),'-c:v','libx264','-preset','fast','-crf','18','-threads','2','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(target)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 try:
  for f in range(s['duration']):proc.stdin.write(frame(s,f).tobytes())
 finally:proc.stdin.close()
 if proc.wait()!=0:raise SystemExit('Falha na renderização da cena '+str(i+1))
 print(f'Cena {i+1}/{len(scenes)} animada',flush=True)
(out/'concat.txt').write_text(''.join(f"file '{i}.mp4'\n" for i in range(len(scenes))))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(out/'concat.txt'),'-i',str(ROOT/'entregas/papiro-revela-11-rebeca-1080p.mp4'),'-map','0:v','-map','1:a','-c:v','copy','-c:a','pcm_s16le',str(ROOT/'out/rebeca-render.mov')],check=True)
print('Animação e áudio montados.',flush=True)
