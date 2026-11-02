# Cavaleiro do Teide

Jogo de ação para o navegador, em 3D, com visão de cima: um cavaleiro defende território.

**Jogar:** https://alexruto64-bot.github.io/jogo/ (GitHub Pages, publicado a partir da `main`).

A história (duas propostas, com a recomendada e a comparação) está em [HISTORIA.md](HISTORIA.md).

Para conferir o mapa depressa, abra com `?turbo=10` no endereço (herói 10x mais rápido).

## O céu

Duas fotos de céu do Poly Haven, só a metade de cima, em `ceu/` (WebP): de dia, nuvens com o sol a 48° (a foto é
girada para o sol dela ficar na direção da luz do jogo, então as sombras batem); de noite, a Via Láctea. O dia passa
para a noite misturando as duas, com o tom laranja do entardecer e o cinza do dia escuro por cima. A névoa usa a cor
do horizonte da foto, e o reflexo do céu nos objetos sai da própria foto. Tamanho da foto: 2048 px no modo leve, 4096 no
automático e 8192 no alto.

## Como se joga

A história recomendada (*Cavaleiro do Teide*) virou o jogo. Duarte chega a um vale com 12 casas em ruína (paredes
queimadas, sem telhado) e reergue a vila aos poucos:

- **Recursos:** o golpe de espada corta árvore (3 golpes, madeira) e quebra pedra (4 golpes, pedra); às vezes a rocha
  esconde uma **pedra-sol**. Cada casa de pé paga 1 de ouro a cada 20 s; porcos e galinhas também rendem ouro.
- **Construir:** `F` perto de uma ruína a reergue (a casa sobe peça por peça); `B` abre as obras: cerca, muro de
  pedra, torre de arqueiro (atira sozinha), porco e galinha. Casas e obras danificadas se consertam com `F`.
- **Mercador:** Lanfranco, na estrada oeste, compra madeira, pedra e pedra-sol.
- **Dia e noite:** um dia dura 6 minutos. A partir do capítulo 2, todo entardecer vem um ataque: os **Cinzentos**
  (gente de rosto pintado de cinza) descem do Teide pelo oeste e pelo sul, e os **diabretes** e **porcos-goblin** saem
  pelo portal ao pé do Pico; depois vem o **orc**. Uns roubam a praça (dá para pegar de volta matando o ladrão antes
  que fuja), outros queimam casas (que voltam a ser ruína) e derrubam cercas e muros.
- **Luta:** os inimigos perseguem Duarte quando ele chega perto ou bate neles; cada um tem barra de vida. Duarte tem
  vida (volta sozinha depois de alguns segundos sem apanhar); se cair, acorda na praça e perde parte da madeira e da pedra.
- **A pedra-sol:** vender rende muito ouro, mas cada uma vendida apaga fogueiras no paredão (os pontos de fogo no Pico,
  de noite) e traz mais diabos. Guardada, vira **a Luz** (`L`): os inimigos perto apanham e ficam tontos.
- **Capítulos:** 1 · A chegada (lenha, pedra, a primeira casa); 2 · Os Cinzentos (mercador, torre, a primeira noite);
  3 · Os cães do vulcão (a pedra-sol, 4 casas, mais ataques); 4 · O Guardião (8 casas, muros e o dia escuro, quando o
  Guardião sai pelo portal). No capítulo 4 o portal abre um tubo de lava até o acampamento dos vilões no Teide, onde o
  círculo de ritual recebe as pedras-sol de volta.
- **Finais:** *Mil Fogueiras* (devolver ao menos 3 pedras-sol ao círculo), *Ouro* (vender 3 ou mais) ou *Cinza*. Depois
  do final dá para continuar jogando.
- O jogo é salvo sozinho no navegador; na abertura aparecem **Continuar** e **Começar de novo**.

## O mundo

Um mapa só, de 2 × 3 km:

- **O vale da vila** (ao sul): praça de pedra, ruas calçadas, 12 casas montadas peça por peça (paredes de pedra e
  enxaimel, janelas, portas, varandas, telhados de telha e uma torre), carroça, caixotes e um pasto cercado, cercado de
  morros. Em volta:
  - ao norte, o **Pico rochoso**: paredão de pedra real (escaneado) com mais de 230 m acima do vale, apoiado num morro;
  - a leste, a **Ponte natural**: arco de pedra real (escaneado), com uns 240 m de comprimento e 70 m de altura;
  - perto da estrada norte, um afloramento de **pedras reais** (escaneadas em Mt Andrew, Austrália);
  - uma **torre de vigia** de pedra na entrada oeste, um **portal gótico** no fim da estrada norte e **árvores secas**;
  - **bosques** de árvores comuns e pinheiros (pinheiros nos morros mais altos), árvores soltas, duas árvores
    retorcidas grandes e pedras soltas. Cada árvore e pedra fica registrada em `RECURSOS`, para virar madeira e pedra.
