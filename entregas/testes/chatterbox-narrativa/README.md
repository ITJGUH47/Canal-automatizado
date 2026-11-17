# Teste de narração mais pausada e grave

[Baixar o comparativo original × ajustada](comparativo-narracao-1080p.mp4?raw=true)

[Ouvir somente a versão ajustada](voz-narrativa.mp3?raw=true)

Base: a amostra equilibrada do teste anterior do Chatterbox. Mantivemos a mesma fala e identidade de voz para comparar apenas o efeito do ajuste.

- Velocidade em 88% da original: fala cerca de 12% mais lenta.
- Tom em 94% da frequência original: aproximadamente um semitom mais grave.
- Reforço leve em 130 Hz e compressão moderada para dar corpo e presença.
- Volume normalizado para a comparação.

Este é um ajuste de áudio feito com FFmpeg/Rubber Band, sem nova síntese, sem utilizar os áudios do Brian e sem chamadas ao ElevenLabs. A intenção é avaliar o ritmo e a presença antes de aplicar o processamento ao episódio completo. A naturalidade deve ser avaliada ouvindo a amostra; os parâmetros podem ser suavizados ou intensificados depois.

[Parâmetros](ajuste.json) · [Script reproduzível](ajustar-voz.py) · [Verificação técnica](verificacao.json)

Para reproduzir a partir do repositório, com Python 3/Pillow e FFmpeg com suporte Rubber Band:

```sh
python entregas/testes/chatterbox-narrativa/ajustar-voz.py
```

A fonte original permanece em `entregas/testes/chatterbox/voz-equilibrada.wav`. Nenhuma configuração global do narrador do canal foi alterada.
