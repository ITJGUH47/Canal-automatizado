# Lia e os nomes dos filhos — produção

Vídeo vertical 1080×1920, 30 fps, com 12 cenas. Fonte: Gênesis 29:30–35. Arte aprovada em `../previas/lia-filhos/`.

`animar-cenas.py` usa Pillow, FFmpeg, `cenas-tempos.json` e `public/assets/lia-filhos-mix.wav`. `gerar-narracao.py` requer NumPy, SciPy, FFmpeg, a chave segura ELEVENLABS_API_KEY, o roteiro em `production/lia-filhos/roteiro-aprovado.json` e a configuração em `production/elevenlabs-settings.json` (cópia não secreta em `voz-config.json`). A síntese pode consumir créditos; não precisa executá-la para assistir ao vídeo. Cache por texto, voz e configuração; encerramento reutilizado.

`narracao-trilha.mp3` contém a mistura entregue separadamente. As legendas SRT são um arquivo separado: os tempos de cada frase seguem os segmentos reais, com estimativa proporcional para divisões internas.

Lia mantém a roupa lilás e Jacó o verde. A filiação é explicitada. Os quatro filhos mostrados são os primeiros de Lia, não todos. As falas são paráfrases das explicações dos nomes no relato; não uma tradução literal ou estudo etimológico independente. Aparência, roupas e cenário são interpretações artísticas. O louvor ao nascer Judá não é apresentado como comprovação de que toda a dor de Lia acabou.

Nenhuma recarga, alteração de plano ou publicação em rede social foi realizada. `producao.json` registra o contador observado após a geração; `verificacao.json` registra as verificações técnicas do MP4.
