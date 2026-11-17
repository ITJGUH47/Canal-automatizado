# Teste local de voz — Chatterbox Multilingual

[Baixar o vídeo comparativo Full HD](teste-vozes-chatterbox-1080p.mp4?raw=true)

O mesmo trecho de Esaú e Jacó em três estilos da **voz padrão do modelo**. Estes presets alteram expressividade e parâmetros de geração; **não são três identidades de voz diferentes**. Sem referência externa de voz e sem usar os áudios do Brian.

1. [Suave — MP3](voz-suave.mp3?raw=true)
2. [Equilibrada — MP3](voz-equilibrada.mp3?raw=true)
3. [Expressiva — MP3](voz-expressiva.mp3?raw=true)

Texto: “Esaú voltou do campo cansado. Jacó havia preparado um cozido. Mas havia uma condição.”

Vídeo curto de avaliação, com as imagens aprovadas do projeto, sem trilha para facilitar a comparação. O roteiro completo não foi narrado. A voz foi gerada em português (`pt`) pelo Chatterbox 0.1.7, em CPU, sem chamadas ou créditos do ElevenLabs. Arquivos WAV originais e seus metadados também estão nesta pasta. Marca-d’água Perth original mantida.

## Como comparar

Ouça a pronúncia de “Esaú” e “Jacó”, as pausas, o ritmo e a expressividade. O fato de o arquivo passar nas verificações técnicas não garante naturalidade ou ausência de erros de fala. Este teste serve para decidir se o timbre padrão combina com o Papiro Revela antes de gerar um episódio inteiro.

## Instalação validada

Python 3.12.14; Chatterbox 0.1.7; PyTorch/torchaudio 2.6.0+cpu; setuptools 80.9.0. O setuptools foi fixado porque a dependência Perth ainda usa `pkg_resources`. Cache de Hugging Face e PKUSEG na pasta gravável do projeto. Os modelos oficiais somam aproximadamente 3.2 GB; os pesos não são enviados ao GitHub. Licença do projeto Chatterbox: MIT. Fonte: https://github.com/resemble-ai/chatterbox

[Scripts de reprodução e dependências](reproduzir) · [Metadados das amostras](geracao.json) · [Verificação do vídeo](verificacao.json)

Execute a partir da raiz do repositório, com o ambiente `.venv-chatterbox` instalado:

```sh
.venv-chatterbox/bin/python entregas/testes/chatterbox/reproduzir/chatterbox_voice.py --download-only
.venv-chatterbox/bin/python entregas/testes/chatterbox/reproduzir/chatterbox_profiles.py
.venv/bin/python entregas/testes/chatterbox/reproduzir/render_chatterbox_comparison.py
```

O último comando utiliza Pillow e FFmpeg do ambiente do projeto. Os scripts reutilizam o cache quando a amostra existe. Para instalação, use `pip install chatterbox-tts==0.1.7 setuptools==80.9.0` num ambiente isolado, depois de instalar torch/torchaudio CPU pelo índice oficial do PyTorch. O lockfile registra as versões usadas. É preciso acesso ao Hugging Face e aos servidores de distribuição para o primeiro download.
