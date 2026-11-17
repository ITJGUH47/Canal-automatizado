"""Full narrated Genesis 27 episode using the approved paper-card articulated art."""
from pathlib import Path
from functools import lru_cache
import json,math,subprocess,sys
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'entregas/previas/esau-jaco-parte2/gerar-previa.py'
ns={'__file__':str(ART),'__name__':'approved_art'};exec(compile(ART.read_text(),str(ART),'exec'),ns)
C=ns['C'];DATA=ns['DATA'];S=2
original_actor=ns['actor'];state={'visual':0,'p':0}
def actor(c,x,y,s=1,who='jacob',**kwargs):
 i=state['visual'];p=state['p']
 if i==0 and who=='isaac':kwargs['right']=(58+7*math.sin(math.pi*p),-83-8*math.sin(math.pi*p))
 if i==6 and who=='isaac':kwargs['right']=(58+20*ns['ease'](p),-104-38*ns['ease'](p))
 if i==8 and who=='isaac':kwargs['tilt']=1.1*math.sin(p*math.pi*8)
 elif i not in [4,5,7] and 'tilt' not in kwargs:kwargs['tilt']=.7*math.sin(p*math.pi*2)
 return original_actor(c,x,y,s,who,**kwargs)
ns['actor']=actor
original_layout=ns['layout']
@lru_cache(maxsize=20)
def layout(i):
 c=C();c.im=original_layout(i).copy();c.d=ImageDraw.Draw(c.im);paper=ns['paper']()
 for box in [(520,60,1040,140),(40,1584,1040,1646),(490,1814,1040,1888)]:c.im.paste(paper.crop(box),(box[0],box[1]))
 c.d=ImageDraw.Draw(c.im)
 c.text(506,40,'DOSSIÊ 013 · PARTE 2',10,ns['TEAL'],anchor='ra',maxw=240)
 c.text(270,801,'Interpretação artística do relato.',12,ns['TEAL'],italic=True,anchor='ma')
 c.text(506,916,'VOZ: ELEVENLABS.IO',10,ns['TEAL'],anchor='ra',maxw=230)
 return c.im
scenes=json.loads((Path(__file__).parent/'cenas-tempos.json').read_text());OUT=ROOT/'out/esau-jaco-parte2-clips';OUT.mkdir(exist_ok=True)
def frame(s,f):
 i=s['visual'];p=f/max(1,s['duration']-1);state.update(visual=i,p=p)
 c=C();c.im=layout(i).copy();c.d=ImageDraw.Draw(c.im)
 art=C(460,410,ns['TEAL']);ns['room'](art);ns['action'](art,i,p)
 zoom=1+(.10 if i==5 else .025)*p;w=920/zoom;h=820/zoom;left=(920-w)/2;top=(820-h)/2
 image=art.im.crop((round(left),round(top),round(left+w),round(top+h))).resize((920,820),Image.Resampling.BICUBIC)
 image=image.rotate(1.2 if i%2==0 else -1.2,Image.Resampling.BICUBIC,expand=False,fillcolor=ns['TEAL'])
 c.im.paste(image,(78,662));c.d=ImageDraw.Draw(c.im);c.d.rectangle((78,662,998,1482),outline=ns['INK'],width=4)
 c.rect((0,956,540*(s['start']+f)/sum(x['duration'] for x in scenes),960),ns['ORANGE'])
 alpha=min(1,f/7,max(0,(s['duration']-1-f)/7))
 if alpha<1:c.im=Image.blend(Image.new('RGB',c.im.size,ns['PAPER']),c.im,alpha)
 return c.im
if '--stills' in sys.argv:
 panel=Image.new('RGB',(1080,1500),ns['PAPER'])
 for i,s in enumerate(scenes):
  im=frame(s,s['duration']//2);im.save(OUT/f'review-{i}.png');panel.paste(im.resize((270,480)),((i%4)*270,(i//4)*500))
 panel.save(ROOT/'out/esau-jaco-parte2-animacao-previa.jpg',quality=92);print('Painel da montagem gerado.');raise SystemExit()
for i,s in enumerate(scenes):
 target=OUT/f'{i}.mp4'
 proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','pipe:0','-an','-frames:v',str(s['duration']),'-c:v','libx264','-preset','fast','-crf','18','-threads','2','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(target)],stdin=subprocess.PIPE)
 try:
  for f in range(s['duration']):proc.stdin.write(frame(s,f).tobytes())
 finally:proc.stdin.close()
 if proc.wait()!=0:raise SystemExit('Falha na cena '+str(i+1))
 print(f'Cena {i+1}/{len(scenes)} renderizada',flush=True)
(OUT/'concat.txt').write_text(''.join(f"file '{i}.mp4'\n" for i in range(len(scenes))))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-i',str(ROOT/'entregas/papiro-revela-13-esau-jaco-parte2-1080p.mp4'),'-map','0:v','-map','1:a','-c:v','copy','-c:a','pcm_s16le',str(ROOT/'out/esau-jaco-parte2-render.mov')],check=True)
print('Vídeo e narração montados.',flush=True)
