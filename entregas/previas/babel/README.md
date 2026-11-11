# Babel — prévia de ilustrações por script

Revisão baseada no roteiro apresentado no chat (Gênesis 11:1–9) e nos arquivos dos episódios anteriores, especialmente `src/Enoch.tsx`, `src/ArkImagePreview.tsx`, as capas de Enoque e da arca. Esta pasta contém apenas a revisão visual; não há vídeo montado nem nova narração.

[Ver todas as cenas no painel](00-painel-de-cenas.jpg)

| Cena | Imagem Full HD vertical |
| --- | --- |
| 1. O motivo da torre | [Abrir](01-por-que-babel.png) |
| 2. Uma só língua e a planície de Sinar | [Abrir](02-sinar.png) |
| 3. Tijolos e betume | [Abrir](03-tijolos.png) |
| 4. Fazer um nome e evitar a dispersão | [Abrir](04-proposito.png) |
| 5. Confusão das línguas | [Abrir](05-linguas.png) |
| 6. Dispersão do povo | [Abrir](06-dispersao.png) |
| 7. O texto não diz que a torre foi destruída | [Abrir](07-detalhe.png) |
| 8. Encerramento nas três redes | [Abrir](08-encerramento.png) |

## Como foram feitas

Ilustrações originais desenhadas por coordenadas, polígonos, linhas e formas em Python/Pillow: [gerar-ilustracoes.py](gerar-ilustracoes.py). Sem imagens de banco ou geração de imagens por IA nesta revisão. Semente fixa e saídas em 1080 × 1920. Layout: papel claro, verde-petróleo, laranja queimado, amarelo, títulos condensados, subtítulo em itálico, cartões e etiquetas de passagem bíblica.

Execute `python gerar-ilustracoes.py` com Python 3, Pillow e fontes DejaVu disponíveis em `/usr/share/fonts/truetype/dejavu`. O script grava os PNGs, o painel JPEG e o manifesto [cenas.json](cenas.json) nesta pasta. As fontes DejaVu usam a licença DejaVu/Bitstream; o script usa as fontes instaladas, sem redistribuí-las.

O formato, a altura e o número de patamares da torre são interpretação artística. Gênesis não fornece essas medidas nem afirma a destruição da torre. Não representamos Deus em forma humana. Os desenhos diferenciam conversa interrompida, obra interrompida e dispersão, sem inventar destruição.

O encerramento mantém o texto combinado: “Segue o Papiro Revela no Instagram, TikTok e YouTube. Curiosidades bíblicas, direto do texto.” O áudio já salvo será reutilizado quando houver montagem aprovada.