- **O Teide** (ao norte, atrás do Pico): o terreno real do vulcão, com 2 km de lado, é a terra dos vilões: sem árvores e
  sem verde, só pedras escuras espalhadas. O chão passa do vale para o Teide entre z = −430 e −600. No Teide, a foto de
  satélite dá as cores de longe e três fotos de chão do Poly Haven dão o detalhe de perto (`terreno/cascalho.jpg`,
  `terreno/cinza.jpg` onde a foto é avermelhada e `terreno/entulho.jpg` nas encostas), cada uma com o relevo fino dela.

O chão é desenhado em blocos de 250 m e as árvores e pedras em blocos de 400 m, para o navegador pular o que está fora
da tela. O herói não atravessa casas, árvores, pedras e itens, sobe nas pedras e no arco onde a inclinação deixa e não
escala paredões. A vila abre primeiro e o resto vai aparecendo assim que chega.

Terrenos avaliados e que ficaram de fora (sem detalhe de perto ou que não agradaram): Represa de Negratín, Monte da
Tentação, Columbia River Gorge, Encosta na floresta, o levantamento de 6 km com foto de satélite e a Gruta do Fogão
(o escaneamento da caverna não tem cor nem foto).

## Comandos

| Comando                       | O que faz                                                        |
| ----------------------------- | ---------------------------------------------------------------- |
| W A S D (ou setas)            | Andar                                                            |
| Shift                         | Correr                                                           |
| Espaço                        | Golpe: luta, corta árvore, quebra pedra, recolhe pedra-sol       |
| F                             | Agir: reerguer, consertar, negociar, tubo de lava, devolver      |
| B                             | Construir (1 a 5 escolhe, F confirma, Esc sai)                   |
| L                             | A Luz (precisa de pedra-sol guardada)                            |
| P / H                         | Pausa / mostrar os comandos                                      |
| Clicar e arrastar             | Girar e inclinar a câmera (até olhar o céu)                      |
| Q E / R V / Z X               | Girar / inclinar / aproximar pelo teclado                        |
| Touchpad: dois dedos          | Para os lados gira; para cima e para baixo aproxima              |
| Touchpad: Shift + dois dedos  | Inclina a câmera                                                 |
| Touchpad: pinça               | Aproximar / afastar                                              |

## Desempenho e instalação

- **Gráficos** (botão no topo, fica guardado no navegador):
  - *automático* (padrão): a resolução sobe ou desce sozinha conforme o FPS e, se mesmo assim ficar muito lento, as
    sombras são desligadas;
  - *leve*: chão mais simples, metade das árvores, sem sombras e resolução baixa;
  - *alto*: resolução e sombras no máximo.

  Abrir a página com `?leve=1` também liga o modo leve.
- Se o Chrome estiver sem aceleração gráfica (desenhando o 3D pelo processador), aparece um aviso explicando como
  ligar: Configurações do Chrome → Sistema → "Usar aceleração gráfica quando disponível".
- **Instalar no PC:** no GitHub Pages, o Chrome mostra o botão "Instalar" na barra de endereço (`manifest.webmanifest`
  e `sw.js`). O jogo ganha um ícone, abre em janela própria e funciona sem internet depois da primeira vez. Ele roda
  no mesmo motor do Chrome, então a velocidade é a mesma; o que pesa é a placa de vídeo e a qualidade escolhida.

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

`objetos/itens/` tem os modelos parados enviados ao Drive, já no tamanho em metros (lista `ITENS_VILA` no `index.html`):

- **Construções:** torre de vigia, portal gótico, Torre da Luz, castelo na rocha, casa-torre, moinho e uma escada de
  pedra na encosta do Pico.
- **História do cristal:** cristais de pedra-sol (brilham sozinhos) na trilha do arco até o portal e em volta do
  círculo ritual dos vilões, no Teide.
- **Árvores:** árvore seca, árvores comuns, bétula e duas árvores de outono.
- **Animais:** cavalos e porcos no pasto, cães, galos, pombos, pardais e uma gaivota.

`objetos/personagens/` tem os que se mexem (lista `ANIMADOS`): um gato na praça, pardais voando sobre a vila e, no
acampamento dos vilões no Teide, um orc, dois diabretes, dois porcos-goblin e o guardião infernal (parado). O diabrete e
o porco-goblin usam o mesmo esqueleto do herói e tocam as animações dele.

As árvores e pedras dos bosques vêm de `vila/natureza.glb` (15 peças do *Stylized Nature MegaKit*) e são desenhadas
com `InstancedMesh`.

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
- Céu: [Kloofendal 48d Partly Cloudy (Pure Sky)](https://polyhaven.com/a/kloofendal_48d_partly_cloudy_puresky) e [Qwantani Night (Pure Sky)](https://polyhaven.com/a/qwantani_night_puresky), Greg Zaal e Jarod Guest, Poly Haven (CC0).
- Terreno do Teide: [El Teide en 3D](https://sketchfab.com/3d-models/el-teide-en-3d-4a961a00043e4d6b912506f9ac895825), por @x_y_es (Sketchfab, CC BY 4.0).
