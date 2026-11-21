# Jacó, Raquel e Lia — produção

Vídeo vertical 1080×1920, 30 fps. Fonte: Gênesis 29:1–30. Arte aprovada em `../previas/jaco-raquel-lia/`.

`animar-cenas.py` reproduz a montagem com Pillow e FFmpeg a partir de `cenas-tempos.json` e `public/assets/jaco-raquel-lia-mix.wav`. `gerar-narracao.py` usa o roteiro em `production/jaco-raquel-lia/roteiro-aprovado.json`, a configuração em `production/elevenlabs-settings.json` (cópia em `voz-config.json`), NumPy, SciPy e uma chave segura ELEVENLABS_API_KEY. Não execute a síntese para apenas assistir: ela pode consumir créditos. O encerramento é reutilizado e as frases são guardadas em cache.

O MP3 entregue permite conferir a mistura separadamente. As legendas SRT são separadas; os intervalos dentro das frases foram estimados a partir das durações reais dos segmentos.

Roupa, aparência, arquitetura e objetos são interpretações artísticas. O painel mantém a identificação de Raquel em terracota e Lia em lilás. A cronologia distingue a semana de celebração dos sete anos adicionais de serviço.

Nenhuma mudança de plano, recarga ou publicação em rede social foi feita. O contador de créditos em `producao.json` foi consultado após a geração e pode atualizar com atraso.
