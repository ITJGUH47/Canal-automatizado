# Esaú e Jacó — Parte 2: imagens e prévia articulada

[Ver as 12 imagens](00-painel-de-cenas.jpg) · [Baixar a prévia de movimentos sem áudio](previa-movimentos-sem-audio-1080p.mp4?raw=true)

O estudo retoma a identidade dos primeiros episódios: papel claro com textura, títulos condensados grandes, subtítulos em itálico, verde-petróleo, laranja queimado, amarelo e cartões com sombra. A ação acontece dentro dos cartões, com personagens em partes articuladas.

A prévia tem **12 segundos, 1080 × 1920 e 30 fps**, sem trilha nem narração. Mostra três trechos de quatro segundos: a entrega da refeição, Isaque estendendo a mão para tocar a mão de Jacó e a chegada de Esaú depois da saída do irmão. É um teste de movimento, não a montagem completa da história.

## Imagens

| Cena | Imagem |
| --- | --- |
| 1. O pedido de Isaque | [Abrir](01-pedido.png) |
| 2. Rebeca orienta Jacó | [Abrir](02-plano.png) |
| 3. A diferença entre os irmãos | [Abrir](03-diferenca.png) |
| 4. Roupas e peles | [Abrir](04-disfarce.png) |
| 5. A entrega da refeição | [Abrir](05-refeicao.png) |
| 6. A voz e as mãos | [Abrir](06-maos.png) |
| 7. A bênção | [Abrir](07-bencao.png) |
| 8. A chegada de Esaú | [Abrir](08-esau.png) |
| 9. A descoberta | [Abrir](09-descoberta.png) |
| 10. A orientação para fugir | [Abrir](10-fuga.png) |
| 11. A distinção entre os episódios | [Abrir](11-episodios.png) |
| 12. Encerramento | [Abrir](12-encerramento.png) |

## Como os movimentos são feitos

[gerar-previa.py](gerar-previa.py) desenha as cenas com Python/Pillow e usa FFmpeg para o MP4. O código calcula a posição dos cotovelos a partir do ombro e da mão, mantendo dois segmentos de braço de comprimento constante. As mãos de Isaque e Jacó se aproximam até o ponto de contato. A cabeça tem rotação independente. Deslocamentos usam interpolação suave; os textos permanecem estáveis. Não há simulação física, animação facial detalhada ou sincronização labial.

Para reproduzir: Python 3, Pillow, FFmpeg e fontes DejaVu em `/usr/share/fonts/truetype/dejavu`.

```sh
python gerar-previa.py --images-only
python gerar-previa.py --video-only
```

Sem argumentos, o script gera ambos. Saídas na mesma pasta. Tipografia DejaVu/Bitstream; fontes não redistribuídas. Ilustrações originais feitas por código, sem geração de imagens por IA.

**Referência: Gênesis 27:1–45; distinção com Gênesis 25.** Aparência, roupas, cadeira, tenda, utensílios e gestos são interpretações artísticas. Cobrimos as mãos e o pescoço de Jacó visualmente, sem cenas gráficas de preparação das peles. Jacó recebe roupa laranja na sequência do disfarce; Esaú mantém cabelo e barba avermelhados. O relato do engano não é apresentado como ordem de Deus. Não há representação humana de Deus nem violência explícita. A cena da fuga mostra a orientação de Rebeca, sem antecipar o desenrolar completo do capítulo seguinte.

Nenhuma voz foi gerada e nenhum crédito do ElevenLabs foi utilizado. [Roteiro](ROTEIRO.md) · [Manifesto](cenas.json) · [Verificação](verificacao.json).
