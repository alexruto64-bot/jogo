# Instruções para o Claude

## Idioma

- Fale sempre em **português do Brasil**. Nunca responda em inglês.
- Isso vale para tudo que o usuário lê: respostas, avisos de andamento ("estou fazendo tal coisa"), perguntas,
  resumos, mensagens de commit, comentários no código e textos do jogo.
- Mesmo que um arquivo, ferramenta ou erro venha em inglês, explique em português.
- Nomes técnicos que não têm tradução (Three.js, GitHub Pages, GLB) podem ficar como estão.

## O projeto

- O jogo está publicado no GitHub Pages a partir da `main`: https://alexruto64-bot.github.io/jogo/ (cada envio para a
  `main` atualiza o link em 1 ou 2 minutos).
- Jogo 3D para o navegador, feito com Three.js r147 (carregado do jsDelivr), sem etapa de build: o jogo inteiro está
  no `index.html`. Para testar, sirva a pasta por um servidor local (por exemplo `python3 -m http.server`) e abra no
  Chrome.
- O dono quer visual o mais realista possível e joga no PC (teclado e touchpad).
- Pastas: `modelos/` (herói e animações), `vila/` (peças da vila, árvores e pedras, grama e terra), `objetos/`
  (terrenos escaneados e itens postos na vila), `terreno/` (o Teide), `ferramentas/` (conversores com o Blender como
  módulo do Python).
- A história do jogo está em `HISTORIA.md` (duas propostas; a recomendada é "Cavaleiro do Teide").
- O mundo é um mapa só: a vila no vale ao sul e o Teide (terra dos vilões, sem verde) ao norte, atrás do Pico.
  Itens parados ficam em `ITENS_VILA`, personagens e bichos animados em `ANIMADOS`.
- Desempenho: botão "Gráficos" (automático, leve, alto), resolução que se ajusta ao FPS e aviso quando o Chrome está
  sem aceleração gráfica. O jogo pode ser instalado pelo Chrome (`manifest.webmanifest` e `sw.js`).
- `TURBO = 10` no `index.html` é temporário (herói 10x mais rápido para conferir os mapas).
- No link de teste do Claude (Artifact), arquivos `.glb` não são servidos: a cópia para lá troca `SUFIXO_GLB` por
  `'.txt'` e grava os `.glb` em base64 (em partes, se passarem de 15 milhões de caracteres).
