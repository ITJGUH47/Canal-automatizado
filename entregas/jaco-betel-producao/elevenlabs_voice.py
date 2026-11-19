"""ElevenLabs REST integration. Uses inherited HTTPS proxy and TLS trust."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.request

API = 'https://api.elevenlabs.io'
ROOT = Path(__file__).resolve().parents[2]

class VoiceError(RuntimeError):
    pass

def settings():
    path = ROOT / 'production/elevenlabs-settings.json'
    return json.loads(path.read_text()) if path.exists() else {}

def configuration(voice_required=True):
    key = os.environ.get('ELEVENLABS_API_KEY', '').strip()
    if not key:
        raise VoiceError('Cadastre ELEVENLABS_API_KEY nas configurações seguras do ambiente. Não envie a chave no chat.')
    voice = os.environ.get('ELEVENLABS_VOICE_ID', settings().get('voice_id', '')).strip()
    if voice_required and not voice:
        raise VoiceError('Escolha uma voz com npm run voices:elevenlabs e configure ELEVENLABS_VOICE_ID.')
    if voice and not re.fullmatch(r'[A-Za-z0-9_-]{1,128}', voice):
        raise VoiceError('ELEVENLABS_VOICE_ID inválido: use o identificador da voz, não uma URL.')
    return key, voice

def request(path, key, payload=None):
    data = None if payload is None else json.dumps(payload).encode('utf-8')
    headers = {'xi-api-key': key, 'Accept': 'application/json' if data is None else 'audio/mpeg'}
    if data is not None:
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(API + path, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            body = response.read(10_000_001)
            if len(body) > 10_000_000:
                raise VoiceError('Resposta de áudio acima do limite esperado; nenhum arquivo foi substituído.')
            content_type = response.headers.get('Content-Type', '')
            if payload is not None and not content_type.startswith('audio/'):
                raise VoiceError('ElevenLabs não retornou áudio. Nenhum arquivo foi substituído.')
            return body
    except urllib.error.HTTPError as exc:
        hints = {400:'Verifique o modelo, a voz e os parâmetros.',401:'Verifique a chave cadastrada.',403:'Verifique as permissões da chave, acesso à voz e a política de rede.',404:'Confira o identificador da voz.',429:'Verifique os créditos e os limites da conta antes de tentar novamente.'}
        status=''
        try:
            detail=json.loads(exc.read(8192)).get('detail',{})
            candidate=detail.get('status','') if isinstance(detail,dict) else ''
            if isinstance(candidate,str) and re.fullmatch(r'[A-Za-z0-9_]{1,80}',candidate): status=' ('+candidate+')'
        except (ValueError,OSError):
            pass
        raise VoiceError(f'ElevenLabs HTTP {exc.code}{status}. '+hints.get(exc.code,'Verifique o serviço antes de tentar novamente.')) from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise VoiceError('Não foi possível concluir a conexão HTTPS com api.elevenlabs.io. Verifique a rede e as configurações salvas. A geração não é repetida automaticamente para evitar consumo duplicado.') from None

def list_voices():
    key, _ = configuration(False)
    result = json.loads(request('/v1/voices', key))
    return [{'voice_id':v['voice_id'], 'name':v.get('name',''), 'labels':v.get('labels',{})} for v in result.get('voices',[])]

def synthesize(text, cache_dir, *, allow_cached=True):
    key, voice = configuration()
    if not text.strip():
        raise VoiceError('O texto de narração está vazio.')
    config = settings()
    if len(text) > config.get('max_characters_per_request', 600):
        raise VoiceError('Texto acima do limite de economia por chamada. Divida ou revise o roteiro antes de gerar.')
    model = os.environ.get('ELEVENLABS_MODEL_ID', config.get('model_id', 'eleven_multilingual_v2'))
    if model not in {'eleven_multilingual_v2', 'eleven_turbo_v2_5', 'eleven_flash_v2_5'}:
        raise VoiceError('Modelo fora da lista aprovada. Verifique o custo antes de habilitar outro modelo.')
    payload = {'text':text,'model_id':model,'language_code':'pt','voice_settings':config.get('voice_settings', {'stability':0.65,'similarity_boost':0.75,'style':0.15,'use_speaker_boost':True})}
    fingerprint = hashlib.sha256(json.dumps({'voice':voice,**payload},sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    cache_dir=Path(cache_dir)
    cache_dir.mkdir(parents=True,exist_ok=True)
    audio=cache_dir/(fingerprint+'.mp3')
    if allow_cached and audio.exists():
        return audio
    # Restore the approved social CTA from its durable asset if the transient cache is absent.
    record = ROOT / 'production/cta-redes.json'
    reusable = ROOT / 'public/assets/cta-redes-brian-turbo-v2-5.mp3'
    if not record.exists() or not reusable.exists():
        record = ROOT / 'entregas/identidade/encerramento-redes-config.json'
        reusable = ROOT / 'entregas/identidade/encerramento-redes-brian.mp3'
    if allow_cached and record.exists() and reusable.exists():
        try:
            saved = json.loads(record.read_text())
            exact_match = (saved.get('text') == text and saved.get('voice_id') == voice
                           and saved.get('model_id') == model and saved.get('settings') == payload['voice_settings']
                           and saved.get('sha256') == hashlib.sha256(reusable.read_bytes()).hexdigest())
            if exact_match:
                subprocess.run(['ffmpeg', '-v', 'error', '-i', str(reusable), '-f', 'null', '-'], check=True, capture_output=True)
                audio.write_bytes(reusable.read_bytes())
                return audio
        except (ValueError, OSError, subprocess.CalledProcessError):
            pass
    # Never automatically retry a billable POST. Cache each completed segment.
    body=request(f'/v1/text-to-speech/{voice}?output_format=mp3_44100_128',key,payload)
    temp=audio.with_suffix('.part.mp3')
    temp.write_bytes(body)
    try:
        subprocess.run(['ffprobe','-v','error','-select_streams','a:0','-show_entries','stream=codec_name','-of','csv=p=0',str(temp)],check=True,capture_output=True)
        check=subprocess.run(['ffmpeg','-v','error','-i',str(temp),'-f','null','-'],check=True,capture_output=True)
    except subprocess.CalledProcessError:
        temp.unlink(missing_ok=True)
        raise VoiceError('O áudio recebido não pôde ser decodificado. Nenhum áudio do projeto foi substituído.') from None
    temp.replace(audio)
    audio.with_suffix('.json').write_text(json.dumps({'voice_id':voice,'model_id':payload['model_id'],'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'settings':payload['voice_settings']},indent=2))
    return audio

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['voices','preview','check'])
    args=parser.parse_args()
    try:
        if args.command=='voices':
            print(json.dumps(list_voices(),ensure_ascii=False,indent=2))
        elif args.command=='check':
            configuration()
            voices=list_voices()
            _,selected=configuration()
            if not any(v['voice_id']==selected for v in voices):
                raise VoiceError('A voz selecionada não aparece na biblioteca desta conta. Adicione-a à biblioteca ou escolha outra voz.')
            print('Conexão de leitura e voz selecionada verificadas. Nenhum crédito de síntese foi usado.')
        else:
            text=json.loads((ROOT/'production/roteiro.json').read_text())[0]['text']
            path=synthesize(text,ROOT/'production/elevenlabs-cache')
            target=ROOT/'out/elevenlabs-previa.mp3'
            target.parent.mkdir(exist_ok=True)
            target.write_bytes(path.read_bytes())
            print('Prévia gerada:',target)
    except (VoiceError,json.JSONDecodeError) as exc:
        print(str(exc) if isinstance(exc,VoiceError) else 'Resposta inesperada ao consultar vozes.',file=sys.stderr)
        return 1
    return 0

if __name__=='__main__':
    raise SystemExit(main())
