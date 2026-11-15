# Reprodução da animação de Rebeca

Este arquivo acompanha o episódio 11 e reutiliza as funções de desenho das [imagens aprovadas](../previas/rebeca/gerar-ilustracoes.py). Cenário, humanos, animais, fonte e bebedouro são desenhados como camadas separadas. O script move as camadas, anima água e ondulações, aplica um movimento de câmera e mantém as legendas estáveis. São movimentos simples de animação 2D, não simulação física ou sincronização labial.

Execute na cópia do repositório com Python 3, Pillow, FFmpeg e fontes DejaVu em `/usr/share/fonts/truetype/dejavu`:

```sh
python entregas/rebeca-producao/animar-cenas.py --stills
python entregas/rebeca-producao/animar-cenas.py
```

O primeiro comando gera o painel em `out/rebeca-animacao-previa.jpg`. O segundo grava os clipes em `out/rebeca-clips/` e a montagem em `out/rebeca-render.mov`, usando [cenas-tempos.json](cenas-tempos.json). A versão reproduzível extrai a faixa de áudio do MP4 final entregue, sem chamar o ElevenLabs ou gastar créditos. É necessário ter o vídeo final baixado no caminho `entregas/papiro-revela-11-rebeca-1080p.mp4`.

O vídeo original foi produzido com a mesma animação, usando a mixagem WAV local antes da normalização final e codificação AAC. O roteiro final está em [REBECA-ROTEIRO.md](../REBECA-ROTEIRO.md). As imagens continuam sendo interpretações artísticas de Gênesis 24.
