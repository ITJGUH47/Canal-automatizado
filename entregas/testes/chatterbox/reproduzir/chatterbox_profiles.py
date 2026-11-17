"""Generate a short, repeatable three-style Portuguese comparison on CPU."""
from pathlib import Path
import json,time,hashlib
import chatterbox_voice as setup
ROOT=setup.ROOT
OUT=ROOT/'entregas/testes/chatterbox';OUT.mkdir(parents=True,exist_ok=True)
TEXT='Esaú voltou do campo cansado. Jacó havia preparado um cozido. Mas havia uma condição.'
def main():
 import torch,torchaudio
 from chatterbox.mtl_tts import ChatterboxMultilingualTTS,REPO_ID
 from huggingface_hub import snapshot_download
 torch.set_num_threads(min(4,setup.os.cpu_count() or 1))
 ckpt=snapshot_download(REPO_ID,allow_patterns=setup.FILES,local_files_only=True)
 assert all((Path(ckpt)/f).exists() for f in setup.FILES),'O download dos modelos ainda não está completo.'
 print('Carregando modelo multilíngue em CPU.',flush=True)
 model=ChatterboxMultilingualTTS.from_local(ckpt,device='cpu')
 report=[]
 for name,params in setup.PRESETS.items():
  target=OUT/f'voz-{name}.wav';meta=target.with_suffix('.json')
  if target.exists() and meta.exists():
   report.append(json.loads(meta.read_text()));print('Amostra reutilizada:',name,flush=True);continue
  torch.manual_seed(42);t=time.monotonic()
  print('Gerando estilo:',name,flush=True)
  with torch.inference_mode():wav=model.generate(TEXT,language_id='pt',**params)
  if not torch.isfinite(wav).all() or float(wav.abs().max())<.001:raise RuntimeError('Áudio inválido no estilo '+name)
  torchaudio.save(str(target),wav.cpu(),model.sr)
  r={'preset':name,'settings':params,'text':TEXT,'language':'pt','device':'cpu','sample_rate':model.sr,'duration':wav.shape[-1]/model.sr,'generation_seconds':time.monotonic()-t,'seed':42,'model_snapshot':Path(ckpt).name,'reference':'builtin default voice, no external reference','sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
  meta.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');report.append(r)
  print('Concluído:',name,r['duration'],'s de áudio;',round(r['generation_seconds'],1),'s de processamento.',flush=True)
 (OUT/'geracao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
