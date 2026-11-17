"""Subtle slower, lower-pitched narration from the user's chosen test voice."""
from pathlib import Path
import subprocess,json,math
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
SOURCE=ROOT/'entregas/testes/chatterbox/voz-equilibrada.wav'
WORK=ROOT/'out/chatterbox-narrativa';WORK.mkdir(parents=True,exist_ok=True)
filters='rubberband=tempo=0.88:pitch=0.94:transients=smooth:detector=soft:window=long:pitchq=quality,highpass=f=65,equalizer=f=130:t=q:w=0.8:g=2,acompressor=threshold=0.18:ratio=2:attack=15:release=180,loudnorm=I=-16:TP=-2.5:LRA=9'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(SOURCE),'-af',filters,'-ar','48000','-ac','1','-c:a','pcm_s16le',str(OUT/'voz-narrativa.wav')],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(OUT/'voz-narrativa.wav'),'-c:a','libmp3lame','-b:a','160k',str(OUT/'voz-narrativa.mp3')],check=True)
font='/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf';report=[]
for name,label,audio in [('original','ORIGINAL · EQUILIBRADA',SOURCE),('narrativa','NOVA · NARRATIVA MAIS GRAVE',OUT/'voz-narrativa.wav')]:
 info=json.loads(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(audio)],check=True,capture_output=True,text=True).stdout)
 dur=float(info['format']['duration']);duration=math.ceil((dur+.85)*30)/30
 im=Image.open(ROOT/'entregas/previas/esau-jaco/01-panela.png').convert('RGB');d=ImageDraw.Draw(im)
 d.rectangle((36,164,1044,278),fill='#f7edce');f=ImageFont.truetype(font,49 if name=='original' else 46)
 d.text((540,188),label,font=f,anchor='ma',fill='#28675f')
 d.rectangle((36,1646,1044,1824),fill='#ead9b4')
 for k,t in enumerate(['ESAÚ VOLTOU CANSADO.','JACÓ HAVIA PREPARADO UM COZIDO.']):d.text((540,1667+k*66),t,font=ImageFont.truetype(font,47),anchor='ma',fill='#342e27')
 d.rectangle((575,1840,1044,1900),fill='#ead9b4');d.text((1020,1865),'CHATTERBOX · TESTE DE NARRAÇÃO',font=ImageFont.truetype(font,21),anchor='rm',fill='#28675f')
 im.save(WORK/f'{name}.png')
 subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-i',str(WORK/f'{name}.png'),'-i',str(audio),'-vf',f'scale=1102:1960,crop=1080:1920:11:20,fade=t=in:st=0:d=0.2:color=0xead9b4,fade=t=out:st={duration-.25}:d=0.25:color=0xead9b4,format=yuv420p','-af','adelay=250:all=1,apad,loudnorm=I=-16:TP=-2.5:LRA=9','-t',str(duration),'-c:v','libx264','-preset','fast','-crf','19','-threads','2','-c:a','aac','-ar','48000','-ac','2','-b:a','160k',str(WORK/f'{name}.mp4')],check=True)
 report.append({'name':name,'audio_duration':dur,'video_duration':duration})
(WORK/'concat.txt').write_text("file 'original.mp4'\nfile 'narrativa.mp4'\n")
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(WORK/'concat.txt'),'-c','copy','-movflags','+faststart',str(OUT/'comparativo-narracao-1080p.mp4')],check=True)
(OUT/'ajuste.json').write_text(json.dumps({'source':'../chatterbox/voz-equilibrada.wav','tempo_ratio':.88,'pitch_ratio':.94,'pitch_semitones':12*math.log2(.94),'equalizer_db_at_130hz':2,'filter':filters,'samples':report,'new_tts_generation':False,'elevenlabs_calls':0},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False),flush=True)
