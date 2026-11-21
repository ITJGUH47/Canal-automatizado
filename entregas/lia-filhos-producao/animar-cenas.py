"""Reproduz a animação em 1080x1920/30fps a partir da arte aprovada e tempos da voz."""
from pathlib import Path
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
import json,math,subprocess,sys
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'entregas/previas/lia-filhos/gerar-ilustracoes.py'
ns={'__file__':str(ART),'__name__':'approved_art'};exec(compile(ART.read_text(),str(ART),'exec'),ns)
C=ns['C'];original_actor=ns['actor']
def actor(c,x,y,s=1,who='jacob',**kwargs):
 kwargs['tilt']=kwargs.get('tilt',0)+.65*math.sin(x*.07)
 return original_actor(c,x,y,s,who,**kwargs)
ns['actor']=actor
@lru_cache(maxsize=12)
def layout(i):
 c=C();c.im=ns['layout'](i).copy();c.d=ImageDraw.Draw(c.im);paper=ns['paper']()
 for box in [(520,60,1040,140),(490,1814,1040,1888)]:c.im.paste(paper.crop(box),(box[0],box[1]))
 c.d=ImageDraw.Draw(c.im)
 c.text(506,40,'DOSSIÊ 016 · GÊNESIS 29',10,ns['TEAL'],anchor='ra',maxw=240)
 c.text(506,916,'VOZ: ELEVENLABS.IO',10,ns['TEAL'],anchor='ra',maxw=230)
 return c.im
scenes=json.loads((Path(__file__).parent/'cenas-tempos.json').read_text());OUT=ROOT/'out/lia-filhos-clips';OUT.mkdir(exist_ok=True)
def frame(s,f):
 i=s['visual'];p=f/max(1,s['duration']-1)
 c=C();c.im=layout(i).copy();c.d=ImageDraw.Draw(c.im)
 art=C(460,410,ns['TEAL']);ns['action'](art,i,p)
 zoom=1+.035*ns['ease'](p);w=920/zoom;h=820/zoom;left=(920-w)/2;top=(820-h)/2
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
  im=frame(s,s['duration']//2);panel.paste(im.resize((270,480)),((i%4)*270,(i//4)*500))
 panel.save(ROOT/'entregas/lia-filhos-producao/painel-montagem.jpg',quality=92);raise SystemExit()
def render(item):
 i,s=item;target=OUT/f'{i}.mp4'
 if target.exists():
  check=subprocess.run(['ffprobe','-v','error','-show_entries','stream=nb_frames','-of','csv=p=0',str(target)],capture_output=True,text=True)
  if check.returncode==0 and check.stdout.strip()==str(s['duration']):return
 proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','pipe:0','-an','-frames:v',str(s['duration']),'-c:v','libx264','-preset','fast','-crf','18','-threads','2','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(target)],stdin=subprocess.PIPE)
 try:
  for f in range(s['duration']):proc.stdin.write(frame(s,f).tobytes())
 finally:proc.stdin.close()
 if proc.wait()!=0:raise SystemExit('Falha na cena '+str(i+1))
 print(f'Cena {i+1}/12 renderizada',flush=True)
with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(render,enumerate(scenes)))
(OUT/'concat.txt').write_text(''.join(f"file '{i}.mp4'\n" for i in range(len(scenes))))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-i',str(ROOT/'public/assets/lia-filhos-mix.wav'),'-map','0:v','-map','1:a','-c:v','copy','-af','highpass=f=65,loudnorm=I=-16:TP=-2.5:LRA=9','-ar','48000','-ac','2','-c:a','aac','-b:a','192k','-movflags','+faststart','-metadata','title=Papiro Revela - Lia e seus filhos | elevenlabs.io','-metadata','comment=Genesis 29:30-35. Brian / ElevenLabs Turbo v2.5.',str(ROOT/'entregas/papiro-revela-16-lia-filhos-1080p.mp4')],check=True)
print('Vídeo e narração montados.',flush=True)
