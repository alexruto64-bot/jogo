# Cavaleiro do Teide

Jogo de ação para o navegador, em 3D, com visão de cima: um cavaleiro defende território.
Por enquanto é a base: o herói animado andando pelo mapa, sem inimigos.

A história (duas propostas, com a recomendada e a comparação) está em [HISTORIA.md](HISTORIA.md).

> **Temporário:** o herói está 10x mais rápido para conferir os mapas (`TURBO = 10` no `index.html`). Voltar para 1 depois.

## Mapas

- **Vila medieval** (padrão): praça de pedra, ruas calçadas, 12 casas montadas peça por peça (paredes de pedra e
  enxaimel, janelas, portas, varandas, telhados de telha e uma torre), carroça, caixotes e um pasto cercado, num vale
  cercado de morros. Em volta:
  - ao norte, o **Pico rochoso**: paredão de pedra real (escaneado) com mais de 230 m acima do vale, apoiado num morro;
  - a leste, a **Ponte natural**: arco de pedra real (escaneado), com uns 60 m, num platô;
  - perto da estrada norte, um afloramento de **pedras reais** (escaneadas em Mt Andrew, Austrália);
  - uma **torre de vigia** de pedra na entrada oeste, um **portal gótico** no fim da estrada norte e **árvores secas**;
  - **bosques** de árvores comuns e pinheiros (pinheiros nos morros mais altos), árvores soltas, duas árvores
    retorcidas grandes e pedras soltas. Cada árvore e pedra fica registrada em `RECURSOS`, para virar madeira e pedra.

  O herói não atravessa casas, árvores, pedras e itens, sobe nas pedras e no arco onde a inclinação deixa e não escala
  paredões. A vila abre primeiro e o resto vai aparecendo assim que chega.
- **Teide (versão 1)**: o terreno real do Teide, com 2 km de lado. De perto, o chão ganha a pedra da Ponte natural:
  um trecho da foto dela virou uma textura que repete sem emenda (`terreno/pedra.jpg`), com relevo fino para a luz
  (`terreno/pedra_normal.jpg`).

Troque de mapa pelas setas ◀ ▶ ou pela lista no topo; só o mapa escolhido é carregado. O Teide também abre com
`#teide` no fim do endereço.

Terrenos avaliados e que ficaram de fora (sem detalhe de perto ou que não agradaram): Represa de Negratín, Monte da
Tentação, Columbia River Gorge, Encosta na floresta, o levantamento de 6 km com foto de satélite e a Gruta do Fogão
(o escaneamento da caverna não tem cor nem foto).

## Comandos

| Comando                     | O que faz                                        |
| --------------------------- | ------------------------------------------------ |
| W A S D (ou setas)          | Andar                                            |
| Shift                       | Correr                                           |
| Espaço                      | Golpe de espada                                  |
| Touchpad: dois dedos ← →    | Girar a câmera                                   |
| Touchpad: dois dedos ↑ ↓    | Aproximar / afastar (a rodinha do mouse também)  |
| Touchpad: pinça             | Aproximar / afastar                              |
| Clicar e arrastar           | Girar e inclinar a câmera                        |
| Q E / Z X                   | Girar / aproximar pelo teclado                   |

Abrir a página com `?leve=1` reduz a malha do chão e as sombras, para máquinas fracas.

## O herói

Um patrulheiro de capuz, barba e espada, montado com os pacotes de personagem da Quaternius (todos no mesmo esqueleto):
a cabeça do corpo base, a roupa de patrulheiro (*Ranger*) com ombreira e botas, o cabelo com barba e a espada do pacote do
cavaleiro presa no osso da mão direita. Tem 1,87 m e fica em `modelos/heroi.glb` (texturas de 2048 px em WebP).

As animações ficam à parte em `modelos/animacoes.glb` (18 da *Universal Animation Library*) e tocam no mesmo esqueleto:

