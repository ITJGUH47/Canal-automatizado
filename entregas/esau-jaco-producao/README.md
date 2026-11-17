# Animação de Esaú e Jacó

Script reproduzível em Python/Pillow + FFmpeg, usando as funções das imagens aprovadas em `entregas/previas/esau-jaco/gerar-ilustracoes.py`. Personagens, panela, pão e tigela são camadas separadas. A animação utiliza movimentos simples, vapor, chama e câmera; sem sincronização labial ou simulação física.

```sh
python entregas/esau-jaco-producao/animar-cenas.py --stills
python entregas/esau-jaco-producao/animar-cenas.py
```

Requisitos: Python 3, Pillow, FFmpeg e fontes DejaVu em `/usr/share/fonts/truetype/dejavu`. Saídas em `out/esau-jaco-clips` e `out/esau-jaco-render.mov`. A versão reproduzível usa a faixa de áudio do MP4 final entregue, em `entregas/papiro-revela-12-esau-jaco-1080p.mp4`, sem síntese de voz e sem consumo de créditos. A produção original usou o WAV local antes da normalização e codificação AAC.

Os tempos medidos estão em [cenas-tempos.json](cenas-tempos.json). O vídeo usa Brian / ElevenLabs, sem os ajustes de voz do teste Chatterbox. Roteiro da montagem em [ESAU-JACO-ROTEIRO.md](../ESAU-JACO-ROTEIRO.md).
