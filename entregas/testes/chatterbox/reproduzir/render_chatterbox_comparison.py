"""Render one labelled comparison video from the three local audio samples."""
from pathlib import Path
import json,math,subprocess
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[4];OUT=ROOT/'entregas/testes/chatterbox';WORK=ROOT/'out/chatterbox-comparison';WORK.mkdir(parents=True,exist_ok=True)
report=json.loads((OUT/'geracao.json').read_text());font='/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'
for i,s in enumerate(report):
 name=s['preset'];im=Image.open(ROOT/'entregas/previas/esau-jaco/01-panela.png').convert('RGB');d=ImageDraw.Draw(im)
 d.rectangle((36,164,1044,278),fill='#f7edce')
 d.text((540,181),f'TESTE {i+1} · {name.upper()}',font=ImageFont.truetype(font,53),anchor='ma',fill='#28675f')
 d.rectangle((36,1646,1044,1824),fill='#ead9b4')
 for j,t in enumerate(['ESAÚ VOLTOU CANSADO.','JACÓ HAVIA PREPARADO UM COZIDO.']):
  f=ImageFont.truetype(font,47);d.text((540,1667+j*66),t,font=f,anchor='ma',fill='#342e27')
 d.rectangle((575,1840,1044,1900),fill='#ead9b4');d.text((1020,1865),'CHATTERBOX · PORTUGUÊS',font=ImageFont.truetype(font,22),anchor='rm',fill='#28675f')
 still=WORK/f'{name}.png';im.save(still)
 duration=math.ceil((s['duration']+.85)*30)/30
 subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-i',str(still),'-i',str(OUT/f'voz-{name}.wav'),'-vf',f"scale=1102:1960,crop=1080:1920:x='11+3*sin(t)':y=20,fade=t=in:st=0:d=0.2:color=0xead9b4,fade=t=out:st={duration-.25}:d=0.25:color=0xead9b4,format=yuv420p",'-af','adelay=250:all=1,apad,highpass=f=65,loudnorm=I=-16:TP=-2.5:LRA=9','-t',str(duration),'-c:v','libx264','-preset','fast','-crf','19','-threads','2','-c:a','aac','-ar','48000','-ac','2','-b:a','160k',str(WORK/f'{name}.mp4')],check=True)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(OUT/f'voz-{name}.wav'),'-af','loudnorm=I=-16:TP=-2.5:LRA=9','-c:a','libmp3lame','-b:a','160k',str(OUT/f'voz-{name}.mp3')],check=True)
 print('Vídeo de teste pronto:',name,flush=True)
(WORK/'concat.txt').write_text(''.join(f"file '{s['preset']}.mp4'\n" for s in report))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(WORK/'concat.txt'),'-c','copy','-movflags','+faststart','-metadata','title=Papiro Revela - teste de estilos Chatterbox',str(OUT/'teste-vozes-chatterbox-1080p.mp4')],check=True)
print('Comparativo concluído.',flush=True)