| Situação                     | Animação        |
| ---------------------------- | --------------- |
| Parado                       | `Idle_Loop`     |
| Parado logo depois do golpe  | `Sword_Idle`    |
| Andando                      | `Walk_Loop`     |
| Correndo (Shift)             | `Jog_Fwd_Loop`  |
| Golpe (Espaço)               | `Sword_Attack`  |

O ritmo dos passos acompanha a velocidade, para o pé não escorregar no chão.

Nas versões grátis desses pacotes só vêm as roupas de camponês e de patrulheiro; a armadura completa de cavaleiro está
só na versão paga (*Source*).

## Como os terrenos escaneados entram no jogo

`ferramentas/preparar_mapa.py` (Blender como módulo do Python) converte cada escaneamento. Os que ficam na vila estão
em `objetos/<nome>/`:

- `modelo.glb`: a malha reduzida (300 mil triângulos no Pico e na Ponte) e compactada (quantização), sem as fotos.
- `foto*.webp`: as fotos do terreno quase na resolução original (até 8192 px).
- `altura.png`: o chão por cima do objeto, para o herói pisar (R e G = altura em 16 bits; B = onde dá para pisar).
- `objeto.json`: tamanho, alturas, cor média e crédito.

Na conversão dá para recortar a base (`corte`), nivelar pelo chão (`nivelar`), tirar a água pela cor (`agua`) e tirar
lascas compridas (`aresta_max`); foi assim que a Ponte perdeu a caixa de água e as pedras do Mt Andrew perderam o chão de
areia. A foto já vem com luz e sombra, então metade do brilho vem dela e metade do sol do jogo. De perto, um grão de
cascalho projetado pelos três lados dá textura.

Para avaliar um terreno novo como mapa inteiro, ponha os arquivos em `mapas/<nome>/` (com `mapa.json`) e acrescente o
mapa na lista `MAPAS` do `index.html`.

## Itens

`objetos/itens/` tem a torre de vigia, o portal e a árvore seca, com o tamanho em metros e texturas de 2048 px
(convertidos com `ferramentas/preparar_item.py`). As árvores e pedras dos bosques vêm de `vila/natureza.glb`
(15 peças do *Stylized Nature MegaKit*) e são desenhadas com `InstancedMesh`.

## Como a vila é montada

`vila/pecas.glb` junta 51 peças do *Medieval Village MegaKit* (texturas de 2048 px, em WebP). O código
monta cada casa a partir de uma lista (posição, giro, largura e fundo em módulos de 2 m, número de andares, base de
pedra ou reboco, chaminé, varanda, trepadeira). As peças repetidas são desenhadas com `InstancedMesh`, então a vila
inteira custa poucas chamadas de desenho. O chão mistura duas fotos de chão (grama e terra) pelo próprio shader, com
as estradas de terra saindo da praça.

## Créditos

- Casas e peças da vila: [Medieval Village MegaKit](https://quaternius.itch.io/medieval-village-megakit), Quaternius (CC0).
- Herói: [Universal Base Characters](https://quaternius.itch.io/universal-base-characters), [Modular Character Outfits - Fantasy](https://quaternius.itch.io/modular-character-outfits-fantasy) e [Universal Animation Library](https://quaternius.itch.io/universal-animation-library), Quaternius (CC0).
- Espada: [Knight Character](https://quaternius.itch.io/lowpoly-animated-knight), Quaternius (CC0).
- Árvores e pedras dos bosques: [Stylized Nature MegaKit](https://quaternius.itch.io/stylized-nature-megakit), Quaternius (CC0).
- Torre de vigia, portal gótico e árvore seca: modelos "pixellabs" enviados pelo dono do jogo (conferir a licença antes de publicar).
- Pico rochoso, Ponte natural e pedras de Mt Andrew: escaneamentos do Sketchfab enviados pelo dono do jogo (conferir autor e licença antes de publicar).
- Grama, terra e cascalho: [Poly Haven](https://polyhaven.com) (CC0).
- Terreno do Teide: [El Teide en 3D](https://sketchfab.com/3d-models/el-teide-en-3d-4a961a00043e4d6b912506f9ac895825), por @x_y_es (Sketchfab, CC BY 4.0).
