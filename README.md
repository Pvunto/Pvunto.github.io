# Alberto / Field notes

Sito personale statico rifatto da zero con **HTML, CSS e JavaScript** e pubblicato su GitHub Pages.

## Direzione visiva

Reinterpretazione originale dell'estetica retro-futurista da game show: colori pop, tipografia da poster, griglie tecniche, texture CRT, badge `ON AIR`, statistiche da player card e dettagli da trasmissione televisiva. L'energia richiama il tono competitivo e spettacolare dei videogiochi moderni senza usare marchi, loghi o asset di terze parti.

## Contenuti

- homepage con presentazione personale e hero da broadcast;
- passioni e hobby;
- **Player Card / Loadout** con statistiche personali;
- pagina musica;
- pagina games;
- sezione su cosa studio;
- **Live Feed** con playlist, side quest e nuove connessioni;
- contatti via mail, Discord e Spotify;
- layout responsive, scroll reveal e tilt cards;
- nessun backend e nessuna fase di build necessaria.

## Struttura

```text
.
├── index.html       # Homepage
├── hobby.html       # Hobby personali
├── music.html       # Preferenze musicali
├── games.html       # Preferenze videoludiche
├── style.css        # Identità visiva e responsive
├── script.js        # Scroll reveal, navigazione e hover tilt
└── .nojekyll        # Disabilita il processing Jekyll
```

## Personalizzare i contatti

In `index.html`, nella sezione `#contact`, sostituisci i segnaposto con il tuo indirizzo mail, il link al profilo/invito Discord e il profilo o la playlist Spotify.

## Pubblicazione

Il sito non richiede una build. In **Settings → Pages**, seleziona **Deploy from a branch**, branch `main`, cartella `/ (root)`.

URL: `https://pvunto.github.io`
