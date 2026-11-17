# Esaú e Jacó — Parte 2: reprodução da animação

A montagem utiliza o [desenho aprovado](../previas/esau-jaco-parte2/gerar-previa.py), retomando o papel claro, os títulos grandes e os cartões em verde-petróleo dos primeiros episódios. Braços são formados por ombro, cotovelo e punho; a posição do cotovelo é calculada com segmentos de comprimento constante. A cabeça tem rotação própria. Há movimento na entrega da comida, no toque das mãos, na bênção e na chegada de Esaú, além de aproximações de câmera.

```sh
python entregas/esau-jaco-parte2-producao/animar-cenas.py --stills
python entregas/esau-jaco-parte2-producao/animar-cenas.py
```

Requisitos: Python 3, Pillow, FFmpeg e fontes DejaVu em `/usr/share/fonts/truetype/dejavu`. Saídas em `out/esau-jaco-parte2-clips/` e `out/esau-jaco-parte2-render.mov`. Esta cópia reproduzível usa a faixa de áudio do vídeo final entregue, em `entregas/papiro-revela-13-esau-jaco-parte2-1080p.mp4`, sem chamadas ao ElevenLabs. A produção original usou a mixagem WAV local antes da normalização e codificação AAC.

[Tempos das cenas](cenas-tempos.json) · [Roteiro da montagem](../ESAU-JACO-PARTE2-ROTEIRO.md). Não há simulação física, sincronização labial ou reconstrução histórica exata dos gestos. Os pequenos intervalos entre cenas foram reduzidos para caber em dois minutos; o áudio falado não foi acelerado nem teve seu tom alterado.
