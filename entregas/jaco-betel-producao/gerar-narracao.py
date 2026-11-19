"""Generate only the approved Esau and Jacob narration; preserve the earlier episode."""
from pathlib import Path
import json, math, subprocess, wave, sys, hashlib, time, re
import numpy as np
from scipy.signal import resample_poly
from scipy.ndimage import uniform_filter1d
from elevenlabs_voice import configuration, settings, request, synthesize, VoiceError
ROOT=Path(__file__).resolve().parents[2]
folder=ROOT/'production/jaco-betel'; folder.mkdir(exist_ok=True)
scenes=json.loads((folder/'roteiro-aprovado.json').read_text())
config=settings(); key,voice_id=configuration()
characters=sum(len(s['text']) for s in scenes)
if voice_id != 'nPczCjzI2devNBz1zQrb': raise SystemExit('A voz selecionada não é Brian; nenhuma geração foi feita.')
if characters>2500: raise SystemExit('Roteiro acima do limite econômico deste episódio; revise antes de gerar.')
try:
    current=json.loads(request('/v1/user/subscription?refresh='+str(time.time_ns()),key))
    baseline=folder/'budget-before.json'
    if baseline.exists(): before=json.loads(baseline.read_text())
    else:
        before=current
        baseline.write_text(json.dumps({k:before[k] for k in ['tier','character_count','character_limit']},indent=2))
    models=json.loads(request('/v1/models',key))
    model=next(m for m in models if m['model_id']==config['model_id'])
    rate=model['model_rates']['character_cost_multiplier']
    if rate>.5: raise VoiceError('O modelo não está na faixa econômica aprovada. Nenhuma narração foi gerada.')
    upper=sum(math.ceil(len(t)*rate) for s in scenes if s['id']!='end' for t in re.split(r'(?<=[.!?])\s+',s['text']))
    if current['character_limit']-current['character_count']<upper:
        raise VoiceError('Créditos insuficientes; nenhuma recarga ou mudança de plano será feita.')
    print('Roteiro:',characters,'caracteres. Previsão conservadora:',upper,'créditos.',flush=True)
    meta=json.loads((ROOT/'entregas/identidade/encerramento-redes-config.json').read_text())
    cta=ROOT/'entregas/identidade/encerramento-redes-brian.mp3'
    if not (meta['text']==scenes[-1]['text'] and meta['voice_id']==voice_id and meta['model_id']==config['model_id'] and meta['settings']==config['voice_settings'] and meta['sha256']==hashlib.sha256(cta.read_bytes()).hexdigest()):
        raise VoiceError('O encerramento salvo não coincide com a configuração. Revisar antes de gerar.')
    clips=[];result=[];cursor=0;sr=48000
    for i,s in enumerate(scenes):
        pieces=[]
        phrases=[s['text']] if s['id']=='end' else re.split(r'(?<=[.!?])\s+',s['text'])
        for j,phrase in enumerate(phrases):
            audio=cta if s['id']=='end' else synthesize(phrase,ROOT/'production/elevenlabs-cache')
            raw=folder/f'voz-{i}-frase-{j}.wav'
            subprocess.run(['ffmpeg','-v','error','-y','-i',str(audio),'-ac','1','-ar',str(sr),str(raw)],check=True)
            with wave.open(str(raw)) as w:
                part=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(float)/32768
            pieces.append(part)
            if j<len(phrases)-1:pieces.append(np.zeros(round(.12*sr)))
        x=np.concatenate(pieces)
        with wave.open(str(folder/f'voz-{i}.wav'),'wb') as w:
            w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((x*32768).clip(-32768,32767).astype('<i2').tobytes())
        lead=.14; tail=.35 if i<len(scenes)-1 else 1.2
        frames=math.ceil((len(x)/sr+lead+tail)*30)
        total=frames*1600
        x=np.pad(x,(round(lead*sr),max(0,total-len(x)-round(lead*sr))))[:total]
        result.append({**s,'start':cursor,'duration':frames})
        cursor+=frames;clips.append(x)
        print(f'Cena {i+1}/{len(scenes)}: {frames/30:.2f}s',flush=True)
    speech=np.concatenate(clips);speech*=.78/max(np.max(np.abs(speech)),.01)
    length=len(speech);t=np.arange(length)/sr
    music=np.zeros((length,2))
    # Original slow pad: Cmaj7 / Am7 / Fmaj7 / Gsus. No third-party recordings.
    chords=[[130.8128,164.8138,195.9977,246.9417],[110,130.8128,164.8138,195.9977],[87.3071,110,130.8128,164.8138],[97.9989,130.8128,146.8324,195.9977]]
    for j,notes in enumerate(chords):
        phase=np.mod(t,32)
        center=j*8+4
        dist=np.minimum(np.abs(phase-center),32-np.abs(phase-center))
        env=np.maximum(0,1-dist/6)
        for k,freq in enumerate(notes):
            tone=np.sin(2*np.pi*freq*t+.13*np.sin(t*.4))+.16*np.sin(2*np.pi*2*freq*t)
            pan=k/3
            music[:,0]+=tone*env*.006*(1-pan*.35)
            music[:,1]+=tone*env*.006*(.65+pan*.35)
    activity=uniform_filter1d(np.abs(speech),size=round(sr*.16))
    duck=np.clip(1-activity*4,.32,1)
    music*=duck[:,None]
    music*=np.minimum(t/2,1)[:,None]*np.clip((t[-1]-t)/2.5,0,1)[:,None]
    rng=np.random.default_rng(281);sfx=np.zeros(length)
    for i,s in enumerate(result[1:],1):
        start=round(s['start']/30*sr);n=min(round(.28*sr),length-start)
        tt=np.arange(n)/sr
        noise=np.convolve(rng.normal(size=n),np.ones(10)/10,mode='same')
        sfx[start:start+n]+=noise*np.sin(np.linspace(0,np.pi,n))*.018
        n=min(sr,length-start);tt=np.arange(n)/sr
        note=[523.25,587.33,659.25,698.46,783.99,880,1046.5,523.25][(i-1)%8]
        sfx[start:start+n]+=np.sin(2*np.pi*note*tt)*np.exp(-tt*7)*.013*np.minimum(tt/.015,1)
    mix=speech[:,None]+music+sfx[:,None]
    mix*=min(1,.95/max(float(np.max(np.abs(mix))),.01))
    target=ROOT/'public/assets/jaco-betel-mix.wav'
    with wave.open(str(target),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr)
        w.writeframes((np.clip(mix,-1,1)*32767).astype('<i2').tobytes())
    (ROOT/'src/jaco-betel-scenes.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    after=json.loads(request('/v1/user/subscription?refresh='+str(time.time_ns()),key))
    report={'model':config['model_id'],'voice_id':voice_id,'voice_name':config['voice_name'],'characters':characters,'cta_reused':True,'cta_characters_saved':len(scenes[-1]['text']),'predicted_credits_upper':upper,'credits_observed':after['character_count']-before['character_count'],'remaining_reported':after['character_limit']-after['character_count'],'tier':after['tier'],'frames':cursor,'duration':cursor/30,'monthly_budget_brl':50,'notes':'Roteiro aprovado pelo usuário. Nenhuma mudança de plano, recarga ou cobrança excedente foi autorizada ou realizada. Cache por texto/voz/configuração. O delta de uso é o observado no contador da conta.'}
    (folder/'producao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False),flush=True)
except VoiceError as exc:
    raise SystemExit(str(exc))
