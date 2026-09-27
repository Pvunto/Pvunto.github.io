# Alberto — sito personale

Portfolio personale statico realizzato con **HTML, CSS e JavaScript**, pensato per GitHub Pages.

## Cosa contiene

- presentazione personale in homepage;
- passioni e hobby: fotografia, design, codice, musica e videogiochi;
- sezione dedicata a cosa studio e ai progetti in corso;
- contatti rapidi via mail, Discord e Spotify;
- pagine di dettaglio `hobby.html`, `music.html` e `games.html`;
- animazioni leggere, scroll reveal, navigazione ancorata e layout responsive.

## Struttura

```text
.
├── index.html       # Homepage
├── hobby.html       # Hobby personali
├── music.html       # Preferenze musicali
├── games.html       # Preferenze videoludiche
├── style.css        # Stili globali e responsive
├── script.js        # Animazioni e navigazione
├── intro-art.jpg    # Immagine introduttiva
└── .nojekyll        # Disabilita il processing Jekyll
```

## Personalizzare i contatti

In `index.html`, nella sezione `#contatti`, sostituisci:

- `ciao@example.com` con il tuo indirizzo mail;
- `https://discord.com` con il tuo profilo o invito Discord;
- `https://open.spotify.com/` con il tuo profilo o la tua playlist Spotify;
- `@Pvunto` con il tuo username pubblico.

## Pubblicazione su GitHub Pages

Il sito non richiede Node.js o una fase di build. In **Settings → Pages**, seleziona **Deploy from a branch**, branch `main`, cartella `/ (root)`.

URL atteso: `https://pvunto.github.io`

## Backup

Prima della nuova versione è stato creato localmente il branch `archive/2026-09-27-before-redesign`, che conserva lo stato precedente.
