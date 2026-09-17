# Alberto — sito personale

Sito personale statico realizzato con **HTML, CSS e JavaScript**.

Il progetto raccoglie una breve presentazione, hobby, preferenze musicali, videogiochi, attività personali e link social.

## Stile

Il design usa un linguaggio **brutalista, svizzero e retro**, con:

- sfondo nero;
- rosso e giallo come colori principali;
- tipografia compatta e ad alto contrasto;
- layout responsive per desktop e smartphone;
- animazioni leggere e interazioni JavaScript.

## Struttura

```text
.
├── index.html       # Homepage
├── hobby.html       # Hobby personali
├── music.html       # Preferenze musicali
├── games.html       # Preferenze videoludiche
├── style.css        # Stili globali e responsive
├── script.js        # Animazioni e interazioni
├── intro-art.jpg    # Immagine introduttiva
└── .nojekyll        # Disabilita il processing Jekyll
```

## Pubblicazione

Il sito è pensato per **GitHub Pages** e non richiede Node.js, npm o una fase di build.

Per pubblicarlo:

1. Apri **Settings → Pages** nel repository.
2. Seleziona **Deploy from a branch**.
3. Scegli il branch `main`.
4. Scegli la cartella `/ (root)`.
5. Salva le impostazioni.

Il sito sarà disponibile all’indirizzo:

```text
https://pvunto.github.io
```

## Modifiche rapide

Per cambiare i contenuti, modifica direttamente i file HTML. Per cambiare colori, spaziature o responsive design, modifica `style.css`. Le animazioni e il comportamento dinamico si trovano in `script.js`.

## Social

I link social sono presenti nel footer di `index.html` e possono essere sostituiti con gli indirizzi personali.

## Licenza

Progetto personale. I contenuti e l’immagine introduttiva appartengono al rispettivo autore.
