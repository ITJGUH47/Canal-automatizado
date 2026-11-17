"""Local Portuguese Chatterbox samples; never calls ElevenLabs."""
from pathlib import Path
import argparse,os,json,hashlib,time
ROOT=Path(__file__).resolve().parents[4]
CACHE=ROOT/'.cache/chatterbox'
os.environ['HF_HOME']=str(CACHE/'huggingface')
os.environ['PKUSEG_HOME']=str(CACHE/'pkuseg')
os.environ.setdefault('HF_HUB_DISABLE_TELEMETRY','1')
os.environ.setdefault('HF_HUB_DISABLE_XET','0')
os.environ.setdefault('GRADIO_ANALYTICS_ENABLED','False')
PRESETS={'suave':{'exaggeration':.25,'cfg_weight':.5,'temperature':.65},'equilibrada':{'exaggeration':.45,'cfg_weight':.5,'temperature':.7},'expressiva':{'exaggeration':.65,'cfg_weight':.5,'temperature':.75}}
FILES=['ve.pt','t3_mtl23ls_v2.safetensors','s3gen.pt','grapheme_mtl_merged_expanded_v1.json','conds.pt','Cangjie5_TC.json']
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--check',action='store_true',help='Validate imports without downloading models or generating speech')
 p.add_argument('--download-only',action='store_true')
 p.add_argument('--preset',choices=PRESETS,default='equilibrada')
 p.add_argument('--text',default='Esaú voltou do campo cansado. Jacó havia preparado um cozido. Mas havia uma condição.')
 p.add_argument('--reference',type=Path,help='Optional recording supplied with permission to use its voice')
 p.add_argument('--seed',type=int,default=42)
 a=p.parse_args()
 import importlib.metadata as md
 import torch,torchaudio
 from chatterbox.mtl_tts import ChatterboxMultilingualTTS,SUPPORTED_LANGUAGES,REPO_ID
 torch.set_num_threads(min(4,os.cpu_count() or 1))
 assert 'pt' in SUPPORTED_LANGUAGES
 if a.check:
  print(json.dumps({'package':md.version('chatterbox-tts'),'torch':torch.__version__,'device':'cpu','portuguese':SUPPORTED_LANGUAGES['pt'],'model_repository':REPO_ID,'imports_ok':True,'model_download_attempted':False},ensure_ascii=False,indent=2));return
 if not a.text.strip() or len(a.text)>600:raise SystemExit('Use um trecho curto, de 1 a 600 caracteres.')
 if a.reference and not a.reference.is_file():raise SystemExit('O arquivo de referência informado não existe.')
 params={'text':a.text,'language_id':'pt','preset':a.preset,'settings':PRESETS[a.preset],'seed':a.seed,'package_version':md.version('chatterbox-tts'),'reference_sha256':hashlib.sha256(a.reference.read_bytes()).hexdigest() if a.reference else None}
 key=hashlib.sha256(json.dumps(params,sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:16]
 target=ROOT/'out/chatterbox'/f'{a.preset}-{key}.wav';target.parent.mkdir(parents=True,exist_ok=True)
 if target.exists() and not a.download_only:print('Amostra em cache:',target);return
 from huggingface_hub import snapshot_download
 print('Baixando/verificando os modelos oficiais. Pode exigir alguns GB de espaço.',flush=True)
 ckpt=snapshot_download(REPO_ID,allow_patterns=FILES,revision='main',max_workers=1)
 if a.download_only:print('Modelos disponíveis:',ckpt);return
 model=ChatterboxMultilingualTTS.from_local(ckpt,device='cpu')
 torch.manual_seed(a.seed);t=time.monotonic()
 with torch.inference_mode():
  wav=model.generate(a.text,language_id='pt',audio_prompt_path=str(a.reference.resolve()) if a.reference else None,**PRESETS[a.preset])
 torchaudio.save(str(target),wav.cpu(),model.sr)
 params.update(sample_rate=model.sr,generation_seconds=time.monotonic()-t,seconds=wav.shape[-1]/model.sr,model_snapshot=Path(ckpt).name)
 target.with_suffix('.json').write_text(json.dumps(params,ensure_ascii=False,indent=2)+'\n')
 print('Amostra gerada:',target)
if __name__=='__main__':main()
