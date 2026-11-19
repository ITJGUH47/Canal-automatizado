# Jacó em Betel — produção

Vídeo vertical 1080×1920, 30 fps, 12 cenas. Fonte: Gênesis 28:10–22. Arte aprovada em `../previas/jaco-betel/`.

- `animar-cenas.py`: anima a arte aprovada e monta o MP4; requer Pillow, FFmpeg e `public/assets/jaco-betel-mix.wav`. O áudio entregue em `narracao-trilha.mp3` permite assistir à mistura separadamente; o WAV de produção é recriado pelo gerador de narração com seu cache.
- `cenas-tempos.json`: tempos reais de cada cena, em quadros a 30 fps.
- `roteiro-aprovado.json`: texto aprovado, dividido entre as 12 cenas.
- `gerar-narracao.py` e `elevenlabs_voice.py`: reprodução da voz com chave segura ELEVENLABS_API_KEY. Usam a configuração não secreta `production/elevenlabs-settings.json` (cópia em `voz-config.json`). Copiar o roteiro para `production/jaco-betel/roteiro-aprovado.json` antes de reproduzir. Requer NumPy e SciPy. Não executar para apenas assistir; a síntese pode consumir créditos. Preserva cache e reutiliza o encerramento.
- `producao.json`: duração e contador observado da conta. O contador pode refletir atualização atrasada e não constitui uma promessa de custo zero.
- `verificacao.json`: verificação técnica do arquivo final.

As legendas SRT são um arquivo separado. Tempos internos de cada frase estimados a partir da duração real do segmento; não foram usados créditos adicionais para alinhamento. Nenhuma recarga, alteração de plano ou publicação em rede social foi feita.
